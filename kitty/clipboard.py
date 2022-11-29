#!/usr/bin/env python
# License: GPLv3 Copyright: 2022, Kovid Goyal <kovid at kovidgoyal.net>

import io
from enum import Enum, IntEnum
from gettext import gettext as _
from tempfile import SpooledTemporaryFile
from typing import (
    IO, Callable, Dict, List, NamedTuple, Optional, Tuple, Union,
)

from .conf.utils import uniq
from .constants import supports_primary_selection
from .fast_data_types import (
    GLFW_CLIPBOARD, GLFW_PRIMARY_SELECTION, OSC, get_boss, get_clipboard_mime,
    get_options, set_clipboard_data_types,
)
from .utils import log_error

DataType = Union[bytes, 'IO[bytes]']
TARGETS_MIME = '.'


class ClipboardType(IntEnum):
    clipboard = GLFW_CLIPBOARD
    primary_selection = GLFW_PRIMARY_SELECTION

    @staticmethod
    def from_osc52_where_field(where: str) -> 'ClipboardType':
        where = where or 's0'
        return ClipboardType.clipboard if 'c' in where or 's' in where else ClipboardType.primary_selection


class Clipboard:

    def __init__(self, clipboard_type: ClipboardType = ClipboardType.clipboard) -> None:
        self.data: Dict[str, DataType] = {}
        self.clipboard_type = clipboard_type
        self.enabled = self.clipboard_type is ClipboardType.clipboard or supports_primary_selection

    def set_text(self, x: Union[str, bytes]) -> None:
        if isinstance(x, str):
            x = x.encode('utf-8')
        self.set_mime({'text/plain': x})

    def set_mime(self, data: Dict[str, DataType]) -> None:
        if self.enabled and isinstance(data, dict):
            self.data = data
            set_clipboard_data_types(self.clipboard_type, tuple(self.data))

    def get_text(self) -> str:
        parts: List[bytes] = []
        self.get_mime("text/plain", parts.append)
        return b''.join(parts).decode('utf-8', 'replace')

    def get_mime(self, mime: str, output: Callable[[bytes], None]) -> None:
        if self.enabled:
            try:
                get_clipboard_mime(self.clipboard_type, mime, output)
            except RuntimeError as err:
                if str(err) != 'is_self_offer':
                    raise
                data = self.data.get(mime, b'')
                if isinstance(data, bytes):
                    output(data)
                else:
                    data.seek(0, 0)
                    q = b' '
                    while q:
                        q = data.read(io.DEFAULT_BUFFER_SIZE)
                        output(q)

    def get_mime_data(self, mime: str) -> bytes:
        ans: List[bytes] = []
        self.get_mime(mime, ans.append)
        return b''.join(ans)

    def get_available_mime_types_for_paste(self) -> Tuple[str, ...]:
        if self.enabled:
            parts: List[bytes] = []
            try:
                get_clipboard_mime(self.clipboard_type, None, parts.append)
            except RuntimeError as err:
                if str(err) != 'is_self_offer':
                    raise
                return tuple(self.data)
            return tuple(x.decode('utf-8', 'replace') for x in uniq(parts))
        return ()

    def __call__(self, mime: str) -> Callable[[], bytes]:
        data = self.data.get(mime, b'')
        if isinstance(data, str):  # type: ignore
            data = data.encode('utf-8')  # type: ignore
        if isinstance(data, bytes):
            def chunker() -> bytes:
                nonlocal data
                assert isinstance(data, bytes)
                ans = data
                data = b''
                return ans
            return chunker

        data.seek(0, 0)

        def io_chunker() -> bytes:
            assert not isinstance(data, bytes)
            return data.read(io.DEFAULT_BUFFER_SIZE)
        return io_chunker


def set_clipboard_string(x: Union[str, bytes]) -> None:
    get_boss().clipboard.set_text(x)


def get_clipboard_string() -> str:
    return get_boss().clipboard.get_text()


def set_primary_selection(x: Union[str, bytes]) -> None:
    get_boss().primary_selection.set_text(x)


def get_primary_selection() -> str:
    return get_boss().primary_selection.get_text()


def develop() -> Tuple[Clipboard, Clipboard]:
    from .constants import detect_if_wayland_ok, is_macos
    from .fast_data_types import set_boss
    from .main import init_glfw_module
    glfw_module = 'cocoa' if is_macos else ('wayland' if detect_if_wayland_ok() else 'x11')

    class Boss:
        clipboard = Clipboard()
        primary_selection = Clipboard(ClipboardType.primary_selection)
    init_glfw_module(glfw_module)
    set_boss(Boss())  # type: ignore
    return Boss.clipboard, Boss.primary_selection


class ProtocolType(Enum):
    osc_52 = 52
    osc_5522 = 5522


class ReadRequest(NamedTuple):
    is_primary_selection: bool = False
    mime_types: Tuple[str, ...] = ('text/plain',)
    id: str = ''
    protocol_type: ProtocolType = ProtocolType.osc_52

    def encode_response(self, status: str = 'DATA', mime: str = '', payload: bytes = b'') -> bytes:
        ans = f'{self.protocol_type.value};type=read:status={status}'
        if status == 'OK' and self.is_primary_selection:
            ans += ':loc=primary'
        if self.id:
            ans += f':id={self.id}'
        if mime:
            ans += f':mime={mime}'
        a = ans.encode('ascii')
        if payload:
            import base64
            a += b';' + base64.standard_b64encode(payload)
        return a


def encode_osc52(loc: str, response: str) -> str:
    from base64 import standard_b64encode
    return '52;{};{}'.format(
        loc, standard_b64encode(response.encode('utf-8')).decode('ascii'))


class MimePos(NamedTuple):
    start: int
    size: int


class WriteRequest:

    def __init__(
        self, is_primary_selection: bool = False, protocol_type: ProtocolType = ProtocolType.osc_52,
        rollover_size: int = 16 * 1024 * 1024, max_size: int = -1,
    ) -> None:
        self.is_primary_selection = is_primary_selection
        self.protocol_type = protocol_type
        self.max_size_exceeded = False
        self.tempfile = SpooledTemporaryFile(max_size=rollover_size)
        self.mime_map: Dict[str, MimePos] = {}
        self.currently_writing_mime = ''
        self.current_leftover_bytes = memoryview(b'')
        self.max_size = (get_options().clipboard_max_size * 1024 * 1024) if max_size < 0 else max_size

    def close(self) -> None:
        if not self.tempfile.closed:
            self.tempfile.close()

    def add_base64_data(self, data: Union[str, bytes], mime: str = 'text/plain') -> None:
        if isinstance(data, str):
            data = data.encode('ascii')
        if self.currently_writing_mime and self.currently_writing_mime != mime:
            self.flush_base64_data()
        if not self.currently_writing_mime:
            self.mime_map[mime] = MimePos(self.tempfile.tell(), -1)
            self.currently_writing_mime = mime
        if len(self.current_leftover_bytes) > 0:
            extra = 4 - len(self.current_leftover_bytes)
            if len(data) >= extra:
                self.write_base64_data(memoryview(bytes(self.current_leftover_bytes) + data[:extra]))
                data = memoryview(data)[extra:]
                self.current_leftover_bytes = memoryview(b'')
            else:
                self.current_leftover_bytes = memoryview(bytes(self.current_leftover_bytes) + data)
        else:
            extra = len(data) % 4
            if extra > 0:
                mv = memoryview(data)
                self.current_leftover_bytes = mv[-extra:]
                mv = mv[:-extra]
                if len(mv) > 0:
                    self.write_base64_data(mv)
            else:
                self.write_base64_data(data)

    def flush_base64_data(self) -> None:
        if self.currently_writing_mime:
            b = self.current_leftover_bytes
            padding = 4 - len(b)
            if padding in (1, 2):
                self.write_base64_data(memoryview(bytes(b) + b'=' * padding))
            start = self.mime_map[self.currently_writing_mime][0]
            self.mime_map[self.currently_writing_mime] = MimePos(start, self.tempfile.tell() - start)
            self.currently_writing_mime = ''
            self.current_leftover_bytes = memoryview(b'')

    def write_base64_data(self, b: bytes) -> None:
        from base64 import standard_b64decode
        if not self.max_size_exceeded:
            d = standard_b64decode(b)
            self.tempfile.write(d)
            if self.max_size > 0 and self.tempfile.tell() > (self.max_size * 1024 * 1024):
                log_error(f'Clipboard write request has more data than allowed by clipboard_max_size ({self.max_size}), truncating')
                self.max_size_exceeded = True

    def data_for(self, mime: str = 'text/plain', offset: int = 0, size: int = -1) -> bytes:
        start, full_size = self.mime_map[mime]
        if size == -1:
            size = full_size
        self.tempfile.seek(start + offset)
        return self.tempfile.read(size)


class ClipboardRequestManager:

    def __init__(self, window_id: int) -> None:
        self.window_id = window_id
        self.currently_asking_permission_for: Optional[ReadRequest] = None
        self.in_flight_write_request: Optional[WriteRequest] = None

    def parse_osc_5522(self, data: str) -> None:
        from .notify import sanitize_id
        metadata, _, payload = data.partition(';')
        m: Dict[str, str] = {}
        for record in metadata.split(':'):
            try:
                k, v = record.split('=', 1)
            except Exception:
                log_error('Malformed OSC 5522: metadata is not key=value pairs')
                return
            m[k] = v
        typ = m.get('type', '')
        if typ == 'read':
            rr = ReadRequest(
                is_primary_selection=m.get('loc', '') == 'primary',
                mime_types=tuple(payload.split()),
                protocol_type=ProtocolType.osc_5522, id=sanitize_id(m.get('id', ''))
            )
            self.handle_read_request(rr)

    def parse_osc_52(self, data: str, is_partial: bool = False) -> None:
        where, text = data.partition(';')[::2]
        if text == '?':
            rr = ReadRequest(is_primary_selection=ClipboardType.from_osc52_where_field(where) is ClipboardType.primary_selection)
            self.handle_read_request(rr)
        else:
            wr = self.in_flight_write_request
            if wr is None:
                wr = self.in_flight_write_request = WriteRequest(ClipboardType.from_osc52_where_field(where) is ClipboardType.primary_selection)
            wr.add_base64_data(text)
            if is_partial:
                return
            self.in_flight_write_request = None
            self.handle_write_request(wr)

    def handle_write_request(self, wr: WriteRequest) -> None:
        wr.flush_base64_data()
        q = 'write-primary' if wr.is_primary_selection else 'write-clipboard'
        allowed = q in get_options().clipboard_control
        self.fulfill_write_request(wr, allowed)

    def fulfill_write_request(self, wr: WriteRequest, allowed: bool = True) -> None:
        if wr.protocol_type is ProtocolType.osc_52:
            self.fulfill_legacy_write_request(wr, allowed)

    def fulfill_legacy_write_request(self, wr: WriteRequest, allowed: bool = True) -> None:
        cp = get_boss().primary_selection if wr.is_primary_selection else get_boss().clipboard
        w = get_boss().window_id_map.get(self.window_id)
        if w is not None and cp.enabled and allowed:
            cp.set_text(wr.data_for('text/plain'))

    def handle_read_request(self, rr: ReadRequest) -> None:
        cc = get_options().clipboard_control
        if rr.is_primary_selection:
            ask_for_permission = 'read-primary-ask' in cc
            allowed = 'read-primary' in cc
        else:
            ask_for_permission = 'read-clipboard-ask' in cc
            allowed = 'read-clipboard' in cc
        if ask_for_permission:
            self.ask_to_read_clipboard(rr)
        else:
            self.fulfill_read_request(rr, allowed=allowed)

    def fulfill_read_request(self, rr: ReadRequest, allowed: bool = True) -> None:
        if rr.protocol_type is ProtocolType.osc_52:
            return self.fulfill_legacy_read_request(rr, allowed)
        w = get_boss().window_id_map.get(self.window_id)
        if w is None:
            return
        cp = get_boss().primary_selection if rr.is_primary_selection else get_boss().clipboard
        if not cp.enabled:
            w.screen.send_escape_code_to_child(OSC, rr.encode_response(status='EINVAL'))
            return
        if not allowed:
            w.screen.send_escape_code_to_child(OSC, rr.encode_response(status='EPERM'))
            return
        w.screen.send_escape_code_to_child(OSC, rr.encode_response(status='OK'))

        current_mime = ''

        def write_chunks(data: bytes) -> None:
            assert w is not None
            mv = memoryview(data)
            while mv:
                w.screen.send_escape_code_to_child(OSC, rr.encode_response(payload=mv[:4096], mime=current_mime))
                mv = mv[4096:]

        for mime in rr.mime_types:
            current_mime = mime
            if mime == TARGETS_MIME:
                w.screen.send_escape_code_to_child(
                    OSC, rr.encode_response(payload=' '.join(cp.get_available_mime_types_for_paste()).encode('utf-8'), mime=current_mime))
                continue
            try:
                cp.get_mime(mime, write_chunks)
            except Exception as e:
                log_error(f'Failed to read requested mime type {mime} with error: {e}')
        w.screen.send_escape_code_to_child(OSC, rr.encode_response(status='DONE'))

    def reject_read_request(self, rr: ReadRequest) -> None:
        if rr.protocol_type is ProtocolType.osc_52:
            return self.fulfill_legacy_read_request(rr, False)
        w = get_boss().window_id_map.get(self.window_id)
        if w is not None:
            w.screen.send_escape_code_to_child(OSC, rr.encode_response(status='EPERM'))

    def fulfill_legacy_read_request(self, rr: ReadRequest, allowed: bool = True) -> None:
        cp = get_boss().primary_selection if rr.is_primary_selection else get_boss().clipboard
        w = get_boss().window_id_map.get(self.window_id)
        if w is not None:
            text = ''
            if cp.enabled and allowed:
                text = cp.get_text()
            loc = 'p' if rr.is_primary_selection else 'c'
            w.screen.send_escape_code_to_child(OSC, encode_osc52(loc, text))

    def ask_to_read_clipboard(self, rr: ReadRequest) -> None:
        if rr.mime_types == (TARGETS_MIME,):
            self.fulfill_read_request(rr, True)
            return
        if self.currently_asking_permission_for is not None:
            self.reject_read_request(rr)
            return
        w = get_boss().window_id_map.get(self.window_id)
        if w is not None:
            self.currently_asking_permission_for = rr
            get_boss().confirm(_(
                'A program running in this window wants to read from the system clipboard.'
                ' Allow it to do so, once?'),
                self.handle_clipboard_confirmation, window=w,
            )

    def handle_clipboard_confirmation(self, confirmed: bool) -> None:
        rr = self.currently_asking_permission_for
        self.currently_asking_permission_for = None
        if rr is not None:
            self.fulfill_read_request(rr, confirmed)

    def close(self) -> None:
        if self.in_flight_write_request is not None:
            self.in_flight_write_request.close()
            self.in_flight_write_request = None

# generated by gen-config.py DO NOT edit

import typing
from kittens.diff.options.utils import parse_map, pattern_list, syntax_aliases
from kitty.conf.utils import merge_dicts, positive_int, python_string, to_color, to_color_or_none


class Parser:

    def added_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['added_bg'] = to_color(val)

    def added_margin_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['added_margin_bg'] = to_color(val)

    def background(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['background'] = to_color(val)

    def diff_cmd(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['diff_cmd'] = str(val)

    def filler_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['filler_bg'] = to_color(val)

    def foreground(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['foreground'] = to_color(val)

    def highlight_added_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['highlight_added_bg'] = to_color(val)

    def highlight_removed_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['highlight_removed_bg'] = to_color(val)

    def hunk_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['hunk_bg'] = to_color(val)

    def hunk_margin_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['hunk_margin_bg'] = to_color(val)

    def margin_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['margin_bg'] = to_color(val)

    def margin_fg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['margin_fg'] = to_color(val)

    def margin_filler_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['margin_filler_bg'] = to_color_or_none(val)

    def num_context_lines(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['num_context_lines'] = positive_int(val)

    def pygments_style(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['pygments_style'] = str(val)

    def removed_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['removed_bg'] = to_color(val)

    def removed_margin_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['removed_margin_bg'] = to_color(val)

    def replace_tab_by(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['replace_tab_by'] = python_string(val)

    def search_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['search_bg'] = to_color(val)

    def search_fg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['search_fg'] = to_color(val)

    def select_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['select_bg'] = to_color(val)

    def select_fg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['select_fg'] = to_color_or_none(val)

    def syntax_aliases(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['syntax_aliases'] = syntax_aliases(val)

    def title_bg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['title_bg'] = to_color(val)

    def title_fg(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        ans['title_fg'] = to_color(val)

    def map(self, val: str, ans: typing.Dict[str, typing.Any]) -> None:
        for k in parse_map(val):
            ans['map'].append(k)

    def file_ignores(self, val: str, ans: typing.Dict[str, typing.List[str]]):
        ans['file_ignores'] = pattern_list(val)

    def ignore_paths(self, val: str, ans: typing.Dict[str, typing.List[str]]):
        ans['ignore_paths'] = pattern_list(val)


def create_result_dict() -> typing.Dict[str, typing.Any]:
    return {
        'map': [],
    }


actions: typing.FrozenSet[str] = frozenset(('map',))


def merge_result_dicts(defaults: typing.Dict[str, typing.Any], vals: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    ans = {}
    for k, v in defaults.items():
        if isinstance(v, dict):
            ans[k] = merge_dicts(v, vals.get(k, {}))
        elif k in actions:
            ans[k] = v + vals.get(k, [])
        else:
            ans[k] = vals.get(k, v)
    return ans


parser = Parser()


def parse_conf_item(key: str, val: str, ans: typing.Dict[str, typing.Any]) -> bool:
    func = getattr(parser, key, None)
    if func is not None:
        func(val, ans)
        return True
    return False

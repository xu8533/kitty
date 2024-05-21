### kitty简介
[kitty的github主页](https://github.com/kovidgoyal/kitty)

[kitty官方主页](https://sw.kovidgoyal.net/kitty/)

[kitty官方手册](https://sw.kovidgoyal.net/kitty/overview/)

kitty是一款基于GPU的快速的，功能丰富的，跨平台(支持linux, bsd, macos)的终端
kitty由C语言(核心性能部分)，python语言(UI部分)，go语言(命令行扩展，如kittens)混合编写而成
kitty支持所有现代终端特性，如Unicode, 真色彩，粗/斜字体，文本格式化等

### 标签页(tabs)和窗口(windows)
kitty通过标签页和窗口可以同时运行多个程序。

kitty的标签页和窗口组织结构如下：
<kitty-topology.png>

### 配置文件

### 快捷键
#### 回滚(Scrolling)
| 动作                       | 快捷键                                                   | 描述                        |
| ------------------------ | ----------------------------------------------------- | ------------------------- |
| scroll_line_up           | **<font color="#548dd4">ctrl+shift+up</font>**        | 上一行                       |
| scroll_line_down         | **<font color="#548dd4">ctrl+shift+down</font>**      | 下一行                       |
| scroll_page_up           | **<font color="#548dd4">ctrl+shift+page_up</font>**   | 上一页                       |
| scroll_page_down         | **<font color="#548dd4">ctrl+shift+page_down</font>** | 下一页                       |
| scroll_home              | **<font color="#548dd4">ctrl+shift+home</font>**      | 顶部                        |
| scroll_end               | **<font color="#548dd4">ctrl+shift+end</font>**       | 底部                        |
| scroll_line_up           | **<font color="#548dd4">ctrl+shift+k</font>**         | 上一行                       |
| scroll_line_down         | **<font color="#548dd4">ctrl+shift+k </font>**        | 下一行                       |
| show_scrollback          | **<font color="#548dd4">ctrl+shift+h</font>**         | Browse scrollback in less |
| show_last_command_output | **<font color="#548dd4">ctrl+shift+g</font>**         | Browse last cmd output    |
| scroll_to_prompt -1      | **<font color="#548dd4">ctrl+shift+z</font>**         | Previous shell prompt     |
| scroll_to_prompt 1       | **<font color="#548dd4">ctrl+shift+x</font>**         | Next shell prompt         |
#### 标签页(Tabs)
| 动作                | 快捷键                                               | 描述        |
| ----------------- | ------------------------------------------------- | --------- |
| new_tab           | **<font color="#548dd4">ctrl+shift+t</font>**     | 新建标签页     |
| new_tab_with_cwd  | **<font color="#548dd4">ctrl+shift+n</font>**     | 当前目录新建标签页 |
| close_tab         | **<font color="#548dd4">ctrl+shift+q</font>**     | 关闭标签页     |
| close_tab         | **<font color="#548dd4">ctrl+shift+w</font>**     | 关闭标签页     |
| previous_tab      | **<font color="#548dd4">ctrl+shift+left</font>**  | 后一个标签页    |
| next_tab          | **<font color="#548dd4">ctrl+shift+right</font>** | 前一个标签页    |
| next_layout       | **<font color="#548dd4">ctrl+shift+l</font>**     | 下一个布局     |
| move_tab_forward  | **<font color="#548dd4">ctrl+shift+.</font>**     | 前移标签页     |
| move_tab_backward | **<font color="#548dd4">ctrl+shift+,</font>**     | 后移标签页     |
| set_tab_title     | **<font color="#548dd4">ctrl+shift+alt+t</font>** | 设置标签页名称   |
| goto_tab 1        | **<font color="#548dd4">ctrl+1</font>**           | 跳转到第一个标签页 |
| goto_tab 2        | **<font color="#548dd4">ctrl+2</font>**           | 跳转到第二个标签页 |
| goto_tab 3        | **<font color="#548dd4">ctrl+3</font>**           | 跳转到第三个标签页 |
| goto_tab 4        | **<font color="#548dd4">ctrl+4</font>**           | 跳转到第四个标签页 |
| goto_tab 5        | **<font color="#548dd4">ctrl+5</font>**           | 跳转到第五个标签页 |
| goto_tab 6        | **<font color="#548dd4">ctrl+6</font>**           | 跳转到第六个标签页 |
| goto_tab 7        | **<font color="#548dd4">ctrl+7</font>**           | 跳转到第七个标签页 |
| goto_tab 8        | **<font color="#548dd4">ctrl+8</font>**           | 跳转到第八个标签页 |
| goto_tab 9        | **<font color="#548dd4">ctrl+9</font>**           | 跳转到第九个标签页 |
| goto_tab 10       | **<font color="#548dd4">ctrl+0</font>**           | 跳转到第十个标签页 |
| goto_tab -1       | **<font color="#548dd4">ctrl+-</font>**           | 跳转到前一个标签页 |
#### 窗口(Windows)
| 动作                                       | 快捷键                                               | 描述                             |
| ---------------------------------------- | ------------------------------------------------- | ------------------------------ |
| new_os_window                            | **<font color="#548dd4">super+n</font>**          | New OS window                  |
| new_os_window_with_cwd                   | **<font color="#548dd4">ctrl+super+n</font>**     | New OS window with cwd         |
| new_window                               | **<font color="#548dd4">ctrl+shift+enter</font>** | New window                     |
| close_window                             | **<font color="#548dd4">ctrl+shift+w</font>**     | Close window                   |
| close_window                             | **<font color="#548dd4">super+w</font>**          | Close window                   |
| close_os_window                          | **<font color="#548dd4">ctrl+q</font>**           | Close current active OS Window |
| next_window                              | **<font color="#548dd4">alt+n</font>**            | Next window                    |
| previous_window                          | **<font color="#548dd4">alt+p</font>**            | Previous window                |
| move_window_to_top                       | **<font color="#548dd4">alt+`</font>**            | Move window to top             |
| move_window_to_top                       | **<font color="#548dd4">ctrl+shift+`</font>**     | Move window to top             |
| move_window_forward                      | **<font color="#548dd4">ctrl+shift+f</font>**     | Move window forward            |
| move_window_backward                     | **<font color="#548dd4">ctrl+shift+b</font>**     | Move window backward           |
| move_window_forward                      | **<font color="#548dd4">ctrl+shift+]</font>**     | Move window forward            |
| move_window_backward                     | **<font color="#548dd4">ctrl+shift+[</font>**     | Move window backward           |
| visually_focus_window                    | **<font color="#548dd4">ctrl+shift+f7</font>**    | Visually focus window          |
| visually_swap_window                     | **<font color="#548dd4">ctrl+shift+f8</font>**    | Visually swap window           |
| move_window up                           | **<font color="#548dd4">alt+up</font>**           | Move window in up direction    |
| move_window down                         | **<font color="#548dd4">alt+down</font>**         | Move window in down direction  |
| move_window left                         | **<font color="#548dd4">alt+left</font>**         | Move window in left direction  |
| move_window right                        | **<font color="#548dd4">alt+right</font>**        | Move window in right direction |
| neighboring_window left                  | **<font color="#548dd4">alt+h</font>**            | Focus left neighbor window     |
| neighboring_window right                 | **<font color="#548dd4">alt+l</font>**            | Focus right neighbor window    |
| neighboring_window up                    | **<font color="#548dd4">alt+k</font>**            | Focus up neighbor window       |
| neighboring_window down                  | **<font color="#548dd4">alt+j</font>**            | Focus down neighbor window     |
| first_window                             | **<font color="#548dd4">alt+1</font>**            | Focus 1 window                 |
| second_window                            | **<font color="#548dd4">alt+2</font>**            | Focus 2 window                 |
| third_window                             | **<font color="#548dd4">alt+3</font>**            | Focus 3 window                 |
| fourth_window                            | **<font color="#548dd4">alt+4</font>**            | Focus 4 window                 |
| fifth_window                             | **<font color="#548dd4">alt+5</font>**            | Focus 5 window                 |
| sixth_window                             | **<font color="#548dd4">alt+6</font>**            | Focus 6 window                 |
| seventh_window                           | **<font color="#548dd4">alt+7</font>**            | Focus 7 window                 |
| eighth_window                            | **<font color="#548dd4">alt+8</font>**            | Focus 8 window                 |
| ninth_window                             | **<font color="#548dd4">alt+9</font>**            | Focus 9 window                 |
| tenth_window                             | **<font color="#548dd4">alt+10</font>**           | Focus 10 window                |
| first_window                             | **<font color="#548dd4">ctrl+shift+1</font>**     | Focus 1 window                 |
| second_window                            | **<font color="#548dd4">ctrl+shift+2</font>**     | Focus 2 window                 |
| third_window                             | **<font color="#548dd4">ctrl+shift+3</font>**     | Focus 3 window                 |
| fourth_window                            | **<font color="#548dd4">ctrl+shift+4</font>**     | Focus 4 window                 |
| fifth_window                             | **<font color="#548dd4">ctrl+shift+5</font>**     | Focus 5 window                 |
| sixth_window                             | **<font color="#548dd4">ctrl+shift+6</font>**     | Focus 6 window                 |
| seventh_window                           | **<font color="#548dd4">ctrl+shift+7</font>**     | Focus 7 window                 |
| eighth_window                            | **<font color="#548dd4">ctrl+shift+8</font>**     | Focus 8 window                 |
| ninth_window                             | **<font color="#548dd4">ctrl+shift+9</font>**     | Focus 9 window                 |
| tenth_window                             | **<font color="#548dd4">ctrl+shift+0</font>**     | Focus 10 window                |
| resize_window                            | **<font color="#548dd4">ctrl+shift+r</font>**     |                                |
| resize_window                            | **<font color="#548dd4">ctrl+home</font>**        |                                |
| resize_window narrower                   | **<font color="#548dd4">alt+a>n</font>**          |                                |
| resize_window wider                      | **<font color="#548dd4">alt+a>w</font>**          |                                |
| resize_window taller                     | **<font color="#548dd4">alt+a>u</font>**          |                                |
| resize_window shorter 3                  | **<font color="#548dd4">alt+a>d</font>**          |                                |
| layout_action move_to_screen_edge left   | **<font color="#548dd4">alt+a>left</font>**       |                                |
| layout_action move_to_screen_edge right  | **<font color="#548dd4">alt+a>right</font>**      |                                |
| layout_action move_to_screen_edge top    | **<font color="#548dd4">alt+a>up</font>**         |                                |
| layout_action move_to_screen_edge bottom | **<font color="#548dd4">alt+a>down</font>**       |                                |
| launch --location=split                  | **<font color="#548dd4">f4</font>**               |                                |
| launch --location=hsplit                 | **<font color="#548dd4">f5</font>**               |                                |
| launch --location=vsplit                 | **<font color="#548dd4">f6</font>**               |                                |
#### 剪切板(clipboard)
| 动作                        | 快捷键                                           | 描述  |
| ------------------------- | --------------------------------------------- | --- |
| copy_to_clipboard         | **<font color="#548dd4">ctrl+shift+c</font>** |     |
| paste_from_clipboard      | **<font color="#548dd4">ctrl+shift+v</font>** |     |
| paste_from_selection      | **<font color="#548dd4">ctrl+shift+s</font>** |     |
| paste_from_selection      | **<font color="#548dd4">ctrl+shift+e</font>** |     |
| pass_selection_to program | **<font color="#548dd4">ctrl+shift+o</font>** |     |
#### 字体控制(font)
| 动作                 | 快捷键                                                   | 描述  |
| ------------------ | ----------------------------------------------------- | --- |
| increase_font_size | **<font color="#548dd4">ctrl+shift+equal</font>**     |     |
| decrease_font_size | **<font color="#548dd4">ctrl+shift+minus</font>**     |     |
| increase_font_size | **<font color="#548dd4">ctrl+shift+up</font>**        |     |
| decrease_font_size | **<font color="#548dd4">ctrl+shift+down</font>**      |     |
| restore_font_size  | **<font color="#548dd4">ctrl+shift+backspace</font>** |     |
#### 配置文件控制 
| <center>动作</center> | 快捷键                                            | 描述  |
| ------------------- | ---------------------------------------------- | --- |
| edit_config_file    | **<font color="#548dd4">ctrl+shift+f2</font>** |     |
| load_config_file    | **<font color="#548dd4">ctrl+shift+f5</font>** |     |
| debug_config        | **<font color="#548dd4">ctrl+shift+f6</font>** |     |
#### 布局(layouts)
| 布局             | 描述  |
| -------------- | --- |
| **Fat**        |     |
| **Grid**       |     |
| **Horizontal** |     |
| **Splits**     |     |
| **Stack**      |     |
| **Tall**       |     |
| **Vertical**   |     |

| 动作                   | 快捷键                                 | 描述  |
| -------------------- | ----------------------------------- | --- |
| toggle_layout stack  | **<font color="#548dd4">f1</font>** |     |
| layout_action rotate | **<font color="#548dd4">f7</font>** |     |
#### 其他
| 动作                             | 快捷键                                                | 描述  |
| ------------------------------ | -------------------------------------------------- | --- |
| toggle_fullscreen              | **<font color="#548dd4">ctrl+shift+f11</font>**    |     |
| toggle_maximized               | **<font color="#548dd4">ctrl+shift+f10</font>**    |     |
| kitten unicode_input           | **<font color="#548dd4">ctrl+shift+u</font>**      |     |
| open_url_with_hints            | **<font color="#548dd4">ctrl+shift+e</font>**      |     |
| clear_terminal reset active    | **<font color="#548dd4">ctrl+shift+delete</font>** |     |
| kitty_shell window             | **<font color="#548dd4">ctrl+shift+escape</font>** |     |
| set_background_opacity +0.1    | **<font color="#548dd4">ctrl+shift+a>m</font>**    |     |
| set_background_opacity -0.1    | **<font color="#548dd4">ctrl+shift+a>l</font>**    |     |
| set_background_opacity 1       | **<font color="#548dd4">ctrl+shift+a>1</font>**    |     |
| set_background_opacity default | **<font color="#548dd4">ctrl+shift+a>d</font>**    |     |


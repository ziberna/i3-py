#!/usr/bin/env python
"""
Cycling through scratchpad windows...

Add this to your i3 config file:
    bindsym <key-combo> exec python /path/to/this/script.py
"""

import i3

def scratchpad_windows():
    # get containers with appropriate scratchpad state
    containers = i3.filter(scratchpad_state='changed')
    # filter out windows (leaf nodes of the above containers)
    return i3.filter(containers, nodes=[])

def main():
    windows = scratchpad_windows()
    # search for focused window among scratchpad windows
    if i3.filter(windows, focused=True):
        # move that window back to scratchpad
        i3.move('scratchpad')
    # show the next scratchpad window
    i3.scratchpad('show')

if __name__ == '__main__':
    main()


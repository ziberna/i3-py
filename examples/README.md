i3 usage examples
=================

cycle.py
--------

__cycle.py__ will cycle through all windows (by focusing them) and stop at the
previously focused one(s). This is done by filtering currently focused and
unfocused windows with the help of `i3.filter` function, and the focusing each
of them with the help of `i3.window` function.


fibonaccy.py
------------

__fibonacci.py__ will switch to a (new) workspace named 'fibonacci', then open
default terminal windows in a fibonacci spiral. All newly opened terminals will
close after a few seconds and the script will switch back to the previously
focused workspace.


ipc.py
------

__ipc.py__ is a close clone of the i3-msg; it is a command-line tool for sending
messages to i3-wm.

    usage: i3-ipc [-h] [-s <socket>] [-t <type>] [-T <timeout>]
                  [<message> [<message> ...]]
    
    i3-ipc 0.5.5 (2012-03-29). Implemented in Python.
    
    positional arguments:
      <message>     message or "payload" to send, can be multiple strings
    
    optional arguments:
      -h, --help    show this help message and exit
      -s <socket>   custom path to an i3 socket file
      -t <type>     message type in text form (e.g. "get_tree")
      -T <timeout>  seconds before socket times out, floating point values allowed

wsbar.py
--------

__wsbar.py__ launches a __dzen2__ bar that displays current workspaces.


winmenu.py
----------

__winmenu.py__ launches dmenu (with vertical patch) with a list of clients,
sorted after workspaces. Selecting a client jumps to that window. 


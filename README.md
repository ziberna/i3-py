From [i3's website](http://i3wm.org/):

> i3 is a tiling window manager, completely written from scratch. The target
> platforms are GNU/Linux and BSD operating systems, our code is Free and Open
> Source Software (FOSS) under the BSD license. i3 is primarily targeted at
> advanced users and developers.

--------------------------------------------------------------------------------

__i3-py__ allows you to communicate with __i3-wm__ in various ways.


i3.py
=====

Basic usage
-----------

You can use i3-py by simply calling the i3's commands or any other message types
right through the i3 module:

```python
import i3

workspaces = i3.get_workspaces()

print('List of workspaces:')
for workspace in workspaces:
    print('-', workspace['name'])

msg = i3.focus('right')
if i3.success(msg):
    print('Successfully switched to the right window.')

i3.reload()
```

`i3.success` is just a convience function. It returns `None` if success key
isn't present in the received dictionary. Example output of the above script:

    List of workspaces:
    - 1: main
    - 2: www
    - 3: dev
    - #! sys
    Successfully switched to the right window.

The `i3.focus('right')` could be also written like so:

```python
msg = i3.focus__right() # __ is replaced with a space in a message to i3-wm
```

i3.py is case insensitive when it comes to i3-ipc calls and it also support
number values of each message type. This means that `i3.GET_WORKSPACES` and
`i3.msg(1)` is valid. (1 is the i3-ipc value of the 'GET_WORKSPACES' message
type.)


Socket path
-----------

```python
path = i3.get_socket_path()
print(path)
```

Output:

    Socket path: /tmp/i3-jure.Fs0ayj/ipc-socket.2042


Creating sockets
----------------

```python
socket = i3.socket(path, timeout=1, chunk_size=2048, magic_string='i9-ipc')
socket.send('command', 'restart')
data = socket.receive()
print(data)
socket.close()
```

The first argument is a message type and the second one is the message itself.
You can get all available message types from `i3.msg_types`.

Some of the socket's settings can be changed. Here are the changeable attributes
and their default values:

```python
path = i3.get_socket_path()
magic_string = 'i3-ipc' # safety string for i3-ipc
chunk_size = 1024 # in bytes
timeout = 0.5 # in seconds
buffer = ''.encode('utf-8') # byte string
```

Instead of dealing with sockets you can communicate with i3.msg:

```python
tree = i3.msg('get_tree') # equivalent to i3.get_tree()
i3.msg('command', 'restart') # equivalent to i3.restart()
i3.msg(4) # equivalent to the first line since the i3-ipc value of 'GET_TREE' is 4
```


Creating subscriptions
----------------------

```python
def callback(data, subscription):
    print(data)

subscription = i3.subscription(callback, 'workspace', 'focus')
...
subscription.close() # OR subscription.subscribed = False
```

There's `i3.subscribe(event_type, event)` function that does something similar
to the code above, but waits until KeyboardInterrupt exception is raised.

Available event types are listed in `i3.event_types`.

Subscription class also excepts `event_socket` and `data_socket` if you ever
want to provide already created sockets with non-default settings.


--------------------------------------------------------------------------------

i3-ipc
======

i3-ipc is a Python implementation of an i3-ipc program. It uses i3.py.

Usage
-----

    usage: i3-ipc [-h] [-s <socket>] [-t <type>] [-T <timeout>]
                  [<message> [<message> ...]]
    
    i3-ipc 0.2.0 (2012-02-04). Implemented in Python.
    
    positional arguments:
      <message>     message or "payload" to send, can be multiple strings
    
    optional arguments:
      -h, --help    show this help message and exit
      -s <socket>   custom path to an i3 socket file
      -t <type>     message type in text form (e.g. "get_tree")
      -T <timeout>  seconds before socket times out, floating point values allowed

Examples
--------

    $ i3-ipc focus left
    {'success': True}
    $ i3-ipc -t get_tree
    <huge dictionary>
    $ i3-ipc -t 3    # equivalent to i3-ipc get_outputs
    $ i3-ipc -t workspace init    # equivalent to i3-ipc -t subscribe workspace init
    <events>
    <CTRL-C>
    $ i3-ipc workspace 5: media    # switches to workspace named "5: media"
    {'success': True}


--------------------------------------------------------------------------------

Author: Jure Žiberna  
License: GNU GPL 3

The socket and subscription code is more or less a fix and a cleanup of
[Nathan Middleton's](https://github.com/thepub/i3ipc) and
[David Bronke's](https://github.com/whitelynx/i3ipc) Python implementation of
i3-ipc.

i3-py was communicating to i3 via shell command at first. That didn't work for
subscriptions, so i3-py needed its own sockets. In result, much of the socket
implementation of the above project was rewritten and fixed for use in i3-py.


See [i3-wm's ipc page](http://i3wm.org/docs/ipc.html) for more information about
all features.

--------------------------------------------------------------------------------

i3-py was tested with Python 3.2.2 and 2.7.2.

Dependencies:

- i3-wm
- Python


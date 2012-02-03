i3-py
=====

What is i3?
-----------

From [i3's website](http://i3wm.org/):

> i3 is a tiling window manager, completely written from scratch. The target
> platforms are GNU/Linux and BSD operating systems, our code is Free and Open
> Source Software (FOSS) under the BSD license. i3 is primarily targeted at
> advanced users and developers.


So what does i3-py do?
----------------------

It allows you to communicate with i3 through i3-ipc with the help of i3-msg
command. But it's all hidden away from you.

The module is useful if you want i3 to do something based on its state since any
recieved data is decoded from json into Python lists and dictionaries.


Examples
--------

Basic usage:

```python
import i3

workspaces = i3.get_workspaces()

print('List of workspaces:')
for workspace in workspaces:
	print('-', workspace['name'])

msg = i3.reload()
if i3.success(msg):
	print('Successfully reloaded i3.')

print('Socket path:', i3.get_socket_path())
```

Output:

	List of workspaces:
	- 1: main
	- 2: www
	- 3: dev
	- #! sys
	Successfully reloaded i3.
	Socket path: /tmp/i3-jure.Fs0ayj/ipc-socket.2042

What's great is that you can call commands like this:

```python
msg = i3.focus('right') # will focus the right window
if i3.success(msg):
    print('successfully focused the right window')
```

Or like this:

```python
msg = i3.focus__right() # __ (double underscore) is replaced with space
```

You can also communicate directly through i3-msg:

```python
tree = i3.msg('get_tree') # equivalent to i3.get_tree()
i3.msg('command', 'restart') # equivalent to i3.restart()
```

The first argument is a message type and the second one is the message itself.
You can get all available message types from `i3.msg_types`.


--------------------------------------------------------------------------------

i3-py was tested with Python 3.2.2 and 2.7.2.
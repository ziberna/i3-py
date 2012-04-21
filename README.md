What is i3?
-----------

Well, from [i3's website](http://i3wm.org/) itself:

> i3 is a tiling window manager, completely written from scratch. The target
> platforms are GNU/Linux and BSD operating systems, our code is Free and Open
> Source Software (FOSS) under the BSD license. i3 is primarily targeted at
> advanced users and developers.

i3-py contains tools for i3 users and Python developers. To avoid the confusion,
I'll be refering to i3 as _i3-wm_ from here on.


Install
-------

    pip install i3-py
    # OR/AND (for Python 2.x)
    pip2 install i3-py


Run examples
------------

See `examples/` and their
[README](https://github.com/ziberna/i3-py/tree/master/examples). 


--------------------------------------------------------------------------------

Usage
=====

The basics
----------

The communication with i3-wm is through sockets. There are 7 types of messages:

 - command (0)
 - get_workspaces (1)
 - subscribe (2)
 - get_outputs (3)
 - get_tree (4)
 - get_marks (5)
 - get_bar_config (6)

You can control i3-wm with _command_ messages. Other message types return
information about i3-wm without changing its behaviour.

_Subscribe_ offers 2 event types (read: _changes_) to subscribe for:

 - workspace (0)
 - output (1)

There are various ways to do this with i3.py. Let's start with...


Sending commands
----------------

This is best explained by an example. Say you want to switch a layout from the
current one to tabbed. Here's how to do it:

```python
import i3
success = i3.layout('tabbed')
if success:
    print('Successfully changed layout of the current workspace.')
```

Each command is just a function which accepts any number of parameters. i3.py
formats this function and its parameters into a message to i3-wm.

None of these functions are actually implemented. i3.py checks each attribute
as it is accessed. If it exists in the module, it returns that attribute.
Otherwise it creates a function on the fly. Calling that function sends a
message to i3-wm, based on the name of the attribute and its parameters.

### container criteria

These dynamic functions also take keyword arguments which specify container
criteria. So if you want to focus a particular window, you can do it like so:

```python
i3.focus(title="window title")
```


Other message types
-------------------

OK, _command_ is one type of message, but what about the other ones? Well, they
have to be accessed in a bit different way. You see, when we changed the layout
to tabbed, we didn't have to say that it's a _command_ type of message. But for
other types we'll have to specify the name of the type.

So, getting a list of workspaces (and displaying them) is as simple as this:

```python
import i3
workspaces = i3.get_workspaces()
for workspace in workspaces:
    print(workspace['name'])
```

If the attribute you accessed is an existing message type, then the resulting
function sends a message as a parameter. In fact, we could change the current
layout to stacked like so:

```python
import i3
i3.command('layout', 'stacking')
```

This works for all message types. Actually, if you want to get even lower,
there's this function:

```python
import i3
i3.msg(<message type>, <message>)
```

A message type can be in other formats, as an example here are the alternatives
for get_outputs: GET_OUTPUTS, '3', 3

i3.py is case insensitive when it comes to message types. This also holds true
for accessing non-existent attributes, like `i3.GeT_OuTpUtS()`.


Convenience functions
---------------------

Since all returned data is in a form of a dictionary or list, some
convenience function have been written to effectively work with the data.

### i3.container

i3.container will take keyword arguments and formats them into i3-wm's syntax
for container criteria. The resulting string can be used in i3.msg. Example:

```python
i3.container(title="abc", con_id=123) # returns '[title="abc" con_id="123"]'
```

This function is also used internally for dynamic methods.


### i3.filter

Some calls to i3 will return a huge amount of data, namely `i3.get_tree`. It can
be quite stressful to find what you want in such large dictionary. i3-py
provides this convenience function that will filter the given tree:

```python
i3.filter(focused=False)
```

The above would get you all unfocused nodes in the tree. One useful thing would
be to get a list of focused windows. Since windows are just leaf nodes (that is,
nodes without sub-nodes), you can do this:

```python
i3.filter(nodes=[], focused=True)
```

You can also supply your own tree with `tree` keyword argument.


Lets continue to more advanced stuff...


Subscribing to events
---------------------

Say you want to display information about workspaces whenever a new workspaces
is created. There's a function for that called _subscribe_:

```python
import i3
i3.subscribe('workspace')
```

_Workspace_ is one of the two event types. The other one is _output_, which
watches for output changes.

Just displaying the list of workspaces isn't very useful, we want to actually
do something. Because of that, you can define your own subscription:

```python
import i3

def my_function(event, data, subscription):
    <do something based on the event and data received>
    if <enough of this, let's end subscription>:
        subscription.close()

subscription = i3.Subscription(my_function, 'workspace')
```

There are more parameters available for Subscription class, but some are too
advanced for what has been explained so far.

--------------------------------------------------------------------------------
__NOTE:__ Everything in i3-py project contains a doc string. You can get help
about any feature like so:

```python
import i3
help(i3.Subscription)
```

--------------------------------------------------------------------------------

Okay, so now let's move to some of the more lower-level stuff...


Sockets
-------

Sockets are created with the help of `i3.Socket` class. The class has the
following parameters, all of them optional:

 - path of the i3-wm's socket
 - timeout in seconds when receiving the message
 - chunk size in bytes of a single chunk that is send to i3-wm
 - magic string, that i3-wm checks for (it is "i3-ipc")

The path, if not provided, is retrieved via this unmentioned function:

```python
i3.get_socket_path()
```

The most common-stuff methods of an `i3.Socket` object are `connect`, `close`
and `msg(msg_type, payload='')`. Example of usage:

```python
import i3
socket = i3.Socket()
response = socket.msg(`command`, `focus right`)
socket.close()
```

To check if socket has been closed use the `socket.connected` property. There's
even more lower-level stuff, like packing and unpacking the payload, sending
it and receiving it... See the docs for these.


Exceptions
----------

There are three exceptions:

 - `i3.MessageTypeError`, raised when you use unavailable message type
 - `i3.EventTypeError`, raised when you use unavaible event type
 - `i3.MessageError`, raised when i3 sends back an error (the exception contains
   that error string)

If you want to get the list of available ones from Python, use `i3.MSG_TYPES`
and `i3.EVENT_TYPES`.

Okay, that's all for now. Some stuff has been left out, so be
sure to check the docs via Python's `help` function.


--------------------------------------------------------------------------------

About
=====

Author: Jure Žiberna  
License: GNU GPL 3

Thanks:

 - [i3 window manager](http://i3wm.org/) and its author Michael Stapelberg
 - [Nathan Middleton and his i3ipc](http://github.com/thepub/i3ipc) and its
   current maintainer [David Bronke](http://github.com/whitelynx/i3ipc). The
   existing project was used as a reference on how to implement sockets in
   Python. i3-py fixed some of the critical bugs that i3ipc contains and
   added more high-level features in addition to lower-level ones.

References:

 - [i3-wm's ipc page](http://i3wm.org/docs/ipc.html) has more information
   about i3-ipc interface.
 - [i3-wm's user guide](http://i3wm.org/docs/userguide.html) contains lots of
   commands that you can use with i3-py.

i3-py was tested with Python 3.2.2 and 2.7.2.

Dependencies:

- i3-wm
- Python


#======================================================================
# i3 (Python module for communicating with i3 window manager)
# Copyright (C) 2012  Jure Ziberna
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#======================================================================


import sys
import subprocess
import json
import socket as socks
import struct
import threading


__author__ = 'Jure Ziberna'
__version__ = '0.0.3'
__license__ = 'GNU GPLv3'


msg_types = [
    'command',
    'get_workspaces',
    'subscribe',
    'get_outputs',
    'get_tree',
    'get_marks',
    'get_bar_config',
]


event_types = [
    'workspace',
    'output',
]


class subscribtion(threading.Thread):
    subscribed = False
    type_translation = {
        'workspace': 'get_workspaces',
        'output': 'get_outputs'
    }
    
    def __init__(self, callback, event_type, event=None):
        # Variable initialization
        if not callable(callback):
            raise TypeError("callback must be callable")
        if event_type not in event_types:
            raise ValueError("Unsupported event type")
        self.callback = callback
        self.event_type = event_type
        self.event = event
        # Socket initialization
        self.event_socket = socket()
        self.event_socket.subscribe(event_type, event)
        self.data_socket = socket()
        # Thread initialization
        threading.Thread.__init__(self)
        self.start()
    
    def run(self):
        self.subscribed = True
        while self.subscribed:
            event = self.event_socket.receive()
            while event and self.subscribed:
                if 'change' in event and event['change'] == self.event:
                    msg_type = self.type_translation[self.event_type]
                    data = self.data_socket.get(msg_type)
                    self.callback(data)
                event = self.event_socket.receive()
    
    def close(self):
        self.subscribed = False


class socket(object):
    magic_string = 'i3-ipc'
    chunk_size = 1024 # in bytes
    timeout = 0.5 # in seconds
    event_mask = 1 << 31
    event_workspace = event_mask | 0
    event_output = event_mask | 1
    buffer = ''.encode('utf-8')
    
    def __init__(self, path=None):
        if not path:
            path = get_socket_path()
        self.path = path
        # Socket initialization
        self.socket = socks.socket(socks.AF_UNIX, socks.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect(self.path)
        # Struct format initialization, length of magic string is in bytes
        self.struct_header = '<%dsII' % len(self.magic_string.encode('utf-8'))
        self.struct_header_size = struct.calcsize(self.struct_header)
    
    def get(self, msg_type, payload=''):
        self.send(msg_type, payload)
        return self.receive()
    
    def subscribe(self, event_type, event=None):
        if event_type not in event_types:
            raise ValueError("Unsupported event type")
        # Create JSON payload from given event type and event
        payload = [event_type]
        if event:
            payload.append(event)
        payload = json.dumps(payload)
        return self.get('subscribe', payload)
    
    def send(self, msg_type, payload=''):
        if msg_type not in msg_types:
            raise ValueError("Unsupported message type")
        message = self.pack(msg_type, payload)
        # Continuously send the bytes from message
        self.socket.sendall(message)
    
    def receive(self):
        try:
            data = self.socket.recv(self.chunk_size)
            msg_magic, msg_length, msg_type = self.unpack_header(data)
            msg_size = self.struct_header_size + msg_length
            # Receive data until whole message is through
            while len(data) < msg_size:
                data += self.socket.recv(msg_length)
            data = self.buffer + data
            return self.unpack(data)
        except socks.timeout:
            self.buffer
    
    def pack(self, msg_type, payload):
        msg_magic = self.magic_string
        # Get the byte count instead of number of characters
        msg_length = len(payload.encode('utf-8'))
        msg_type = msg_types.index(msg_type)
        # "struct.pack" returns byte string, decoding it for concatenation
        msg_length = struct.pack('I', msg_length).decode('utf-8')
        msg_type = struct.pack('I', msg_type).decode('utf-8')
        message = '%s%s%s%s' % (msg_magic, msg_length, msg_type, payload)
        # Encoding the message back to byte string
        return message.encode('utf-8')
    
    def unpack(self, data):
        data_size = len(data)
        msg_magic, msg_length, msg_type = self.unpack_header(data)
        msg_size = self.struct_header_size + msg_length
        # Message shouldn't be any longer than the data
        if data_size >= msg_size:
            payload = data[self.struct_header_size:msg_size].decode('utf-8')
            payload = json.loads(payload)
            self.buffer = data[msg_size:]
            return payload
        else:
            self.buffer = data
            return None
    
    def unpack_header(self, data):
        return struct.unpack(self.struct_header, data[:self.struct_header_size])
    
    def close(self):
        self.socket.close()
    

def __call_cmd__(cmd):
    """
    Excepts command arguments.
    Returns output (stdout or stderr).
    Uses subprocess module for executing the command.
    """
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as error:
        output = error.output
    output = output.decode('utf-8') # byte string decoding
    return output.strip()


def msg(type, message=''):
    """
    Excepts a message type and a message itself.
    Talks to the i3 via i3-msg command, returns the output.
    Uses json module for decoding output.
    """
    cmd = ['i3-msg', '-t', type, message]
    output = __call_cmd__(cmd)
    if output:
        try:
            output = json.loads(output)
        except ValueError:
            pass
    return output


def __function__(type, message=''):
    """
    Excepts a message type and a message itself.
    Returns lambda function, which excepts arguments and adds them to the
    message string, calls message function with the resulting arguments.
    """
    message = ' '.join(message.split('__'))
    return lambda *args: msg(type, ' '.join([message] + list(args)))


def subscribe(payload=None):
    raise NotImplementedError("Subscribing not implemented. Sorry.")


def get_socket_path():
    """
    Get the path via i3 command.
    """
    cmd = ['i3', '--get-socketpath']
    output = __call_cmd__(cmd)
    return output


def success(json_msg):
    """
    Convenience method for checking success value.
    Returns None if the "success" key isn't in the received message.
    """
    if isinstance(json_msg, dict) and 'success' in json_msg:
        return json_msg['success']
    return None
    


""" The magic starts here """
class i3(object):
    def __getattr__(self, name):
        """
        Turns a nonexistent attribute into a function.
        Returns the resulting function.
        """
        try:
            return getattr(self.__module__, name)
        except AttributeError:
            pass
        if name in self.__module__.msg_types and name is not 'command':
            return self.__module__.__function__(type=name)
        else:
            return self.__module__.__function__(type='command', message=name)
    

# Save the module to the i3 class
i3.__module__ = sys.modules[__name__]

# Turn the module into an i3 object
sys.modules[__name__] = i3()


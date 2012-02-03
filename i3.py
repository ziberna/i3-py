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


__author__ = 'Jure Ziberna'
__version__ = '0.0.3'
__license__ = 'GNU GPLv3'


msg_types = [
    'get_workspaces',
    'get_outputs',
    'get_tree',
    'get_marks',
    'get_bar_config',
]


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


def get_socket_path(self):
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
        if name in self.__module__.msg_types:
            return self.__module__.__function__(type=name)
        else:
            return self.__module__.__function__(type='command', message=name)
    

# Save the module to the i3 class
i3.__module__ = sys.modules[__name__]

# Turn the module into an i3 object
sys.modules[__name__] = i3()


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
__version__ = '0.0.2'
__license__ = 'GNU GPLv3'


msg_types = [
    'get_workspaces',
    'subscribe',
    'get_outputs',
    'get_tree',
    'get_marks',
    'get_bar_config',
]


class i3(object):
    def __init__(self, module):
        self.__module = module
    
    def __getattr__(self, name):
        """
        Turns a nonexistent attribute into a function.
        Returns the resulting function.
        """
        try:
            return getattr(self.__module, name)
        except AttributeError:
            pass
        if name in msg_types:
            return self.func(type=name)
        else:
            return self.func(type='command', message=name)
    
    def __call_cmd(self, cmd):
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
    
    def msg(self, type, message=''):
        """
        Excepts a message type and a message itself.
        Talks to the i3 via i3-msg command, returns the output.
        Uses json module for decoding output.
        """
        cmd = ['i3-msg', '-t', type, message]
        output = self.__call_cmd(cmd)
        if output:
            try:
                output = json.loads(output)
            except ValueError:
                pass
        return output
    
    def func(self, type, message=''):
        """
        Excepts a message type and a message itself.
        Returns lambda function, which excepts arguments and adds them to the
        message string, calls message function with the resulting arguments.
        """
        message = ' '.join(message.split('__'))
        return lambda *args: self.msg(type, ' '.join([message] + list(args)))
    
    def subscribe(self, payload=None):
        raise NotImplementedError("Subscribing not implemented. Sorry.")
    
    def get_socket_path(self):
        """
        Get the path via i3 command.
        """
        cmd = ['i3', '--get-socketpath']
        output = self.__call_cmd(cmd)
        return output
    
    def success(self, json_msg):
        """
        Convenience method for checking success value.
        Returns None if the "success" key isn't in the received message.
        """
        if isinstance(json_msg, dict) and 'success' in json_msg:
            return json_msg['success']
        return None
    


""" The magic """
sys.modules[__name__] = i3(sys.modules[__name__])


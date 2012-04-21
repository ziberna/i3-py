#!/usr/bin/env python
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


import os
import argparse

import i3


# Generate description based on current version and its date
DESCRIPTION = 'i3-ipc %s (%s).' % (i3.__version__, i3.__date__)
DESCRIPTION += ' Implemented in Python.'

# Dictionary of command-line help messages
HELP = {
    'socket': "custom path to an i3 socket file",
    'type': "message type in text form (e.g. \"get_tree\")",
    'timeout': "seconds before socket times out, floating point values allowed",
    'message': "message or \"payload\" to send, can be multiple strings",
}


def parse():
    """
    Creates argument parser for parsing command-line arguments. Returns parsed
    arguments in a form of a namespace.
    """
    # Setting up argument parses
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-s', metavar='<socket>', dest='socket', type=str, default=None, help=HELP['socket'])
    parser.add_argument('-t', metavar='<type>', dest='type', type=str, default='command', help=HELP['type'])
    parser.add_argument('-T', metavar='<timeout>', dest='timeout', type=float, default=None, help=HELP['timeout'])
    parser.add_argument('<message>', type=str, nargs='*', help=HELP['message'])
    # Parsing and hacks
    args = parser.parse_args()
    message = args.__dict__['<message>']
    args.message = ' '.join(message)
    return args


def main(socket, type, timeout, message):
    """
    Excepts arguments and evaluates them.
    """
    if not socket:
        socket = i3.get_socket_path()
        if not socket:
            print("Couldn't get socket path. Are you sure i3 is running?")
            return False
    # Initializes default socket with given path and timeout
    try:
        i3.default_socket(i3.Socket(path=socket, timeout=timeout))
    except i3.ConnectionError:
        print("Couldn't connect to socket at '%s'." % socket)
        return False
    # Format input
    if type in i3.EVENT_TYPES:
        event_type = type
        event = message
        type = 'subscribe'
    elif type == 'subscribe':
        message = message.split(' ')
        message_len = len(message)
        if message_len >= 1:
            event_type = message[0]
            if message_len >= 2:
                event = ' '.join(message[1:])
            else:
                event = ''
        else:
            # Let if fail
            event_type = ''
    try:
        if type == 'subscribe':
            i3.subscribe(event_type, event)
        else:
            output = i3.msg(type, message)
            print(output)
    except i3.i3Exception as i3error:
        print(i3error)


if __name__ == '__main__':
    args = parse()
    main(args.socket, args.type, args.timeout, args.message)


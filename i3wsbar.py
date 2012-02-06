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


import subprocess

import i3


__author__ = 'Jure Ziberna'
__version__ = '0.1.0'
__date__ = '2012-02-06'
__license__ = 'GNU GPL 3'


class Colors(object):
    """
    A class for easier managing of bar's colors.
    Attributes (hexadecimal color values):
    - background
    - statusline (foreground)
    (below are (foreground, background) tuples for workspace buttons)
    - focused
    - active (when a workspace is opened on unfocused output)
    - inactive (unfocused workspace)
    - urgent
    The naming comes from i3-wm itself.
    Default values are also i3-wm's defaults.
    """
    # bar colors
    background = '#000000'
    statusline = '#ffffff'
    # workspace button colors
    focused = ('#ffffff', '#285577')
    active = ('#ffffff', '#333333')
    inactive = ('#888888', '#222222')
    urgent = ('#ffffff', '#900000')
    
    def get_color(self, workspace, output):
        """
        Returns a (foreground, background) tuple based on given workspace
        state.
        """
        if workspace['focused']:
            if output['current_workspace'] == workspace['name']:
                return self.focused
            else:
                return self.active
        if workspace['urgent']:
            return self.urgent
        else:
            return self.inactive


class i3wsbar(object):
    """
    A workspace bar; display a list of workspaces using a given bar
    application. Defaults to dzen2.
    Changeable settings (attributes):
    - button_format
    - bar_format
    - colors (see i3wsbar.Colors docs)
    - font
    - bar_command (the bar application)
    - bar_arguments (command-line arguments for the bar application)
    """
    # bar formatting (set for dzen)
    button_format = '^bg(%s)^ca(1,i3-ipc workspace %s)^fg(%s)%s^ca()^bg() '
    bar_format = '^p(_LEFT) %s^p(_RIGHT) '
    # default bar style
    colors = Colors()
    font = '-misc-fixed-medium-r-normal--13-120-75-75-C-70-iso10646-1'
    # default bar settings
    bar_command = 'dzen2'
    bar_arguments = ['-dock', '-fn', font, '-bg', colors.background, '-fg', colors.statusline]
    
    def __init__(self, colors=None, font=None, bar_cmd=None, bar_args=None):
        if colors:
            self.colors = colors
        if font:
            self.font = font
        if bar_cmd:
            self.dzen_command = bar_cmd
        if bar_args:
            self.bar_arguments = bar_args
        # Initialize bar application...
        args = [self.bar_command] + self.bar_arguments
        self.bar = subprocess.Popen(args, stdin=subprocess.PIPE)
        # ...and socket
        self.socket = i3.Socket()
        # Output to the bar right away
        workspaces = self.socket.get('get_workspaces')
        outputs = self.socket.get('get_outputs')
        self.display(self.format(workspaces, outputs))
        # Subscribe to an event
        callback = lambda data, event, _: self.change(data, event)
        self.subscription = i3.Subscription(callback, 'workspace')
    
    def change(self, event, workspaces):
        """
        Receives event and workspace data, changes the bar if change is
        present in event.
        """
        if 'change' in event:
            outputs = self.socket.get('get_outputs')
            bar_text = self.format(workspaces, outputs)
            self.display(bar_text)
    
    def format(self, workspaces, outputs):
        """
        Formats the bar text according to the workspace data given.
        """
        bar = ''
        for workspace in workspaces:
            output = None
            for output_ in outputs:
                if output_['name'] == workspace['output']:
                    output = output_
                    break
            if not output:
                continue
            foreground, background = self.colors.get_color(workspace, output)
            if not foreground:
                continue
            name = workspace['name']
            button = self.button_format % (background, "'"+name+"'", foreground, name)
            bar += button
        return self.bar_format % bar
    
    def display(self, bar_text):
        """
        Displays a text on the bar by piping it to the bar application.
        """
        bar_text += '\n'
        try:
            bar_text = bar_text.encode()
        except AttributeError:
            pass  # already a byte string
        self.bar.stdin.write(bar_text)
    
    def quit(self):
        """
        Quits the i3wsbar; closes the subscription and terminates the bar
        application.
        """
        self.subscription.close()
        self.bar.terminate()
    

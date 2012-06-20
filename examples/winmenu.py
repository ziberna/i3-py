#!/usr/bin/env python
# dmenu script to jump to windows in i3.
# Makes a list of nicely formatted strings for each open window, containing
# workspace name, mark (if any), window title, and instance (would the previous
# give a non-unique result). dmenu provides a fast method of selection. 
# If the result of dmenu is that there is no match for an existing window, 
# the currently focused window will get a mark with this word. 
#
# using ziberna's i3-py library: https://github.com/ziberna/i3-py
# depends: dmenu (vertical patch), i3.
# released by joepd under WTFPLv2-license:
# http://sam.zoy.org/wtfpl/COPYING
#
# edited by Jure Ziberna for i3-py's examples section

import i3
import subprocess

def i3clients():
    """
    Returns a dictionary with convoluted strings with window information as keys, 
    and the i3 window id as values. Each window text is of format 
    "[workspace] mark window title (instance number)."
    """
    clients = {}
    lengths = {'workspace': 0, 'mark': 0}
    for ws in i3.get_workspaces():
        wsname = ws['name']
        if len(wsname) > lengths['workspace']:
            lengths['workspace'] = len(wsname)
        workspace = i3.filter(name=wsname)
        if not workspace:
            continue
        workspace = workspace[0]
        windows = i3.filter(workspace, nodes=[])
        instances = {}
        # Adds windows and their ids to the clients dictionary
        for window in windows:
            windowdict = {
                    'con_id': window['id'], \
                    'ws': wsname, \
                    'name': window['name']}
            try: 
                windowdict['mark'] = window['mark']
                if len(window['mark']) > lengths['mark']:
                    lengths['mark'] = len(window['mark'])
            except KeyError:
                windowdict['mark'] = ""
            if window['name'] in instances: 
                instances[window['name']] += 1
            else: 
                instances[window['name']]  = 1
            windowdict['instance'] = instances[window['name']]
            # win_str = '[%s] %s' % (workspace['name'], window['name'])
            clients[window['id']] = windowdict

    # Now build the strings to pass to dmenu: 
    newdict = {}
    clientlist = []
    for con_id in clients.keys():
        clientlist.append(con_id)
    for con_id in clientlist:
        wslen = lengths['workspace']
        mlen = lengths['mark']
        win_str = '[{k:<{v}}] {l:<{w}} {m} ({n})'.format(\
                k=clients[con_id]['ws'], v=wslen, \
                l=clients[con_id]['mark'], w=mlen, \
                m=clients[con_id]['name'], \
                n=clients[con_id]['instance'])
        clients[win_str] = clients[con_id]
        del clients[con_id]
    return clients


def win_menu(clients, l=20):
    """
    Displays a window menu using dmenu.
    """
    dmenu = subprocess.Popen(['/usr/bin/dmenu','-i','-l', str(l)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
    menu_str = '\n'.join(sorted(clients.keys()))
    # Popen.communicate returns a tuple stdout, stderr
    win_str = dmenu.communicate(menu_str.encode('utf-8'))[0].decode().rstrip()
    return win_str

if __name__ == '__main__':
    clients = i3clients()
    win_str = win_menu(clients)
    try:
        clients[win_str]
    except:
        i3.mark(win_str)
        raise SystemExit
    con_id = clients[win_str]['con_id']
    i3.focus(con_id=con_id)



import i3
import os
import time

term = os.environ.get('TERM', 'xterm')
if 'rxvt-unicode' in term: 
    term = 'urxvt'

def fibonacci(num):
    i3.exec(term)
    time.sleep(0.5)
    if num % 2 == 0:
        if num % 4 == 0:
            i3.focus('up')
        i3.split('h')
    else:
        if num % 4 == 1:
            i3.focus('left')
        i3.split('v')
    if num > 1:
        fibonacci(num - 1)

def run(num):
    # current workspace
    current = [ws for ws in i3.get_workspaces() if ws['focused']][0]
    # switch to workspace named 'fibonacci'
    i3.workspace('fibonacci')
    i3.layout('default')
    fibonacci(num)
    time.sleep(3)
    # close all opened terminals
    for n in range(num):
        i3.kill()
        time.sleep(0.5)
    i3.workspace(current['name'])

if __name__ == '__main__':
    run(8)

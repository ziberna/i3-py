import i3
import time

def cycle():
    # get currently focused windows
    current = i3.filter(nodes=[], focused=True)
    # get unfocused windows
    other = i3.filter(nodes=[], focused=False)
    # focus each previously unfocused window for 0.5 seconds
    for window in other:
        i3.window('focus', title=window['name'])
        time.sleep(0.5)
    # focus the original windows
    for window in current:
        i3.window('focus', title=window['name'])

if __name__ == '__main__':
    cycle()
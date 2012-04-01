import i3
import time

def cycle():
    current = i3.filter(nodes=[], focused=True)
    other = i3.filter(nodes=[], focused=False)
    for window in other:
        i3.window('focus', title=window['name'])
        time.sleep(0.5)
    for window in current:
        i3.window('focus', title=window['name'])

if __name__ == '__main__':
    cycle()
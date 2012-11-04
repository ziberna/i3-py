#!/usr/bin/env python
"""
Find the first free workspace and switch to it

Add this to your i3 config file:
	bindsym <key-combo> exec python /path/to/this/script.py
"""
import i3

def main():
	workspaces = i3.get_workspaces()
	workints = list()
	for w in workspaces:
		workints.append(w['name'])
	for i in range(1,11):
		if str(i) not in workints:
			i3.workspace(str(i))
			break

if __name__ == '__main__':
	main()

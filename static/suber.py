#!/usr/bin/python
#coding:utf-8

import re
import sys
import os

def change(f_name):
	dirs = ['ad', 'css', 'fonts', 'images', 'js']
	f = open(f_name, 'r')
	html = ''.join(f.readlines())
	f.close()
	for d in dirs:
		pattern = re.compile('(?<=")(' + d + '\/[\w\.-]+)(?=[" ])')
		subs = pattern.findall(html)
		subs = set(subs)
		for s in subs:
			# html = html.replace(s, '{{ url_for(\'static\', filename=\'' + s + '\') }}')
			print s
			html = html.replace(s, '/static/' + s)

	f = open(f_name, 'w')
	f.writelines(html)
	f.close()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		l = os.walk('.')
		for root, dirs, files in l:
			if root != '.':
				continue
			for j in files:
				print ' ******', root, j
				change(j)
				print 'input anything to continue'
				raw_input()
	else:
		print sys.argv[1]
		change(sys.argv[1])
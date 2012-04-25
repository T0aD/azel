#! /usr/bin/python

import sys
sys.path.insert(0, sys.path[0] + '/..')

import azel

s = azel.Azel()
url = 'https://github.com/' + sys.argv[1]
s.get(url)

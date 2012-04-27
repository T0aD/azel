#! /usr/bin/python

import sys
sys.path.insert(0, sys.path[0] + '/..')

import io # open / read
import os # getenv
import azel # cause its awesome.

if len(sys.argv) < 2:
    print "syntax:", sys.argv[0], "<file>"
    exit()

fd = io.open(sys.argv[1], 'r')
content = fd.read(None)
fd.close

bin = azel.Azel()

bin.get('http://bpaste.net/+python')
bin.fillForm()

bin.data['language'] = 'python'
bin.data['code'] = content
bin.post('')

print 'Paste found on:', bin.url





#! /usr/bin/python

"""
Paste the given file as parameter on GIST
"""

import sys
import os
import io

sys.path.insert(0, sys.path[0] + '/..')
import azel

a = azel.Azel()

if len(sys.argv) < 2:
    print "syntax:", sys.argv[0], "<file>"
    exit()

fd = io.open(sys.argv[1], 'r')
content = fd.read(None)
fd.close()

a.get('http://gist.github.com/')
a.fillForm()

#a.data['file_ext[gistfile1]'] = '.py'
a.data['file_name[gistfile1]'] = sys.argv[1].strip('./')
a.data['description'] = 'This was published by awesome azel!'
a.data['file_contents[gistfile1]'] = content

a.post('') # will post the first form

print 'Paste found on:', a.url





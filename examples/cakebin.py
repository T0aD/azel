#! /usr/bin/python

"""
Paste a file on a pastebin web app
""" # what do you mean by 'my multiline comment is useless' ?!

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

bin.get('http://bin.cakephp.org')
bin.fillForm()

bin.data['data[NewPaste][lang]'] = 'python'
bin.data['data[NewPaste][nick]'] = os.getenv('USER') # yeah pwd.getpwuid(os.getuid()).pw_name
# would have been more awesome
bin.data['data[NewPaste][note]'] = 'Content of file ' + sys.argv[1]
bin.data['data[NewPaste][body]'] = content
bin.post('')

print 'Paste found on:', bin.url





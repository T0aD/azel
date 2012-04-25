#! /usr/bin/python

import sys
sys.path.insert(0, sys.path[0] + '/..')

import azel
import re

s = azel.Azel()

# Here we specify a HTTP proxy:
s.proxyHost = '10.7.0.1'
s.proxyPort = 8118

url = 'http://www.brigada.sk/'

s.get(url)
s.fillForm()
s.post()
pattern = '<span class="brigady">([^<]+)</span>'
for i in range(1, 20):
    s.fillForm()
    s.data['page_current'] = i
    s.post()
    m = re.findall(pattern, s.read(), re.I)
    for match in m:
        m2 = re.search('(call)', match, re.I)
        if m2 != None:
            print 'PAGE', i, '='*20, match
            print s.url



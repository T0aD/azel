#! /usr/bin/python

import sys
sys.path.insert(0, sys.path[0] + '/..') # to fetch azel.py in the directory up

"""
-> GET http://freeproxyserver.net/
<- 200 OK
-> GET http://freeproxyserver.net/?q=aHR0cDovL2dldG15aXBhZGRyZXNzLm5ldC8-&hl=1111101001
<- 200 OK
IP address found: 67.159.44.96
"""

import azel
import base64
import re

azel = azel.Azel()

# Target URL:
url = 'http://getmyipaddress.net/'

proxy_url = 'http://freeproxyserver.net/'
azel.get(proxy_url)
azel.fillForm()

azel.data = {}
azel.data['q'] = base64.b64encode(url)
azel.data['hl'] = '1111101001'
urlEncoded = base64.b64encode(url, '._').replace('=', '-')
azel.get(proxy_url + '?q=' + urlEncoded + '&hl=1111101001')

pattern = 'My IP Address is:</font>[\r\n ]+<font size="10" face="verdana">([0-9\.]+)</font>'
m = re.search(pattern, azel.read())
if m is not None:
    print 'IP address found:', m.group(1)


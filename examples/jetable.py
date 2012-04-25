#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, sys.path[0] + '/..')

# Used to work (to create a temporary email through an alias), but you get the idea..

import azel

# Jetable.org
def generateAlias(email):
    jetable = azel.Azel()
    jetable.get('http://www.jetable.org')
    jetable.fillForm()
    jetable.data['time'] = 3600
    jetable.data['email'] = email
    jetable.post()
# Get back the created alias: <span id="aliasgenerated">00rq8gnmdcyxuxc@jetable.org</span>
    page = jetable.response.read()
    m = re.search('"aliasgenerated"\>(.*)\</span', page)
    if m == None:
        print 'could not get an alias, aborting..'
        print page
        exit()
    alias = m.group(1)
    print '++ Alias generated:', alias
    return alias


alias = generateAlias('toaddy@yopmail.com')

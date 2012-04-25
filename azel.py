#! /usr/bin/python
# -*- coding: utf-8 -*-

import httplib
import urllib
from HTMLParser import HTMLParser
from sgmllib import SGMLParser
import re
import os.path # using dirname() on URI actually ;)

# Used to store Link properties the object way
class Link:
    href = None
    value = '' # the textual value of the link
    title = None

    def search(self, text):
        text = unicode(text, 'utf-8')
        if self.href == None:        # no need to return None..
            return None
        m = re.search(text, self.href)
        if m != None:
            return self.href
        if self.value != None:
            m = re.search(text, self.value)
            if m != None:
                return self.href
        if self.title != None: 
            m = re.search(text, self.title)
            if m != None:
                return self.href

class LinkParser(HTMLParser):
    in_a = False
    links = []
    currentLink = None

    def handle_starttag(self, tag, attrs):
        if self.in_a == True:
            self.currentLink.value += self.get_starttag_text()
        if tag == 'a':
            self.in_a = True
            self.currentLink = Link()
            for key, value in attrs:
                if key == 'href' and value:
                    self.currentLink.href = value
                if key == 'title' and value:
                    self.currentLink.title = value

    def handle_data(self, data):
        if self.in_a == True:
            self.currentLink.value += data + ' '

    def handle_endtag(self, tag):
        if tag == 'a':
            self.in_a = False
            if self.currentLink != None:
#                print self.currentLink
                self.links.append(self.currentLink)
                link = self.currentLink
                #print str(link.href)[:14], '#' * 4, link.value, '#' * 4, link.title
                self.currentLink = None
        if self.in_a == True:
            self.currentLink.value += '</' + tag + '>'


# Basic parser to collect interesting fields
class MyHTMLParser(SGMLParser):
    nbForms = 0
    inForm = False
    tagsofinterest = ('input', 'select', 'textarea')
    # The URL of the form
    targetURL = False
    # The different names of the fields to post
    fields = []
    postdata = {}
    # links management
    links = [] # list of links found
    currentLink = None
    # iframes
    iframes = []
    # future targets in forms:
    target = None

    def __init__(self, verbose=0):
        SGMLParser.__init__(self, verbose)
        self.links = []
        self.iframes = []
        self.starting_description = False

    def restart(self):
        self.targetURL = False
        self.inForm = False
        self.fields = []
        self.nbForms = 0

    def start_iframe(self, attrs):
        for key, value in attrs:
            if key == 'src' and value != '':
                self.iframes.append(value)
        
    def start_a(self, attrs):
        self.currentLink = Link()
        for key, value in attrs:
            if key == "title" and value:
                self.currentLink.title = value
            if key == "href" and value != '':
                self.currentLink.href = value
#               if value not in self.links:
#                    self.links.append(value)

#                    print self.get_starttag_text()
#        self.starting_description = True

    def end_a(self):
#        return None
        link = self.currentLink
#        print 'completed', link.href, '###'*3, link.title, '###'*3
#        print 'completed', link.href, '###'*3, link.value, '###'*3
        self.links.append(link)
#        self.currentLink = None
#        print 'start text', self.get_starttag_text()

    def handle_data(self, data):
        if self.currentLink != None:
            if self.starting_description:
#                print 'started', data, '#######'
#                print 'found', data
                self.starting_description = False
                self.currentLink.value = data
            else:
#            print 'adding', data
                self.currentLink.value = data


    def unknown_starttag(self, tag, attrs):
#        if self.currentLink != None:
#            print tag, attrs
        if self.inForm == True:
            for key in self.tagsofinterest:
                if key == tag:
                    ntag = {}
                    for key, value in attrs:
                        ntag[key] = value
#                    print ntag
                    if ntag.has_key('type') and ntag['type'] == "hidden" and ntag.has_key('value'):
                        # we can directly fill values for hidden fields:
                        self.postdata[ntag['name']] = ntag['value']
                    elif ntag.has_key('name') and ntag['name'] != '':
                        self.postdata[ntag['name']] = ''
                        self.fields.append(ntag['name'])
        if tag == "form":
            self.inForm = True
            self.nbForms += 1
#            print 'forms', self.nbForms
            for key, value in attrs:
                if key == 'action':
                    self.targetURL = value

    def unknown_endtag(self, tag):
        if tag == "form":
            self.inForm = False

class Azel: # Hommage to Elza macro language
    # cookies to be sent
    cookies = {}
    cookiesList = []
    cookies_set = False
    display_cookies = False
    # referer if any
    referer = False
    # reference to sgml parser
    parser = False
    # reference to httplib
    http = False
    response = False
    ssl = False
    host = ''
    uri = '/'
    url = ''
    # data to POST
    data = {}
    content = None # page content (response.read())

    proxyHost = False
    proxyPort = False

    def __init__(self):
        self.parser = MyHTMLParser()
        self.data = {}
        self.cookies.clear()

    def read(self):
        if self.content == None:
            self.content = self.response.read()
        return self.content

    def post(self, url=None):
        self.request('POST', url)

    def get(self, url=None):
        self.request('GET', url)

    def request(self, method, url):
        self.content = None
        # If url aint specified, used the one saved in the property by fillForm():
        if url == '' or url == None:
            url = self.url
        self.parseURL(url)
        if self.ssl == False:
            if self.proxyHost != False:
                self.http = httplib.HTTPConnection(self.proxyHost, self.proxyPort)
            else:
                self.http = httplib.HTTPConnection(self.host)
        else:
            self.http = httplib.HTTPSConnection(self.host)
        if self.proxyHost != False:
            print '->', method, self.url, '(proxy)'
            self.http.putrequest(method, self.url)            
        else:
            print '->', method, self.url
            self.http.putrequest(method, self.uri)

        # Set cookies if needed
        if self.cookies_set == True:
            if self.display_cookies == True:
                print '== Cookies:', '; '.join(self.cookiesList)
            self.http.putheader('Cookie', '; '.join(self.cookiesList))
        if self.referer:
#            print '== Referer:', self.referer
            self.http.putheader('Referer', self.referer)
        # Add data to post
        if method == "POST":
            self.http.putheader('Content-type', 'application/x-www-form-urlencoded')
            self.http.putheader('Content-length', len(urllib.urlencode(self.data)))
        try:
            self.http.endheaders()

            self.http.send(urllib.urlencode(self.data))
        except Exception as e:
            print 'Error:', e
            exit()
        # Always clean data
        self.data = {}

        # Set the new referer
        self.referer = self.url


        self.response = self.http.getresponse()
        print '<-', self.response.status, self.response.reason

#        print self.read()
#        print self.response.msg

        self.handleCookies()
        self.handleRedirection()

    def handleRedirection(self):
        if str(self.response.status).startswith("3"):
            redirect = self.response.getheader('Location')
            self.get(redirect)

    def handleCookies(self):
        cookies = self.response.msg.getallmatchingheaders('set-cookie')
        for cookie in cookies:
            start = cookie.find(' ') + 1 # Skip Set-Cookie: 
            end = cookie.find(';')
            cookie = cookie[start:end]
            sep = cookie.find('=')
            name = cookie[:sep]
            value = cookie[sep+1:]
            self.cookies[name] = value
        # Prepare cookies for insertion in headers
        self.cookiesList = []
        self.cookies_set = False # reset completely cookies
        for key in self.cookies.keys():
            self.cookies_set = True
            cookie = key + '=' + self.cookies[key]
            self.cookiesList.append(cookie)

    def parseURL(self, url):
        offset = url.find('#')
        if offset != -1:
            url = url[:offset] # remove #links
        self.url = url
        relative = False
        if url.startswith("http://"):
            newURL = url[len("http://"):]
            self.ssl = False
        elif url.startswith("https://"):
            newURL = url[len("https://"):]
            self.ssl = True
        else:
            newURL = url
            relative = True
        if relative == False:
            offset = newURL.find('/')
            if offset == -1:
                self.uri = '/'
                self.host = newURL
            else:
                self.host = newURL[0:offset]
                self.uri = newURL[offset:]
        else: # relative == True:
            if not newURL.startswith('/'): # fix urls like 'confirm' instead of /confirm:
                self.uri = os.path.join(os.path.dirname(self.uri), newURL)
            else:
                self.uri = newURL
            if self.ssl == True:
                self.url = 'https://' + self.host + self.uri
            else:
                self.url = 'http://' + self.host + self.uri

    def parse(self):
        self.parser = MyHTMLParser()
        self.parser.feed(self.read())
        self.parser.close()

    # Will prepare hidden fields and new url to POST
    def fillForm(self, target=None):
        self.parser = MyHTMLParser()
        self.parser.postdata = {}
        self.parser.targetURL = None
        self.parser.target
        self.parser.feed(self.read())
        self.parser.close()
        self.data = self.parser.postdata
        self.url = self.parser.targetURL

    def getLink(self, text):
        content = self.read() # read the content received
        p = LinkParser()
        p.feed(unicode(content, 'utf-8'))
        p.close()
        for link in p.links:
            if link.search(text):
                return link.href
        return None

    # Parse all links using LinkParser:
    def parseLinks(self, content):
        p = LinkParser()
        p.links = [] # reset list of links
        p.feed(unicode(content, 'utf-8'))
        p.close()
        return p.links

    def getLinks(self, text):
        content = self.read()
        links = self.parseLinks(content)
        match = []
        for link in links:
            if link.search(text):
                match.append(link)
        return match


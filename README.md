# Azel

### Or how to have fun with the internet

Azel is a python library equivalent to the Elza Perl macro-language (HTTP scripting)

It basically allows you to automatize sequences of HTTP requests and to script around it (without having to care about sessions / redirections / randomly generated input fields)...


## Usage

Initialization

``` python
import azel
a = azel.Azel()
```

Query a website

``` python
a.get('http://www.lescigales.org') # promo never hurts !
```

Specify a proxy to use

``` python
a.proxyHost = '10.7.0.1'
a.proxyPort = 8118
```

Collect links from a web page:

getLink(re.pattern) will return the href of the first link match
getLinks(re.pattern) will return a list of links

``` python
a.get('http://sk.php.net/')
dl = a.getLink('downloads')
a.get(dl)
links = a.getLinks('PHP 5.')
for link in links:
    print link.href, link.value, link.title

    # Download the first link                                                                    
    a.get(link.href)
    l = a.getLink('sk.php.net')
    a.get(l)

    tarball = a.read() # thats right babe, we just got php's tarball                              
    break
```

Pre-fill a form

``` python
a.get('https://gist.github.com/')
a.fillForm()
print a.data # this will return the prefilled form data
```

Post a form (and publish cool stuff on gist)

``` python
a.get('http://gist.github.com/')
a.fillForm()

a.data['file_ext[gistfile1]'] = '.py'
a.data['file_name[gistfile1]'] = __file__.strip('./')
a.data['description'] = 'This was published by awesome azel!'
a.data['file_contents[gistfile1]'] = content

a.post('') # will post the first form
```
will produce the following output:

``` sh
-> GET http://gist.github.com/
<- 301 Moved Permanently
-> GET https://gist.github.com/
<- 200 OK
-> POST https://gist.github.com/gists
<- 302 Found
-> GET https://gist.github.com/2491246
<- 200 OK
```

Annoy the hell of an asshole by trashing his blog:

``` python
blog = azel.Azel()
final = []
blog.get('http://strepoetlo.legtux.org/')
links = blog.getLinks('/#respond')
for l in links: final.append(l.href)
links = blog.getLinks('/#comments')
for l in links: final.append(l.href)
previous = blog.getLink('Previous')
blog.get(previous)
links = blog.getLinks('/#respond')
for l in links: final.append(l.href)
links = blog.getLinks('/#comments')
for l in links: final.append(l.href)

for link in final:
    print link
    blog.get(link)
    blog.fillForm()
    post = 'http://strepoetlo.legtux.org/wp-comments-post.php'
    s = 'http://forum.lescigales.org/topic1638-site-de-phishing-httpstrepoetlolescigalesorg-par-strepoetlo.html'
    blog.data['author'] = 'Paul Gonsolin'
    blog.data['url'] = 'http://strepoetlo.lescigales.org/'
    blog.data['email'] = 'no-reply@lescigales.org'
    blog.data['comment'] = 'Createur de sites de phishing Facebook, priere de ne plus venir sur lesCigales.ORG. -> <a href="'+s+'">'+s+'</a>'
    blog.post(post)

```

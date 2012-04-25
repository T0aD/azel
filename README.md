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



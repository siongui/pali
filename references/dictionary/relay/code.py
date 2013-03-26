#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
import urllib
import urllib2
from urlparse import parse_qs

urls = (
  '/', 'index',
  '/browse.*', 'index',
  '/js/.*', 'index',
  '/css/.*', 'index',
  '/json/.*', 'json',
  '/favicon.ico', 'index',
  '/robots.txt', 'robot',
  '/lookup', 'index'
)

http_header_string = {
  'HTTP_ACCEPT_CHARSET'  : 'Accept-Charset',
  'HTTP_USER_AGENT'      : 'User-Agent',
  'HTTP_CONNECTION'      : 'Connection',
#  'HTTP_HOST'            : 'Host',
  'HTTP_CACHE_CONTROL'   : 'Cache-Control',
  'HTTP_ACCEPT'          : 'Accept',
  'HTTP_ACCEPT_LANGUAGE' : 'Accept-Language',
  'HTTP_ACCEPT_ENCODING' : 'Accept-Encoding'
}


class index:
  def GET(self):
    if 'Googlebot' in web.ctx.env['HTTP_USER_AGENT']:
      return
    request = urllib2.Request('http://palidictionary.appspot.com%s%s' \
      % (urllib2.quote(web.ctx.path.encode('utf-8')), web.ctx.query))
    for headerItem in web.ctx.env:
      try:
        if http_header_string[headerItem] != None:
          if http_header_string[headerItem] == 'User-Agent':
            request.add_header(http_header_string[headerItem], "".join([web.ctx.env[headerItem], " from: %s" % web.ctx.host]))
          else:
            request.add_header(http_header_string[headerItem], web.ctx.env[headerItem])
      except KeyError:
        pass
    response = urllib2.urlopen(request)
    #web.debug(response.info()["Content-Type"])
    for headerItem in response.info().items():
      web.header(headerItem[0], headerItem[1])
    return response.read()

  def POST(self):
    url = "http://palidictionary.appspot.com/lookup"
    value = {"word": web.input().word.encode('utf-8')}
    data = urllib.urlencode(value)
    request = urllib2.Request(url, data)
    for headerItem in web.ctx.env:
      try:
        if http_header_string[headerItem] != None:
          if http_header_string[headerItem] == 'User-Agent':
            request.add_header(http_header_string[headerItem], "".join([web.ctx.env[headerItem], " from: %s" % web.ctx.host]))
          else:
            request.add_header(http_header_string[headerItem], web.ctx.env[headerItem])
      except KeyError:
        pass
    response = urllib2.urlopen(request)
    #web.debug(response.info()["Content-Type"])
    for headerItem in response.info().items():
      web.header(headerItem[0], headerItem[1])
    return response.read()


class json:
  def GET(self):
    v = parse_qs(web.ctx.query[1:])['v'][0]
    request = urllib2.Request('http://%s.palidictionary.appspot.com/%s' \
      % (v, urllib2.quote(web.ctx.path.encode('utf-8'))))
    for headerItem in web.ctx.env:
      try:
        if http_header_string[headerItem] != None:
          if http_header_string[headerItem] == 'User-Agent':
            request.add_header(http_header_string[headerItem], "".join([web.ctx.env[headerItem], " from: %s" % web.ctx.host]))
          else:
            request.add_header(http_header_string[headerItem], web.ctx.env[headerItem])
      except KeyError:
        pass
    response = urllib2.urlopen(request)
    #web.debug(response.info()["Content-Type"])
    for headerItem in response.info().items():
      web.header(headerItem[0], headerItem[1])
    web.header('Access-Control-Allow-Origin', '*')
    return response.read()


class robot:
  def GET(self):
    return 'User-agent: *\nDisallow: /'


# To run on PythonAnywhere and WebFaction, see the following link:
# http://webpy.org/cookbook/mod_wsgi-apache
#app = web.application(urls, globals())
#application = app.wsgifunc()

# To work with Apache and mod_wsgi, Add WSGIScriptAlias / /path_to_python_script_dir/code.py
# http://stackoverflow.com/questions/3613594/web-py-url-mapping-not-accepting

if __name__ == "__main__":
  app = web.application(urls, globals())
  app.run()

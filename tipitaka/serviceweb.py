#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/gae/libs'))
import web
sys.path.append(os.path.join(os.path.dirname(__file__), 'gaelibs'))
from url import getAllLocalesTranslationsHtml

import urllib2

urls = (
  "/json/.+", "json",
  "/robots.txt", "robots",
  "/html/MainPage/([^/]+)/([^/]+)", "htmlMainPage",
)

class json:
  def GET(self):
    url = 'http://%s.palidictionary.appspot.com/%s' % \
          (web.input().v, web.ctx.path)
    result = urllib2.urlopen(url)
    return result.read()

class robots:
  def GET(self):
    if web.ctx.host == 'localhost:8080':
      return 'User-agent: *\nDisallow: /'
    return 'User-agent: *\nDisallow:\n'

class htmlMainPage:
  def GET(self, urlLocale, userLocale):
    if urlLocale == 'None':
      return getAllLocalesTranslationsHtml(None, userLocale)
    else:
      return getAllLocalesTranslationsHtml(urlLocale, userLocale)

app = web.application(urls, globals())
app = app.gaerun()

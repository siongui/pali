#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/gae/libs'))
import web
sys.path.append(os.path.join(os.path.dirname(__file__), 'gaelibs'))
from url import getAllLocalesTranslationsHtml

import urllib2
import json

urls = (
  "/json/.+", "jsonService",
  "/robots.txt", "robots",
  "/html/MainPage", "htmlMainPage",
)

class jsonService:
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
  def POST(self):
    data = json.loads(web.data())
    if data['userLocale'] not in ['en_US', 'zh_TW', 'zh_CN']:
      raise web.notfound()
    if data['urlLocale'] not in ['en_US', 'zh_TW', 'zh_CN', None]:
      raise web.notfound()
    return getAllLocalesTranslationsHtml(data['urlLocale'], data['userLocale'])

app = web.application(urls, globals())
app = app.gaerun()

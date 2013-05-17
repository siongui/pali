#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/gae/libs'))
import web

import urllib2

urls = (
  "/json/.+", "jsonService",
  "/robots.txt", "robots",
)

class jsonService:
  def GET(self):
    url = 'http://%s.palidictionary.appspot.com/%s' % \
          (web.input().v, web.ctx.path)
    return urllib2.urlopen(url).read()

class robots:
  def GET(self):
    if web.ctx.host == 'localhost:8080':
      return 'User-agent: *\nDisallow: /'
    return 'User-agent: *\nDisallow:\n'


app = web.application(urls, globals())
app = app.gaerun()

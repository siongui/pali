#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
import urllib2

urls = (
  "/json/.+", "json",
)

app = web.application(urls, globals())

class json:
  def GET(self):
    url = 'http://%s.palidictionary.appspot.com/%s' % \
          (web.input().v, web.ctx.path)
    result = urllib2.urlopen(url)
    return result.read()

app = app.gaerun()

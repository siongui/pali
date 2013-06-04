#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/gae/libs'))
import web
sys.path.append(os.path.join(os.path.dirname(__file__), 'gaelibs'))
from wordJson import getWordJson

import urllib2

urls = (
#  "/wordJson/([abcdeghijklmnoprstuvyāīūṁṃŋṇṅñṭḍḷ…'’° -]+)", "wordJsonService",
  "/wordJson/(.+)", "wordJsonService",
  "/robots.txt", "robots",
)

class wordJsonService:
  def GET(self, word):
    # web.py server which allow cross-site xmlhttprequest
    # https://gist.github.com/1271118/52eca29d23a1f307597e04d434b0421011843e2f
    #web.header('Access-Control-Allow-Origin', '*')
    #web.header('Access-Control-Allow-Credentials', 'true')
    return getWordJson(word.encode('utf-8'))

class robots:
  def GET(self):
    if web.ctx.host == 'palidictionary.appspot.com':
      return 'User-agent: *\nDisallow: /wordJson/\n'
    return 'User-agent: *\nDisallow: /'


app = web.application(urls, globals())
try:
  from google.appengine.ext import ndb
  app = app.gaerun()
except ImportError:
  application = app.wsgifunc()

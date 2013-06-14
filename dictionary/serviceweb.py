#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/pylib'))
import web
sys.path.append(os.path.join(os.path.dirname(__file__), 'pylib'))
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
    if type(word) is not unicode:
      word = word.decode('utf-8')
    return getWordJson(word)

class robots:
  def GET(self):
    if web.ctx.host == 'dictionary.online-dhamma.net':
      return 'User-agent: *\nDisallow: /wordJson/\n'
    return 'User-agent: *\nDisallow: /'


app = web.application(urls, globals())
try:
  from google.appengine.ext import ndb
  # runs on Google App Engine
  app = app.gaerun()
except ImportError:
  application = app.wsgifunc()

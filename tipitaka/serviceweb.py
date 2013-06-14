#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/pylib'))
import web
from i18n import getSupportedLocales
sys.path.append(os.path.join(os.path.dirname(__file__), 'pylib'))
from url import getAllLocalesTranslationsHtml
from url import serveCanonPageHtml
from url import serveTranslationPageHtml
from url import serveContrastReadingPageHtml

import urllib2
import urllib
import json

urls = (
  "/wordJson/(.+)", "wordJsonService",
  "/robots.txt", "robots",
  "/html/MainPage", "htmlMainPage",
  "/html/CanonPage", "htmlCanonPage",
  "/html/TranslationPage", "htmlTranslationPage",
  "/html/ContrastReadingPage", "htmlContrastReadingPage",
)

try:
  from google.appengine.api import memcache
  isGAE = True
except ImportError:
  isGAE = False

class wordJsonService:
  def GET(self, word):
    if isGAE:
      data = memcache.get(word)
      if data is not None:
        return data
      else:
        url = 'http://palidictionary.appspot.com/wordJson/%s' % \
            urllib.quote(word.encode('utf-8')) 
        jdata = urllib2.urlopen(url).read()
        memcache.set(word, jdata)
        return jdata
    else:
      path = os.path.join(os.path.dirname(__file__),
          '../dictionary/pylib/paliwords/%s' % word.encode('utf-8'))
      with open(path, 'r') as f:
        return f.read()


class robots:
  def GET(self):
    if web.ctx.host == 'epalitipitaka.appspot.com':
      return 'User-agent: *\nDisallow: /html/\n'
    return 'User-agent: *\nDisallow: /'

def checkData(urlLocale, userLocale):
  if userLocale not in getSupportedLocales():
    raise web.notfound()
  if urlLocale not in getSupportedLocales() and None:
    raise web.notfound()

class htmlMainPage:
  def POST(self):
    data = json.loads(web.data())
    checkData(data['urlLocale'], data['userLocale'])
    return getAllLocalesTranslationsHtml(data['urlLocale'], data['userLocale'])

class htmlCanonPage:
  def POST(self):
    data = json.loads(web.data())
    checkData(data['urlLocale'], data['userLocale'])
    result = serveCanonPageHtml(
        data['reqPath'],
        data['urlLocale'],
        data['paliTextPath'].encode('utf-8'),
        data['userLocale'])
    if result: return json.dumps(result)
    else: raise web.notfound()

class htmlTranslationPage:
  def POST(self):
    data = json.loads(web.data())
    checkData(data['urlLocale'], data['userLocale'])
    result = serveTranslationPageHtml(
        data['reqPath'],
        data['urlLocale'],
        data['paliTextPath'].encode('utf-8'),
        data['userLocale'],
        data['translationLocale'],
        data['translator'].encode('utf-8'))
    if result: return json.dumps(result)
    else: raise web.notfound()

class htmlContrastReadingPage:
  def POST(self):
    data = json.loads(web.data())
    checkData(data['urlLocale'], data['userLocale'])
    result = serveContrastReadingPageHtml(
        data['reqPath'],
        data['urlLocale'],
        data['paliTextPath'].encode('utf-8'),
        data['userLocale'],
        data['translationLocale'],
        data['translator'].encode('utf-8'))
    if result: return json.dumps(result)
    else: raise web.notfound()


app = web.application(urls, globals())
try:
  from google.appengine.api import app_identity
  # runs on Google App Engine
  app = app.gaerun()
except ImportError:
  pass

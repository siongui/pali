#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/gae/libs'))
import web
sys.path.append(os.path.join(os.path.dirname(__file__), 'gaelibs'))
from url import getAllLocalesTranslationsHtml
from url import serveCanonPageHtml
from url import serveTranslationPageHtml
from url import serveContrastReadingPageHtml

import urllib2
import json

urls = (
  "/json/.+", "jsonService",
  "/robots.txt", "robots",
  "/html/MainPage", "htmlMainPage",
  "/html/CanonPage", "htmlCanonPage",
  "/html/TranslationPage", "htmlTranslationPage",
  "/html/ContrastReadingPage", "htmlContrastReadingPage",
)

class jsonService:
  def GET(self):
    url = 'http://%s.palidictionary.appspot.com/%s' % \
          (web.input().v, web.ctx.path)
    result = urllib2.urlopen(url)
    return result.read()

class robots:
  def GET(self):
    if web.ctx.host == 'epalitipitaka.appspot.com':
      return 'User-agent: *\nDisallow:\n'
    return 'User-agent: *\nDisallow: /'

def checkData(urlLocale, userLocale):
  if userLocale not in ['en_US', 'zh_TW', 'zh_CN']:
    raise web.notfound()
  if urlLocale not in ['en_US', 'zh_TW', 'zh_CN', None]:
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
app = app.gaerun()

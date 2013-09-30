#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/pylib'))
from localeUtil import getLocale
from localeUtil import parseAcceptLanguage
from misc import isDevServer
from misc import isTrack
import i18n
import web

sys.path.append(os.path.join(os.path.dirname(__file__), 'pylib'))
from url2 import isValidPrefixAndWord
from url2 import getPrefixHtml
from url2 import getWordHtml
from url2 import getHtmlTitle

import jinja2
import json
import urllib

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
      [os.path.join(os.path.dirname(__file__), 'app'),
       os.path.join(os.path.dirname(__file__), 'app/css'),
       os.path.join(os.path.dirname(__file__), 'app/partials')]),
    extensions=['jinja2.ext.i18n'],
    variable_start_string='{$',
    variable_end_string='$}')

jinja_environment.install_gettext_translations(i18n)

urls = (
  r"/browse/noSuchWord", "RedirectPage",
  r"/", "MainPage",
  r"/about", "MainPage",
  r"/(%s)/" % i18n.localesRegex, "MainPage",
  r"/(%s)/browse/([^/]+)/([^/]+)" % i18n.localesRegex, "WordPage2",
  r"/browse/([^/]+)/([^/]+)", "WordPage",
  r"/(%s)/browse/([^/]+)" % i18n.localesRegex, "PrefixPage2",
  r"/browse/([^/]+)", "PrefixPage",
)


def RedirectToNewDomain(oldDomain, newDomain):
  if web.ctx.host.split(':')[0] == oldDomain:
    url = newDomain + urllib.quote(web.ctx.path.encode('utf-8')) + web.ctx.query
    raise web.redirect(url)

def commonTemplateValues(urlLocale, reqHandlerName, prefix=None, word=None):
  userLocale = getLocale(urlLocale, web.ctx.env.get('HTTP_ACCEPT_LANGUAGE'))
  i18n.setLocale(userLocale)
  template_values = {
#    'serverEnv': 'ec2',
#    'tpkWebAppUrl': 'http://tipitaka.sutta.org/',
    'serverEnv': 'appspot',
    'tpkWebAppUrl': 'http://epalitipitaka.appspot.com/',
    'dicWebAppUrl': 'http://palidictionary.appspot.com/',
#    'tpkWebAppUrl': 'http://tipitaka.online-dhamma.net/',
#    'dicWebAppUrl': 'http://dictionary.online-dhamma.net/',
    'htmlTitle': getHtmlTitle(userLocale, reqHandlerName, i18n, prefix, word),
    'userLocale': userLocale,
    'locales': json.dumps(i18n.locales),
    'localeLanguageMapping': json.dumps(i18n.localeLanguageMapping),
    'langQs': json.dumps(parseAcceptLanguage(web.ctx.env.get('HTTP_ACCEPT_LANGUAGE'))),
    'urlLocale': urlLocale,
    'isTrack': isTrack(web.input(track=None).track),
    'isDevServer': isDevServer(),
  }
  return template_values

class MainPage:
  def GET(self, urlLocale=None):
    template_values = commonTemplateValues(urlLocale, self.__class__.__name__)
    template = jinja_environment.get_template('index.html')
    return template.render(template_values)

def commonPage(prefix, word, reqHandlerName, urlLocale=None):
  if type(prefix) is not unicode:
    prefix = prefix.decode('utf-8')

  if word:
    if type(word) is not unicode:
      word = word.decode('utf-8')

  if not isValidPrefixAndWord(prefix, word):
    raise web.notfound()

  template_values = commonTemplateValues(
      urlLocale, reqHandlerName, prefix, word)

  if reqHandlerName == 'WordPage':
    pageHtml = getWordHtml(prefix, word)
  elif reqHandlerName == 'PrefixPage':
    pageHtml = getPrefixHtml(prefix)
  else:
    raise Exception('invalid reqHandlerName: %s' % reqHandlerName)

  if pageHtml is None: raise web.notfound()
  template_values['pageHtml'] = pageHtml
  template = jinja_environment.get_template('index.html')
  return template.render(template_values)

class WordPage:
  def GET(self, prefix, word):
    return commonPage(prefix, word, self.__class__.__name__)

class WordPage2:
  def GET(self, urlLocale, prefix, word):
    return commonPage(prefix, word, 'WordPage', urlLocale)

class PrefixPage:
  def GET(self, prefix):
    return commonPage(prefix, None, self.__class__.__name__)

class PrefixPage2:
  def GET(self, urlLocale, prefix):
    return commonPage(prefix, None, 'PrefixPage', urlLocale)

class RedirectPage:
  def GET(self):
    raise web.seeother('/')


app = web.application(urls, globals())
try:
  from google.appengine.ext import ndb
  # runs on Google App Engine
  app = app.gaerun()
except ImportError:
  application = app.wsgifunc()

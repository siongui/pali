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
from url import checkPath

import json
import jinja2
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
  r"/(%s)/" % i18n.localesRegex, "MainPage2",
  r"/(%s)(.+)/(%s)/([^/]+)/ContrastReading" % (i18n.localesRegex, i18n.localesRegex), "ContrastReadingPage2",
  r"/(%s)(.+)/(%s)/([^/]+)" % (i18n.localesRegex, i18n.localesRegex), "TranslationPage2",
  r"/(%s)(.+)" % i18n.localesRegex, "CanonPage2",
  r"/", "MainPage",
  r"(.+)/(%s)/([^/]+)/ContrastReading" % i18n.localesRegex, "ContrastReadingPage",
  r"(.+)/(%s)/([^/]+)" % i18n.localesRegex, "TranslationPage",
  r"(.+)", "CanonPage",
)


def commonTemplateValues(urlLocale, userLocale):
  i18n.setLocale(userLocale)
  template_values = {
#    'serverEnv': 'ec2',
#    'dicWebAppUrl': 'http://dictionary.sutta.org/',
    'serverEnv': 'appspot',
#    'dicWebAppUrl': 'http://palidictionary.appspot.com/',
    'dicWebAppUrl': 'http://dictionary.online-dhamma.net/',
    'htmlTitle': u'',
    'userLocale': userLocale,
    'locales': json.dumps(i18n.locales),
    'localeLanguageMapping': json.dumps(i18n.localeLanguageMapping),
    'langQs': json.dumps(parseAcceptLanguage(web.ctx.env.get('HTTP_ACCEPT_LANGUAGE'))),
    'urlLocale': urlLocale,
    'isTrack': isTrack(web.input(track=None).track),
    'isDevServer': isDevServer(),
  }
  return template_values


def commonPage(paliTextPath, translationLocale=None, translator=None, urlLocale=None):
  if web.ctx.host.split(':')[0] == "epalitipitaka.appspot.com":
    # redirect to new domain
    url = "http://tipitaka.online-dhamma.net" + \
          urllib.quote(web.ctx.path.encode('utf-8')) + \
          web.ctx.query
    raise web.redirect(url)

  userLocale = getLocale(urlLocale, web.ctx.env.get('HTTP_ACCEPT_LANGUAGE'))
  result = checkPath(web.ctx.path, urlLocale, paliTextPath,
                     userLocale, translationLocale, translator)
  if not result['isValid']:
    raise web.notfound()
  template_values = commonTemplateValues(urlLocale, userLocale)
  template_values['pageHtml'] = result['pageHtml']
  template_values['htmlTitle'] = result['htmlTitle']
  template = jinja_environment.get_template('index.html')
  return template.render(template_values)


def commonMainPage(urlLocale=None):
  if web.ctx.host.split(':')[0] == "epalitipitaka.appspot.com":
    # redirect to new domain
    url = "http://tipitaka.online-dhamma.net" + \
          urllib.quote(web.ctx.path.encode('utf-8')) + \
          web.ctx.query
    raise web.redirect(url)

  userLocale = getLocale(urlLocale, web.ctx.env.get('HTTP_ACCEPT_LANGUAGE'))
  template_values = commonTemplateValues(urlLocale, userLocale)
  template_values['isIncludeAbout'] = True
  template_values['pageHtml'] = ''
  template = jinja_environment.get_template('index.html')
  return template.render(template_values)


class MainPage:
  def GET(self): return commonMainPage()

class MainPage2:
  def GET(self, urlLocale): return commonMainPage(urlLocale)

class CanonPage:
  def GET(self, paliTextPath):
    return commonPage(paliTextPath.encode('utf-8'))

class CanonPage2:
  def GET(self, urlLocale, paliTextPath):
    return commonPage(paliTextPath.encode('utf-8'), None, None, urlLocale)

class TranslationPage:
  def GET(self, paliTextPath, translationLocale, translator):
    return commonPage(paliTextPath.encode('utf-8'), translationLocale,
                      translator.encode('utf-8'))

class TranslationPage2:
  def GET(self, urlLocale, paliTextPath, translationLocale, translator):
    return commonPage(paliTextPath.encode('utf-8'), translationLocale,
                      translator.encode('utf-8'), urlLocale)

class ContrastReadingPage:
  def GET(self, paliTextPath, translationLocale, translator):
    return commonPage(paliTextPath.encode('utf-8'), translationLocale,
                      translator.encode('utf-8'))

class ContrastReadingPage2:
  def GET(self, urlLocale, paliTextPath, translationLocale, translator):
    return commonPage(paliTextPath.encode('utf-8'), translationLocale,
                      translator.encode('utf-8'), urlLocale)


app = web.application(urls, globals())
try:
  from google.appengine.api import app_identity
  # runs on Google App Engine
  app = app.gaerun()
except ImportError:
  pass

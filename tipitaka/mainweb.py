#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common/gae/libs'))
from localeUtil import getLocale
from localeUtil import parseAcceptLanguage
from misc import isCompiledJS
from misc import isTrack
import i18n
import web

sys.path.append(os.path.join(os.path.dirname(__file__), 'gaelibs'))
from url import getAllLocalesTranslationsHtml
from url import checkPath

import json
import jinja2

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
  r"/(.+)/(en_US|zh_TW|zh_CN)/([^/]+)/ContrastReading", "ContrastReadingPage",
  r"/(.+)/(en_US|zh_TW|zh_CN)/([^/]+)", "TranslationPage",
  r"/(.+)", "CanonPage",
  r"/", "MainPage",
)

def getCommonTemplateValues(urlLocale, userLocale, className):
  i18n.setLocale(userLocale)
  template_values = {
    'htmlTitle': u'',
    'userLocale': userLocale,
    'langQs': json.dumps(parseAcceptLanguage(web.ctx.env['HTTP_ACCEPT_LANGUAGE'])),
    'urlLocale': urlLocale,
#    'isCompiledJS': isCompiledJS(web.input().js),
#    'isTrack': isTrack(web.input().track),
    'isCompiledJS': False,
    'isTrack': False,
    'reqHandlerName': className
  }

  return template_values

class MainPage:
  def GET(self):
    userLocale = getLocale(None, web.ctx.env['HTTP_ACCEPT_LANGUAGE'])
    template_values = getCommonTemplateValues(None, userLocale, 'MainPage')
    template_values['pageHtml'] = getAllLocalesTranslationsHtml(None, userLocale)
    template = jinja_environment.get_template('index.html')
    return template.render(template_values)

class CanonPage:
  def GET(self, paliTextPath):
    return 'CanonPage'

class TranslationPage:
  def GET(self, paliTextPath, translationLocale, translator):
    return 'TranslationPage'

class ContrastReadingPage:
  def GET(self, paliTextPath, translationLocale, translator):
    return 'ContrastReadingPage'


app = web.application(urls, globals())
app = app.gaerun()

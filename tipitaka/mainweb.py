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
  r"/", "MainPage",
  r"(.+)/(en_US|zh_TW|zh_CN)/([^/]+)/ContrastReading", "ContrastReadingPage",
  r"(.+)/(en_US|zh_TW|zh_CN)/([^/]+)", "TranslationPage",
  r"(.+)", "CanonPage",
)


def commonTemplateValues(urlLocale, userLocale, className):
  i18n.setLocale(userLocale)
  template_values = {
    'htmlTitle': u'',
    'userLocale': userLocale,
    'langQs': json.dumps(parseAcceptLanguage(web.ctx.env['HTTP_ACCEPT_LANGUAGE'])),
    'urlLocale': urlLocale,
    'isCompiledJS': isCompiledJS(web.input(js=None).js),
    'isTrack': isTrack(web.input(track=None).track),
    'reqHandlerName': className
  }
  return template_values


def commonPage(paliTextPath, translationLocale=None, translator=None, urlLocale=None):
  userLocale = getLocale(urlLocale, web.ctx.env['HTTP_ACCEPT_LANGUAGE'])
  result = checkPath(web.ctx.path, urlLocale, paliTextPath,
                     userLocale, translationLocale, translator)
  if not result['isValid']:
    raise web.notfound()
  template_values = commonTemplateValues(urlLocale, userLocale, 'OtherPage')
  template_values['pageHtml'] = result['pageHtml']
  template_values['htmlTitle'] = result['htmlTitle']
  template = jinja_environment.get_template('index.html')
  return template.render(template_values)


class MainPage:
  def GET(self):
    userLocale = getLocale(None, web.ctx.env['HTTP_ACCEPT_LANGUAGE'])
    template_values = commonTemplateValues(None, userLocale, 'MainPage')
    template_values['pageHtml'] = getAllLocalesTranslationsHtml(None, userLocale)
    template = jinja_environment.get_template('index.html')
    return template.render(template_values)

class CanonPage:
  def GET(self, paliTextPath):
    return commonPage(paliTextPath.encode('utf-8'))

class TranslationPage:
  def GET(self, paliTextPath, translationLocale, translator):
    return commonPage(paliTextPath.encode('utf-8'), translationLocale,
                      translator.encode('utf-8'))

class ContrastReadingPage:
  def GET(self, paliTextPath, translationLocale, translator):
    return commonPage(paliTextPath.encode('utf-8'), translationLocale,
                      translator.encode('utf-8'))


app = web.application(urls, globals())
app = app.gaerun()

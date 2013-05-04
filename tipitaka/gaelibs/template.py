#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import jinja2
from pathInfo import xmlFilename2Path

jj2env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'partials')),
  extensions=['jinja2.ext.i18n'])

def translateLocale(value):
  if value == u'en_US': return u'English'
  if value == u'zh_TW': return u'中文 (繁體)'
  if value == u'zh_CN': return u'中文 (简体)'
  if value == u'ja_JP': return u'日本語'
  return value

jj2env.filters['translateLocale'] = translateLocale
jj2env.filters['xmlFilename2Path'] = xmlFilename2Path

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common/gae/libs'))
import i18n
jj2env.install_gettext_translations(i18n)


def getJinja2Env():
  return jj2env

def getTranslationPageOriPaliLinkHtml(reqPath):
  return u'<div>&lt;&lt; <a href="%s">%s</a></div>' % \
         (os.path.sep.join(reqPath.split(os.path.sep)[:-2]),
          i18n.ugettext(u'Original Pāḷi Text'))

def getContrastReadingPageOriPaliLinkHtml(reqPath):
  return u'<div>&lt;&lt; <a href="%s">%s</a></div>' % \
         (os.path.sep.join(reqPath.split(os.path.sep)[:-3]),
          i18n.ugettext(u'Original Pāḷi Text'))


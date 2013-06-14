#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import jinja2

jj2env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(
           os.path.join(os.path.dirname(__file__), 'partials')),
  extensions=['jinja2.ext.i18n'])

def translateLocale(value):
  if value == u'en_US': return u'English'
  if value == u'fr_FR': return u'Français'
  if value == u'vi_VN': return u'Tiếng Việt'
  if value == u'zh_TW': return u'中文 (繁體)'
  if value == u'zh_CN': return u'中文 (简体)'
  if value == u'ja_JP': return u'日本語'
  return value

def originalPaliLink(reqPath, flag):
  if flag:
    # translation page
    return os.path.sep.join(reqPath.split(os.path.sep)[:-2])
  else:
    # contrast reading page
    return os.path.sep.join(reqPath.split(os.path.sep)[:-3])

jj2env.filters['translateLocale'] = translateLocale
jj2env.filters['originalPaliLink'] = originalPaliLink

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common/pylib'))
import i18n
jj2env.install_gettext_translations(i18n)


def getJinja2Env(locale):
  if locale:
    i18n.setLocale(locale)
  else:
    i18n.setLocale('en_US')
  return jj2env


#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
References:
http://docs.python.org/2/library/gettext.html
http://jinja.pocoo.org/docs/extensions/
http://webpy.org/cookbook/i18n_support_in_template_file
http://webpy.org/cookbook/runtime-language-switch
https://code.google.com/p/webapp-improved/source/browse/webapp2_extras/i18n.py
http://docs.python.org/2/library/threading.html
"""

import os
import gettext
import threading

localedir = os.path.join(os.path.dirname(__file__), '../locale')
domain = 'messages'
threadLocalData = threading.local()
threadLocalData.locale = 'en_US'

locales = []
localesRegex = ''
for dirpath, dirnames, filenames in os.walk(localedir):
  for dirname in dirnames:
    locales.append(dirname)
    localesRegex += (dirname + '|')
  localesRegex = localesRegex[:-1]
  break

AllTranslations = {}
for locale in locales:
  AllTranslations[locale] = gettext.translation(domain, localedir, [locale])

def gettext(message):
  return AllTranslations[ threadLocalData.locale ].gettext(message)

def ugettext(message):
  return AllTranslations[ threadLocalData.locale ].ugettext(message)

def ngettext(singular, plural, n):
  return AllTranslations[ threadLocalData.locale ].ngettext(singular, plural, n)

def ungettext(singular, plural, n):
  return AllTranslations[ threadLocalData.locale ].ungettext(singular, plural, n)

def setLocale(locale):
  if locale in locales:
    threadLocalData.locale = locale


localeLanguageMapping = {
  u'en_US': u'English',
  u'fr_FR': u'Français',
  u'vi_VN': u'Tiếng Việt',
  u'zh_TW': u'中文 (繁體)',
  u'zh_CN': u'中文 (简体)',
  u'ja_JP': u'日本語',
}

def translateLocale(value):
  if value in localeLanguageMapping:
    return localeLanguageMapping[value]
  return value


if __name__ == '__main__':
  # for test purpose
  for dirpath, dirnames, filenames in os.walk(localedir):
    for dirname in dirnames:
      print(dirname)
    break

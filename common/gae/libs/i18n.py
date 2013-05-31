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

localedir = os.path.join(os.path.dirname(__file__), '../../locale')
domain = 'messages'
threadLocalData = threading.local()
threadLocalData.locale = 'en_US'

AllTranslations = {
'en_US': gettext.translation(domain, localedir, ['en_US']),
'fr_FR': gettext.translation(domain, localedir, ['fr_FR']),
'zh_TW': gettext.translation(domain, localedir, ['zh_TW']),
'zh_CN': gettext.translation(domain, localedir, ['zh_CN'])
}

def gettext(message):
  return AllTranslations[ threadLocalData.locale ].gettext(message)

def ugettext(message):
  return AllTranslations[ threadLocalData.locale ].ugettext(message)

def ngettext(singular, plural, n):
  return AllTranslations[ threadLocalData.locale ].ngettext(singular, plural, n)

def ungettext(singular, plural, n):
  return AllTranslations[ threadLocalData.locale ].ungettext(singular, plural, n)

def setLocale(locale):
  if locale in ['en_US', 'zh_TW', 'zh_CN', 'fr_FR']:
    threadLocalData.locale = locale


#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
References:
http://docs.python.org/2/library/gettext.html
http://jinja.pocoo.org/docs/extensions/
http://webpy.org/cookbook/i18n_support_in_template_file
http://webpy.org/cookbook/runtime-language-switch
https://code.google.com/p/webapp-improved/source/browse/webapp2_extras/i18n.py
"""

import os
import gettext

localedir = os.path.join(os.path.dirname(__file__), '../../locale')
domain = 'messages'

AllTranslations = {
'en_US': gettext.translation(domain, localedir, ['en_US']),
'zh_TW': gettext.translation(domain, localedir, ['zh_TW']),
'zh_CN': gettext.translation(domain, localedir, ['zh_CN']),
'locale': 'en_US'
}

def gettext(message):
  return AllTranslations[ AllTranslations['locale'] ].gettext(message)

def ugettext(message):
  return AllTranslations[ AllTranslations['locale'] ].ugettext(message)

def ngettext(singular, plural, n):
  return AllTranslations[ AllTranslations['locale'] ].ngettext(singular, plural, n)

def ungettext(singular, plural, n):
  return AllTranslations[ AllTranslations['locale'] ].ungettext(singular, plural, n)

def setLocale(locale):
  if locale in ['en_US', 'zh_TW', 'zh_CN']:
    AllTranslations['locale'] = locale


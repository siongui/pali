#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import jinja2

jj2env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(
           os.path.join(os.path.dirname(__file__), 'partials')),
  extensions=['jinja2.ext.i18n'])


def originalPaliLink(reqPath, flag):
  if flag:
    # translation page
    return os.path.sep.join(reqPath.split(os.path.sep)[:-2])
  else:
    # contrast reading page
    return os.path.sep.join(reqPath.split(os.path.sep)[:-3])

jj2env.filters['originalPaliLink'] = originalPaliLink

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common/pylib'))
import i18n
jj2env.filters['translateLocale'] = i18n.translateLocale
jj2env.install_gettext_translations(i18n)


def getJinja2Env(locale):
  if locale in i18n.locales:
    i18n.setLocale(locale)
  else:
    i18n.setLocale('en_US')
  return jj2env


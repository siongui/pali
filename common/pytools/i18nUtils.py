#!/usr/bin/env python
# -*- coding:utf-8 -*-

# References
# https://developers.google.com/edu/python/regular-expressions
# http://stackoverflow.com/questions/490597/regex-replace-in-python-a-more-simple-way
# http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
# http://wiki.maemo.org/Internationalize_a_Python_application
# http://www.supernifty.org/blog/2011/09/16/python-localization-made-easy/

import os, sys, re, json, shutil
sys.path.append(os.path.join(os.path.dirname(__file__), '../gae/libs'))
from jianfan import ftoj

# global variable
locale_dir = os.path.join(os.path.dirname(__file__), '../locale')
dictionary_html_dir = os.path.join(os.path.dirname(__file__), '../../dictionary/app')
tipitaka_html_dir = os.path.join(os.path.dirname(__file__), '../../tipitaka/app')
potpath = os.path.join(locale_dir, 'messages.pot')
twPoPath = os.path.join(locale_dir, 'zh_TW/LC_MESSAGES/messages.po')
cnPoPath = os.path.join(locale_dir, 'zh_CN/LC_MESSAGES/messages.po')
#dstLocalesJson = os.path.join(os.path.dirname(__file__), '../gae/libs/json/locales.json') 
dstLocalesJs = os.path.join(os.path.dirname(__file__), '../app/js/services-i18nStrings.js') 
locales = ['en_US', 'zh_TW', 'zh_CN']


def searchI18n(string):
  # only first match and longest match
  # i.e., the string {{_("ddd")}}12345{{_("sss")}} will return
  # {{_("ddd")}}12345{{_("sss")}}, not return {{_("ddd")}}
  return re.search(r'{{\s*_\(\s*(.+)\s*\)\s*}}', string)


def getAllMatchesInFile(filepath):
  with open(filepath, 'r') as f:
    # [^)] to prevent {{_("ddd")}}12345{{_("sss")}}
    return re.findall(r'{{\s*_\(\s*([^)]+)\s*\)\s*}}', f.read())


def createPOT():
  if not os.path.exists(locale_dir):
    os.makedirs(locale_dir)

  # The default locale dir of webapp2 i18n is $PROJECT_DIR/locale
  # The default domain of webapp2 i18n is 'messages'
  # see http://webapp-improved.appspot.com/api/webapp2_extras/i18n.html#webapp2_extras.i18n.default_config
  cmd_xgettext = 'xgettext --no-wrap --from-code=UTF-8 --keyword=_ --output=%s/messages.pot `find %s -name *.html` `find %s -name *.html`' % (locale_dir, dictionary_html_dir, tipitaka_html_dir)
  cmd_sed = 'sed -i "s/charset=CHARSET/charset=utf-8/g" %s/messages.pot' % locale_dir

  print(cmd_xgettext)
  os.system(cmd_xgettext)
  print(cmd_sed)
  os.system(cmd_sed)


def initLocalePO(locale):
  popath = os.path.join(locale_dir, '%s/LC_MESSAGES/messages.po' % locale)

  if not os.path.exists(os.path.dirname(popath)):
    os.makedirs(os.path.dirname(popath))
  cmd_msginit = 'msginit --no-wrap --no-translator --input=%s --locale=%s -o %s' % (potpath, locale, popath)
  print(cmd_msginit)
  os.system(cmd_msginit)


def initPOs():
  for locale in locales:
    initLocalePO(locale)


def updateLocalePO(locale):
  popath = os.path.join(locale_dir, '%s/LC_MESSAGES/messages.po' % locale)

  if not os.path.exists(os.path.dirname(popath)):
    os.makedirs(os.path.dirname(popath))
  cmd_msginit = 'msgmerge --no-wrap --backup=none --update %s %s' % (popath, potpath)
  print(cmd_msginit)
  os.system(cmd_msginit)


def updatePOs():
  for locale in locales:
    updateLocalePO(locale)


def initOrUpdatePOs():
  for locale in locales:
    popath = os.path.join(locale_dir, '%s/LC_MESSAGES/messages.po' % locale)
    if os.path.exists(popath):
      updateLocalePO(locale)
    else:
      initLocalePO(locale)


def formatMO(locale):
  popath = os.path.join(locale_dir, '%s/LC_MESSAGES/messages.po' % locale)
  mopath = popath[:-2] + 'mo'

  cmd_msgfmt = 'msgfmt %s -o %s' % (popath, mopath)
  print(cmd_msgfmt)
  os.system(cmd_msgfmt)


def POtoMO():
  for locale in locales:
    formatMO(locale)


def TWtoCN():
  with open(twPoPath, 'r') as f:
    with open(cnPoPath, 'w') as fd:
      for line in f.readlines():
        if 'zh_TW' in line:
          fd.write(line.replace('zh_TW', 'zh_CN'))
        elif line.startswith('msgstr'):
          fd.write(re.sub('msgstr "(.+)"', lambda m: 'msgstr "%s"' % ftoj(m.group(1)), line).encode('utf-8'))
        else:
          fd.write(line)


def writeJson():
  # create PO-like object for i18n
  if not os.path.exists(os.path.dirname(dstLocalesJson)):
    os.makedirs(os.path.dirname(dstLocalesJson))

  with open(twPoPath, 'r') as f:
    tuples = re.findall(r'msgid "(.+)"\nmsgstr "(.+)"', f.read())

  obj = {'zh_TW': {}}
  for tuple in tuples:
    obj['zh_TW'][tuple[0].decode('utf-8')] = tuple[1].decode('utf-8')

  with open(dstLocalesJson, 'w') as f:
    f.write(json.dumps(obj))

  print(json.dumps(obj))


def writeJs():
  # create PO-like js file for i18n
  with open(twPoPath, 'r') as f:
    tuples = re.findall(r'msgid "(.+)"\nmsgstr "(.+)"', f.read())

  obj = {'zh_TW': {}}
  for tuple in tuples:
    obj['zh_TW'][tuple[0].decode('utf-8')] = tuple[1].decode('utf-8')

  with open(dstLocalesJs, 'w') as f:
    f.write("angular.module('pali.i18nStrings', []).\n")
    f.write("  factory('i18nStrings', [function() {\n")
    f.write("    var str = ")
    f.write(json.dumps(obj))
    f.write(";\n")
    f.write("    var serviceInstance = { all: str };\n")
    f.write("    return serviceInstance;\n")
    f.write("  }]);\n")

  print(json.dumps(obj))


if __name__ == '__main__':
  if len(sys.argv) != 2:
    sys.exit(1)

  if sys.argv[1] == "pot":
    createPOT()
    sys.exit(0)

  if sys.argv[1] == "initpo":
    initPOs()
    sys.exit(0)

  if sys.argv[1] == "updatepo":
    updatePOs()
    sys.exit(0)

  if sys.argv[1] == "po":
    initOrUpdatePOs()
    sys.exit(0)

  if sys.argv[1] == "mo":
    POtoMO()
    sys.exit(0)

  if sys.argv[1] == "cn":
    TWtoCN()
    sys.exit(0)

  """
  if sys.argv[1] == "json":
    writeJson()
    sys.exit(0)
  """

  if sys.argv[1] == "js":
    writeJs()
    sys.exit(0)


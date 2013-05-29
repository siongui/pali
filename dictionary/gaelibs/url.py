#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json, urllib, jinja2
from google.appengine.api import app_identity
from google.appengine.api import urlfetch
from google.appengine.api import memcache

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common/gae/libs'))
from jianfan import jtof, ftoj

jj2env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'partials')))

appname = app_identity.get_application_id()

with open(os.path.join(os.path.dirname(__file__), '../common/gae/libs/json/dicPrefixWordLists.json'), 'r') as f:
  dicPrefixWordLists = json.loads(f.read())

with open(os.path.join(os.path.dirname(__file__), '../common/gae/libs/json/dicPrefixGroup.json'), 'r') as f:
  dicPrefixGroup = json.loads(f.read())


def toCht(value, urlLocale):
  try:
    if urlLocale == 'zh_CN':
      return value
    else:
      return jtof(value)
  except:
    return value

jj2env.filters['toCht'] = toCht


def isValidPrefixAndWord(prefix, word):
  if (prefix == None):
    if (word != None):
      # prefix = None AND word != None
      raise Exception("Impossible case: prefix = None AND word != None")
    # prefix = None AND word = None
    return True

  # prefix != None, check prefix sanity
  if prefix.decode('utf-8') in dicPrefixWordLists:
    # prefix != None AND prefix is valid
    if (word == None):
      # prefix != None AND prefix is valid AND word == None
      return True

    # prefix != None AND prefix is valid AND word != None
    if word.decode('utf-8') in dicPrefixWordLists[prefix.decode('utf-8')]:
      # word is valid
      return True
    else:
      return False
  else:
    # prefix != None AND prefix is invalid
    return False

  raise Exception("Impossible case: End of isValidPrefixOrWord!")


def getWordJsonUrl(prefix, word):
  # Please always use isValidPrefixAndWord to check validity of (prefix, word)
  # pair before using this function
  return 'http://jsons%d.%s.appspot.com/json/%s/%s.json' % \
          (dicPrefixGroup[prefix.decode('utf-8')], appname,
           urllib.quote(prefix).replace("%", 'Z'),
           urllib.quote(word).replace("%", 'Z') );


def fetchJson(prefix, word):
  # Please always use isValidPrefixAndWord to check validity of (prefix, word)
  # pair before using this function
  url = getWordJsonUrl(prefix, word)
  data = memcache.get(url)
  if data is not None:
    return data
  else:
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      memcache.add(url, result.content)
      return result.content
    else:
      return None


def getWordHtml(prefix, word, urlLocale):
  # Please always use isValidPrefixAndWord to check validity of (prefix, word)
  # pair before using this function
  jsonData = fetchJson(prefix, word)

  if jsonData == None:
    return None
  else:
    template = jj2env.get_template('word.html')
    return template.render({'dicWordExps': json.loads(jsonData),
                            'word': word,
                            'urlLocale': urlLocale})


def getPrefixHtml(prefix, urlLocale):
  # Please always use isValidPrefixAndWord to check validity of prefix
  # before using this function
  words = dicPrefixWordLists[prefix.decode('utf-8')]
  template = jj2env.get_template('prefix.html')
  return template.render({'words': words, 'prefix': prefix.decode('utf-8'), 'urlLocale': urlLocale})


def getHtmlTitle(userLocale, reqHandlerName, i18n, prefix, word):
  if reqHandlerName == 'WordPage':
    return word.decode('utf-8') + u' - ' + i18n.ugettext(u'Definition and Meaning') + u' - '
  elif reqHandlerName == 'PrefixPage':
    return i18n.ugettext(u'Words Start with') + u' ' + prefix.decode('utf-8') + u' - '
  else:
    return ''

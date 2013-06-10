#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import jinja2
import json
import urllib
from wordJson import getWordJson

jj2env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'partials')))

# load index of dictionary books
with open(os.path.join(os.path.dirname(__file__),
     'json/books.json'), 'r') as f:
  dicIndex = json.loads(f.read())


def isValidPrefixAndWord(prefix, word):
  if (prefix == None):
    if (word != None):
      # prefix = None AND word != None
      raise Exception("Impossible case: prefix = None AND word != None")
    # prefix = None AND word = None
    return True

  # prefix != None, check prefix sanity
  if prefix in [u'a', u'ā', u'b', u'c', u'd', u'ḍ', u'e', u'g', u'h', u'i', u'ī', u'j', u'k', u'l', u'ḷ', u'm', u'ŋ', u'n', u'ñ', u'ṅ', u'ṇ', u'o', u'p', u'r', u's', u't', u'ṭ', u'u', u'ū', u'v', u'y', u'-', u'°']:
    # prefix != None AND prefix is valid
    if (word == None):
      # prefix != None AND prefix is valid AND word == None
      return True

    # prefix != None AND prefix is valid AND word != None
    try:
      getWordJson(word)
      return True
    except:
      return False
  else:
    # prefix != None AND prefix is invalid
    return False

  raise Exception("Impossible case: End of isValidPrefixOrWord!")


def getPrefixHtml(prefix):
  legalNameOnGAE = urllib.quote(
                     (u'prefixWordsHtml/%s.html' % prefix).encode('utf-8')
                   ).replace('%', 'Z')
  path = os.path.join(os.path.dirname(__file__), legalNameOnGAE)
  with open(path, 'r') as f:
    return f.read().decode('utf-8')


def getWordHtml(prefix, word):
  template = jj2env.get_template('word2.html')
  return template.render({'bookExps': json.loads(getWordJson(word)),
                          'booksIndex': dicIndex,
                          'word': word})


def getHtmlTitle(userLocale, reqHandlerName, i18n, prefix, word):
  if reqHandlerName == 'WordPage':
    return word + u' - ' + i18n.ugettext(u'Definition and Meaning') + u' - '
  elif reqHandlerName == 'PrefixPage':
    return i18n.ugettext(u'Words Start with') + u' ' + prefix + u' - '
  else:
    return ''

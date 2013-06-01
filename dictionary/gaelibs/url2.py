#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import jinja2
import json
from wordJson import getWordJson

jj2env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'partials')))

# load index of dictionary books
# TODO: move the location of books.json to ./json/
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
  if prefix in ['a', 'ā', 'b', 'c', 'd', 'ḍ', 'e', 'g', 'h', 'i', 'ī', 'j', 'k', 'l', 'ḷ', 'm', 'ŋ', 'n', 'ñ', 'ṅ', 'ṇ', 'o', 'p', 'r', 's', 't', 'ṭ', 'u', 'ū', 'v', 'y', '-', '°']:
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


def getWordHtml(prefix, word, urlLocale):
  template = jj2env.get_template('word2.html')
  return template.render({'bookExps': json.loads(getWordJson(word)),
                          'booksIndex': dicIndex,
                          'word': word,
                          'urlLocale': urlLocale})


def getHtmlTitle(userLocale, reqHandlerName, i18n, prefix, word):
  if reqHandlerName == 'WordPage':
    return word.decode('utf-8') + u' - ' + i18n.ugettext(u'Definition and Meaning') + u' - '
  elif reqHandlerName == 'PrefixPage':
    return i18n.ugettext(u'Words Start with') + u' ' + prefix.decode('utf-8') + u' - '
  else:
    return ''

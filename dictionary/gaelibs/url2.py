#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import jinja2
import json
from wordJson import getWordJson

jj2env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

# load index of dictionary books
with open(os.path.join(os.path.dirname(__file__),
     '../common/gae/libs/json/books.json'), 'r') as f:
  dicIndex = json.loads(f.read())


def getWordHtml(prefix, word, urlLocale):
  template = jj2env.get_template('word2.html')
  return template.render({'bookExps': json.loads(getWordJson(word)),
                          'booksIndex': dicIndex,
                          'word': word,
                          'urlLocale': urlLocale})


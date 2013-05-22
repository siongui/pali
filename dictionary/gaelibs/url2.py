#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import jinja2
import json

jj2env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

with open(os.path.join(os.path.dirname(__file__),
     '../common/gae/libs/json/books.json'), 'r') as f:
  dicIndex = json.loads(f.read())

def getWordHtml(prefix, word, urlLocale):
  with open(os.path.join(os.path.dirname(__file__), 'dhamma'), 'r') as f:
    jsonData = f.read()

  template = jj2env.get_template('word2.html')
  return template.render({'bookExps': json.loads(jsonData),
                          'booksIndex': dicIndex,
                          'word': word,
                          'urlLocale': urlLocale})


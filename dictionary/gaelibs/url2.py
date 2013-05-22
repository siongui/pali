#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import jinja2
import json
from google.appengine.ext import ndb

class PaliWordJsonBlob(ndb.Model):
  """blob which stores json data"""
  data = ndb.BlobProperty()

jj2env = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

# load index of dictionary books
with open(os.path.join(os.path.dirname(__file__),
     '../common/gae/libs/json/books.json'), 'r') as f:
  dicIndex = json.loads(f.read())


def readWordFromGAEDatastore(word):
  jblob = PaliWordJsonBlob.get_by_id(word)
  if jblob:
    return jblob.data
  else:
    raise Exception('word not found: %s' % word)


def getWordHtml(prefix, word, urlLocale):
  jsonData = readWordFromGAEDatastore(word)

  template = jj2env.get_template('word2.html')
  return template.render({'bookExps': json.loads(jsonData),
                          'booksIndex': dicIndex,
                          'word': word,
                          'urlLocale': urlLocale})


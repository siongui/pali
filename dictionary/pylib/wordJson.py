#!/usr/bin/env python
# -*- coding:utf-8 -*-

try:
  from google.appengine.ext import ndb

  class PaliWordJsonBlob(ndb.Model):
    """blob which stores json data"""
    data = ndb.BlobProperty()

  def readWordJson(word):
    """read word json from GAE datastore"""
    jblob = PaliWordJsonBlob.get_by_id(word)
    if jblob:
      return jblob.data
    else:
      raise Exception('word not found: %s' % word)

  def isValidWord(word):
    return PaliWordJsonBlob.get_by_id(word) != None

except ImportError:
  """obsoleted. Never used.

  In apache config, the files in 'paliwords' diretory are served as static
  files. No need to serve them through web framework.
  """
  import os

  wordsDir = os.path.join(os.path.dirname(__file__), 'paliwords')

  def readWordJson(word):
    path = os.path.join(wordsDir, word).encode('utf-8')
    with open(path, 'r') as f:
      return f.read()

  def isValidWord(word):
    path = os.path.join(wordsDir, word).encode('utf-8')
    return os.path.isfile(path)


def getWordJson(word):
  return readWordJson(word)

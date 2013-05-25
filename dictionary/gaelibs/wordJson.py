#!/usr/bin/env python
# -*- coding:utf-8 -*-

from google.appengine.ext import ndb

class PaliWordJsonBlob(ndb.Model):
  """blob which stores json data"""
  data = ndb.BlobProperty()

def readWordFromGAEDatastore(word):
  jblob = PaliWordJsonBlob.get_by_id(word)
  if jblob:
    return jblob.data
  else:
    raise Exception('word not found: %s' % word)

def getWordJson(word):
  return readWordFromGAEDatastore(word)

#!/usr/bin/env python
# -*- coding:utf-8 -*-

from google.appengine.ext import ndb

class PaliWordJson(ndb.Model):
  """data is in json-format (deprecated)"""
  data = ndb.BlobProperty()

class Xml(ndb.Model):
  """deprecated"""
  # maybe can try optional keyword argument "compressed". See
  # https://developers.google.com/appengine/docs/python/ndb/properties#compressed
  content = ndb.BlobProperty()

class PaliWord(ndb.Model):
  xmlfilename = ndb.StringProperty()
  xmlfiledata = ndb.TextProperty()

def deleteAllXmlModel():
  """FIXME: The following command cannot be used via remote api of production
     server, because it will run out of free quota!!!
  """
  ndb.delete_multi(Xml.query().fetch(999999, keys_only=True))

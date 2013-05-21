#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
SDK_PATH = os.path.expanduser("~/google_appengine/")
sys.path.insert(0, SDK_PATH)
sys.path.append(os.path.join(SDK_PATH, 'lib/yaml/lib'))
sys.path.append(os.path.join(SDK_PATH, 'lib/fancy_urllib'))
from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.ext import ndb
import getpass

def auth_func():
  return (raw_input('Username:'), getpass.getpass('Password:'))

remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', auth_func,
                                   'palidictionary.appspot.com')

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

def deleteXmlModel(num):
  """num cannot be too large (will run out of free quota immediately),
     num=100 is a good fit.
  """
  ndb.delete_multi(Xml.query().fetch(num, keys_only=True))

def deletePaliWordModel(num):
  """num cannot be too large (will run out of free quota immediately),
     num=100 is a good fit.
  """
  ndb.delete_multi(PaliWord.query().fetch(num, keys_only=True))


if __name__ == '__main__':
  #deleteXmlModel(100)
  deletePaliWordModel(100)

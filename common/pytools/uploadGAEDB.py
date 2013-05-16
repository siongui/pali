#!/usr/bin/env python
# -*- coding:utf-8 -*-

# For uploading data to Google App Engine datastore

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
                                   'epalitipitaka.appspot.com')

class Xml(ndb.Model):
  content = ndb.BlobProperty()

if __name__ == '__main__':
  romn_dir = os.path.join(os.path.dirname(__file__), '../romn/')
  key = 'cscd/s0502m.mul5.xml'
  print(key)

  with open(os.path.join(romn_dir, key), 'rb') as f:
    xml = Xml(id=key, content=f.read())
  xml.put()

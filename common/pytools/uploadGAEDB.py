#!/usr/bin/env python
# -*- coding:utf-8 -*-

# For uploading data to Google App Engine datastore

import os
import sys
import json

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


def uploadXmls():
  romn_dir = os.path.join(os.path.dirname(__file__), '../romn/')
  fail_to_uploaded_xmls = []

  for dirpath, dirnames, filenames in os.walk(romn_dir):
    for filename in filenames:
      path = os.path.join(dirpath, filename)
      key = path.lstrip(romn_dir)
      print('uploading %s ...' % key)
      with open(path, 'rb') as f:
        try:
          Xml(id=key, content=f.read()).put()
        except:
          fail_to_uploaded_xmls.append(key)
          print('fail to upload %s' % key)

  with open(os.path.join(os.path.dirname(__file__), 'fail.json'), 'w') as f:
    f.write(json.dumps(fail_to_uploaded_xmls))


def deleteAll():
  ndb.delete_multi(Xml.query().fetch(999999, keys_only=True))


from google.appengine.api import files

class XmlBlobKey(ndb.Model):
  blob_key = ndb.BlobKeyProperty()

def uploadXmlsToBlobstore():
  """Writing Files to the Blobstore (Experimental) via remote api not working!

  https://developers.google.com/appengine/docs/python/blobstore/overview#Writing_Files_to_the_Blobstore
  http://stackoverflow.com/questions/8201283/google-app-engine-how-to-write-large-files-to-google-cloud-storage
  http://stackoverflow.com/questions/3530990/upload-data-to-blobstore-using-remote-api
  http://stackoverflow.com/questions/6545247/erratic-problem-with-app-engine-when-writing-files-directly-to-the-blobstore
  """
  romn_dir = os.path.join(os.path.dirname(__file__), '../romn/')

  for dirpath, dirnames, filenames in os.walk(romn_dir):
    for filename in filenames:
      path = os.path.join(dirpath, filename)
      key = path.lstrip(romn_dir)
      print('uploading %s ...' % key)
      with open(path, 'rb') as f:
        # Create the file
        file_name = files.blobstore.create(mime_type='application/octet-stream')

        # Open the file and write to it
        with files.open(file_name, 'a') as f2:
          f2.write(f.read())

        # Finalize the file. Do this before attempting to read it.
        files.finalize(file_name)

        XmlBlobKey(id=key, blob_key=files.blobstore.get_blob_key(file_name)).put()


if __name__ == '__main__':
  #deleteAll()
  #uploadXmls()
  uploadXmlsToBlobstore()

#!/usr/bin/env python
# -*- coding:utf-8 -*-

# For uploading data to Google App Engine datastore or blobstore

import os
import sys
import json
import urllib2
import base64

SDK_PATH = os.path.expanduser("~/google_appengine/")
"""
cannot use:
    sys.path.append(SDK_PATH)
must use:
    sys.path.insert(0, SDK_PATH)
"""
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
"""
# For credentials of remote api on dev server of app engine,
# http://stackoverflow.com/questions/1260835/which-credentials-should-i-put-in-for-google-app-engine-bulkloader-at-developmen
def auth_func():
  return ("test@example.com", "")

remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', auth_func,
                                   'localhost:8080')
"""

class Xml(ndb.Model):
  """deprecated"""
  # maybe can try optional keyword argument "compressed". See
  # https://developers.google.com/appengine/docs/python/ndb/properties#compressed
  content = ndb.BlobProperty()


def uploadXmls():
  """(deprecated) Upload all xml files to the datastore of production server
     programmatically via remote api.
  """
  romn_dir = os.path.join(os.path.dirname(__file__), '../romn/')
  fail_to_be_uploaded_xmls = []

  for dirpath, dirnames, filenames in os.walk(romn_dir):
    for filename in filenames:
      path = os.path.join(dirpath, filename)
      key = path.lstrip(romn_dir)
      print('uploading %s ...' % key)
      with open(path, 'rb') as f:
        # because of "1 MB API limits apply" of remote_api, see
        # https://developers.google.com/appengine/articles/remote_api#limitations
        # The following code may raise exception if request over 1 MB
        try:
          Xml(id=key, content=f.read()).put()
        except:
          fail_to_be_uploaded_xmls.append(key)
          print('fail to upload %s' % key)

  with open(os.path.join(os.path.dirname(__file__), 'fail.json'), 'w') as f:
    f.write(json.dumps(fail_to_be_uploaded_xmls))


def deleteAllXmlModel():
  """deprecated"""
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


def uploadXmlsViaCustomRemoteBlobstoreAPI():
  romn_dir = os.path.join(os.path.dirname(__file__), '../romn/')

  for dirpath, dirnames, filenames in os.walk(romn_dir):
    for filename in filenames:
      path = os.path.join(dirpath, filename)
      key = path.lstrip(romn_dir)
      print('uploading %s ...' % key)

      """Python HTTP POST json-format data (payload is encoded with base64).

      Reference:
          http://stackoverflow.com/questions/4348061/how-to-use-python-urllib2-to-send-json-data-for-login
          http://stackoverflow.com/questions/16329786/how-can-i-get-python-base64-encoding-to-play-nice-with-json
      """
      with open(path, 'rb') as f:
        jdata = json.dumps({'key': key,
                            'payload': base64.b64encode(f.read()) })
      #response = urllib2.urlopen("http://localhost:8080/customRemoteBlobstoreAPI", jdata)
      response = urllib2.urlopen(
          "http://epalitipitaka.appspot.com/customRemoteBlobstoreAPI",
          jdata)
      result_array = response.read().split('<br />')
      if result_array[0] == 'OK':
        print('key: %s, blob_key: %s' % (result_array[1], result_array[2]))
      else:
        raise Exception('server return error: %s' % response.read())


if __name__ == '__main__':
  #deleteAllXmlModel()
  #uploadXmls()
  #uploadXmlsToBlobstore()
  uploadXmlsViaCustomRemoteBlobstoreAPI()

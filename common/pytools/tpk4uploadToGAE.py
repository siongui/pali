#!/usr/bin/env python
# -*- coding:utf-8 -*-

# For uploading data to Google App Engine datastore or blobstore

import os
import sys
import json
import urllib2
import base64

from variables import getSDKPath
sys.path.insert(0, getSDKPath())
sys.path.append(os.path.join(getSDKPath(), 'lib/yaml/lib'))
sys.path.append(os.path.join(getSDKPath(), 'lib/fancy_urllib'))
from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.ext import ndb

import getpass

def AskIfUploadToDevServer():
  answer = raw_input('upload to dev server? (y/n): ')
  if answer == 'y':
    return True
  else:
    return False

isUploadeToDevServer = AskIfUploadToDevServer()

def auth_func():
  if isUploadeToDevServer:
    return ("test@example.com", "")
  else:
    return (raw_input('Username:'), getpass.getpass('Password:'))

def host_func():
  if isUploadeToDevServer:
    return 'localhost:8080'
  else:
    return '%s.appspot.com' % raw_input('app_name:')

remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', auth_func,
                                   host_func())


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
  """
  http://stackoverflow.com/questions/101742/how-do-you-access-an-authenticated-google-app-engine-service-from-a-non-web-py
  http://stackoverflow.com/questions/10118585/how-to-make-an-authenticated-request-from-a-script-to-appengine?lq=1
  """
  app_name = raw_input('app_name:')
  from google.appengine.tools import appengine_rpc
  rpcServer = appengine_rpc.HttpRpcServer(
      "%s.appspot.com" % app_name,
      auth_func,
      None,
      app_name,
      save_cookies=True,
      secure=True)

  romn_dir = os.path.join(os.path.dirname(__file__), '../../../data/pali/common/romn/')

  for dirpath, dirnames, filenames in os.walk(romn_dir):
    for filename in filenames:
      path = os.path.join(dirpath, filename)
      # FIXME: key is not correct
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
      #response = urllib2.urlopen(
      #    "http://epalitipitaka.appspot.com/customRemoteBlobstoreAPI",
      #    jdata)
      #result_array = response.read().split('<br />')
      result_array = rpcServer.Send('/customRemoteBlobstoreAPI', jdata).split('<br />')
      if result_array[0] == 'OK':
        print('key: %s, blob_key: %s' % (result_array[1], result_array[2]))
      else:
        #raise Exception('server return error: %s' % response.read())
        raise Exception('server return error!')


if __name__ == '__main__':
  #uploadXmlsToBlobstore()
  uploadXmlsViaCustomRemoteBlobstoreAPI()

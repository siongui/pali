#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Upload pali words data to Google App Engine datastore

import os
import sys

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


class PaliWordJsonBlob(ndb.Model):
  """blob which stores json data"""
  data = ndb.BlobProperty()


dictWordsJsonDir = os.path.join(os.path.dirname(__file__), 'paliwords')

def uploadToServer():
  """Upload all pali words definitions to the datastore of server
     programmatically via remote api.

     References:
     find the 10 largest file or folder in the directory:
     ls -lS path_to_folder | head -n 10
     http://stackoverflow.com/questions/12522269/bash-how-to-find-the-largest-file-in-a-directory-and-its-subdirectories
  """
  count = 0
  list_of_entities = []

  for dirpath, dirnames, filenames in os.walk(dictWordsJsonDir):
    for filename in filenames:
      path = os.path.join(dirpath, filename)
      print('uploading %s ...' % path)
      with open(path, 'r') as f:
        #PaliWordJsonBlob(id=filename[:-5], data=f.read()).put()
        #PaliWordJsonBlob(id=filename, data=f.read()).put()
        list_of_entities.append(PaliWordJsonBlob(id=filename, data=f.read()))
        # Remember "1 MB API limits apply" of remote_api
        if len(list_of_entities) == 40:
          print('putting %d records ...' % len(list_of_entities))
          ndb.put_multi(list_of_entities)
          count += len(list_of_entities)
          print('total number uploaded: %d' % count)
          list_of_entities = []

  if len(list_of_entities) > 0:
    print('putting %d records ...' % len(list_of_entities))
    ndb.put_multi(list_of_entities)
    count += len(list_of_entities)
    print('total number uploaded: %d' % count)


if __name__ == '__main__':
  uploadToServer()

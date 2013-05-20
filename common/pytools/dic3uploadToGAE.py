#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Upload pali words data to Google App Engine datastore

import os
import sys

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

"""
def auth_func():
  return (raw_input('Username:'), getpass.getpass('Password:'))

remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', auth_func,
                                   'palidictionary.appspot.com')
"""
# For credentials of remote api on dev server of app engine,
# http://stackoverflow.com/questions/1260835/which-credentials-should-i-put-in-for-google-app-engine-bulkloader-at-developmen
def auth_func():
  return ("test@example.com", "")

remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', auth_func,
                                   'localhost:8080')

class PaliWordJsonBlob(ndb.Model):
  """blob which stores json data"""
  data = ndb.BlobProperty()


def uploadBooksAndWordsToServer():
  """Upload all pali words definitions to the datastore of dev server 
     programmatically via remote api.

     References:
     find the 10 largest file or folder in the directory:
     ls -lS path_to_folder | head -n 10
     http://stackoverflow.com/questions/12522269/bash-how-to-find-the-largest-file-in-a-directory-and-its-subdirectories
  """
  count = 0
  list_of_entities = []

  print('uploading %s ...' % dictBooksJsonPath)
  with open(dictBooksJsonPath, 'r') as f:
    #PaliWordJsonBlob(id='books.json', data=f.read()).put()
    list_of_entities.append(PaliWordJsonBlob(id='books.json', data=f.read()))
    count += 1

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
          ndb.put_multi(list_of_entities)
          print('putting %d records ...' % len(list_of_entities))
          count += len(list_of_entities)
          print('total number uploaded: %d' % count)
          list_of_entities = []

  if len(list_of_entities) > 0:
    ndb.put_multi(list_of_entities)
    print('putting %d records ...' % len(list_of_entities))
    count += len(list_of_entities)
    print('total number uploaded: %d' % count)


if __name__ == '__main__':
  uploadBooksAndWordsToServer()

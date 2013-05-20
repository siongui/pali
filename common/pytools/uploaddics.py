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

class PaliWordJson(ndb.Model):
  """data is in json-format"""
  data = ndb.BlobProperty()


dictWordsCSV1Path = os.path.join(os.path.dirname(__file__),
    "../../../data/pali/common/dictionary/dict_words_1.csv")
dictWordsCSV2Path = os.path.join(os.path.dirname(__file__),
    "../../../data/pali/common/dictionary/dict_words_2.csv")

dictWordsJsonDir = os.path.join(os.path.dirname(__file__), 'paliwords')

def processWordCSV(csvPath, dicIndex, output_dir):
  import json
  import csv
  with open(csvPath, "r") as wordsCsvfile:
    wordreader = csv.reader(wordsCsvfile, delimiter=',', quotechar='"')
    for row in wordreader:

      if len(row) != 7:
        raise Exception('len(row) != 7')

      if row[0] == 'db_id': continue

      """
      print(dicIndex[row[2]]['locale'])
      print(dicIndex[row[2]]['data'][2])
      print(dicIndex[row[2]]['data'][3])
      print(row[4])
      print(row[6])
      """

      #path = os.path.join(output_dir, '%s.json' % 
      path = os.path.join(output_dir, '%s' % 
          row[4].decode('utf-8').lower())
      print(path)
      #print([dicIndex[row[2]]['data'][1], row[6]])

      if os.path.exists(path):
        # append new data to existing data
        with open(path, 'r') as f:
          data = json.loads(f.read())

        if dicIndex[row[2]]['locale'] == 'zh':
          data.append([dicIndex[row[2]]['data'][1], jtof(row[6])])
        else:
          data.append([dicIndex[row[2]]['data'][1], row[6]])

        with open(path, 'w') as f:
          f.write(json.dumps(data))
      else:
        # create new data file
        if dicIndex[row[2]]['locale'] == 'zh':
          data = [ [dicIndex[row[2]]['data'][1], jtof(row[6])] ]
        else:
          data = [ [dicIndex[row[2]]['data'][1], row[6]] ]

        with open(path, 'w') as f:
          f.write(json.dumps(data))


def processDictionariesWords():
  import json
  with open(dictBooksJsonPath, 'r') as f:
    dicIndex = json.loads(f.read())

  import shutil
  output_dir = dictWordsJsonDir
  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
  else:
    os.makedirs(output_dir)

  processWordCSV(dictWordsCSV1Path, dicIndex, output_dir)
  processWordCSV(dictWordsCSV2Path, dicIndex, output_dir)


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
    #PaliWordJson(id='books.json', data=f.read()).put()
    list_of_entities.append(PaliWordJson(id='books.json', data=f.read()))
    count += 1

  for dirpath, dirnames, filenames in os.walk(dictWordsJsonDir):
    for filename in filenames:
      path = os.path.join(dirpath, filename)
      print('uploading %s ...' % path)
      with open(path, 'r') as f:
        #PaliWordJson(id=filename[:-5], data=f.read()).put()
        #PaliWordJson(id=filename, data=f.read()).put()
        list_of_entities.append(PaliWordJson(id=filename, data=f.read()))
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
  #processDictionariesBooks()
  processDictionariesWords()
  #uploadBooksAndWordsToServer()

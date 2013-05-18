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


"""
keyword: "python traditional chinese to simplified chinese"
https://code.google.com/p/python-jianfan/
https://pypi.python.org/pypi/pyopencc
https://bitbucket.org/victorlin/opencc_python

install pyopencc:
sudo apt-get install libopencc-dev python-dev
git clone https://github.com/cute/pyopencc.git
cd pyopencc
python setup.py build_ext -I /usr/include/opencc/
sudo python setup.py install

pyopencc usage:
import pyopencc
"""
try:
  import pyopencc
  cc = pyopencc.OpenCC('zhs2zht.ini')
  jtof = cc.convert
except:
  print('cannot import opencc, import jianfan')
  sys.path.append(os.path.join(os.path.dirname(__file__), '../gae/libs'))
  from jianfan import jtof


dictBooksCSVPath = os.path.join(os.path.dirname(__file__),
    "../../../data/pali/common/dictionary/dict-books.csv")
dictWordsCSVPath = os.path.join(os.path.dirname(__file__),
    "../../../data/pali/common/dictionary/dict-words.csv")


def processDictionariesBooks():
  import csv
  with open(dictBooksCSVPath, "r") as booksCsvfile:
    bookreader = csv.reader(booksCsvfile, delimiter=',', quotechar='"')
    dicIndex = {}
    for row in bookreader:

      if len(row) != 4:
        raise Exception('len(row) != 4')

      if row[0] == 'b_lang':
        continue

      dicIndex[row[1]] = { 'locale': None,
                           'data': row }

      if row[0] == 'C':
        # Chinese and Japanese dictionaries
        if row[1] == 'A':
          # Japanese dictionary
          dicIndex[row[1]]['locale'] = 'ja'
          row[2] = '《パーリ語辞典》'
          row[3] = '増補改訂パーリ語辞典  水野弘元著'
        elif row[1] == 'S':
          # Japanese dictionary
          dicIndex[row[1]]['locale'] = 'ja'
          row[2] = '《パーリ語辞典》'
          row[3] = 'パーリ語辞典  水野弘元著'
        else:
          # Chinese dictionary
          dicIndex[row[1]]['locale'] = 'zh'
          row[2] = jtof(row[2])
          row[3] = jtof(row[3])

      else:
        # English, Vietnam, Myanmar dictionaries
        if row[1] == 'U' or \
           row[1] == 'Q' or \
           row[1] == 'E':
          # Vietnamese dictionary
          dicIndex[row[1]]['locale'] = 'vi'
        elif row[1] == 'B' or \
             row[1] == 'K' or \
             row[1] == 'O' or \
             row[1] == 'R':
          # Burmese(Myanmar) dictionary
          dicIndex[row[1]]['locale'] = 'my'
        else:
          # English dictionary
          dicIndex[row[1]]['locale'] = 'en'

      print(dicIndex[row[1]]['locale'])
      for cell in dicIndex[row[1]]['data']:
        print(cell)

    import json
    with open(os.path.join(os.path.dirname(__file__), 'books.json'), 'w') as f:
      f.write(json.dumps(dicIndex))


def processDictionariesWords():
  """Upload all pali words definitions to the datastore of dev server 
     programmatically via remote api.
  """
  import csv
  with open(dictWordsCSVPath, "r") as wordsCsvfile:
    wordreader = csv.reader(wordsCsvfile, delimiter=',', quotechar='"')
    index = 0
    for row in wordreader:
      if len(row) != 7:
        raise Exception('len(row) != 7')
      index += 1
      print(row)
      if index > 10: break


if __name__ == '__main__':
  #processDictionariesBooks()
  processDictionariesWords()

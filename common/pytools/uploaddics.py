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


def uploadWords2DevStore():
  """Upload all pali words definitions to the datastore of dev server 
     programmatically via remote api.
  """
  import csv
  with open(dictBooksCSVPath, "r") as booksCsvfile:
    bookreader = csv.reader(booksCsvfile, delimiter=',', quotechar='"')
    for row in bookreader:
      if len(row) != 4:
        raise Exception('len(row) != 4')
      #row[2] = row[2].decode('utf-8')
      #row[3] = row[3].decode('utf-8')
      if row[0] == 'C':
        print(row[2])
        print(row[3])
        if row[1] == 'A':
          print('《パーリ語辞典》')
          print('増補改訂パーリ語辞典  水野弘元著')
        elif row[1] == 'S':
          print('《パーリ語辞典》')
          print('パーリ語辞典  水野弘元著')
        else:
          print(jtof(row[2]))
          print(jtof(row[3]))
        print('---')
      #for cell in row:
      #  print(cell)
      #  print(type(cell))

    """
    with open(dictWordsCSVPath, "r") as wordsCsvfile:
      wordreader = csv.reader(wordsCsvfile, delimiter=',', quotechar='"')
      index = 0
      for row in wordreader:
        if len(row) != 7:
          raise Exception('len(row) != 7')
        index += 1
        print(row)
        if index > 10: break
    """


if __name__ == '__main__':
  uploadWords2DevStore()

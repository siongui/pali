#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import csv
import json

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
dictBooksJsonPath = os.path.join(os.path.dirname(__file__),
    '../gae/libs/json/books.json')

def processDictionariesBooks():
  with open(dictBooksCSVPath, "r") as booksCsvfile:
    bookreader = csv.reader(booksCsvfile, delimiter=',', quotechar='"')
    dicIndex = {}
    for row in bookreader:

      if len(row) != 4:
        raise Exception('len(row) != 4')

      if row[0] == 'b_lang': continue

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
      print('---')

    with open(dictBooksJsonPath, 'w') as f:
      f.write(json.dumps(dicIndex))


if __name__ == '__main__':
  processDictionariesBooks()

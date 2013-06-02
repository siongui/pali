#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import json
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), '../../common/pytools'))
from variables import getDictBooksJsonPath
from variables import getDictWordsCSV1Path
from variables import getDictWordsCSV2Path

import goslate
from time import sleep


def extractOneDicExps(dicIndex, dicId):
  with open(getDictWordsCSV1Path(), 'r') as f:
    wordreader = csv.reader(f, delimiter=',', quotechar='"')
    for row in wordreader:
      if len(row) != 7:
        raise Exception('len(row) != 7')
      if row[0] == 'db_id': continue

      word = row[4].decode('utf-8').lower()
      if row[2] == dicId:
        yield [word, row[6]]

  with open(getDictWordsCSV2Path(), 'r') as f:
    wordreader = csv.reader(f, delimiter=',', quotechar='"')
    for row in wordreader:
      if len(row) != 7:
        raise Exception('len(row) != 7')
      if row[0] == 'db_id': continue

      word = row[4].decode('utf-8').lower()
      if row[2] == dicId:
        yield [word, row[6]]


if __name__ == '__main__':
  gs = goslate.Goslate()
  #print(gs.get_languages())

  with open(getDictBooksJsonPath(), 'r') as f:
    dicIndex = json.loads(f.read())

  """
  Pali-English Id:
    "N": "Buddhist Dictionary by NYANATILOKA MAHATHERA"
    "C": "Concise Pali-English Dictionary by A.P. Buddhadatta Mahathera"
    "P": "PTS Pali-English dictionary The Pali Text Society's Pali-English dictionary"
    "V": "Buddhist Dictionary of Pali Proper Names by G P Malalasekera"
    "I": "Pali-Dictionary Vipassana Research Institute"
  """
  dicId = 'C'

  with open(os.path.join(os.path.dirname(__file__), 'output.csv'), 'wb') as f:
    frWriter = csv.writer(f, delimiter=',', quotechar='"')

    index = 0
    for word, explanation in extractOneDicExps(dicIndex, dicId):
      index += 1
      if index < 22560: continue

      translatedExplanation = gs.translate(explanation, 'fr', 'en')
      frWriter.writerow([word.encode('utf-8'),
                         translatedExplanation.encode('utf-8')])

      print(explanation)
      print(translatedExplanation)

      sleep(0.9)

  print('number of words in %s: %d' % (dicIndex[dicId][3], index + 1))

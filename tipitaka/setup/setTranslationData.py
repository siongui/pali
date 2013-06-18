#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import collections
import re
import imp

from variables import ftoj
from variables import localedir

jstr = """{
  'zh_TW': {
    'canon': {
      's0101m.mul1.xml': [ { 'source': '3' } ],
      's0102m.mul2.xml': [ { 'source': '3' } ],
      's0102m.mul6.xml': [ { 'source': '5' } ],
      's0102m.mul8.xml': [ { 'source': '3' } ],
      's0103m.mul7.xml': [ { 'source': '3' } ],
      's0201m.mul0.xml': [ { 'source': '3', 'excerpt': true } ],
      's0201m.mul1.xml': [ { 'source': '3', 'excerpt': true } ],
      's0201m.mul2.xml': [ { 'source': '3', 'excerpt': true } ],
      's0201m.mul3.xml': [ { 'source': '3', 'excerpt': true } ],
      's0201m.mul4.xml': [ { 'source': '3', 'excerpt': true } ],
      's0202m.mul0.xml': [ { 'source': '3', 'excerpt': true } ],
      's0202m.mul1.xml': [ { 'source': '3', 'excerpt': true } ],
      's0202m.mul4.xml': [ { 'source': '3', 'excerpt': true } ],
      's0402m2.mul6.xml': [ { 'source': '3', 'excerpt': true } ],
      's0501m.mul0.xml': [ { 'source': '4' },
                           { 'source': '5' } ],
      's0501m.mul1.xml': [ { 'source': '4' },
                           { 'source': '5' } ],
      's0501m.mul2.xml': [ { 'source': '4' },
                           { 'source': '5' } ],
      's0501m.mul3.xml': [ { 'source': '4' },
                           { 'source': '5' } ],
      's0501m.mul4.xml': [ { 'source': '4' },
                           { 'source': '5' } ],
      's0501m.mul5.xml': [ { 'source': '4' },
                           { 'source': '5' } ],
      's0501m.mul6.xml': [ { 'source': '6' } ],
      's0502m.mul0.xml': [ { 'source': '2' } ],
      's0502m.mul1.xml': [ { 'source': '2' } ],
      's0502m.mul2.xml': [ { 'source': '2' } ],
      's0502m.mul3.xml': [ { 'source': '2' } ],
      's0502m.mul4.xml': [ { 'source': '2' } ],
      's0502m.mul5.xml': [ { 'source': '2' } ],
      's0502m.mul6.xml': [ { 'source': '2' } ],
      's0502m.mul7.xml': [ { 'source': '2' } ],
      's0502m.mul8.xml': [ { 'source': '2' } ],
      's0502m.mul9.xml': [ { 'source': '2' } ],
      's0502m.mul10.xml': [ { 'source': '2' } ],
      's0502m.mul11.xml': [ { 'source': '2' } ],
      's0502m.mul12.xml': [ { 'source': '2' } ],
      's0502m.mul13.xml': [ { 'source': '2' } ],
      's0502m.mul14.xml': [ { 'source': '2' } ],
      's0502m.mul15.xml': [ { 'source': '2' } ],
      's0502m.mul16.xml': [ { 'source': '2' } ],
      's0502m.mul17.xml': [ { 'source': '2' } ],
      's0502m.mul18.xml': [ { 'source': '2' } ],
      's0502m.mul19.xml': [ { 'source': '2' } ],
      's0502m.mul20.xml': [ { 'source': '2' } ],
      's0502m.mul21.xml': [ { 'source': '2' } ],
      's0502m.mul22.xml': [ { 'source': '2' } ],
      's0502m.mul23.xml': [ { 'source': '2' } ],
      's0502m.mul24.xml': [ { 'source': '2' } ],
      's0502m.mul25.xml': [ { 'source': '2' } ],
      's0505m.mul0.xml': [ { 'source': '1' } ],
      's0505m.mul1.xml': [ { 'source': '1' } ],
      's0505m.mul2.xml': [ { 'source': '1' } ],
      's0505m.mul3.xml': [ { 'source': '1' } ],
      's0505m.mul4.xml': [ { 'source': '1' } ]
    },
    'source': {
      '1': ['郭良鋆', 'http://blog.yam.com/benji/article/34665984'],
      '2': ['了參法師(葉均)', 'http://myweb.ncku.edu.tw/~lsn46/Tipitaka/Sutta/Khuddaka/Dhammapada/ven-l-z-all.htm'],
      '3': ['蕭式球', 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5'],
      '4': ['悟醒', 'http://www.online-dhamma.net/dhammarain/canon/cy-1-Khuddakapaatha-Dhammapada-Udaana-Itivuttaka.pdf'],
      '5': ['瑪欣德尊者', 'http://www.taiwandipa.org.tw/images/k/k473-0.zip', 'http://www.taiwandipa.org.tw/images/k/k485-0.zip'],
      '6': ['鄧殿臣', 'http://tripitaka.cbeta.org/mobile/index.php?index=W05']
    }
  },
  'en_US': {
    'canon': {
      's0401m.mul2.xml': [ { 'source': '1' } ],
      's0401m.mul3.xml': [ { 'source': '1' } ],
      's0401m.mul4.xml': [ { 'source': '1', 'excerpt': true } ],
      's0401m.mul5.xml': [ { 'source': '1', 'excerpt': true } ],
      's0402m1.mul0.xml': [ { 'source': '1', 'excerpt': true } ],
      's0402m1.mul2.xml': [ { 'source': '1', 'excerpt': true } ],
      's0402m1.mul3.xml': [ { 'source': '1', 'excerpt': true } ],
      's0402m1.mul4.xml': [ { 'source': '1', 'excerpt': true } ],
      's0402m1.mul9.xml': [ { 'source': '1', 'excerpt': true } ],
      's0402m1.mul10.xml': [ { 'source': '1', 'excerpt': true } ],
      's0501m.mul0.xml': [ { 'source': '1' } ],
      's0502m.mul0.xml': [ { 'source': '1' } ],
      's0502m.mul1.xml': [ { 'source': '1' } ],
      's0502m.mul2.xml': [ { 'source': '1' } ],
      's0502m.mul3.xml': [ { 'source': '1' } ],
      's0502m.mul4.xml': [ { 'source': '1' } ],
      's0502m.mul5.xml': [ { 'source': '1' } ],
      's0502m.mul6.xml': [ { 'source': '1' } ],
      's0502m.mul7.xml': [ { 'source': '1' } ],
      's0502m.mul8.xml': [ { 'source': '1' } ],
      's0502m.mul9.xml': [ { 'source': '1' } ],
      's0502m.mul10.xml': [ { 'source': '1' } ],
      's0502m.mul11.xml': [ { 'source': '1' } ],
      's0502m.mul12.xml': [ { 'source': '1' } ],
      's0502m.mul13.xml': [ { 'source': '1' } ],
      's0502m.mul14.xml': [ { 'source': '1' } ],
      's0502m.mul15.xml': [ { 'source': '1' } ],
      's0502m.mul16.xml': [ { 'source': '1' } ],
      's0502m.mul17.xml': [ { 'source': '1' } ],
      's0502m.mul18.xml': [ { 'source': '1' } ],
      's0502m.mul19.xml': [ { 'source': '1' } ],
      's0502m.mul20.xml': [ { 'source': '1' } ],
      's0502m.mul21.xml': [ { 'source': '1' } ],
      's0502m.mul22.xml': [ { 'source': '1' } ],
      's0502m.mul23.xml': [ { 'source': '1' } ],
      's0502m.mul24.xml': [ { 'source': '1' } ],
      's0502m.mul25.xml': [ { 'source': '1' } ],
      's0505m.mul0.xml': [ { 'source': '1', 'excerpt': true } ],
      's0505m.mul1.xml': [ { 'source': '1', 'excerpt': true } ],
      's0505m.mul2.xml': [ { 'source': '1', 'excerpt': true } ],
      's0505m.mul3.xml': [ { 'source': '1' } ],
      's0505m.mul4.xml': [ { 'source': '1', 'excerpt': true } ]
    },
    'source': {
      '1': ['Ṭhānissaro Bhikkhu', 'http://www.accesstoinsight.org/tipitaka/translators.html#than', 'http://www.accesstoinsight.org/lib/authors/thanissaro/dhammapada.pdf']
    }
  },
  'ja_JP': {
    'canon': {
    },
    'source': {
      '1': ['光明寺住職', 'http://komyojikyozo.web.fc2.com/top.html', 'komyojikyozo@hotmail.co.jp']
    }
  }
}"""
jstr = re.sub(r"'", r'"', jstr)
# http://stackoverflow.com/questions/7878933/is-possible-to-override-the-notation-so-i-get-an-ordereddict-instead-of
d = json.JSONDecoder(object_pairs_hook = collections.OrderedDict)
translationInfo = d.decode(jstr)

canonTextTranslation = {}

if __name__ == '__main__':
  dstTrInfoPath = os.path.join(os.path.dirname(__file__),
      '../pylib/json/translationInfo.json')
  dstCanonTextTranslationPath = os.path.join(os.path.dirname(__file__),
      '../pylib/json/canonTextTranslation.json')

  if not os.path.exists(os.path.dirname(dstTrInfoPath)):
    os.makedirs(os.path.dirname(dstTrInfoPath))

  with open(dstTrInfoPath, 'w') as f:
    f.write(json.dumps(translationInfo))

  # initialize canonTextTranslation
  for dirpath, dirnames, filenames in os.walk(localedir):
    for dirname in dirnames:
      locale = dirname
      path = os.path.join(localedir, '%s/LC_MESSAGES/PaliTextTitle.py' % locale)
      if os.path.isfile(path):
        var = imp.load_source('PaliTextTitle', path)
        canonTextTranslation[locale] = var.PaliTextTitle
    break

  # derive zh_CN from zh_TW
  canonTextTranslation['zh_CN'] = {}
  for key in canonTextTranslation['zh_TW']:
    canonTextTranslation['zh_CN'][key] = ftoj(canonTextTranslation['zh_TW'][key])
  with open(dstCanonTextTranslationPath, 'w') as f:
    f.write(json.dumps(canonTextTranslation))

  dstTrServicePath = os.path.join(os.path.dirname(__file__),
      '../app/scripts/services/data/i18nTpk.js')

  if not os.path.exists(os.path.dirname(dstTrServicePath)):
    os.makedirs(os.path.dirname(dstTrServicePath))
  with open(dstTrServicePath, 'w') as f:
    f.write("angular.module('pali.data.i18nTpk', []).\n")
    f.write("  factory('i18nTpk', [function() {\n")
    #f.write("    var translationInfo = ")
    #f.write(json.dumps(translationInfo))
    #f.write(";\n")
    f.write("    var canonTextTranslation = ")
    f.write(json.dumps(canonTextTranslation))
    f.write(";\n")
    f.write("    return { canonTextTranslation: canonTextTranslation };\n")
    #f.write("    var serviceInstance = { translationInfo: translationInfo, canonTextTranslation: canonTextTranslation };\n")
    #f.write("    return serviceInstance;\n")
    f.write("  }]);\n")

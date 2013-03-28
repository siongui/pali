#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, json


translationInfo = {
  'zh_TW': {
    'canon': {
      's0201m.mul0.xml': ['3'],
      's0201m.mul1.xml': ['3'],
      's0201m.mul2.xml': ['3'],
      's0201m.mul3.xml': ['3'],
      's0201m.mul4.xml': ['3'],
      's0202m.mul0.xml': ['3'],
      's0202m.mul1.xml': ['3'],
      's0202m.mul4.xml': ['3'],
      's0402m2.mul6.xml': ['3'],
      's0502m.mul0.xml': ['2'],
      's0502m.mul1.xml': ['2'],
      's0502m.mul2.xml': ['2'],
      's0502m.mul3.xml': ['2'],
      's0502m.mul4.xml': ['2'],
      's0505m.mul0.xml': ['1']
    },
    'source': {
      '1': ['郭良鋆', 'http://blog.yam.com/benji/article/34665984'],
      '2': ['了參法師(葉均)', 'http://myweb.ncku.edu.tw/~lsn46/Tipitaka/Sutta/Khuddaka/Dhammapada/ven-l-z-all.htm'],
      '3': ['蕭式球', 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5']
    }
  },
  'en_US': {
    'canon': {
      's0502m.mul0.xml': ['1'],
      's0502m.mul1.xml': ['1'],
      's0502m.mul2.xml': ['1'],
      's0502m.mul3.xml': ['1'],
      's0502m.mul4.xml': ['1']
    },
    'source': {
      '1': ['Ṭhānissaro Bhikkhu', 'http://www.accesstoinsight.org/tipitaka/translators.html#than', 'http://www.accesstoinsight.org/lib/authors/thanissaro/dhammapada.pdf']
    }
  }
}

canonName = {
  's0201m.mul0.xml': {
    'pali': 'Mūlapariyāyavaggo, Mūlapaṇṇāsa, Majjhima, Sutta',
    'zh_TW': '根本法門品, 根本五十經, 中部, 經藏'
  },
  's0201m.mul1.xml': {
    'pali': 'Sīhanādavaggo, Mūlapaṇṇāsa, Majjhima, Sutta',
    'zh_TW': '獅子吼品, 根本五十經, 中部, 經藏'
  },
  's0201m.mul2.xml': {
    'pali': 'Opammavaggo, Mūlapaṇṇāsa, Majjhima, Sutta',
    'zh_TW': '譬喻品, 根本五十經, 中部, 經藏'
  },
  's0201m.mul3.xml': {
    'pali': 'Mahāyamakavaggo, Mūlapaṇṇāsa, Majjhima, Sutta',
    'zh_TW': '雙大品, 根本五十經, 中部, 經藏'
  },
  's0201m.mul4.xml': {
    'pali': 'Cūḷayamakavaggo, Mūlapaṇṇāsa, Majjhima, Sutta',
    'zh_TW': '雙小品, 根本五十經, 中部, 經藏'
  },
  's0202m.mul0.xml': {
    'pali': 'Gahapativaggo, Majjhimapaṇṇāsa, Majjhima, Sutta',
    'zh_TW': '居士品, 中分五十經篇, 中部, 經藏'
  },
  's0202m.mul1.xml': {
    'pali': 'Bhikkhuvaggo, Majjhimapaṇṇāsa, Majjhima, Sutta',
    'zh_TW': '比丘品, 中分五十經篇, 中部, 經藏'
  },
  's0202m.mul4.xml': {
    'pali': 'Brāhmaṇavaggo, Majjhimapaṇṇāsa, Majjhima, Sutta',
    'zh_TW': '婆羅門品, 中分五十經篇, 中部, 經藏'
  },
  's0402m2.mul6.xml': {
    'pali': 'Mahāvaggo, Tikanipāta, Aṅguttara, Sutta',
    'zh_TW': '大品, 三集, 增支部, 經藏'
  },
  's0505m.mul0.xml': {
    'pali': 'Uragavaggo, Suttanipāta, Khuddaka, Sutta',
    'zh_TW': '蛇品, 經集, 小部, 經藏'
  },
  's0502m.mul0.xml': {
    'pali': 'Dhammapada, Yamakavaggo',
    'en_US': 'Dhammapada, Pairs',
    'zh_TW': '法句, 雙品'
  },
  's0502m.mul1.xml': {
    'pali': 'Dhammapada, Appamādavaggo',
    'en_US': 'Dhammapada, Heedfulness',
    'zh_TW': '法句, 不放逸品'
  },
  's0502m.mul2.xml': {
    'pali': 'Dhammapada, Cittavaggo',
    'en_US': 'Dhammapada, The Mind',
    'zh_TW': '法句, 心品'
  },
  's0502m.mul3.xml': {
    'pali': 'Dhammapada, Pupphavaggo',
    'en_US': 'Dhammapada, Blossoms',
    'zh_TW': '法句, 華(花)品'
  },
  's0502m.mul4.xml': {
    'pali': 'Dhammapada, Bālavaggo',
    'en_US': 'Dhammapada, Fools',
    'zh_TW': '法句, 愚品'
  }
}


if __name__ == '__main__':
  dstTrInfoPath = os.path.join(os.path.dirname(__file__), 'json/translationInfo.json')
  dstCanonNamePath = os.path.join(os.path.dirname(__file__), 'json/canonName.json')

  if not os.path.exists(os.path.dirname(dstTrInfoPath)):
    os.makedirs(os.path.dirname(dstTrInfoPath))

  with open(dstTrInfoPath, 'w') as f:
    f.write(json.dumps(translationInfo))

  with open(dstCanonNamePath, 'w') as f:
    f.write(json.dumps(canonName))

  dstTrServicePath = os.path.join(os.path.dirname(__file__), '../app/js/data-i18nTpk-service.js')

  with open(dstTrServicePath, 'w') as f:
    f.write("angular.module('pali.data.i18nTpk', []).\n")
    f.write("  factory('i18nTpk', [function() {\n")
    f.write("    var translationInfo = ")
    f.write(json.dumps(translationInfo))
    f.write(";\n")
    f.write("    var canonName = ")
    f.write(json.dumps(canonName))
    f.write(";\n")
    f.write("    var serviceInstance = { translationInfo: translationInfo, canonName: canonName };\n")
    f.write("    return serviceInstance;\n")
    f.write("  }]);\n")

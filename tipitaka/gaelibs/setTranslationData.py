#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import collections
import re

try:
  import pyopencc
  cc = pyopencc.OpenCC('zht2zhs.ini')
  ftoj = cc.convert
except:
  print('cannot import opencc, import jianfan')
  import sys
  sys.path.append(os.path.join(os.path.dirname(__file__), '../common/gae/libs'))
  from jianfan import ftoj


jstr = """{
  'zh_TW': {
    'canon': {
      's0101m.mul1.xml': [ { 'source': '3', 'URL': 'http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=59&id=272' } ],
      's0102m.mul2.xml': [ { 'source': '3', 'URL': 'http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=59&id=359' } ],
      's0102m.mul6.xml': [ { 'source': '5' } ],
      's0102m.mul8.xml': [ { 'source': '3', 'URL': 'http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=59&id=274' } ],
      's0103m.mul7.xml': [ { 'source': '3', 'URL': 'http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=59&id=275' } ],
      's0201m.mul0.xml': [ { 'source': '3', 'excerpt': true, 'URL': 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5' } ],
      's0201m.mul1.xml': [ { 'source': '3', 'excerpt': true, 'URL': 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5' } ],
      's0201m.mul2.xml': [ { 'source': '3', 'excerpt': true, 'URL': 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5' } ],
      's0201m.mul3.xml': [ { 'source': '3', 'excerpt': true, 'URL': 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5' } ],
      's0201m.mul4.xml': [ { 'source': '3', 'excerpt': true, 'URL': 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5' } ],
      's0202m.mul0.xml': [ { 'source': '3', 'excerpt': true, 'URL': 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5' } ],
      's0202m.mul1.xml': [ { 'source': '3', 'excerpt': true, 'URL': 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5' } ],
      's0202m.mul4.xml': [ { 'source': '3', 'excerpt': true, 'URL': 'http://www.chilin.edu.hk/edu/report_section.asp?section_id=5' } ],
      's0402m2.mul6.xml': [ { 'source': '3', 'excerpt': true, 'URL': 'http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=62&id=342' } ],
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
      's0501m.mul6.xml': [ { 'source': '6', 'copyrightURL': 'http://www.cbeta.org/copyright.php', 'URL': 'http://tripitaka.cbeta.org/W05n0045_001' } ],
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
      's0401m.mul2.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/an/an01/an01.021-040.than.html' } ],
      's0401m.mul3.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/an/an01/an01.021-040.than.html' } ],
      's0401m.mul4.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/an/index.html#an1' } ],
      's0401m.mul5.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/an/index.html#an1' } ],
      's0402m1.mul0.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/an/index.html#an2' } ],
      's0402m1.mul2.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/an/index.html#an2' } ],
      's0402m1.mul3.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/an/index.html#an2' } ],
      's0402m1.mul4.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/an/index.html#an2' } ],
      's0402m1.mul9.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/an/index.html#an2' } ],
      's0402m1.mul10.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/an/index.html#an2' } ],
      's0501m.mul0.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/khp/khp.1-9.than.html#khp-1' } ],
      's0502m.mul0.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.01.than.html' } ],
      's0502m.mul1.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.02.than.html' } ],
      's0502m.mul2.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.03.than.html' } ],
      's0502m.mul3.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.04.than.html' } ],
      's0502m.mul4.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.05.than.html' } ],
      's0502m.mul5.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.06.than.html' } ],
      's0502m.mul6.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.07.than.html' } ],
      's0502m.mul7.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.08.than.html' } ],
      's0502m.mul8.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.09.than.html' } ],
      's0502m.mul9.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.10.than.html' } ],
      's0502m.mul10.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.11.than.html' } ],
      's0502m.mul11.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.12.than.html' } ],
      's0502m.mul12.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.13.than.html' } ],
      's0502m.mul13.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.14.than.html' } ],
      's0502m.mul14.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.15.than.html' } ],
      's0502m.mul15.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.16.than.html' } ],
      's0502m.mul16.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.17.than.html' } ],
      's0502m.mul17.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.18.than.html' } ],
      's0502m.mul18.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.19.than.html' } ],
      's0502m.mul19.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.20.than.html' } ],
      's0502m.mul20.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.21.than.html' } ],
      's0502m.mul21.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.22.than.html' } ],
      's0502m.mul22.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.23.than.html' } ],
      's0502m.mul23.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.24.than.html' } ],
      's0502m.mul24.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.25.than.html' } ],
      's0502m.mul25.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/dhp/dhp.26.than.html' } ],
      's0505m.mul0.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/snp/index.html#vagga-1' } ],
      's0505m.mul1.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/snp/index.html#vagga-2' } ],
      's0505m.mul2.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/snp/index.html#vagga-3' } ],
      's0505m.mul3.xml': [ { 'source': '1', 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/snp/index.html#vagga-4' } ],
      's0505m.mul4.xml': [ { 'source': '1', 'excerpt': true, 'copyrightURL': 'http://www.accesstoinsight.org/faq.html#copyright', 'URL': 'http://www.accesstoinsight.org/tipitaka/kn/snp/index.html#vagga-5' } ]
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
# http://www.accesstoinsight.org/tipitaka/index.html
# http://www.xin-yuan.com/cityzen/jiangtan/AHAN/ahan.htm
# http://www.dhammarain.org.tw/canon/pali-tipitaka-f1/index-pali.htm
canonTextTranslation['en_US'] = {
'Tipiṭaka (Mūla)': 'Pāḷi Canon',
'Vinayapiṭaka': 'The Basket of the Discipline',
'Suttapiṭaka': 'The Basket of Discourses',
  'Dīghanikāya': 'Long Discourses',
  'Dīgha nikāya': 'Long Discourses',
    'Sīlakkhandhavaggapāḷi':'The Division Concerning Morality',
      'Brahmajālasuttaṃ': 'The All-embracing Net of Views',
      'Sāmaññaphalasuttaṃ': 'The Fruits of the Contemplative Life',
#     'Ambaṭṭhasuttaṃ': '',
#     'Soṇadaṇḍasuttaṃ': '',
#     'Kūṭadantasuttaṃ': '',
#     'Mahālisuttaṃ': '',
#     'Jāliyasuttaṃ': '',
#     'Mahāsīhanādasuttaṃ': '',
      'Poṭṭhapādasuttaṃ': 'About Poṭṭhapāda',
#     'Subhasuttaṃ': '',
      'Kevaṭṭasuttaṃ': 'To Kevaṭṭa',
      'Lohiccasuttaṃ': 'To Lohicca',
#     'Tevijjasuttaṃ': '',
    'Mahāvaggapāḷi':'The Large Division',
#     'Mahāpadānasuttaṃ': '',
      'Mahānidānasuttaṃ': 'The Great Causes Discourse',
      'Mahāparinibbānasuttaṃ': 'Last Days of the Buddha/The Great Discourse on the Total Unbinding',
#     'Mahāsudassanasuttaṃ': '',
#     'Janavasabhasuttaṃ': '',
#     'Mahāgovindasuttaṃ': '',
      'Mahāsamayasuttaṃ': 'The Great Assembly/The Great Meeting',
      'Sakkapañhasuttaṃ': "Sakka's Questions",
      'Mahāsatipaṭṭhānasuttaṃ': 'The Great Frames of Reference',
#     'Pāyāsisuttaṃ': '',
    'Pāthikavaggapāḷi':'The Pāthika Division',
#     'Pāthikasuttaṃ': '',
#     'Udumbarikasuttaṃ': '',
      'Cakkavattisuttaṃ': 'The Wheel-turning Emperor',
#     'Aggaññasuttaṃ': '',
#     'Sampasādanīyasuttaṃ': '',
#     'Pāsādikasuttaṃ': '',
#     'Lakkhaṇasuttaṃ': '',
      'Siṅgālasuttaṃ': "The Buddha's Advice to Sigalaka/The Discourse to Sigala",
      'Āṭānāṭiyasuttaṃ': 'Discourse on Āṭānāṭiya',
#     'Saṅgītisuttaṃ': '',
#     'Dasuttarasuttaṃ': '',
  'Majjhimanikāya': 'Middle-length Discourses',
  'Saṃyuttanikāya': 'Grouped" Discourses',
    'Sagāthāvaggapāḷi': 'The Section of Verses',
#     'Devatāsaṃyuttaṃ': '',
#     'Devaputtasaṃyuttaṃ': '',
#     'Kosalasaṃyuttaṃ': '',
#     'Mārasaṃyuttaṃ': '',
#     'Bhikkhunīsaṃyuttaṃ': '',
#     'Brahmasaṃyuttaṃ': '',
#     'Brāhmaṇasaṃyuttaṃ': '',
#     'Vaṅgīsasaṃyuttaṃ': '',
#     'Vanasaṃyuttaṃ': '',
#     'Yakkhasaṃyuttaṃ': '',
#     'Sakkasaṃyuttaṃ': '',
    'Nidānavaggapāḷi': 'The Section on Causation',
#     'Nidānasaṃyuttaṃ': '',
#     'Abhisamayasaṃyuttaṃ': '',
#     'Dhātusaṃyuttaṃ': '',
#     'Anamataggasaṃyuttaṃ': '',
#     'Kassapasaṃyuttaṃ': '',
#     'Lābhasakkārasaṃyuttaṃ': '',
#     'Rāhulasaṃyuttaṃ': '',
#     'Lakkhaṇasaṃyuttaṃ': '',
#     'Opammasaṃyuttaṃ': '',
#     'Bhikkhusaṃyuttaṃ': '',
    'Khandhavaggapāḷi': 'The Section on the Aggregates',
#     'Khandhasaṃyuttaṃ': '',
#     'Rādhasaṃyuttaṃ': '',
#     'Diṭṭhisaṃyuttaṃ': '',
#     'Okkantasaṃyuttaṃ': '',
#     'Uppādasaṃyuttaṃ': '',
#     'Kilesasaṃyuttaṃ': '',
#     'Sāriputtasaṃyuttaṃ': '',
#     'Nāgasaṃyuttaṃ': '',
#     'Supaṇṇasaṃyuttaṃ': '',
#     'Gandhabbakāyasaṃyuttaṃ': '',
#     'Valāhakasaṃyuttaṃ': '',
#     'Vacchagottasaṃyuttaṃ': '',
#     'Jhānasaṃyuttaṃ': '',
    'Saḷāyatanavaggapāḷi': 'The Section on the Six Sense Bases',
#     'Saḷāyatanasaṃyuttaṃ': '六處相應',
#     'Vedanāsaṃyuttaṃ': '受相應',
#     'Mātugāmasaṃyuttaṃ': '女人相應',
#     'Jambukhādakasaṃyuttaṃ': '閻浮車相應',
#     'Sāmaṇḍakasaṃyuttaṃ': '沙門出家相應',
#     'Moggallānasaṃyuttaṃ': '目犍連相應',
#     'Cittasaṃyuttaṃ': '質多相應',
#     'Gāmaṇisaṃyuttaṃ': '聚落主相應',
#     'Asaṅkhatasaṃyuttaṃ': '無為相應',
#     'Abyākatasaṃyuttaṃ': '無記相應',
    'Mahāvaggapāḷi': 'The Great Section',
#     'Maggasaṃyuttaṃ': '道相應',
#     'Bojjhaṅgasaṃyuttaṃ': '覺支相應',
#     'Satipaṭṭhānasaṃyuttaṃ': '念處相應',
#     'Indriyasaṃyuttaṃ': '根相應',
#     'Sammappadhānasaṃyuttaṃ': '正勤相應',
#     'Balasaṃyuttaṃ': '力相應',
#     'Iddhipādasaṃyuttaṃ': '神足相應',
#     'Anuruddhasaṃyuttaṃ': '阿那律相應',
#     'Jhānasaṃyuttaṃ': '靜慮相應',
#     'Ānāpānasaṃyuttaṃ': '入出息相應',
#     'Sotāpattisaṃyuttaṃ': '入流 (須陀洹)相應',
#     'Saccasaṃyuttaṃ': '諦相應',
  'Aṅguttaranikāya': 'Further-factored Discourses',
    'Ekakanipātapāḷi': 'Book of the Ones',
#     'Rūpādivaggo': '色等品',
#     'Nīvaraṇappahānavaggo': '斷蓋品',
#     'Akammaniyavaggo': '無堪忍品',
#     'Adantavaggo': '無調品',
#     'Paṇihitaacchavaggo': '向與隱覆品',
#     'Accharāsaṅghātavaggo': '彈指品',
#     'Vīriyārambhādivaggo': '發精進等品',
#     'Kalyāṇamittādivaggo': '善友等品',
#     'Pamādādivaggo': '放逸等品',
#     'Dutiyapamādādivaggo': '',
#     'Adhammavaggo': '非法等品',
#     'Anāpattivaggo': '無范等品',
#     'Ekapuggalavaggo': '一人品',
#     'Etadaggavaggo': '是第一品',
#     'Aṭṭhānapāḷi': '無有是處品',
#     'Ekadhammapāḷi': '一法品',
#     'Pasādakaradhammavaggo': '種子品',
#     'Aparaaccharāsaṅghātavaggo': '末伽梨品',
#     'Kāyagatāsativaggo': '不放逸品',
#     'Amatavaggo': '靜慮品',
    'Dukanipātapāḷi': 'Book of the Twos',
#     'Kammakaraṇavaggo': '科刑罰品',
#     'Adhikaraṇavaggo': '靜論品',
#     'Bālavaggo': '愚人品',
#     'Samacittavaggo': '等心品',
#     'Parisavaggo': '會眾品',
#     'Puggalavaggo': '人品',
#     'Sukhavaggo': '樂品',
#     'Sanimittavaggo': '有品',
#     'Dhammavaggo': '法品',
#     'Bālavaggo': '愚者品',
#     'Āsāduppajahavaggo': '希望品',
#     'Āyācanavaggo': '希求品',
#     'Dānavaggo': '施品',
#     'Santhāravaggo': '覆護品',
#     'Samāpattivaggo': '入定品',
#     'Kodhapeyyālaṃ': '忿品',
#     'Akusalapeyyālaṃ': '(律廣說)品',
#     'Vinayapeyyālaṃ': '',
#     'Rāgapeyyālaṃ': '',
    'Tikanipātapāḷi': 'Book of the Threes',
#     'Bālavaggo': '愚人品',
#     'Rathakāravaggo': '車匠品',
#     'Puggalavaggo': '補特羅品',
#     'Devadūtavaggo': '天使品',
#     'Cūḷavaggo': '小品',
#     'Brāhmaṇavaggo': '婆羅門品',
#     'Mahāvaggo': '大品',
#     'Ānandavaggo': '阿難品',
#     'Samaṇavaggo': '沙門品',
#     'Loṇakapallavaggo': '掬鹽品',
#     'Sambodhavaggo': '等覺品',
#     'Āpāyikavaggo': '惡趣品',
#     'Kusināravaggo': '古西那拉品',
#     'Yodhājīvavaggo': '戰士品',
#     'Maṅgalavaggo': '吉祥品',
#     'Acelakavaggo': '裸形品',
#     'Kammapathapeyyālaṃ': '',
#     'Rāgapeyyālaṃ': '',
    'Catukkanipātapāḷi': 'Book of the Fours',
    'Pañcakanipātapāḷi': 'Book of the Fives',
    'Chakkanipātapāḷi': 'Book of the Sixes',
    'Sattakanipātapāḷi': 'Book of the Sevens',
    'Aṭṭhakādinipātapāḷi': 'Book of the Eights',
    'Navakanipātapāḷi': 'Book of the Nines',
    'Dasakanipātapāḷi': 'Book of the Tens',
    'Ekādasakanipātapāḷi': 'Book of the Elevens',
#     'Nissayavaggo': '依止品',
#     'Anussativaggo': '憶念品',
#     'Sāmaññavaggo': '沙門品',
#     'Rāgapeyyālaṃ': '貪品',
  'Khuddakanikāya': 'Collection of Short Discourses',
#  'Khuddakanikāya': 'Division of Short Books',
    'Khuddakapāṭhapāḷi': 'The Short Passages',
      'Saraṇattayaṃ': 'Saranagamana — Going for Refuge',
      'Dasasikkhāpadaṃ': 'The Ten Training Rules',
      'Dvattiṃsākāro': 'The 32 Parts',
      'Kumārapañhā': "Samanera Pañha — The Novice's Questions",
      'Maṅgalasuttaṃ': 'Protection',
      'Ratanasuttaṃ': 'Treasures',
      'Tirokuṭṭasuttaṃ': 'Tirokudda Kanda — Hungry Shades Outside the Walls',
      'Nidhikaṇḍasuttaṃ': 'The Reserve Fund',
      'Mettasuttaṃ': 'Karaniya Metta Sutta — Good Will',
    'Dhammapadapāḷi': 'The Path of Dhamma',
      'Yamakavaggo': 'Pairs',
      'Appamādavaggo': 'Heedfulness',
      'Cittavaggo': 'The Mind',
      'Pupphavaggo': 'Blossoms',
      'Bālavaggo': 'Fools',
      'Paṇḍitavaggo': 'The Wise',
      'Arahantavaggo': 'Arahants',
      'Sahassavaggo': 'Thousands',
      'Pāpavaggo': 'Evil',
      'Daṇḍavaggo': 'The Rod',
      'Jarāvaggo': 'Aging',
      'Attavaggo': 'Self',
      'Lokavaggo': 'Worlds',
      'Buddhavaggo': 'Awakened',
      'Sukhavaggo': 'Happy',
      'Piyavaggo': 'Dear Ones',
      'Kodhavaggo': 'Anger',
      'Malavaggo': 'Impurities',
      'Dhammaṭṭhavaggo': 'The Judge',
      'Maggavaggo': 'The Path',
      'Pakiṇṇakavaggo': 'Miscellany',
      'Nirayavaggo': 'Hell',
      'Nāgavaggo': 'Elephants',
      'Taṇhāvaggo': 'Craving',
      'Bhikkhuvaggo': 'Monks',
      'Brāhmaṇavaggo': 'Brahmans',
    'Udānapāḷi': 'Exclamations',
    'Itivuttakapāḷi': 'The Thus-saids',
    'Suttanipātapāḷi': 'The Discourses Collection',
      'Uragavaggo': 'The Snake Chapter',
      'Cūḷavaggo': 'The Lesser Chapter',
      'Mahāvaggo': 'The Great Chapter',
      'Aṭṭhakavaggo': 'The Octet Chapter',
      'Pārāyanavaggo': 'The Chapter on the Way to the Far Shore',
    'Vimānavatthupāḷi': 'Stories of the Celestial Mansions',
    'Petavatthupāḷi': 'Stories of the Hungry Ghosts',
    'Theragāthāpāḷi': 'Verses of the Elder Monks',
    'Therīgāthāpāḷi': 'Verses of the Elder Nuns',
    'Apadānapāḷi': 'Stories',
    'Buddhavaṃsapāḷi': 'History of the Buddhas',
    'Cariyāpiṭakapāḷi': 'Basket of Conduct',
    'Jātakapāḷi': 'Birth Stories',
#   'Mahāniddesapāḷi': '大義釋',
#   'Cūḷaniddesapāḷi': '小義釋',
    'Paṭisambhidāmaggapāḷi': 'Path of Discrimination',
#   'Nettippakaraṇapāḷi': '導論',
    'Milindapañhapāḷi': 'Questions of Milinda',
#   'Peṭakopadesapāḷi': '藏釋 (三藏知津)',
#'Abhidhammapiṭaka': '',
  'Dhammasaṅgaṇīpāḷi': 'Enumeration of Phenomena',
  'Vibhaṅgapāḷi': 'The Book of Analysis',
# 'Vibhaṅgapāḷi': 'The Book of Treatises',
  'Dhātukathāpāḷi': 'Discourse on Elements',
# 'Dhātukathāpāḷi': 'Discussion with Reference to the Elements',
  'Puggalapaññattipāḷi': 'A Designation of Human Types',
# 'Puggalapaññattipāḷi': 'Description of Individuals',
  'Kathāvatthupāḷi': 'Points of Controversy',
  'Yamakapāḷi': 'The Book of Pairs',
  'Paṭṭhānapāḷi': 'The Book of Relations',
'Aṭṭhakathā': 'Commentaries',
'Tīkā': 'Sub-commentaries',
  'Abhidhammatthasaṅgaho': 'A Comprehensive Manual of Abhidhamma',
  'Visuddhimagga': 'The Path of Purification',
      'Sīlaniddeso': 'DESCRIPTION OF VIRTUE',
      'Dhutaṅganiddeso': 'THE ASCETIC PRACTICES',
      'Kammaṭṭhānaggahaṇaniddeso': 'TAKING A MEDITATION SUBJECT',
      'Pathavīkasiṇaniddeso': 'THE EARTH KASIṆA',
      'Sesakasiṇaniddeso': 'THE REMAINING KASIṆAS',
      'Asubhakammaṭṭhānaniddeso': 'FOULNESS AS A MEDITATION SUBJECT',
      'Chaanussatiniddeso': 'SIX RECOLLECTIONS',
      'Anussatikammaṭṭhānaniddeso': 'OTHER RECOLLECTIONS AS MEDITATION SUBJECTS',
      'Brahmavihāraniddeso': 'THE DIVINE ABIDINGS',
      'Āruppaniddeso': 'THE IMMATERIAL STATES',
      'Samādhiniddeso': 'CONCENTRATION—CONCLUSION: NUTRIMENT AND THE ELEMENTS',
      'Iddhividhaniddeso': 'THE SUPERNORMAL POWERS',
      'Abhiññāniddeso': 'OTHER DIRECT-KNOWLEDGES',
      'Khandhaniddeso': 'THE AGGREGATES',
      'Āyatanadhātuniddeso': 'THE BASES AND ELEMENTS',
      'Indriyasaccaniddeso': 'THE FACULTIES AND TRUTHS',
      'Paññābhūminiddeso': 'THE SOIL OF UNDERSTANDING—CONCLUSION: DEPENDENT ORIGINATION',
      'Diṭṭhivisuddhiniddeso': 'PURIFICATION OF VIEW',
      'Kaṅkhāvitaraṇavisuddhiniddeso': 'PURIFICATION BY OVERCOMING DOUBT',
      'Maggāmaggañāṇadassanavisuddhiniddeso': 'PURIFICATION BY KNOWLEDGE AND VISION OF WHAT IS THE PATH AND WHAT IS NOT THE PATH',
      'Paṭipadāñāṇadassanavisuddhiniddeso': 'PURIFICATION BY KNOWLEDGE AND VISION OF THE WAY',
      'Ñāṇadassanavisuddhiniddeso': 'PURIFICATION BY KNOWLEDGE AND VISION',
      'Paññābhāvanānisaṃsaniddeso': 'THE BENEFITS IN DEVELOPING UNDERSTANDING',
' ': ' '
}

# http://www.therawikipedia.org/wiki/%E5%A2%9E%E6%94%AF%E9%83%A8
# http://yifertw.blogspot.tw/2008/04/9-2008421.html
canonTextTranslation['zh_TW'] = {
'Tipiṭaka (Mūla)': '巴利三藏',
'Vinayapiṭaka': '律藏',
  'Pārājikapāḷi': '波羅夷品',
#   'Verañjakaṇḍaṃ': '',
    'Pārājikakaṇḍaṃ': '波羅夷 (他勝,斷頭)章',
    'Saṅghādisesakaṇḍaṃ': '僧殘 (僧伽胝施沙)章',
    'Aniyatakaṇḍaṃ': '不定章',
    'Nissaggiyakaṇḍaṃ': '捨墮 (尼薩耆波逸提)章',
  'Pācittiyapāḷi': '波逸提品',
    'Pācittiyakaṇḍaṃ': '波逸提 (單墮)章',
    'Pāṭidesanīyakaṇḍaṃ': '悔過 (波胝提舍尼)章',
    'Sekhiyakaṇḍaṃ': '眾學章',
    'Adhikaraṇasamathā': '滅諍',
    'bhikkhunīvibhaṅgo': '比丘尼分別',
  'Mahāvaggapāḷi': '大品',
    'Mahākhandhako': '大篇 (大犍度)',
    'Uposathakkhandhako': '伍波薩他篇 (布薩犍度)',
    'Vassūpanāyikakkhandhako': '入雨安居篇 (入雨安居犍度)',
    'Pavāraṇākkhandhako': '自恣篇 (自恣犍度)',
    'Cammakkhandhako': '皮革篇 (皮革犍度)',
    'Bhesajjakkhandhako': '藥篇 (藥犍度)',
    'Kathinakkhandhako': '咖提那篇 (迦絺那衣犍度)',
    'Cīvarakkhandhako': '衣篇 (衣犍度)',
    'Campeyyakkhandhako': '瞻巴篇 (瞻波犍度)',
    'Kosambakakkhandhako': '高賞比篇 (拘晱彌犍度)',
  'Cūḷavaggapāḷi': '小品',
    'Kammakkhandhakaṃ': '甘馬篇 (羯摩犍度)',
    'Pārivāsikakkhandhakaṃ': '別住篇 (別住犍度)',
    'Samuccayakkhandhakaṃ': '集篇 (集犍度)',
    'Samathakkhandhakaṃ': '止篇 (滅諍犍度)',
    'Khuddakavatthukkhandhakaṃ': '小事篇 (小犍度)',
    'Senāsanakkhandhakaṃ': '坐卧處篇 (臥坐具犍度)',
    'Saṅghabhedakakkhandhakaṃ': '破僧篇 (破僧犍度)',
    'Vattakkhandhakaṃ': '行儀篇 (儀法犍度)',
    'Pātimokkhaṭṭhapanakkhandhakaṃ': '遮誦戒篇 (遮說戒犍度)',
    'Bhikkhunikkhandhakaṃ': '比庫尼篇 (比丘尼犍度)',
    'Pañcasatikakkhandhakaṃ': '五百篇 (五百結集犍度)',
    'Sattasatikakkhandhakaṃ': '七百篇 (七百結集犍度)',
  'Parivārapāḷi': '附隨',
#   'Soḷasamahāvāro': '',
    'Samuṭṭhānasīsasaṅkhepo': '等起攝頌 (等起)',
    'Antarapeyyālaṃ': '無間省略',
    'Khandhakapucchāvāro': '問犍度章',
    'Ekuttarikanayo': '增一法',
    'Uposathādipucchāvissajjanā': '伍波薩他初解答章 (布薩初解答以及制戒義利論)',
    'Gāthāsaṅgaṇikaṃ': '伽陀集',
    'Adhikaraṇabhedo': '諍事分解',
    'Aparagāthāsaṅgaṇikaṃ': '別伽陀集',
    'Codanākaṇḍaṃ': '呵責品',
    'Cūḷasaṅgāmo': '小諍',
    'Mahāsaṅgāmo': '大諍',
    'Kathinabhedo': '咖提那衣分解 (迦絺那衣分解)',
    'Upālipañcakaṃ': '伍巴離五法 (優婆離五法)',
    'Atthāpattisamuṭṭhānaṃ': '等起',
    'Dutiyagāthāsaṅgaṇikaṃ': '第二伽陀集',
    'Sedamocanagāthā': '發汗偈',
    'Pañcavaggo': '五品',
'Suttapiṭaka': '經藏',
  'Dīghanikāya': '長部',
  'Dīgha nikāya': '長部',
    'Sīlakkhandhavaggapāḷi':'戒蘊品',
      'Brahmajālasuttaṃ': '梵網經',
      'Sāmaññaphalasuttaṃ': '沙門果經',
      'Ambaṭṭhasuttaṃ': '阿摩晝經',
      'Soṇadaṇḍasuttaṃ': '種德經',
      'Kūṭadantasuttaṃ': '究羅檀頭經',
      'Mahālisuttaṃ': '摩訶梨經',
      'Jāliyasuttaṃ': '闍利經',
      'Mahāsīhanādasuttaṃ': '迦葉獅子吼經',
      'Poṭṭhapādasuttaṃ': '布吒婆樓經',
      'Subhasuttaṃ': '須婆經',
      'Kevaṭṭasuttaṃ': '堅固經',
      'Lohiccasuttaṃ': '露遮經',
      'Tevijjasuttaṃ': '三明經',
    'Mahāvaggapāḷi':'大品',
      'Mahāpadānasuttaṃ': '大本經',
      'Mahānidānasuttaṃ': '大緣經',
      'Mahāparinibbānasuttaṃ': '大般涅槃經',
      'Mahāsudassanasuttaṃ': '大善見王經',
      'Janavasabhasuttaṃ': '闍尼沙經',
      'Mahāgovindasuttaṃ': '大典尊經',
      'Mahāsamayasuttaṃ': '大會經',
      'Sakkapañhasuttaṃ': '帝釋所問經',
      'Mahāsatipaṭṭhānasuttaṃ': '大念處經',
      'Pāyāsisuttaṃ': '弊宿經',
    'Pāthikavaggapāḷi':'波梨品',
      'Pāthikasuttaṃ': '波梨經',
      'Udumbarikasuttaṃ': '優曇婆邏獅子吼經',
      'Cakkavattisuttaṃ': '轉輪聖王獅子吼經',
      'Aggaññasuttaṃ': '起世因本經',
      'Sampasādanīyasuttaṃ': '自歡喜經',
      'Pāsādikasuttaṃ': '清淨經',
      'Lakkhaṇasuttaṃ': '三十二相經',
      'Siṅgālasuttaṃ': '教授屍迦羅越經',
      'Āṭānāṭiyasuttaṃ': '阿吒曩胝經',
      'Saṅgītisuttaṃ': '等誦經',
      'Dasuttarasuttaṃ': '十上經',
  'Majjhimanikāya': '中部',
    'Mūlapaṇṇāsapāḷi': '根本五十經編',
      'Mūlapariyāyavaggo': '根本法門品',
      'Sīhanādavaggo': '師子吼品',
      'Opammavaggo': '譬喻品',
      'Mahāyamakavaggo': '大雙品',
      'Cūḷayamakavaggo': '小雙品',
    'Majjhimapaṇṇāsapāḷi': '中分五十經編',
      'Gahapativaggo': '居士品',
      'Bhikkhuvaggo': '比丘品',
      'Paribbājakavaggo': '遊行者品',
      'Rājavaggo': '王品',
      'Brāhmaṇavaggo': '婆羅門品',
    'Uparipaṇṇāsapāḷi': '後分五十經編',
      'Devadahavaggo': '天臂品',
      'Anupadavaggo': '緊隨品',
      'Suññatavaggo': '空品',
      'Vibhaṅgavaggo': '分別品',
      'Saḷāyatanavaggo': '六處品',
  'Saṃyuttanikāya': '相應部',
    'Sagāthāvaggapāḷi': '有偈篇',
      'Devatāsaṃyuttaṃ': '諸天相應',
      'Devaputtasaṃyuttaṃ': '天子相應',
      'Kosalasaṃyuttaṃ': '憍薩羅相應',
      'Mārasaṃyuttaṃ': '魔羅相應',
      'Bhikkhunīsaṃyuttaṃ': '比丘尼相應',
      'Brahmasaṃyuttaṃ': '梵天相應',
      'Brāhmaṇasaṃyuttaṃ': '婆羅門相應',
      'Vaṅgīsasaṃyuttaṃ': '婆耆沙長老相應',
      'Vanasaṃyuttaṃ': '森林相應',
      'Yakkhasaṃyuttaṃ': '夜叉相應',
      'Sakkasaṃyuttaṃ': '帝釋天帝相應',
    'Nidānavaggapāḷi': '因緣篇',
      'Nidānasaṃyuttaṃ': '因緣相應',
      'Abhisamayasaṃyuttaṃ': '現觀相應',
      'Dhātusaṃyuttaṃ': '界相應',
      'Anamataggasaṃyuttaṃ': '無始相應',
      'Kassapasaṃyuttaṃ': '迦葉相應',
      'Lābhasakkārasaṃyuttaṃ': '利得與供養相應',
      'Rāhulasaṃyuttaṃ': '羅睺羅相應',
      'Lakkhaṇasaṃyuttaṃ': '勒叉那相應',
      'Opammasaṃyuttaṃ': '譬喻相應',
      'Bhikkhusaṃyuttaṃ': '比丘相應',
    'Khandhavaggapāḷi': '蘊篇',
      'Khandhasaṃyuttaṃ': '蘊相應',
      'Rādhasaṃyuttaṃ': '羅陀相應',
      'Diṭṭhisaṃyuttaṃ': '見相應',
      'Okkantasaṃyuttaṃ': '入相應',
      'Uppādasaṃyuttaṃ': '生相應',
      'Kilesasaṃyuttaṃ': '煩惱相應',
      'Sāriputtasaṃyuttaṃ': '舍利弗相應',
      'Nāgasaṃyuttaṃ': '龍相應',
      'Supaṇṇasaṃyuttaṃ': '金翅鳥相應',
      'Gandhabbakāyasaṃyuttaṃ': '乾闥婆相應',
      'Valāhakasaṃyuttaṃ': '雲相應',
      'Vacchagottasaṃyuttaṃ': '婆磋種相應',
      'Jhānasaṃyuttaṃ': '禪定相應',
    'Saḷāyatanavaggapāḷi': '六處篇',
      'Saḷāyatanasaṃyuttaṃ': '六處相應',
      'Vedanāsaṃyuttaṃ': '受相應',
      'Mātugāmasaṃyuttaṃ': '女人相應',
      'Jambukhādakasaṃyuttaṃ': '閻浮車相應',
      'Sāmaṇḍakasaṃyuttaṃ': '沙門出家相應',
      'Moggallānasaṃyuttaṃ': '目犍連相應',
      'Cittasaṃyuttaṃ': '質多相應',
      'Gāmaṇisaṃyuttaṃ': '聚落主相應',
      'Asaṅkhatasaṃyuttaṃ': '無為相應',
      'Abyākatasaṃyuttaṃ': '無記相應',
#   'Mahāvaggapāḷi': '大篇',
      'Maggasaṃyuttaṃ': '道相應',
      'Bojjhaṅgasaṃyuttaṃ': '覺支相應',
      'Satipaṭṭhānasaṃyuttaṃ': '念處相應',
      'Indriyasaṃyuttaṃ': '根相應',
      'Sammappadhānasaṃyuttaṃ': '正勤相應',
      'Balasaṃyuttaṃ': '力相應',
      'Iddhipādasaṃyuttaṃ': '神足相應',
      'Anuruddhasaṃyuttaṃ': '阿那律相應',
#     'Jhānasaṃyuttaṃ': '靜慮相應',
      'Ānāpānasaṃyuttaṃ': '入出息相應',
      'Sotāpattisaṃyuttaṃ': '入流 (須陀洹)相應',
      'Saccasaṃyuttaṃ': '諦相應',
  'Aṅguttaranikāya': '增支部',
    'Ekakanipātapāḷi': '一集',
      'Rūpādivaggo': '色等品',
      'Nīvaraṇappahānavaggo': '斷蓋品',
      'Akammaniyavaggo': '無堪忍品',
      'Adantavaggo': '無調品',
      'Paṇihitaacchavaggo': '向與隱覆品',
      'Accharāsaṅghātavaggo': '彈指品',
      'Vīriyārambhādivaggo': '發精進等品',
      'Kalyāṇamittādivaggo': '善友等品',
      'Pamādādivaggo': '放逸等品',
#     'Dutiyapamādādivaggo': '',
      'Adhammavaggo': '非法等品',
      'Anāpattivaggo': '無范等品',
      'Ekapuggalavaggo': '一人品',
      'Etadaggavaggo': '是第一品',
      'Aṭṭhānapāḷi': '無有是處品',
      'Ekadhammapāḷi': '一法品',
      'Pasādakaradhammavaggo': '種子品',
      'Aparaaccharāsaṅghātavaggo': '末伽梨品',
      'Kāyagatāsativaggo': '不放逸品',
      'Amatavaggo': '靜慮品',
    'Dukanipātapāḷi': '二集',
      'Kammakaraṇavaggo': '科刑罰品',
      'Adhikaraṇavaggo': '靜論品',
      'Bālavaggo': '愚人品',
      'Samacittavaggo': '等心品',
      'Parisavaggo': '會眾品',
      'Puggalavaggo': '人品',
      'Sukhavaggo': '樂品',
      'Sanimittavaggo': '有品',
      'Dhammavaggo': '法品',
#     'Bālavaggo': '愚者品',
      'Āsāduppajahavaggo': '希望品',
      'Āyācanavaggo': '希求品',
      'Dānavaggo': '施品',
      'Santhāravaggo': '覆護品',
      'Samāpattivaggo': '入定品',
      'Kodhapeyyālaṃ': '忿品',
      'Akusalapeyyālaṃ': '(律廣說)品',
#     'Vinayapeyyālaṃ': '',
#     'Rāgapeyyālaṃ': '',
    'Tikanipātapāḷi': '三集',
#     'Bālavaggo': '愚人品',
      'Rathakāravaggo': '車匠品',
#     'Puggalavaggo': '補特羅品',
      'Devadūtavaggo': '天使品',
#     'Cūḷavaggo': '小品',
#     'Brāhmaṇavaggo': '婆羅門品',
#     'Mahāvaggo': '大品',
      'Ānandavaggo': '阿難品',
      'Samaṇavaggo': '沙門品',
      'Loṇakapallavaggo': '掬鹽品',
      'Sambodhavaggo': '等覺品',
      'Āpāyikavaggo': '惡趣品',
      'Kusināravaggo': '古西那拉品',
      'Yodhājīvavaggo': '戰士品',
      'Maṅgalavaggo': '吉祥品',
      'Acelakavaggo': '裸形品',
#     'Kammapathapeyyālaṃ': '',
#     'Rāgapeyyālaṃ': '',
    'Catukkanipātapāḷi': '四集',
    'Pañcakanipātapāḷi': '五集',
    'Chakkanipātapāḷi': '六集',
    'Sattakanipātapāḷi': '七集',
    'Aṭṭhakādinipātapāḷi': '八集',
    'Navakanipātapāḷi': '九集',
    'Dasakanipātapāḷi': '十集',
    'Ekādasakanipātapāḷi': '十一集',
      'Nissayavaggo': '依止品',
      'Anussativaggo': '憶念品',
      'Sāmaññavaggo': '沙門品',
      'Rāgapeyyālaṃ': '貪品',
  'Khuddakanikāya': '小部',
    'Khuddakapāṭhapāḷi': '小誦',
      'Saraṇattayaṃ': '三皈依',
      'Dasasikkhāpadaṃ': '十戒',
      'Dvattiṃsākāro': '三十二身分',
      'Kumārapañhā': '問童子',
      'Maṅgalasuttaṃ': '吉祥經',
      'Ratanasuttaṃ': '寶經',
      'Tirokuṭṭasuttaṃ': '戶外經',
      'Nidhikaṇḍasuttaṃ': '伏藏經',
      'Mettasuttaṃ': '慈經',
    'Dhammapadapāḷi': '法句(經)',
      'Yamakavaggo': '雙品',
      'Appamādavaggo': '不放逸品',
      'Cittavaggo': '心品',
      'Pupphavaggo': '華(花)品',
#     'Bālavaggo': '愚品',
      'Paṇḍitavaggo': '智者品',
      'Arahantavaggo': '阿羅漢品',
      'Sahassavaggo': '千品',
      'Pāpavaggo': '惡品',
      'Daṇḍavaggo': '刀杖品',
      'Jarāvaggo': '老品',
      'Attavaggo': '自己品',
      'Lokavaggo': '世品',
      'Buddhavaggo': '佛陀品',
#     'Sukhavaggo': '樂品',
      'Piyavaggo': '喜愛品',
      'Kodhavaggo': '忿怒品',
      'Malavaggo': '垢穢品',
      'Dhammaṭṭhavaggo': '法住品',
      'Maggavaggo': '道品',
      'Pakiṇṇakavaggo': '雜品',
      'Nirayavaggo': '地獄品',
      'Nāgavaggo': '象品',
      'Taṇhāvaggo': '愛欲品',
#     'Bhikkhuvaggo': '比丘品',
#     'Brāhmaṇavaggo': '婆羅門品',
    'Udānapāḷi': '自說',
    'Itivuttakapāḷi': '如是語',
    'Suttanipātapāḷi': '經集',
      'Uragavaggo': '蛇品',
      'Cūḷavaggo': '小品',
      'Mahāvaggo': '大品',
      'Aṭṭhakavaggo': '八頌經品',
      'Pārāyanavaggo': '彼岸道品',
    'Vimānavatthupāḷi': '天宮事',
    'Petavatthupāḷi': '餓鬼事',
    'Theragāthāpāḷi': '長老偈',
    'Therīgāthāpāḷi': '長老尼偈',
    'Apadānapāḷi': '譬喻',
    'Buddhavaṃsapāḷi': '佛種姓 (諸佛史)',
    'Cariyāpiṭakapāḷi': '所行藏',
    'Jātakapāḷi': '本生(經)',
    'Mahāniddesapāḷi': '大義釋',
    'Cūḷaniddesapāḷi': '小義釋',
    'Paṭisambhidāmaggapāḷi': '無礙解道',
    'Nettippakaraṇapāḷi': '導論',
    'Milindapañhapāḷi': '彌林達問經 (彌林達王問經,那先比丘經)',
    'Peṭakopadesapāḷi': '藏釋 (三藏知津)',
'Abhidhammapiṭaka': '論藏 (阿毘達摩)',
  'Dhammasaṅgaṇīpāḷi': '法集論',
  'Vibhaṅgapāḷi': '分別論',
  'Dhātukathāpāḷi': '界說論',
  'Puggalapaññattipāḷi': '人施設論',
  'Kathāvatthupāḷi': '論事',
  'Yamakapāḷi': '雙對論',
  'Paṭṭhānapāḷi': '發趣論',
'Aṭṭhakathā': '義疏(註釋書)',
'Tīkā': '復註(義疏再解釋)',
  'Abhidhammatthasaṅgaho': '攝阿毘達摩義論',
    'Cittaparicchedo': '第一攝心分別品',
    'Cetasikaparicchedo': '第二攝心所分別品',
    'Pakiṇṇakaparicchedo': '第三攝雜分別品',
    'Vīthiparicchedo': '第四攝路分別品',
    'Vīthimuttaparicchedo': '第五攝離路分別品',
    'Rūpaparicchedo': '第六攝色分別品',
    'Samuccayaparicchedo': '第七攝集分別品',
    'Paccayaparicchedo': '第八攝緣分別品',
    'Kammaṭṭhānaparicchedo': '第九攝業處分別品',
'Anya': '藏外文獻',
  'Visuddhimagga': '清淨道論',
      'Sīlaniddeso': '說戒品',
      'Dhutaṅganiddeso': '說頭陀支品',
      'Kammaṭṭhānaggahaṇaniddeso': '說取業處品',
      'Pathavīkasiṇaniddeso': '說地遍品',
      'Sesakasiṇaniddeso': '說餘遍品',
      'Asubhakammaṭṭhānaniddeso': '說不淨業處品',
      'Chaanussatiniddeso': '說六隨念品',
      'Anussatikammaṭṭhānaniddeso': '說隨念業處品',
      'Brahmavihāraniddeso': '說梵住品',
      'Āruppaniddeso': '說無色品',
      'Samādhiniddeso': '說定品',
      'Iddhividhaniddeso': '說神變品',
      'Abhiññāniddeso': '說神通品',
      'Khandhaniddeso': '說蘊品',
      'Āyatanadhātuniddeso': '說處界品',
      'Indriyasaccaniddeso': '說根諦品',
      'Paññābhūminiddeso': '說慧地品',
      'Diṭṭhivisuddhiniddeso': '說見清淨品',
      'Kaṅkhāvitaraṇavisuddhiniddeso': '說度疑清淨品',
      'Maggāmaggañāṇadassanavisuddhiniddeso': '說道非道智見清淨品',
      'Paṭipadāñāṇadassanavisuddhiniddeso': '說行道智見清淨品',
      'Ñāṇadassanavisuddhiniddeso': '說智見清淨品',
      'Paññābhāvanānisaṃsaniddeso': '說修慧的功德品',
    'Visuddhimagga-mahāṭīkā': '清淨道論大疏',
    'Visuddhimagga nidānakathā': '清淨道論因緣論',
    'Saṅgāyana-puccha vissajjanā': '結集問答',
      'Dīghanikāya (pu-vi)': '長部結集問答',
      'Majjhimanikāya (pu-vi)': '中部結集問答',
      'Saṃyuttanikāya (pu-vi)': '相應部結集問答',
      'Aṅguttaranikāya (pu-vi)': '增支部結集問答',
      'Vinayapiṭaka (pu-vi)': '律藏結集問答',
      'Abhidhammapiṭaka (pu-vi)': '阿毘達摩藏之結集問答',
      'Aṭṭhakathā (pu-vi)': '注釋之結集問答',
' ': ' '
}

# http://www.paliviet.info/VHoc/VHoc_Web.htm

canonTextTranslation['vi_VN'] = {
'Tipiṭaka (Mūla)': 'Tam Tạng',
'Vinayapiṭaka': 'Tạng Luật',
'Suttapiṭaka': 'Tạng Kinh',
 'Dīghanikāya': 'Trường Bộ',
 'Dīgha nikāya': 'Trường Bộ',
   'Sīlakkhandhavaggapāḷi':'Phẩm Giới Uẩn',
     'Brahmajālasuttaṃ': 'Kinh Phạm Võng',
     'Sāmaññaphalasuttaṃ': 'Kinh Sa-môn Quả',
     'Ambaṭṭhasuttaṃ': 'Kinh Ambaṭṭha',

     'Soṇadaṇḍasuttaṃ': 'Kinh Chủng Đức',

     'Kūṭadantasuttaṃ': 'Kinh Kūṭadanta',

     'Mahālisuttaṃ': 'Kinh Mahāli',

     'Jāliyasuttaṃ': 'Kinh Jāliya',

     'Mahāsīhanādasuttaṃ': 'Kinh Đại Sư Tử Hống',

     'Poṭṭhapādasuttaṃ': 'Kinh Poṭṭhapāda',

     'Subhasuttaṃ': 'Kinh Subha',

     'Kevaṭṭasuttaṃ': 'Kinh Kevaṭṭa',

     'Lohiccasuttaṃ': 'Kinh Lohicca',

     'Tevijjasuttaṃ': 'Kinh Tam Minh',

   'Mahāvaggapāḷi':'Đại Phẩm',

     'Mahāpadānasuttaṃ': 'Kinh Mahāpadāna',

     'Mahānidānasuttaṃ': 'Kinh Đại Duyên',

     'Mahāparinibbānasuttaṃ': 'Kinh Đại Bát-niết-bàn',

     'Mahāsudassanasuttaṃ': 'Kinh Mahāsudassana',

     'Janavasabhasuttaṃ': 'Kinh Janavasabha',

     'Mahāgovindasuttaṃ': 'Kinh Mahāgovinda',

     'Mahāsamayasuttaṃ': 'Kinh Ðại hội',

     'Sakkapañhasuttaṃ': 'Kinh Ðế-thích hỏi đạo',

     'Mahāsatipaṭṭhānasuttaṃ': 'Kinh Ðại niệm xứ',

     'Pāyāsisuttaṃ': 'Kinh Pāyāsi',

   'Pāthikavaggapāḷi':'Phẩm Pāthika',

     'Pāthikasuttaṃ': 'Kinh Pāthika',

     'Udumbarikasuttaṃ': 'Kinh Udumbarika',

     'Cakkavattisuttaṃ': 'Kinh Chuyển luân thánh vương',

     'Aggaññasuttaṃ': 'Kinh Khởi thế nhân bổn',

     'Sampasādanīyasuttaṃ': 'Kinh Tự hoan hỷ',

     'Pāsādikasuttaṃ': 'Kinh Thanh tịnh',

     'Lakkhaṇasuttaṃ': 'Kinh Tướng',

     'Siṅgālasuttaṃ': "Kinh giảng cho Siṅgāla",

     'Āṭānāṭiyasuttaṃ': 'Kinh Āṭānāṭiya',

     'Saṅgītisuttaṃ': 'Kinh Phúng tụng',

     'Dasuttarasuttaṃ': 'Kinh Thập thượng',

 'Majjhimanikāya': 'Trung Bộ',

   'Mūlapaṇṇāsapāḷi': 'Nhóm Năm mươi Căn bản',

     'Mūlapariyāyavaggo': 'Phẩm Pháp môn căn bản',

     'Sīhanādavaggo': 'Phẩm Tiếng rống sư tử',

     'Opammavaggo': 'Phẩm So sánh',

     'Mahāyamakavaggo': 'Đại phẩm Song đôi',

     'Cūḷayamakavaggo': 'Tiểu phẩm Song đôi',

   'Majjhimapaṇṇāsapāḷi': 'Nhóm Năm mươi Trung cấp',

     'Gahapativaggo': 'Phẩm Gia Chủ',

     'Bhikkhuvaggo': 'Phẩm Tỳ-khưu',

     'Paribbājakavaggo': 'Phẩm Du sĩ',

     'Rājavaggo': 'Phẩm Vua',

     'Brāhmaṇavaggo': 'Phẩm Phạm Thiên',

   'Uparipaṇṇāsapāḷi': 'Nhóm Năm mươi Cao cấp',

     'Devadahavaggo': 'Phẩm Thị trấn Devadaha',

     'Anupadavaggo': 'Phẩm Bất Đoạn',

     'Suññatavaggo': 'Phẩm Không tánh',

     'Vibhaṅgavaggo': 'Phẩm Phân biệt',

     'Saḷāyatanavaggo': 'Phẩm Sáu xứ',

 'Saṃyuttanikāya': 'Tương Ưng Bộ',

   'Sagāthāvaggapāḷi': 'Thiên Có Kệ',

     'Devatāsaṃyuttaṃ': 'Tương Ưng Chư Thiên',

     'Devaputtasaṃyuttaṃ': 'Tương Ưng Thiên Tử',

     'Kosalasaṃyuttaṃ': 'Tương Ưng Kosala',

     'Mārasaṃyuttaṃ': 'Tương Ưng Ác Ma',

     'Bhikkhunīsaṃyuttaṃ': 'Tương Ưng Tỳ-khưu-ni',

     'Brahmasaṃyuttaṃ': 'Tương Ưng Phạm Thiên',

     'Brāhmaṇasaṃyuttaṃ': 'Tương Ưng Bà-la-môn',

     'Vaṅgīsasaṃyuttaṃ': 'Tương Ưng Trưởng Lão Vaṅgīsa',

     'Vanasaṃyuttaṃ': 'Tương Ưng Rừng',

     'Yakkhasaṃyuttaṃ': 'Tương Ưng Dạ-xoa',

     'Sakkasaṃyuttaṃ': 'Tương Ưng Đế-thích',

   'Nidānavaggapāḷi': 'Thiên Nhân Duyên',

     'Nidānasaṃyuttaṃ': 'Tương Ưng Nhân Duyên',

     'Abhisamayasaṃyuttaṃ': 'Tương Ưng Minh Kiến',

     'Dhātusaṃyuttaṃ': 'Tương Ưng Giới',

     'Anamataggasaṃyuttaṃ': 'Tương Ưng Vô Thỉ',

     'Kassapasaṃyuttaṃ': 'Tương Ưng Kassapa',

     'Lābhasakkārasaṃyuttaṃ': 'Tương Ưng Lợi Ích Ðắc Cung Kính',

     'Rāhulasaṃyuttaṃ': 'Tương Ưng Rahula',

     'Lakkhaṇasaṃyuttaṃ': 'Tương Ưng Lakkhana',

     'Opammasaṃyuttaṃ': 'Tương Ưng Thí Dụ',

     'Bhikkhusaṃyuttaṃ': 'Tương Ưng Tỳ-khưu',

   'Khandhavaggapāḷi': 'Thiên Uẩn',

     'Khandhasaṃyuttaṃ': 'Tương Ưng Uẩn',

     'Rādhasaṃyuttaṃ': 'Tương Ưng Rādha',

     'Diṭṭhisaṃyuttaṃ': 'Tương Ưng Kiến',

     'Okkantasaṃyuttaṃ': 'Tương Ưng Nhập',

     'Uppādasaṃyuttaṃ': 'Tương Ưng Sanh',

     'Kilesasaṃyuttaṃ': 'Tương Ưng Phiền Não',

     'Sāriputtasaṃyuttaṃ': 'Tương Ưng Sāriputta',

     'Nāgasaṃyuttaṃ': 'Tương Ưng Loài Rồng',

     'Supaṇṇasaṃyuttaṃ': 'Tương Ưng Kim Xí Ðiểu',

     'Gandhabbakāyasaṃyuttaṃ': 'Tương Ưng Càn-thát-bà',

     'Valāhakasaṃyuttaṃ': 'Tương Ưng Thần Mây',

     'Vacchagottasaṃyuttaṃ': 'Tương Ưng Vacchagotta',

     'Jhānasaṃyuttaṃ': 'Tương Ưng Thiền',

   'Saḷāyatanavaggapāḷi': 'Thiên Sáu Xứ',

     'Saḷāyatanasaṃyuttaṃ': 'Tương Ưng Sáu Xứ',

     'Vedanāsaṃyuttaṃ': 'Tương Ưng Thọ',

     'Mātugāmasaṃyuttaṃ': 'Tương Ưng Nữ Nhân',

     'Jambukhādakasaṃyuttaṃ': 'Tương Ưng Jambukhādaka',

     'Sāmaṇḍakasaṃyuttaṃ': 'Tương Ưng Sāmaṇḍaka',

     'Moggallānasaṃyuttaṃ': 'Tương Ưng Moggallāna',

     'Cittasaṃyuttaṃ': 'Tương Ưng Tâm',

     'Gāmaṇisaṃyuttaṃ': 'Tương Ưng Thôn Trưởng',

     'Asaṅkhatasaṃyuttaṃ': 'Tương Ưng Vô Vi',

     'Abyākatasaṃyuttaṃ': 'Tương Ưng Không Thuyết',

   'Mahāvaggapāḷi': 'Thiên Ðại Phẩm',

     'Maggasaṃyuttaṃ': 'Tương Ưng Ðạo',

     'Bojjhaṅgasaṃyuttaṃ': 'Tương Ưng Giác Chi',

     'Satipaṭṭhānasaṃyuttaṃ': 'Tương Ưng Niệm Xứ',

     'Indriyasaṃyuttaṃ': 'Tương Ưng Căn',

     'Sammappadhānasaṃyuttaṃ': 'Tương Ưng Chánh Cần',

     'Balasaṃyuttaṃ': 'Tương Ưng Lực',

     'Iddhipādasaṃyuttaṃ': 'Tương Ưng Như Ý Túc',

     'Anuruddhasaṃyuttaṃ': 'Tương Ưng Anuruddha',

     'Jhānasaṃyuttaṃ': 'Tương Ưng Thiền',

     'Ānāpānasaṃyuttaṃ': 'Tương Ưng Hơi Thở Vô, Hơi Thở Ra',

     'Sotāpattisaṃyuttaṃ': 'Tương Ưng Dự Lưu',

     'Saccasaṃyuttaṃ': 'Tương Ưng Sự Thật',

 'Aṅguttaranikāya': 'Tăng Chi Bộ',

   'Ekakanipātapāḷi': 'Chương Một Pháp',

     'Rūpādivaggo': 'Phẩm Sắc',

     'Nīvaraṇappahānavaggo': 'Phẩm Ðoạn Triền Cái',

     'Akammaniyavaggo': 'Phẩm Khó Sử Dụng',

     'Adantavaggo': 'Phẩm Không Ðiều Phục',

     'Paṇihitaacchavaggo': 'Phẩm Ðặt Hướng Và Trong Sáng',

     'Accharāsaṅghātavaggo': 'Phẩm Búng Ngón Tay',

     'Vīriyārambhādivaggo': 'Phẩm Tinh Tấn',

     'Kalyāṇamittādivaggo': 'Phẩm Làm Bạn Với Thiện',

     'Pamādādivaggo': 'Phẩm Phóng Dật',

     'Dutiyapamādādivaggo': 'Phẩm Phóng Dật thứ hai',

     'Adhammavaggo': 'Phẩm Phi Pháp',

     'Anāpattivaggo': 'Phẩm Vô Phạm',

     'Ekapuggalavaggo': 'Phẩm Một Người',

     'Etadaggavaggo': 'Phẩm Người Tối Thắng',

     'Aṭṭhānapāḷi': 'Phẩm Không Thể Có Ðược',

     'Ekadhammapāḷi': 'Phẩm Một Pháp',

     'Pasādakaradhammavaggo': '',

#     'Aparaaccharāsaṅghātavaggo': '',

#     'Kāyagatāsativaggo': '',

#     'Amatavaggo': '',

   'Dukanipātapāḷi': 'Chương Hai Pháp',

#     'Kammakaraṇavaggo': '科刑罰品',

#     'Adhikaraṇavaggo': '靜論品',

#     'Bālavaggo': '愚人品',

#     'Samacittavaggo': '等心品',

#     'Parisavaggo': '會眾品',

#     'Puggalavaggo': '人品',

#     'Sukhavaggo': '樂品',

#     'Sanimittavaggo': '有品',

#     'Dhammavaggo': '法品',

#     'Bālavaggo': '愚者品',

#     'Āsāduppajahavaggo': '希望品',

#     'Āyācanavaggo': '希求品',

#     'Dānavaggo': '施品',

#     'Santhāravaggo': '覆護品',

#     'Samāpattivaggo': '入定品',

#     'Kodhapeyyālaṃ': '忿品',

#     'Akusalapeyyālaṃ': '(律廣說)品',

#     'Vinayapeyyālaṃ': '',

#     'Rāgapeyyālaṃ': '',

   'Tikanipātapāḷi': 'Chương Ba Pháp',

#     'Bālavaggo': '愚人品',

#     'Rathakāravaggo': '車匠品',

#     'Puggalavaggo': '補特羅品',

#     'Devadūtavaggo': '天使品',

#     'Cūḷavaggo': '小品',

#     'Brāhmaṇavaggo': '婆羅門品',

#     'Mahāvaggo': '大品',

#     'Ānandavaggo': '阿難品',

#     'Samaṇavaggo': '沙門品',

#     'Loṇakapallavaggo': '掬鹽品',

#     'Sambodhavaggo': '等覺品',

#     'Āpāyikavaggo': '惡趣品',

#     'Kusināravaggo': '古西那拉品',

#     'Yodhājīvavaggo': '戰士品',

#     'Maṅgalavaggo': '吉祥品',

#     'Acelakavaggo': '裸形品',

#     'Kammapathapeyyālaṃ': '',

#     'Rāgapeyyālaṃ': '',

   'Catukkanipātapāḷi': 'Chương Bốn Pháp',

   'Pañcakanipātapāḷi': 'Chương Năm Pháp',

   'Chakkanipātapāḷi': 'Chương Sáu Pháp',

   'Sattakanipātapāḷi': 'Chương Bảy Pháp',

   'Aṭṭhakādinipātapāḷi': 'Chương Tám Pháp',

   'Navakanipātapāḷi': 'Chương Chín Pháp',

   'Dasakanipātapāḷi': 'Chương Mười Pháp',

   'Ekādasakanipātapāḷi': 'Chương Mười Một Pháp',

#     'Nissayavaggo': '依止品',

#     'Anussativaggo': '憶念品',

#     'Sāmaññavaggo': '沙門品',

#     'Rāgapeyyālaṃ': '貪品',

 'Khuddakanikāya': 'Tiểu Bộ',

#  'Khuddakanikāya': 'Division of Short Books',

   'Khuddakapāṭhapāḷi': 'The Short Passages',

     'Saraṇattayaṃ': 'Saranagamana — Going for Refuge',

     'Dasasikkhāpadaṃ': 'The Ten Training Rules',

     'Dvattiṃsākāro': 'The 32 Parts',

     'Kumārapañhā': "Samanera Pañha — The Novice's Questions",

     'Maṅgalasuttaṃ': 'Protection',

     'Ratanasuttaṃ': 'Treasures',

     'Tirokuṭṭasuttaṃ': 'Tirokudda Kanda — Hungry Shades Outside the Walls',

     'Nidhikaṇḍasuttaṃ': 'The Reserve Fund',

     'Mettasuttaṃ': 'Karaniya Metta Sutta — Good Will',

   'Dhammapadapāḷi': 'Pháp Cú',

     'Yamakavaggo': 'Pairs',

     'Appamādavaggo': 'Heedfulness',

     'Cittavaggo': 'The Mind',

     'Pupphavaggo': 'Blossoms',

     'Bālavaggo': 'Fools',

     'Paṇḍitavaggo': 'The Wise',

     'Arahantavaggo': 'Arahants',

     'Sahassavaggo': 'Thousands',

     'Pāpavaggo': 'Evil',

     'Daṇḍavaggo': 'The Rod',

     'Jarāvaggo': 'Aging',

     'Attavaggo': 'Self',

     'Lokavaggo': 'Worlds',

     'Buddhavaggo': 'Awakened',

     'Sukhavaggo': 'Happy',

     'Piyavaggo': 'Dear Ones',

     'Kodhavaggo': 'Anger',

     'Malavaggo': 'Impurities',

     'Dhammaṭṭhavaggo': 'The Judge',

     'Maggavaggo': 'The Path',

     'Pakiṇṇakavaggo': 'Miscellany',

     'Nirayavaggo': 'Hell',

     'Nāgavaggo': 'Elephants',

     'Taṇhāvaggo': 'Craving',

     'Bhikkhuvaggo': 'Monks',

     'Brāhmaṇavaggo': 'Brahmans',

   'Udānapāḷi': 'Exclamations',

   'Itivuttakapāḷi': 'The Thus-saids',

   'Suttanipātapāḷi': 'The Discourses Collection',

     'Uragavaggo': 'The Snake Chapter',

     'Cūḷavaggo': 'The Lesser Chapter',

     'Mahāvaggo': 'The Great Chapter',

     'Aṭṭhakavaggo': 'The Octet Chapter',

     'Pārāyanavaggo': 'The Chapter on the Way to the Far Shore',

   'Vimānavatthupāḷi': 'Stories of the Celestial Mansions',

   'Petavatthupāḷi': 'Truyện Ngạ Quỷ',

   'Theragāthāpāḷi': 'Trưởng lão Kệ',

   'Therīgāthāpāḷi': 'Trưởng lão ni Kệ',

   'Apadānapāḷi': 'Stories',

   'Buddhavaṃsapāḷi': 'History of the Buddhas',

   'Cariyāpiṭakapāḷi': 'Basket of Conduct',

   'Jātakapāḷi': 'Birth Stories',

#   'Mahāniddesapāḷi': '大義釋',

#   'Cūḷaniddesapāḷi': '小義釋',

   'Paṭisambhidāmaggapāḷi': 'Path of Discrimination',

#   'Nettippakaraṇapāḷi': '導論',

   'Milindapañhapāḷi': 'Milinda Vấn Đạo',

#   'Peṭakopadesapāḷi': '藏釋 (三藏知津)',

#'Abhidhammapiṭaka': '',

 'Dhammasaṅgaṇīpāḷi': 'Enumeration of Phenomena',

 'Vibhaṅgapāḷi': 'The Book of Analysis',

# 'Vibhaṅgapāḷi': 'The Book of Treatises',

 'Dhātukathāpāḷi': 'Discourse on Elements',

# 'Dhātukathāpāḷi': 'Discussion with Reference to the Elements',

 'Puggalapaññattipāḷi': 'A Designation of Human Types',

# 'Puggalapaññattipāḷi': 'Description of Individuals',

 'Kathāvatthupāḷi': 'Points of Controversy',

 'Yamakapāḷi': 'The Book of Pairs',

 'Paṭṭhānapāḷi': 'The Book of Relations',

'Aṭṭhakathā': 'Chú Giải',

'Tīkā': 'Sớ Giải',

 'Abhidhammatthasaṅgaho': 'A Comprehensive Manual of Abhidhamma',

 'Visuddhimagga': 'The Path of Purification',

     'Sīlaniddeso': 'DESCRIPTION OF VIRTUE',

     'Dhutaṅganiddeso': 'THE ASCETIC PRACTICES',

     'Kammaṭṭhānaggahaṇaniddeso': 'TAKING A MEDITATION SUBJECT',

     'Pathavīkasiṇaniddeso': 'THE EARTH KASIṆA',

     'Sesakasiṇaniddeso': 'THE REMAINING KASIṆAS',

     'Asubhakammaṭṭhānaniddeso': 'FOULNESS AS A MEDITATION SUBJECT',

     'Chaanussatiniddeso': 'SIX RECOLLECTIONS',

     'Anussatikammaṭṭhānaniddeso': 'OTHER RECOLLECTIONS AS MEDITATION SUBJECTS',

     'Brahmavihāraniddeso': 'THE DIVINE ABIDINGS',

     'Āruppaniddeso': 'THE IMMATERIAL STATES',

     'Samādhiniddeso': 'CONCENTRATION—CONCLUSION: NUTRIMENT AND THE ELEMENTS',

     'Iddhividhaniddeso': 'THE SUPERNORMAL POWERS',

     'Abhiññāniddeso': 'OTHER DIRECT-KNOWLEDGES',

     'Khandhaniddeso': 'THE AGGREGATES',

     'Āyatanadhātuniddeso': 'THE BASES AND ELEMENTS',

     'Indriyasaccaniddeso': 'THE FACULTIES AND TRUTHS',

     'Paññābhūminiddeso': 'THE SOIL OF UNDERSTANDING—CONCLUSION: DEPENDENT ORIGINATION',

     'Diṭṭhivisuddhiniddeso': 'PURIFICATION OF VIEW',

     'Kaṅkhāvitaraṇavisuddhiniddeso': 'PURIFICATION BY OVERCOMING DOUBT',

     'Maggāmaggañāṇadassanavisuddhiniddeso': 'PURIFICATION BY KNOWLEDGE AND VISION OF WHAT IS THE PATH AND WHAT IS NOT THE PATH',

     'Paṭipadāñāṇadassanavisuddhiniddeso': 'PURIFICATION BY KNOWLEDGE AND VISION OF THE WAY',

     'Ñāṇadassanavisuddhiniddeso': 'PURIFICATION BY KNOWLEDGE AND VISION',

     'Paññābhāvanānisaṃsaniddeso': 'THE BENEFITS IN DEVELOPING UNDERSTANDING',

' ': ' '
}

if __name__ == '__main__':
  dstTrInfoPath = os.path.join(os.path.dirname(__file__), 'json/translationInfo.json')
  dstCanonTextTranslationPath = os.path.join(os.path.dirname(__file__), 'json/canonTextTranslation.json')

  if not os.path.exists(os.path.dirname(dstTrInfoPath)):
    os.makedirs(os.path.dirname(dstTrInfoPath))

  with open(dstTrInfoPath, 'w') as f:
    f.write(json.dumps(translationInfo))

  canonTextTranslation['zh_CN'] = {}
  for key in canonTextTranslation['zh_TW']:
    canonTextTranslation['zh_CN'][key] = ftoj(canonTextTranslation['zh_TW'][key])
  with open(dstCanonTextTranslationPath, 'w') as f:
    f.write(json.dumps(canonTextTranslation))

  dstTrServicePath = os.path.join(os.path.dirname(__file__), '../app/scripts/services/data/i18nTpk.js')

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

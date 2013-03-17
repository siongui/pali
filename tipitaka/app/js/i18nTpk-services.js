'use strict';

/* Services */


angular.module('paliTipitaka.i18nTpk', []).
  factory('i18nTpk', [function() {
    var translationInfo = {
      'zh_TW': {
        'canon': {
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
          // FIXME: use 3 instead of 1?
          '1': ['Ṭhānissaro Bhikkhu', 'http://www.accesstoinsight.org/tipitaka/translators.html#than', 'http://www.accesstoinsight.org/lib/authors/thanissaro/dhammapada.pdf']
        }
      }
    };

    var canonName = {
      's0505m.mul0.xml': {
        'pali': 'Suttanipāta, Uragavaggo',
        'zh_TW': '經集, 蛇品'
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
    };

    return {
      translationInfo: translationInfo,
      canonName: canonName
    };

  }]);

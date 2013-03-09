'use strict';

/* Service for determining language of dictionary */


angular.module('pali.service-dic', []).
  factory('palidic', [function() {

    function lang(dicWordExp) {
      if (dicWordExp[0].indexOf('《パーリ语辞典》') >= 0 ||
          dicWordExp[0].indexOf('《パーリ語辭典》') >= 0) {
        // Pali to Japanese dictionary
        return 'ja';
      } else if (dicWordExp[0].indexOf('パーリ语辞典 增补改订') >= 0 ||
                 dicWordExp[0].indexOf('パーリ語辭典 增補改訂') >= 0) {
        // Pali to Japanese dictionary
        return 'ja';
      } else if (dicWordExp[0].indexOf('Buddhist Dictionary') >= 0) {
        // Pali to English dictionary
        return 'en';
      } else if (dicWordExp[0].indexOf('Pali-English') >= 0) {
        // Pali to English dictionary
        return 'en';
      } else if (dicWordExp[0].indexOf('《巴汉词典》') >= 0 ||
                 dicWordExp[0].indexOf('《巴漢詞典》') >= 0) {
        // Pali to Chinese dictionary
        return 'zh';
      } else if (dicWordExp[0].indexOf('《巴利语字汇》') >= 0 ||
                 dicWordExp[0].indexOf('《巴利語字彙》') >= 0) {
        // Pali to Chinese dictionary
        return 'zh';
      } else if (dicWordExp[0].indexOf('巴利文-汉文') >= 0 ||
                 dicWordExp[0].indexOf('巴利文-漢文') >= 0) {
        // Pali to Chinese dictionary
        return 'zh';
      } else if (dicWordExp[0].indexOf('汉译パーリ') >= 0 ||
                 dicWordExp[0].indexOf('漢譯パーリ') >= 0) {
        // Pali to Chinese dictionary
        return 'zh';
      } else if (dicWordExp[0].indexOf('巴利语入门') >= 0 ||
                 dicWordExp[0].indexOf('巴利語入門') >= 0) {
        // Pali to Chinese dictionary
        return 'zh';
      } else if (dicWordExp[0].indexOf('巴利新音译') >= 0 ||
                 dicWordExp[0].indexOf('巴利新音譯') >= 0) {
        // Pali to Chinese dictionary
        return 'zh';
      } else if (dicWordExp[0].indexOf('巴英术语汇编') >= 0 ||
                 dicWordExp[0].indexOf('巴英術語彙編') >= 0) {
        // Pali to Chinese dictionary
        return 'zh';
      } else {
        // Pali to ?(unknown)
        console.log('unknown: ' + dicWordExp[0]);
        return 'unknown';
      }
    }

    function shortNameAndSeparator(dicWordExp) {
      if (dicWordExp[0].indexOf('《パーリ语辞典》') >= 0) {
        var dicShortName = '《パーリ语辞典》';
        var separator = ' -';
      } else if (dicWordExp[0].indexOf('《パーリ語辭典》') >= 0) {
        var dicShortName = '《パーリ語辭典》';
        var separator = ' -';
      } else if (dicWordExp[0].indexOf('巴汉词典》 Mahāñāṇo') >= 0) {
        var dicShortName = '《巴汉词典》';
        var separator = '~';
      } else if (dicWordExp[0].indexOf('巴漢詞典》 Mahāñāṇo') >= 0) {
        var dicShortName = '《巴漢詞典》';
        var separator = '~';
      } else if (dicWordExp[0].indexOf('巴汉词典》 明法') >= 0) {
        var dicShortName = '《巴汉词典》';
        var separator = '。';
      } else if (dicWordExp[0].indexOf('巴漢詞典》 明法') >= 0) {
        var dicShortName = '《巴漢詞典》';
        var separator = '。';
      } else if (dicWordExp[0].indexOf('巴利语字汇') >= 0) {
        var dicShortName = '《巴利语字汇》';
        var separator = '。';
      } else if (dicWordExp[0].indexOf('巴利語字彙') >= 0) {
        var dicShortName = '《巴利語字彙》';
        var separator = '。';
      } else if (dicWordExp[0].indexOf('巴利文-汉文') >= 0) {
        var dicShortName = '《巴利文-汉文佛学名相辞汇》'
        var separator = '。';
      } else if (dicWordExp[0].indexOf('巴利文-漢文') >= 0) {
        var dicShortName = '《巴利文-漢文佛學名相辭彙》'
        var separator = '。';
      } else if (dicWordExp[0].indexOf('Buddhist Dictionary') >= 0) {
        var dicShortName = '《Buddhist Dictionary》';
        var separator = '<br>';
      } else if (dicWordExp[0].indexOf('Concise Pali-English') >= 0) {
        var dicShortName = '《Concise Pali-English Dictionary》';
        var separator = '<br>';
      } else if (dicWordExp[0].indexOf('PTS Pali-English') >= 0) {
        var dicShortName = '《PTS Pali-English Dictionary》';
        var separator = '<i>';
      } else if (dicWordExp[0].indexOf('汉译パーリ') >= 0) {
        var dicShortName = '《汉译パーリ语辞典》';
        var separator = ' -';
      } else if (dicWordExp[0].indexOf('漢譯パーリ') >= 0) {
        var dicShortName = '《漢譯パーリ語辭典》';
        var separator = ' -';
      } else if (dicWordExp[0].indexOf('パーリ语辞典 增补') >= 0) {
        var dicShortName = '《パーリ语辞典 增补改订》';
        var separator = ' -';
      } else if (dicWordExp[0].indexOf('パーリ語辭典 增補') >= 0) {
        var dicShortName = '《パーリ語辭典 增補改訂》';
        var separator = ' -';
      } else if (dicWordExp[0].indexOf('巴英术语汇编') >= 0) {
        var dicShortName = '《巴英术语汇编》'
        var separator = '。';
      } else if (dicWordExp[0].indexOf('巴英術語彙編') >= 0) {
        var dicShortName = '《巴英術語彙編》'
        var separator = '。';
      } else if (dicWordExp[0].indexOf('巴利新音译') >= 0) {
        var dicShortName = '《巴利语汇解》与《巴利新音译》';
        var separator = '。';
      } else if (dicWordExp[0].indexOf('巴利新音譯') >= 0) {
        var dicShortName = '《巴利語彙解》與《巴利新音譯》';
        var separator = '。';
      } else if (dicWordExp[0].indexOf('巴利语入门') >= 0) {
        var dicShortName = '《巴利语入门》';
        var separator = '。';
      } else if (dicWordExp[0].indexOf('巴利語入門') >= 0) {
        var dicShortName = '《巴利語入門》';
        var separator = '。';
      } else {
        var dicShortName = dicWordExp[0];
        var separator = '。';
      }

      return [dicShortName, separator];
    }

    function shortExp(dicWordExp) {
      var separator = shortNameAndSeparator(dicWordExp)[1];
      var breakPos = dicWordExp[2].indexOf(separator);
      if (breakPos == -1)
        var shortExp = dicWordExp[2];
      else
        var shortExp = dicWordExp[2].slice(0, breakPos);

      if (shortExp.length > 200)
        shortExp = shortExp.slice(0, 200) + '...';

      return shortExp;
    }

    var serviceInstance = {
      lang: lang,
      shortName: function(dicWordExp) {return shortNameAndSeparator(dicWordExp)[0]},
      shortExp: function(dicWordExp) {return shortExp(dicWordExp);}
    };

    return serviceInstance;
  }]);

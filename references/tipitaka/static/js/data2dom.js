/**
 * @fileoverview Convert data to DOM element
 */

var Data2dom = Data2dom || {};


/**
 * Convert JSON format of lookup data to HTML DOM elements
 * This function returns shorter explanations (preview) of a word
 * @param {object} jsonData The json format lookup data of word
 * @return {DOM Element} HTML DOM elements of word preview.
 */
Data2dom.createPreview = function(jsonData) {
  // check if the word exist
  if (jsonData['data'] == null) {
    // the word does NOT exist
    return document.createTextNode(getStringNoSuchWord());
  }

  // The word exist. Build DOM elements.
  var container = document.createElement('div');

  var wordName = document.createElement('a');
  wordName.className = "previewWordName";
  wordName.appendChild(document.createTextNode(jsonData['word']));
  wordName.href = 'http://palidictionary.appspot.com/browse/' +
                  jsonData['word'][0] + '/' + jsonData['word'];
  if (window.location.host == 'localhost:8080') wordName.href += '?track=no';
  wordName.target = '_blank';

  container.appendChild(wordName);

  var note = document.createElement('sup');
  note.appendChild(document.createElement('span'));
  note.firstChild.style.color = 'blue';
  note.firstChild.appendChild(document.createTextNode('(' + 
     i18n.gettext('double click on the word to see details')+')'));

  container.appendChild(note);

  var sortedDicWordExps = Data2dom.getSortedDicWordExpsbyLangs(
                            jsonData['data']);

  for (var index in sortedDicWordExps) {
    container.appendChild(Data2dom.createPreviewDicWordExp(
      sortedDicWordExps[index]));
  }

  return container;
};


/**
 * Build short dictionary name and explanation.
 * @param {object} dicWordExp The dictionary-word-explanation tuple of word
 * @return {DOM Element} HTML DOM elements of short dictionary name and
 *                       explanation.
 * @private
 */
Data2dom.createPreviewDicWordExp = function(dicWordExp) {
  if (dicWordExp[0].indexOf('《パーリ语辞典》') >= 0) {
    var dicShortName = '《パーリ语辞典》';
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

  var shortDicExp = document.createElement('div');
  shortDicExp.className = 'shortDicExp';

  // show short name of the dictionary in the preview
  var dicName = document.createElement('span');
  dicName.appendChild(document.createTextNode(dicShortName));

  shortDicExp.appendChild(dicName);

  // show shorter explanation in the preview
  var breakPos = dicWordExp[2].indexOf(separator);
  if (breakPos == -1) {
    var shortExp = dicWordExp[2];
  } else {
    var shortExp = dicWordExp[2].slice(0, breakPos);
  }

  if (shortExp.length > 200) shortExp = shortExp.slice(0, 200) + '...';

  shortDicExp.innerHTML += shortExp;

  return shortDicExp;
};


/**
 * Create words list by HTML table
 * @param {Array} wordsArray The array of words
 * @return {DOM Element} elements for listing words
 */
Data2dom.createWordsList = function(wordsArray) {
  var container = document.createElement('div');
  container.style.margin = '.5em';
  container.style.lineHeight = '1.5em';
  container.style.textAlign = 'left';

  var tableElem = document.createElement('table');
  tableElem.style.width = '100%';
  var rowCount = 0;
  for (var index in wordsArray) {
    var word = wordsArray[index];
    if (rowCount == 0)
      var trElem = document.createElement('tr');
    var tdElem = document.createElement('td');

    var aElem = document.createElement('a');
    aElem.title = word;
    aElem.href = '/browse/' + word[0] + '/' + word +
                 window.location.search;
    aElem.style.margin = '.5em';
    aElem.style.textDecoration = 'none';
    aElem.appendChild(document.createTextNode(word));

    tdElem.appendChild(aElem);
    trElem.appendChild(tdElem);

    rowCount += 1;
    if (rowCount == 3) {
      tableElem.appendChild(trElem);
      rowCount = 0;
    }
  }
  if (trElem)
    tableElem.appendChild(trElem);

  container.appendChild(tableElem);
  return container;
};


/**
 * Get Parsed HTTP accept-languages header of the user browser. The header is
 * embedded by server in 'locale' DIV of '/' page.
 * @return {Array} Array of language-quality pairs
 */
Data2dom.getParsedAcceptLangs = function() {
  var hdr = document.getElementById('locale').innerHTML.split('~')[1];
  var pairs = hdr.split(',');
  var result = [];
  for (var i=0; i < pairs.length; i++) {
    var pair = pairs[i].split(';');
    if (pair.length == 1) result.push( [pair[0], '1'] );
    else result.push( [pair[0], pair[1].split('=')[1] ] );
  }
  return result;
};


/**
 * Sort [dic, word, explanation]s according http accept-languages header or
 * setting
 * @param {Array} The unsorted array of one or more [dic, word, explanation]
 * @return {Array} The sorted array of one or more [dic, word, explanation]
 *                 according to http accept-languages header or setting
 */
Data2dom.getSortedDicWordExpsbyLangs = function(dicWordExps) {
  // put dictionaries of the same lang into the same array
  var ja = [];
  var zh = [];
  var en = [];
  var unknown = [];
  for (var i=0; i < dicWordExps.length; i++) {
    var dicWordExp = dicWordExps[i];
    if (dicWordExp[0].indexOf('《パーリ语辞典》') >= 0) {
      // Pali to Japanese dictionary
      ja.push(dicWordExp);
    } else if (dicWordExp[0].indexOf('パーリ语辞典 增补改订') >= 0) {
      // Pali to Japanese dictionary
      ja.push(dicWordExp);
    } else if (dicWordExp[0].indexOf('Buddhist Dictionary') >= 0) {
      // Pali to English dictionary
      en.push(dicWordExp);
    } else if (dicWordExp[0].indexOf('Pali-English') >= 0) {
      // Pali to English dictionary
      en.push(dicWordExp);
    } else if (dicWordExp[0].indexOf('《巴汉词典》') >= 0 ||
               dicWordExp[0].indexOf('《巴漢詞典》') >= 0) {
      // Pali to Chinese dictionary
      zh.push(dicWordExp);
    } else if (dicWordExp[0].indexOf('《巴利语字汇》') >= 0 ||
               dicWordExp[0].indexOf('《巴利語字彙》') >= 0) {
      // Pali to Chinese dictionary
      zh.push(dicWordExp);
    } else if (dicWordExp[0].indexOf('巴利文-汉文') >= 0 ||
               dicWordExp[0].indexOf('巴利文-漢文') >= 0) {
      // Pali to Chinese dictionary
      zh.push(dicWordExp);
    } else if (dicWordExp[0].indexOf('汉译パーリ') >= 0 ||
               dicWordExp[0].indexOf('漢譯パーリ') >= 0) {
      // Pali to Chinese dictionary
      zh.push(dicWordExp);
    } else if (dicWordExp[0].indexOf('巴利语入门') >= 0 ||
               dicWordExp[0].indexOf('巴利語入門') >= 0) {
      // Pali to Chinese dictionary
      zh.push(dicWordExp);
    } else if (dicWordExp[0].indexOf('巴利新音译') >= 0 ||
               dicWordExp[0].indexOf('巴利新音譯') >= 0) {
      // Pali to Chinese dictionary
      zh.push(dicWordExp);
    } else if (dicWordExp[0].indexOf('巴英术语汇编') >= 0 ||
               dicWordExp[0].indexOf('巴英術語彙編') >= 0) {
      // Pali to Chinese dictionary
      zh.push(dicWordExp);
    } else {
      // Pali to ?(unknown)
      unknown.push(dicWordExp);
      console.log('unknown: ' + dicWordExp[0]);
    }
  }

  if (document.getElementById('toTraditionalCht').checked) {
    // translate simplified chinses to traditional chinese by TongWen library
    if (typeof TongWen != 'undefined') {
      for (var i=0; i < zh.length; i++) {
        zh[i][0] = TongWen.convert(zh[i][0], TongWen.flagTrad);
        zh[i][2] = TongWen.convert(zh[i][2], TongWen.flagTrad);
      }
    }
  }

  var isLangArrayEmpty = {
    'en' : false,
    'ja' : false,
    'zh' : false,
    'unknown' : false
  };

  // include language of dictionaries by setting
  if (!document.getElementById('p2en').checked)
    isLangArrayEmpty['en'] = true;
  if (!document.getElementById('p2ja').checked)
    isLangArrayEmpty['ja'] = true;
  if (!document.getElementById('p2zh').checked)
    isLangArrayEmpty['zh'] = true;

  var result = [];
  var order = document.getElementById('dicLangOrder').value;
  if (order == 'en2ja2zh') {
    if (!isLangArrayEmpty['en']) result = result.concat(en);
    if (!isLangArrayEmpty['ja']) result = result.concat(ja);
    if (!isLangArrayEmpty['zh']) result = result.concat(zh);
  }
  if (order == 'en2zh2ja') {
    if (!isLangArrayEmpty['en']) result = result.concat(en);
    if (!isLangArrayEmpty['zh']) result = result.concat(zh);
    if (!isLangArrayEmpty['ja']) result = result.concat(ja);
  }
  if (order == 'ja2en2zh') {
    if (!isLangArrayEmpty['ja']) result = result.concat(ja);
    if (!isLangArrayEmpty['en']) result = result.concat(en);
    if (!isLangArrayEmpty['zh']) result = result.concat(zh);
  }
  if (order == 'ja2zh2en') {
    if (!isLangArrayEmpty['ja']) result = result.concat(ja);
    if (!isLangArrayEmpty['zh']) result = result.concat(zh);
    if (!isLangArrayEmpty['en']) result = result.concat(en);
  }
  if (order == 'zh2en2ja') {
    if (!isLangArrayEmpty['zh']) result = result.concat(zh);
    if (!isLangArrayEmpty['en']) result = result.concat(en);
    if (!isLangArrayEmpty['ja']) result = result.concat(ja);
  }
  if (order == 'zh2ja2en') {
    if (!isLangArrayEmpty['zh']) result = result.concat(zh);
    if (!isLangArrayEmpty['ja']) result = result.concat(ja);
    if (!isLangArrayEmpty['en']) result = result.concat(en);
  }
  if (order != 'hdr') {
    result = result.concat(unknown);
    return result;
  }

  // show the order of language of dictionaries according to accept-languages
  // http header (default)
  var langq_pairs = Data2dom.getParsedAcceptLangs();

  for (var i=0; i<langq_pairs.length; i++) {
    if (langq_pairs[i][0].toLowerCase().indexOf('ja') == 0) {
      if (!isLangArrayEmpty['ja']) {
        isLangArrayEmpty['ja'] = true;
        result = result.concat(ja);
      }
    }
    if (langq_pairs[i][0].toLowerCase().indexOf('en') == 0) {
      if (!isLangArrayEmpty['en']) {
        isLangArrayEmpty['en'] = true;
        result = result.concat(en);
      }
    }
    if (langq_pairs[i][0].toLowerCase().indexOf('zh') == 0) {
      if (!isLangArrayEmpty['zh']) {
        isLangArrayEmpty['zh'] = true;
        result = result.concat(zh);
      }
    }
  }

  if (!isLangArrayEmpty['en']) result = result.concat(en);
  if (!isLangArrayEmpty['ja']) result = result.concat(ja);
  if (!isLangArrayEmpty['zh']) result = result.concat(zh);
  result = result.concat(unknown);

  return result;
};

var Lookup = Lookup || {};


// cache for words
Lookup.wordsCache_ = {};


// tooltip dom element: show lookup result here
Lookup.tooltip = document.getElementById('tooltip');
if (!Lookup.tooltip) throw 'no tooltip element';

// add 'mouse enter' event to tooltip
pali.addMouseEnterEventListener(Lookup.tooltip,
function() {
  Lookup.tooltip.name = 'show';
});

// add 'mouse leave' event to tooltip
pali.addMouseLeaveEventListener(Lookup.tooltip,
function() {
  Lookup.tooltip.name = '';
  pali.removeAllChildren(Lookup.tooltip);
  Lookup.tooltip.style.display = 'none';
});


Lookup.delayedCloseTooltip = function() {
  // If mouse cursor is in tooltip, do not close tooltip
  if (Lookup.tooltip.name == 'show') return;

  // Mouse cursor is not in tooltip, close tooltip
  pali.removeAllChildren(Lookup.tooltip);
  Lookup.tooltip.style.display = 'none';
};


// when user's mouse hovers over words, delay a period of time before look up.
Lookup.DELAY_INTERVAL = 1000;


Lookup.callback = function(jsonData) {
  // save the lookup data of word to cache
  if (!Lookup.wordsCache_.hasOwnProperty(jsonData['word']))
    Lookup.wordsCache_[jsonData['word']] = jsonData;

  // process lookup data
  var elems = Data2dom.createPreview(jsonData);

  // show data in the tooltip
  pali.removeAllChildren(Lookup.tooltip);
  Lookup.tooltip.appendChild(elems);
  if (Lookup.adjustTooltipPosition()) {
    pali.removeAllChildren(Lookup.tooltip);
    Lookup.tooltip.appendChild(elems);
  }
};


Lookup.failCallback = function(word) {
  Lookup.wordsCache_[word] = null;

  // show 'no such word' in tooltip
  Lookup.tooltip.innerHTML = i18n.gettext('No Such Word');
};


Lookup.adjustTooltipPosition = function() {
  var width = Lookup.tooltip.offsetWidth;
  var height = Lookup.tooltip.offsetHeight;
  if (height/width > 2) {
//    console.log('too tall! width: ' + width + ', height: ' + height);
    var newLeft = Lookup.tooltip.style.left.replace('px', '') - height / 2;
    if (newLeft < 0) newLeft = 0;
    Lookup.tooltip.style.left = Math.floor(newLeft) + 'px';
    return true;
  }
  return false;
};

Lookup.setTooltipPosition = function(wordElement) {
  // FIXME: show position according to cursor position in the window.
  var pos = pali.getOffset(wordElement);
  Lookup.tooltip.style.left = pos.left + 'px';
  // javascript get height dom element
  // @see http://stackoverflow.com/questions/526347/css-javascript-how-do-you-get-the-rendered-height-of-an-element
  Lookup.tooltip.style.top = pos.top + wordElement.offsetHeight + 'px';
};


/**
 * @this {DOM element}
 */
Lookup.getLookupResult = function() {
  // check whether user cursor is still inside this word. If not, return.
  if (this.style.color != 'red') return;

  // get the word to be looked up
  var word = this.innerHTML.toLowerCase();

  Lookup.tooltip.innerHTML = i18n.gettext("Looking up ") + word + ' ...';
  Lookup.setTooltipPosition(this);
  Lookup.tooltip.style.display = 'block';

  // check sanity of the word to be looked up
  word = Lookup.getProcessedUserInput(word);
  if (word == null) {
    Lookup.tooltip.innerHTML = i18n.gettext('No Such Word');
    return;
  }

  /**
   * Check whether there is already json data of this word in the cache,
   * if yes, use the cached data.
   */
  if (Lookup.wordsCache_.hasOwnProperty(word)) {
    var jsonData = Lookup.wordsCache_[word];
    if (jsonData == null)
      Lookup.tooltip.innerHTML = i18n.gettext('No Such Word');
    else
      Lookup.callback(jsonData);

    return;
  }

  // Get the lookup data of the word from dictionary website
  Lookup.httpget(word,
                 Lookup.callback,
                 function(){Lookup.failCallback(word);});
};


/**
 * Before looking up the word, the word needs to be processed. For example,
 * strip beginning and ending white spaces of the word, and validity of the
 * word.
 * @param {string} word The word to be looked up.
 * @return {string|null} The processed word to be looked up, or null if invalid
 *                       word
 */
Lookup.getProcessedUserInput = function(word) {
  /**
   * Remove whitespace in the beginning and end of user input string
   * @const
   * @type {string}
   * @private
   */
  var userInputStr = word.replace(/(^\s+)|(\s+$)/g, '');
  if (userInputStr.length == 0) return null;

  // check if user input is a valid word
  var prefix = Lookup.matchPrefix(userInputStr);
  // if no words start with 'prefix'
  if (prefix == null) return null;

  var matchedWord = Lookup.matchWord(userInputStr);
  // if no matched word
  if (matchedWord == null) {
    var word = Lookup.guessWordBySuffix(userInputStr);
    if (word == null)
      return Lookup.guessWordCombination(userInputStr);
    return word;
  }

  return matchedWord;
};


/**
 * @param {string} word
 * @return {string|null} return null if the first letter of word is not valid
 */
Lookup.matchPrefix = function(word) {
  // FIXME: bad practice: call of dicPrefixWordLists
  // check if dicPrefixWordLists exists
  if (!dicPrefixWordLists) return null;

  for (var key in dicPrefixWordLists) {
    if (word[0] == key) return key;
  }

  // no match, return null
  return null;
};


/**
 * @param {string} word
 * @return {string|null} return null if the word is not valid
 */
Lookup.matchWord = function(word) {
  // FIXME: bad practice: call of dicPrefixWordLists
  // check if dicPrefixWordLists exists
  if (!dicPrefixWordLists) return null;

  for (var index in dicPrefixWordLists[word[0]]) {
    if (dicPrefixWordLists[word[0]][index] == word) return word;
  }

  // no match, return null
  return null;
};


Lookup.guessWordBySuffix = function(word) {
  // TODO: ends with smā?
  // TODO: ends with suṃ?
  // cittāni
  // vimucciṃsu
  // assamaṇḍalikāsu
  // bhikkhūnaṃ
  // verañjaṃ
  // silāyaṃ
  // ovadituṃ
  // desetuṃ
  // parivattetuṃ
  if (word.length == 0) return null;

  if (pali.endswith(word, 'ṃ')) {
    if (pali.endswith(word, 'iṃ')) {
      var endidm = Lookup.matchWord(word.slice(0,-1));
      // tādiṃ -> tādī
      if (endidm == null)
        endidm = Lookup.matchWord(word.slice(0,-2) + 'ī');
      if (endidm == null) {
        if (pali.endswith(word, 'smiṃ'))
          return Lookup.matchWord(word.slice(0,-4));
      }
      return endidm;
    }

    if (pali.endswith(word, 'uṃ')) {
      // pāraguṃ -> pāragū
      var endudm = Lookup.matchWord(word.slice(0,-2) + 'ū');
      if (endudm == null) {
        if (pali.endswith(word, 'tuṃ')) {
          var endtudm = Lookup.matchWord(word.slice(0,-3));
          if (endtudm == null) {
            // FIXME: is this correct?
            if (pali.endswith(word, 'etuṃ'))
              return Lookup.matchWord(word.slice(0,-4) + 'a');
          }
          return endtudm;
        }

        // upavadeyyuṃ -> upavadati
        if (pali.endswith(word, 'eyyuṃ'))
          return Lookup.matchWord(word.slice(0,-5) + 'ati');
      }
      return endudm;
    }

    if (pali.endswith(word, 'aṃ')) {
      var am = Lookup.matchWord(word.slice(0,-1));
      // pabbajjaṃ -> pabbajjā
      if (am == null)
        am = Lookup.matchWord(word.slice(0,-2) + 'ā');
      if (am == null) {
        // muninaṃ -> muni
        if (pali.endswith(word, 'naṃ')) {
          var endnadm = Lookup.matchWord(word.slice(0,-3));
          if (endnadm == null) {
            if (pali.endswith(word, 'ānaṃ')) {
              var endaanadm = Lookup.matchWord(word.slice(0,-4) + 'a');
              if (endaanadm == null) {
                // avedhamānaṃ -> avedha
                if (pali.endswith(word, 'mānaṃ'))
                  return Lookup.matchWord(word.slice(0,-5));
              }
              return endaanadm;
            }
          }
          return endnadm;
        }

        // pavattāraṃ -> pavattar
        if (pali.endswith(word, 'āraṃ'))
          return Lookup.matchWord(word.slice(0,-4) + 'ar');

        // puccheyyaṃ -> puccheyyaṃ
        // FIXME: -> pucchati? -> puccha? -> pucchana? ...?
        if (pali.endswith(word, 'eyyaṃ'))
          return Lookup.matchWord(word.slice(0,-5) + 'ati');

        // paccavekkhitabbaṃ -> paccavekkhi
        if (pali.endswith(word, 'tabbaṃ'))
          return Lookup.matchWord(word.slice(0,-6));
      }
      return am;
    }

    return null;
  }

  if (pali.endswith(word, 'o')) {
    var endo = Lookup.matchWord(word.slice(0,-1) + 'a');
    if (endo == null)
      endo = Lookup.matchWord(word.slice(0,-1) + 'i');
    if (endo == null) {
      if (pali.endswith(word, 'no')) {
        // vatthino -> vatthi
        var endno = Lookup.matchWord(word.slice(0,-2));
        if (endno == null)
          // khemino -> khemī
          return Lookup.matchWord(word.slice(0,-3) + 'ī');

        return endno;
      }

      if (pali.endswith(word, 'to')) {
        // subhato -> subha
        var endto = Lookup.matchWord(word.slice(0,-2));
        if (endto == null) {
          // pahitatto -> pahita
          if (pali.endswith(word, 'tto'))
            return Lookup.matchWord(word.slice(0,-3));

          // nāsato -> nāsā
          if (pali.endswith(word, 'ato'))
            return Lookup.matchWord(word.slice(0,-3) + 'ā');

          // santhavāto -> santhavati
          if (pali.endswith(word, 'āto'))
            return Lookup.matchWord(word.slice(0,-3) + 'ati');

          // vissavanto -> vissavati
          if (pali.endswith(word, 'nto'))
            return Lookup.matchWord(word.slice(0,-3) + 'ti');
        }
        return endto;
      }

      // ñātayo -> ñātaka
      if (pali.endswith(word, 'yo'))
        return Lookup.matchWord(word.slice(0,-2) + 'ka');

      // antapūro, udarapūro -> anta, udara
      if (pali.endswith(word, 'pūro'))
        return Lookup.matchWord(word.slice(0,-4));
    }
    return endo;
  }

  if (pali.endswith(word, 'e')) {
    var ende = Lookup.matchWord(word.slice(0,-1) + 'a');
    // vindate -> vindati
    if (ende == null)
      ende = Lookup.matchWord(word.slice(0,-1) + 'i');
    // pāṇine -> pāṇin
    if (ende == null)
      ende = Lookup.matchWord(word.slice(0,-1));
    if (ende == null) {
      // virājaye -> virājati
      if (pali.endswith(word, 'ye'))
        return Lookup.matchWord(word.slice(0, -2) + 'ti');

      // ogahaṇe -> ogahana
      if (pali.endswith(word, 'ṇe'))
        return Lookup.matchWord(word.slice(0, -2) + 'na');

      // uṇṇametave -> uṇṇameti
      //if (pali.endswith(word, 'ave'))
      //  return Lookup.matchWord(word.slice(0, -3) + 'i');
    }
    return ende;
  }

  if (pali.endswith(word, 'ā')) {
    var endaa = Lookup.matchWord(word.slice(0,-1) + 'a');
    if (endaa == null) {
      if (pali.endswith(word, 'vā')) {
        var endvaa = Lookup.matchWord(word.slice(0, -2));
        if (endvaa == null) {
          // kasitvā -> kasati
          if (pali.endswith(word, 'itvā'))
            return Lookup.matchWord(word.slice(0, -4) + 'ati');
        }
        return endvaa;
      }

      // uṭṭhātā -> uṭṭhāna
      // FIXME: -> uṭṭhātar? uṭṭhātu?
      if (pali.endswith(word, 'tā'))
        return Lookup.matchWord(word.slice(0, -2) + 'na');

      // khantyā -> khanta
      // FIXME: -> khanta? -> khantar? -> khantu?
      if (pali.endswith(word, 'yā')) {
        var endyaa = Lookup.matchWord(word.slice(0, -2) + 'i');
        if (endyaa == null) {
          // chaviyā -> chavi
          var endiyaa = Lookup.matchWord(word.slice(0, -2));
          if (endiyaa == null)
            // mānusiyā -> mānusī
            return Lookup.matchWord(word.slice(0, -3) + 'ī');

          return endiyaa;
        }
        return endyaa;
      }

      // akkhimhā -> akkhi
      if (pali.endswith(word, 'mhā'))
        return Lookup.matchWord(word.slice(0, -3));

      // vamatekadā -> vamati
      if (pali.endswith(word, 'ekadā'))
        return Lookup.matchWord(word.slice(0, -5) + 'i');

      // paccavekkhitabbā -> paccavekkhi
      if (pali.endswith(word, 'tabbā'))
        return Lookup.matchWord(word.slice(0, -5));
    }
    return endaa;
  }

  if (pali.endswith(word, 'ī')) {
    var endii = Lookup.matchWord(word.slice(0,-1) + 'i');
    if (endii == null) {
      // opilāpehī -> opilāpeti
      if (pali.endswith(word, 'hī'))
        return Lookup.matchWord(word.slice(0,-2) + 'ti');

      // bhuñjāmī -> bhuñjati
      // FIXME: -> bhuñjaka?
      if (pali.endswith(word, 'āmī'))
        return Lookup.matchWord(word.slice(0,-3) + 'ati');

      // patirūpakārī -> patirūpa
      if (pali.endswith(word, 'kārī'))
        return Lookup.matchWord(word.slice(0,-4));
    }
    return endii;
  }

  if (pali.endswith(word, 'a')) {
    // muditañca -> mudita
    if (pali.endswith(word, 'ñca'))
      return Lookup.matchWord(word.slice(0,-3));

    if (pali.endswith(word, 'ena'))
      return Lookup.matchWord(word.slice(0,-3) + 'a');

    // example: addasāma -> addasā
    if (pali.endswith(word, 'ma')) {
      var endma = Lookup.matchWord(word.slice(0,-2));
      if (endma == null) {
        // passāma -> passati
        if (pali.endswith(word, 'āma'))
          return Lookup.matchWord(word.slice(0,-3) + 'ati');
      }
      return endma;
    }

    // example: pubbeva -> pubba
    if (pali.endswith(word, 'eva'))
      return Lookup.matchWord(word.slice(0,-3) + 'a');

    // sīhaṃva -> sīha
    if (pali.endswith(word, 'ṃva'))
      return Lookup.matchWord(word.slice(0,-3));

    if (pali.endswith(word, 'ssa')) {
      var endssa = Lookup.matchWord(word.slice(0,-3));
      if (endssa == null) {
        // yakanapeḷassa -> yakana
        if (pali.endswith(word, 'peḷassa'))
          return Lookup.matchWord(word.slice(0,-7));

        // jāyantamassa -> jāyanta
        if (pali.endswith(word, 'massa'))
          return Lookup.matchWord(word.slice(0,-5));
      }
      return endssa
    }

    if (pali.endswith(word, 'ya')) {
      // siṅghāṇikāya -> siṅghāṇikā
      var endya = Lookup.matchWord(word.slice(0,-2));
      if (endya == null) {
        // bhāvanāya?
        if (pali.endswith(word, 'āya'))
          return Lookup.matchWord(word.slice(0,-3) + 'a');

        // atitariya -> atitarati
        if (pali.endswith(word, 'iya'))
          return Lookup.matchWord(word.slice(0,-3) + 'ati');

        if (pali.endswith(word, 'eyya')) {
          // avajāneyya -> avajānāti
          var endeyya = Lookup.matchWord(word.slice(0,-4) + 'āti');
          // ropayeyya -> ropaya
          if (endeyya == null)
            return Lookup.matchWord(word.slice(0,-4) + 'a');
        }
      }
      return endya;
    }

    // bhiyyodha -> bhiyyo
    if (pali.endswith(word, 'dha'))
      return Lookup.matchWord(word.slice(0,-3));

    if (pali.endswith(word, 'tha')) {
      // nisāmetha -> nisāmeti
      var endtha = Lookup.matchWord(word.slice(0,-2) + 'i');
      if (endtha == null) {
        // labhetha -> labhati
        if (pali.endswith(word, 'etha'))
          return Lookup.matchWord(word.slice(0,-4) + 'ati');
      }
      return endtha;
    }

    return null;
  }

  if (pali.endswith(word, 'i')) {
    // vapāmi -> vapati
    // FIXME: -> vapana?
    if (pali.endswith(word, 'āmi')) {
      var endaami = Lookup.matchWord(word.slice(0,-3) + 'ati');
      // pajānāmi -> pajānāti
      if (endaami == null)
        endaami = Lookup.matchWord(word.slice(0,-2) + 'ti');
      if (endaami == null) {
        // vicarissāmi -> vicarati
        if (pali.endswith(word, 'issāmi'))
          return Lookup.matchWord(word.slice(0,-6) + 'ati');
      }
      return endaami;
    }

    // pantāni -> panta
    if (pali.endswith(word, 'āni'))
      return Lookup.matchWord(word.slice(0,-3) + 'a');

    // vatthūni -> vatthu
    if (pali.endswith(word, 'ūni'))
      return Lookup.matchWord(word.slice(0,-3) + 'u');

    if (pali.endswith(word, 'hi')) {
      // chaḍḍehi -> chaḍḍeti
      var endhi = Lookup.matchWord(word.slice(0,-2) + 'ti');
      // navahi -> nava
      endhi = Lookup.matchWord(word.slice(0,-2));
      if (endhi == null) {
        // *ehi -> *a
        if (pali.endswith(word, 'ehi'))
          return Lookup.matchWord(word.slice(0,-3) + 'a');

        if (pali.endswith(word, 'ebhi'))
          return Lookup.matchWord(word.slice(0,-4) + 'a');

        // jālamhi -> jāla
        if (pali.endswith(word, 'mhi'))
          return Lookup.matchWord(word.slice(0,-3));

        // yathābhūtañhi -> yathābhūta
        if (pali.endswith(word, 'ñhi'))
          return Lookup.matchWord(word.slice(0,-3));
      }
      return endhi;
    }

    // anumodasi -> anumodati
    if (pali.endswith(word, 'si'))
      return Lookup.matchWord(word.slice(0,-2) + 'ti');

    // aññepi -> añña
    if (pali.endswith(word, 'epi'))
      return Lookup.matchWord(word.slice(0,-3) + 'a');

    if (pali.endswith(word, 'mpi')) {
      // tvampi -> tvaṃ
      var endmpi = Lookup.matchWord(word.slice(0,-3) + 'ṃ');
      if (endmpi == null)
        // catutthampi -> catuttha
        return Lookup.matchWord(word.slice(0,-3));
      return endmpi;
    }

    // samiñjeti -> samiñjati
    if (pali.endswith(word, 'eti'))
      return Lookup.matchWord(word.slice(0,-3) + 'ati');

    // honti -> hoti
    if (pali.endswith(word, 'nti'))
      return Lookup.matchWord(word.slice(0,-3) + 'ti');

    // adassanāti -> adassana
    if (pali.endswith(word, 'āti'))
      return Lookup.matchWord(word.slice(0,-3) + 'a');

    // jhāyatoti -> jhāyati
    if (pali.endswith(word, 'oti'))
      return Lookup.matchWord(word.slice(0,-3) + 'i');

    return null;
  }

  if (pali.endswith(word, 'su')) {
    // chasu -> cha
    var endsu = Lookup.matchWord(word.slice(0,-2));
    if (endsu == null) {
      // example: puttesu -> putta
      if (pali.endswith(word, 'esu'))
        return Lookup.matchWord(word.slice(0,-3) + 'a');

      // kasassu -> kasati
      // FIXME: -> kasana?
      if (pali.endswith(word, 'ssu')) {
        var endssu = Lookup.matchWord(word.slice(0,-3) + 'ti');
        if (endssu == null)
          return Lookup.matchWord(word.slice(0,-3));
        return endssu;
      }
    }
    return endsu;
  }

  // upavadeyyuṃ -> upavadati ???
  if (pali.endswith(word, 'eyyu'))
    return Lookup.matchWord(word.slice(0,-4) + 'ati');

  if (pali.endswith(word, 'ū')) {
    // bhuñjassū -> bhuñjati
    // FIXME: -> bhuñjaka?
    if (pali.endswith(word, 'ssū'))
      return Lookup.matchWord(word.slice(0,-3) + 'ti');

    // puthū -> puthu
    return Lookup.matchWord(word.slice(0,-1) + 'u');
  }

  return null;
};


Lookup.guessWordCombination = function(word) {
  if (pali.endswith(word, 'pāḷi'))
    return Lookup.getProcessedUserInput(word.slice(0,-4));

  if (pali.endswith(word, 'vaggo'))
    return Lookup.getProcessedUserInput(word.slice(0,-5));

  if (pali.endswith(word, 'suttaṃ'))
    return Lookup.getProcessedUserInput(word.slice(0,-6));

  if (pali.endswith(word, 'kaṇḍaṃ'))
    return Lookup.getProcessedUserInput(word.slice(0,-6));

  if (pali.startswith(word, 'abhi'))
    return Lookup.getProcessedUserInput(word.slice(4));

  // apariḍayhamāno -> ḍayhamāna
  if (pali.startswith(word, 'apari'))
    return Lookup.getProcessedUserInput(word.slice(5));

  return null;
};


/**
 * Get lookup data of a word from the server by HTTP Get
 * @param {string} word The word to be looked up
 * @param {function} callback The callback function
 * @param {function} failCallback The callback function if http get fails
 * @private
 */
Lookup.httpget = function(word, callback, failCallback) {
  /**
   * Resolve the URL of the word to issue HTTP Get by information provided by
   * groupInfo global variable.
   */

  // FIXME: bad practice: call of groupInfo
  if (!groupInfo) {
    setTimeout(failCallback, 0);
    throw 'groupInfo not ready';
  }

  /**
   * example:
   * groupInfo['version'] = {
   *   'a' : 0,
   *   'b' : 0,
   *   'c' : 1,
   *   ...
   * }
   */
  var version = -1;
  for (var prefix in groupInfo['version']) {
    if (prefix == word[0]) {
      version = groupInfo['version'][prefix];
      break;
    }
  }
  if (version == -1) {
    setTimeout(failCallback, 0);
    console.log('no version (should not happen here)');
    return;
  }

  /**
   * example:
   * groupInfo['dir'] = {
   *   'a' : { ... },
   *   'b' : [],
   *   'c' : [],
   *   ...
   * }
   */
  var path = Lookup.getStaticPath(word, groupInfo['dir'], 'json/', 1);
  if (path == null) {
    setTimeout(failCallback, 0);
    throw 'no path (should not happen here)';
  }

  var encodedPath = path + encodeURIComponent(word) + '.json';
  encodedPath = encodedPath.replace(/%/g, 'Z');

  if (window.location.host == 'siongui.webfactional.com') {
    var url = 'http://siongui.webfactional.com/' +
              encodedPath + '?v=json' + version;
  } else if (window.location.host == 'siongui.pythonanywhere.com') {
    var url = 'http://siongui.pythonanywhere.com/' +
              encodedPath + '?v=json' + version;
  } else {
    var url = 'http://json' + version + '.palidictionary.appspot.com/'
              + encodedPath;
  }

  var xmlhttp = new XMLHttpRequest();

  // @see http://blogs.msdn.com/b/ie/archive/2012/02/09/cors-for-xhr-in-ie10.aspx
  // @see http://bionicspirit.com/blog/2011/03/24/cross-domain-requests.html
  // @see http://msdn.microsoft.com/en-us/library/ie/cc288060(v=vs.85).aspx
  if ("withCredentials" in xmlhttp) {
  } else {
    var xdr = new XDomainRequest();
    xdr.onerror = function(){setTimeout(failCallback, 0);};
    xdr.ontimeout = function(){setTimeout(failCallback, 0);};
    xdr.onload = function() {
      callback(eval('(' + xdr.responseText + ')'));
    };

    xdr.open("get", url);
    xdr.send();
    return;
  }

  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4) {
      if (xmlhttp.status == 200 || xmlhttp.status == 304) {
        callback(eval('(' + xmlhttp.responseText + ')'));
      } else {
        setTimeout(failCallback, 0);
      }
    }
  }

  xmlhttp.open("GET", url, true);
  xmlhttp.send();
};


/**
 * Recursive function to resolve the path of the URL of the word.
 * @param {string} word The word to resolve the path of the URL
 * @param {object|array} dirInfo
 * @param {string} prefix
 * @param {number} digit
 * @return
 * @private
 */
Lookup.getStaticPath = function(word, dirInfo, prefix, digit) {
  if (dirInfo.length == 0) {
    // dirInfo is an empty array
    return prefix;
  } else if (typeof dirInfo == 'object') {
    // dirInfo is an object containing prefixes of words.
    for (var key in dirInfo) {
      // if word startswith key
      if (word.indexOf(key) == 0 && key.length == digit) {
        var suffix = encodeURIComponent(key) + '/';

        if (word.length == digit) {
          if (dirInfo[key].length == 0) return (prefix + suffix);
          return (prefix + suffix + suffix);
        }
        // recursively call self to resolve path
        return Lookup.getStaticPath(word, dirInfo[key],
                                  prefix + suffix, digit + 1);
      }
    }
    return null;
  } else {
    throw 'only {...} or [] is allowed!';
  }
};

'use strict';

/* Services */


angular.module('pali.guess', []).
  factory('paliGuess', ['paliIndexes', function(paliIndexes) {
    /**
     * The string ends with suffix?
     * @param {string} string The string ends with suffix?
     * @param {string} suffix The string ends with suffix?
     * @return {boolean} true if string ends with suffix, otherwise false
     */
    var pali = {
      endswith: function(string, suffix) {
        // JavaScript endswith
        // @see http://stackoverflow.com/questions/280634/endswith-in-javascript
        // @see http://www.w3schools.com/jsref/jsref_indexof.asp
        return string.indexOf(suffix, string.length - suffix.length) != -1;
      }
    };

    /**
     * @param {string} word
     * @return {string|null} return null if the word is not valid
     */
    function matchWord(word) {
      if (paliIndexes.isValidPaliWord(word))
        return word;
      else
        return null;
    }

    function guessWordBySuffix(word) {
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
      var endidm = matchWord(word.slice(0,-1));
      // tādiṃ -> tādī
      if (endidm == null)
        endidm = matchWord(word.slice(0,-2) + 'ī');
      if (endidm == null) {
        if (pali.endswith(word, 'smiṃ'))
          return matchWord(word.slice(0,-4));
      }
      return endidm;
    }

    if (pali.endswith(word, 'uṃ')) {
      // pāraguṃ -> pāragū
      var endudm = matchWord(word.slice(0,-2) + 'ū');
      if (endudm == null) {
        if (pali.endswith(word, 'tuṃ')) {
          var endtudm = matchWord(word.slice(0,-3));
          if (endtudm == null) {
            // FIXME: is this correct?
            if (pali.endswith(word, 'etuṃ'))
              return matchWord(word.slice(0,-4) + 'a');
          }
          return endtudm;
        }

        // upavadeyyuṃ -> upavadati
        if (pali.endswith(word, 'eyyuṃ'))
          return matchWord(word.slice(0,-5) + 'ati');
      }
      return endudm;
    }

    if (pali.endswith(word, 'aṃ')) {
      var am = matchWord(word.slice(0,-1));
      // pabbajjaṃ -> pabbajjā
      if (am == null)
        am = matchWord(word.slice(0,-2) + 'ā');
      if (am == null) {
        // muninaṃ -> muni
        if (pali.endswith(word, 'naṃ')) {
          var endnadm = matchWord(word.slice(0,-3));
          if (endnadm == null) {
            if (pali.endswith(word, 'ānaṃ')) {
              var endaanadm = matchWord(word.slice(0,-4) + 'a');
              if (endaanadm == null) {
                // avedhamānaṃ -> avedha
                if (pali.endswith(word, 'mānaṃ'))
                  return matchWord(word.slice(0,-5));
              }
              return endaanadm;
            }
          }
          return endnadm;
        }

        // pavattāraṃ -> pavattar
        if (pali.endswith(word, 'āraṃ'))
          return matchWord(word.slice(0,-4) + 'ar');

        // puccheyyaṃ -> puccheyyaṃ
        // FIXME: -> pucchati? -> puccha? -> pucchana? ...?
        if (pali.endswith(word, 'eyyaṃ'))
          return matchWord(word.slice(0,-5) + 'ati');

        // paccavekkhitabbaṃ -> paccavekkhi
        if (pali.endswith(word, 'tabbaṃ'))
          return matchWord(word.slice(0,-6));
      }
      return am;
    }

    return null;
  }

  if (pali.endswith(word, 'o')) {
    var endo = matchWord(word.slice(0,-1) + 'a');
    if (endo == null)
      endo = matchWord(word.slice(0,-1) + 'i');
    if (endo == null) {
      if (pali.endswith(word, 'no')) {
        // vatthino -> vatthi
        var endno = matchWord(word.slice(0,-2));
        if (endno == null)
          // khemino -> khemī
          return matchWord(word.slice(0,-3) + 'ī');

        return endno;
      }

      if (pali.endswith(word, 'to')) {
        // subhato -> subha
        var endto = matchWord(word.slice(0,-2));
        if (endto == null) {
          // pahitatto -> pahita
          if (pali.endswith(word, 'tto'))
            return matchWord(word.slice(0,-3));

          // nāsato -> nāsā
          if (pali.endswith(word, 'ato'))
            return matchWord(word.slice(0,-3) + 'ā');

          // santhavāto -> santhavati
          if (pali.endswith(word, 'āto'))
            return matchWord(word.slice(0,-3) + 'ati');

          // vissavanto -> vissavati
          if (pali.endswith(word, 'nto'))
            return matchWord(word.slice(0,-3) + 'ti');
        }
        return endto;
      }

      // ñātayo -> ñātaka
      if (pali.endswith(word, 'yo'))
        return matchWord(word.slice(0,-2) + 'ka');

      // antapūro, udarapūro -> anta, udara
      if (pali.endswith(word, 'pūro'))
        return matchWord(word.slice(0,-4));
    }
    return endo;
  }

  if (pali.endswith(word, 'e')) {
    var ende = matchWord(word.slice(0,-1) + 'a');
    // vindate -> vindati
    if (ende == null)
      ende = matchWord(word.slice(0,-1) + 'i');
    // pāṇine -> pāṇin
    if (ende == null)
      ende = matchWord(word.slice(0,-1));
    if (ende == null) {
      // virājaye -> virājati
      if (pali.endswith(word, 'ye'))
        return matchWord(word.slice(0, -2) + 'ti');

      // ogahaṇe -> ogahana
      if (pali.endswith(word, 'ṇe'))
        return matchWord(word.slice(0, -2) + 'na');

      // uṇṇametave -> uṇṇameti
      //if (pali.endswith(word, 'ave'))
      //  return matchWord(word.slice(0, -3) + 'i');
    }
    return ende;
  }

  if (pali.endswith(word, 'ā')) {
    var endaa = matchWord(word.slice(0,-1) + 'a');
    if (endaa == null) {
      if (pali.endswith(word, 'vā')) {
        var endvaa = matchWord(word.slice(0, -2));
        if (endvaa == null) {
          // kasitvā -> kasati
          if (pali.endswith(word, 'itvā'))
            return matchWord(word.slice(0, -4) + 'ati');
        }
        return endvaa;
      }

      // uṭṭhātā -> uṭṭhāna
      // FIXME: -> uṭṭhātar? uṭṭhātu?
      if (pali.endswith(word, 'tā'))
        return matchWord(word.slice(0, -2) + 'na');

      // khantyā -> khanta
      // FIXME: -> khanta? -> khantar? -> khantu?
      if (pali.endswith(word, 'yā')) {
        var endyaa = matchWord(word.slice(0, -2) + 'i');
        if (endyaa == null) {
          // chaviyā -> chavi
          var endiyaa = matchWord(word.slice(0, -2));
          if (endiyaa == null)
            // mānusiyā -> mānusī
            return matchWord(word.slice(0, -3) + 'ī');

          return endiyaa;
        }
        return endyaa;
      }

      // akkhimhā -> akkhi
      if (pali.endswith(word, 'mhā'))
        return matchWord(word.slice(0, -3));

      // vamatekadā -> vamati
      if (pali.endswith(word, 'ekadā'))
        return matchWord(word.slice(0, -5) + 'i');

      // paccavekkhitabbā -> paccavekkhi
      if (pali.endswith(word, 'tabbā'))
        return matchWord(word.slice(0, -5));
    }
    return endaa;
  }

  if (pali.endswith(word, 'ī')) {
    var endii = matchWord(word.slice(0,-1) + 'i');
    if (endii == null) {
      // opilāpehī -> opilāpeti
      if (pali.endswith(word, 'hī'))
        return matchWord(word.slice(0,-2) + 'ti');

      // bhuñjāmī -> bhuñjati
      // FIXME: -> bhuñjaka?
      if (pali.endswith(word, 'āmī'))
        return matchWord(word.slice(0,-3) + 'ati');

      // patirūpakārī -> patirūpa
      if (pali.endswith(word, 'kārī'))
        return matchWord(word.slice(0,-4));
    }
    return endii;
  }

  if (pali.endswith(word, 'a')) {
    // muditañca -> mudita
    if (pali.endswith(word, 'ñca'))
      return matchWord(word.slice(0,-3));

    if (pali.endswith(word, 'ena'))
      return matchWord(word.slice(0,-3) + 'a');

    // example: addasāma -> addasā
    if (pali.endswith(word, 'ma')) {
      var endma = matchWord(word.slice(0,-2));
      if (endma == null) {
        // passāma -> passati
        if (pali.endswith(word, 'āma'))
          return matchWord(word.slice(0,-3) + 'ati');
      }
      return endma;
    }

    // example: pubbeva -> pubba
    if (pali.endswith(word, 'eva'))
      return matchWord(word.slice(0,-3) + 'a');

    // sīhaṃva -> sīha
    if (pali.endswith(word, 'ṃva'))
      return matchWord(word.slice(0,-3));

    if (pali.endswith(word, 'ssa')) {
      var endssa = matchWord(word.slice(0,-3));
      if (endssa == null) {
        // yakanapeḷassa -> yakana
        if (pali.endswith(word, 'peḷassa'))
          return matchWord(word.slice(0,-7));

        // jāyantamassa -> jāyanta
        if (pali.endswith(word, 'massa'))
          return matchWord(word.slice(0,-5));
      }
      return endssa
    }

    if (pali.endswith(word, 'ya')) {
      // siṅghāṇikāya -> siṅghāṇikā
      var endya = matchWord(word.slice(0,-2));
      if (endya == null) {
        // bhāvanāya?
        if (pali.endswith(word, 'āya'))
          return matchWord(word.slice(0,-3) + 'a');

        // atitariya -> atitarati
        if (pali.endswith(word, 'iya'))
          return matchWord(word.slice(0,-3) + 'ati');

        if (pali.endswith(word, 'eyya')) {
          // avajāneyya -> avajānāti
          var endeyya = matchWord(word.slice(0,-4) + 'āti');
          // ropayeyya -> ropaya
          if (endeyya == null)
            return matchWord(word.slice(0,-4) + 'a');
        }
      }
      return endya;
    }

    // bhiyyodha -> bhiyyo
    if (pali.endswith(word, 'dha'))
      return matchWord(word.slice(0,-3));

    if (pali.endswith(word, 'tha')) {
      // nisāmetha -> nisāmeti
      var endtha = matchWord(word.slice(0,-2) + 'i');
      if (endtha == null) {
        // labhetha -> labhati
        if (pali.endswith(word, 'etha'))
          return matchWord(word.slice(0,-4) + 'ati');
      }
      return endtha;
    }

    return null;
  }

  if (pali.endswith(word, 'i')) {
    // vapāmi -> vapati
    // FIXME: -> vapana?
    if (pali.endswith(word, 'āmi')) {
      var endaami = matchWord(word.slice(0,-3) + 'ati');
      // pajānāmi -> pajānāti
      if (endaami == null)
        endaami = matchWord(word.slice(0,-2) + 'ti');
      if (endaami == null) {
        // vicarissāmi -> vicarati
        if (pali.endswith(word, 'issāmi'))
          return matchWord(word.slice(0,-6) + 'ati');
      }
      return endaami;
    }

    // pantāni -> panta
    if (pali.endswith(word, 'āni'))
      return matchWord(word.slice(0,-3) + 'a');

    // vatthūni -> vatthu
    if (pali.endswith(word, 'ūni'))
      return matchWord(word.slice(0,-3) + 'u');

    if (pali.endswith(word, 'hi')) {
      // chaḍḍehi -> chaḍḍeti
      var endhi = matchWord(word.slice(0,-2) + 'ti');
      // navahi -> nava
      endhi = matchWord(word.slice(0,-2));
      if (endhi == null) {
        // *ehi -> *a
        if (pali.endswith(word, 'ehi'))
          return matchWord(word.slice(0,-3) + 'a');

        if (pali.endswith(word, 'ebhi'))
          return matchWord(word.slice(0,-4) + 'a');

        // jālamhi -> jāla
        if (pali.endswith(word, 'mhi'))
          return matchWord(word.slice(0,-3));

        // yathābhūtañhi -> yathābhūta
        if (pali.endswith(word, 'ñhi'))
          return matchWord(word.slice(0,-3));
      }
      return endhi;
    }

    // anumodasi -> anumodati
    if (pali.endswith(word, 'si'))
      return matchWord(word.slice(0,-2) + 'ti');

    // aññepi -> añña
    if (pali.endswith(word, 'epi'))
      return matchWord(word.slice(0,-3) + 'a');

    if (pali.endswith(word, 'mpi')) {
      // tvampi -> tvaṃ
      var endmpi = matchWord(word.slice(0,-3) + 'ṃ');
      if (endmpi == null)
        // catutthampi -> catuttha
        return matchWord(word.slice(0,-3));
      return endmpi;
    }

    // samiñjeti -> samiñjati
    if (pali.endswith(word, 'eti'))
      return matchWord(word.slice(0,-3) + 'ati');

    // honti -> hoti
    if (pali.endswith(word, 'nti'))
      return matchWord(word.slice(0,-3) + 'ti');

    // adassanāti -> adassana
    if (pali.endswith(word, 'āti'))
      return matchWord(word.slice(0,-3) + 'a');

    // jhāyatoti -> jhāyati
    if (pali.endswith(word, 'oti'))
      return matchWord(word.slice(0,-3) + 'i');

    return null;
  }

  if (pali.endswith(word, 'su')) {
    // chasu -> cha
    var endsu = matchWord(word.slice(0,-2));
    if (endsu == null) {
      // example: puttesu -> putta
      if (pali.endswith(word, 'esu'))
        return matchWord(word.slice(0,-3) + 'a');

      // kasassu -> kasati
      // FIXME: -> kasana?
      if (pali.endswith(word, 'ssu')) {
        var endssu = matchWord(word.slice(0,-3) + 'ti');
        if (endssu == null)
          return matchWord(word.slice(0,-3));
        return endssu;
      }
    }
    return endsu;
  }

  // upavadeyyuṃ -> upavadati ???
  if (pali.endswith(word, 'eyyu'))
    return matchWord(word.slice(0,-4) + 'ati');

  if (pali.endswith(word, 'ū')) {
    // bhuñjassū -> bhuñjati
    // FIXME: -> bhuñjaka?
    if (pali.endswith(word, 'ssū'))
      return matchWord(word.slice(0,-3) + 'ti');

    // puthū -> puthu
    return matchWord(word.slice(0,-1) + 'u');
  }

  return null;
    };

    var serviceInstance = { guessWordBySuffix: guessWordBySuffix };
    return serviceInstance;
  }]);

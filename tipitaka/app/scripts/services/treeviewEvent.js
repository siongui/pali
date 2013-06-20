'use strict';

/* Services */


angular.module('pali.treeviewEvent', []).
  factory('tvEvt', ['$location', 'tvServ', function($location, tvServ) {
    function clickPali(xmlFilename) {
      $location.path( tvServ.xmlFilename2Path(xmlFilename) );
    }

    function clickTranslation(xmlFilename, translator, key, locale) {
      var paliTextPath = tvServ.xmlFilename2Path(xmlFilename);
      var path = paliTextPath + '/' + locale + '/' + translator;
      $location.path(path);
    }

    function clickContrastReading(xmlFilename, translator, key, locale) {
      var paliTextPath = tvServ.xmlFilename2Path(xmlFilename);
      var path = paliTextPath + '/' + locale + '/' + translator + '/ContrastReading';
      $location.path(path);
    }

    return {
      clickPali: clickPali,
      clickTranslation: clickTranslation,
      clickContrastReading: clickContrastReading
    };
  }]);

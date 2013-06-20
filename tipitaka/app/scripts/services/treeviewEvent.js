'use strict';

/* Services */


angular.module('pali.treeviewEvent', []).
  factory('tvEvt', ['$location', '$rootScope', 'tvServ',
                    function($location, $rootScope, tvServ) {

    function redirect(path) {
      $location.path( $rootScope.urlLocaleInPath + path );
    }

    function clickPali2(action) {
      // remove leading 'cscd/'
      clickPali( action.slice(5) );
    }

    function clickPali(xmlFilename) {
      redirect( tvServ.xmlFilename2Path(xmlFilename) );
    }

    function clickTranslation(xmlFilename, translator, key, locale) {
      var paliTextPath = tvServ.xmlFilename2Path(xmlFilename);
      var path = paliTextPath + '/' + locale + '/' + translator;
      redirect( path );
    }

    function clickContrastReading(xmlFilename, translator, key, locale) {
      var paliTextPath = tvServ.xmlFilename2Path(xmlFilename);
      var path = paliTextPath + '/' + locale + '/' + translator + '/ContrastReading';
      redirect( path );
    }

    return {
      clickPali: clickPali,
      clickPali2: clickPali2,
      clickTranslation: clickTranslation,
      clickContrastReading: clickContrastReading
    };
  }]);

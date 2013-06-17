'use strict';

/* Wrap all i18n related filter, service, and directive together */
/**
 * There are two ways to do client localization:
 * (1) {{_("text_to_be_translated")}}
 *     - Cannot use because we use similar syntax on server side
 * (2) <element i18n locale="{{locale}}" str="text_to_be_translated">
 *     - "locale" attribute is optional, if no "locale" attribute
 *       then $rootScope.i18nLocale is used.
 */


angular.module('pali.i18n', ['pali.i18nStrings']).

  provider('i18n', function() {
    // reference: https://gist.github.com/Mithrandir0x/3639232
    this.locales =  eval('(' + document.getElementById('locales').innerHTML + ')');

    this.$get = function() {
      var self = this;
      return { locales: self.locales };
    };
  }).

  factory('i18nSetting', ['$rootScope', '$location', '$route', 'i18nserv',
      function($rootScope, $location, $route, i18nserv) {
  /**
   * FIXME: $route is incurred but not used here because if not referenced here,
   *        $route will not be instantiated without ng-view element, hence
   *        no $routeChangeSuccess event.
   * @see https://groups.google.com/forum/?fromgroups#!topic/angular/7K_agNCJ50Q
   */
  // service: handle settings of i18n
    $rootScope.i18nLocale = document.getElementById('locale').innerHTML;

    var locales =  eval('(' + document.getElementById('locales').innerHTML + ')');
    var localeLanguageMapping =  eval('(' + document.getElementById('localeLanguageMapping').innerHTML + ')');
    var langQs = eval('(' + document.getElementById('langQs').innerHTML + ')');

    // set urlLocale
    $rootScope.$on('$routeChangeSuccess', function() {
      var path = $location.path();
      $rootScope.urlLocale = undefined;
      $rootScope.urlLocaleInPath = '';
      angular.forEach(locales, function(locale) {
        if (path.indexOf('/' + locale + '/') === 0) {
          $rootScope.urlLocale = locale;
          $rootScope.urlLocaleInPath = '/' + locale;
          $rootScope.i18nLocale = locale;
        }
      });
    });

    /**
     * currently {{_("i18n_string")}} cannot be used at client side
     * because similar syntax has been used on server side.
     * it's reserved for possible future use
     */
    $rootScope._ = function(str) {
      return i18nserv.gettext(str, $rootScope.i18nLocale);
    };

    return {
      locales: locales,
      localeLanguageMapping: localeLanguageMapping,
      langQs: langQs
    };
  }]).

  run(['$rootScope', 'i18nSetting', function($rootScope, i18nSetting) {
  // initialization code (similar to main)
    // get value passed by server
    $rootScope.i18nLangQs = i18nSetting.langQs;
    $rootScope.locales = i18nSetting.locales;
  }]).

  filter('translate', ['i18nSetting', function(i18nSetting) {
  // filter
    return function(text) {
      if ( i18nSetting.localeLanguageMapping.hasOwnProperty(text) )
        return i18nSetting.localeLanguageMapping[text];
      return text;
    }
  }]).

  factory('i18nserv', ['i18nStrings', function(i18nStrings) {
  // service: for translating texts according to locale

    var i18nStr = i18nStrings.all;

    function gettext(value, locale) {
      if (i18nStr.hasOwnProperty(locale)) {
        if (i18nStr[locale].hasOwnProperty(value)) {
          if (i18nStr[locale][value] !== '' &&
              i18nStr[locale][value] !== null)
            return i18nStr[locale][value];
        }
      }
      return value;
    }

    return { gettext: gettext };
  }]).

  directive('i18n', ['i18nserv', '$rootScope', function(i18nserv, $rootScope) {
  // direcitive
    /**
     * wrap the string to be translated in ELEMENT 
     * with attribute 'i18n', 'str', and 'locale'(optional)
     * example: <ELEMENT i18n str='Home'>Home</ELEMENT>
     *      or  <ELEMENT i18n locale={{locale}} str='Home'>Home</ELEMENT>
     */
    return {
      restrict: 'A',
      link: function(scope, elm, attrs) {
        // if "locale" attribute exists, use it
        attrs.$observe('locale', function() {
          var trText = i18nserv.gettext(attrs.str, $rootScope.i18nLocale);
          if (trText !== attrs.str) elm.html(trText);
        });

        // if there is no "locale" attribute, use $rootScope.i18nLocale
        if (angular.isUndefined(attrs.locale)) {
          $rootScope.$watch('i18nLocale', function() {
            var trText = i18nserv.gettext(attrs.str, $rootScope.i18nLocale);
            if (trText !== attrs.str) elm.html(trText);
          });
        }
      }
    };
  }]).

  factory('parseAcptLangHdr', [function() {
    /**
     * Parse HTTP accept-language header of the user browser.
     * not used in code.
     * @param {string} hdr The string of accpet-language header
     * @return {Array} Array of language-quality pairs
     */
    function getParsedAcceptLangs(hdr) {
      var pairs = hdr.split(',');
      var result = [];
      for (var i=0; i < pairs.length; i++) {
        var pair = pairs[i].split(';');
        if (pair.length == 1) result.push( [pair[0], '1'] );
        else result.push( [pair[0], pair[1].split('=')[1] ] );
      }
      return result;
    }

    return {
      getParsedAcceptLangs: getParsedAcceptLangs
    };

  }]);

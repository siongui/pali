'use strict';


angular.module('paliTipitaka', ['pali.treeview', 'pali.i18n', 'pali.tooltip', 'pali.dropdown', 'pali.wordSearch', 'pali.resizableViews', 'pali.mainview', 'pali.pathInfo', 'pali.treeviewInfo', 'pali.treeviewEvent', 'pali.i18nTpk', 'pali.expOrder']).
  config(['$locationProvider', function($locationProvider) {
    $locationProvider.html5Mode(true);
  }]).
  config(['$routeProvider', 'i18nProvider',
      function($routeProvider, i18nProvider) {

    $routeProvider.when('/', {templateUrl: '/partials/info.html', controller: infoCtrl});

    for (var i=0; i < i18nProvider.locales.length; i++) {
      var locale = i18nProvider.locales[i];
      var pat = '/' + locale + '/';
      $routeProvider.when(pat, {templateUrl: '/partials/info.html', controller: infoCtrl});
    }

    for (var i=0; i < i18nProvider.locales.length; i++) {
      var locale = i18nProvider.locales[i];
      var pat = '/*prefixPath/' + locale + '/:translator/ContrastReading';
      $routeProvider.when(pat, {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    }

    for (var i=0; i < i18nProvider.locales.length; i++) {
      var locale = i18nProvider.locales[i];
      var pat = '/*prefixPath/' + locale + '/:translator';
      $routeProvider.when(pat, {templateUrl: '/partials/canon.html', controller: translationCtrl});
    }

    $routeProvider.when('/*prefixPath', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.otherwise({redirectTo: '/'});
  }]).
  run(['$rootScope', '$location', '$document', 'resizableViews', 'i18nTpkConvert', 'tvEvt',
  function($rootScope, $location, $document, resizableViews, i18nTpkConvert, tvEvt) {
    // initialize resizable views
    resizableViews.initViews('allContainer', 'treeview', 'viewwrapper', 'viewarrow', 'viewseparator', 'mainview');

    // initialize setting
    $rootScope.setting = {
      'showTooltip': true,
      'translateTreeview': true,
      'p2en': true,
      'p2ja': true,
      'p2zh': true,
      'p2vi': true,
      'p2my': true,
      'dicLangOrder': 'hdr' 
    };

    // initialize ng-include
    if ($location.host() === 'localhost') {
      $rootScope.isDevServer = true;
    } else {
      $rootScope.isDevServer = false;
    }

    $rootScope.initOK = true;
    $rootScope.translateNodeText2 = i18nTpkConvert.translateNodeText2;
    $rootScope.translateNodeText3 = i18nTpkConvert.translateNodeText3;
    $rootScope.treeviewTranslatedNodeText = function(text) {
      if ($rootScope.setting.translateTreeview) {
        var trText = i18nTpkConvert.translateNodeText2(text,
                                                       $rootScope.i18nLocale);
        if (trText !== text) return trText;
      }
      return '';
    }

    $rootScope.clickPali = tvEvt.clickPali;
    $rootScope.clickTranslation = tvEvt.clickTranslation;
    $rootScope.clickContrastReading = tvEvt.clickContrastReading;

  }]);

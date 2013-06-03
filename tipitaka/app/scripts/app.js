'use strict';


angular.module('paliTipitaka', ['paliTipitaka.services', 'paliTipitaka.directives', 'pali.i18n', 'pali.tooltip', 'pali.dropdown', 'pali.wordSearch', 'pali.resizableViews', 'pali.mainview', 'pali.pathInfo']).
  config(['$locationProvider', function($locationProvider) {
    $locationProvider.html5Mode(true);
  }]).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.when('/en_US/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.when('/zh_TW/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.when('/zh_CN/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.when('/*prefixPath/en_US/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/*prefixPath/zh_TW/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/*prefixPath/zh_CN/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/*prefixPath/en_US/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/*prefixPath/zh_TW/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/*prefixPath/zh_CN/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/*prefixPath', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.otherwise({redirectTo: '/'});
  }]).
  run(['$rootScope', '$location', '$document', 'resizableViews', 'i18nTpkConvert',
  function($rootScope, $location, $document, resizableViews, i18nTpkConvert) {
    // initialize resizable views
    resizableViews.initViews('allContainer', 'treeview', 'viewwrapper', 'viewarrow', 'viewseparator', 'mainview');

    // initialize setting
    $rootScope.setting = {
      'showTooltip': true,
      'translateTreeview': true,
      'toTraditionalCht': true,
      'p2en': true,
      'p2ja': true,
      'p2zh': true,
      'dicLangOrder': 'hdr' 
    };
    if ($rootScope.i18nLocale === 'zh_CN')
      $rootScope.setting.toTraditionalCht = false;

    // initialize ng-include
    if ($location.host() === 'localhost') {
      $rootScope.isDevServer = true;
    } else {
      $rootScope.isDevServer = false;
    }

    $rootScope.initOK = true;
    $rootScope.translateNodeText2 = i18nTpkConvert.translateNodeText2;
    $rootScope.translateNodeText3 = i18nTpkConvert.translateNodeText3;
  }]);

'use strict';


angular.module('paliTipitaka', ['paliTipitaka.services', 'paliTipitaka.directives', 'pali.i18n', 'pali.xml', 'pali.tooltip', 'pali.dropdown']).
  config(['$locationProvider', function($locationProvider) {
    $locationProvider.html5Mode(true);
  }]).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/:urlLocale/canon/*canonPath/en_US/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/canon/*canonPath/en_US/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/:urlLocale/canon/*canonPath/zh_TW/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/canon/*canonPath/zh_TW/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/:urlLocale/canon/*canonPath/zh_CN/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/canon/*canonPath/zh_CN/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/:urlLocale/canon/*canonPath/en_US/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/canon/*canonPath/en_US/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/:urlLocale/canon/*canonPath/zh_TW/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/canon/*canonPath/zh_TW/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/:urlLocale/canon/*canonPath/zh_CN/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/canon/*canonPath/zh_CN/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/:urlLocale/canon/*canonPath', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.when('/canon/*canonPath', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.when('/:urlLocale/canon', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.when('/canon', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.when('/en_US/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.when('/zh_TW/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.when('/zh_CN/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.when('/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.otherwise({redirectTo: '/'});
  }]).
  run(['$rootScope', '$location', '$document', 'i18nserv', 'resizableViews', function($rootScope, $location, $document, i18nserv, resizableViews) {
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
  }]);

'use strict';


angular.module('paliTipitaka', ['paliTipitaka.services', 'paliTipitaka.directives', 'pali.i18n', 'pali.xml', 'pali.tooltip']).
  config(['$locationProvider', function($locationProvider) {
    $locationProvider.html5Mode(true);
  }]).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.when('/en_US/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.when('/zh_TW/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.when('/zh_CN/', {templateUrl: '/partials/info.html', controller: infoCtrl});
    $routeProvider.when('/canon/*canonPath/zh_TW/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/canon/*canonPath/zh_CN/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/canon/*canonPath/en_US/:translator/ContrastReading', {templateUrl: '/partials/canon.html', controller: contrastReadingCtrl});
    $routeProvider.when('/canon/*canonPath/zh_TW/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/canon/*canonPath/zh_CN/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/canon/*canonPath/en_US/:translator', {templateUrl: '/partials/canon.html', controller: translationCtrl});
    $routeProvider.when('/canon/*canonPath', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.when('/canon', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.otherwise({redirectTo: '/'});
  }]).
  run(['$rootScope', '$location', '$document', 'i18nserv', 'resizableViews', function($rootScope, $location, $document, i18nserv, resizableViews) {
    // initialize resizable views
    resizableViews.initViews('allContainer', 'treeview', 'viewwrapper', 'viewarrow', 'viewseparator', 'mainview');

    // initialize langSelect select element
    $rootScope.langSelect = $rootScope.i18nLocale;
    var firstTime = true;
    $rootScope.$watch('langSelect', function(newValue) {
      if (firstTime) {
        firstTime = false;
        return;
      }
      $document.prop('title', 'Pāḷi Tipiṭaka (' + i18nserv.gettext('Pali Tipitaka', newValue) + ')');
      $location.path('/'+ newValue +'/');
    });

    // initialize setting
    $rootScope.setting = {
      'showTooltip': true,
      'translateTreeview': false,
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
      if ($location.search()['track'] !== 'no') {
        /* Load Google Analytics Code */
        $rootScope.analyticsUrl = '/partials/analytics.html';
      }
    }

    $rootScope.initOK = true;
  }]);

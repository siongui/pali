'use strict';

angular.module('paliDictionary', ['ngCookies', 'pali.wordJson', 'pali.dicBooks', 'paliDictionary.directives', 'pali.filters', 'pali.services', 'pali.i18n', 'pali.dropdown']).
  config(['$locationProvider', function($locationProvider) {
    $locationProvider.html5Mode(true);
  }]).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/', {template: '<br />', controller: noopCtrl});
    $routeProvider.when('/en_US/', {template: '<br />', controller: noopCtrl});
    $routeProvider.when('/zh_TW/', {template: '<br />', controller: noopCtrl});
    $routeProvider.when('/zh_CN/', {template: '<br />', controller: noopCtrl});
    $routeProvider.when('/about', {templateUrl: '/partials/about.html', controller: noopCtrl});
    $routeProvider.when('/browse/noSuchWord', {template: '<br />', controller: noSuchWordCtrl});
    $routeProvider.when('/browse/:firstLetter', {templateUrl: '/partials/prefix.html', controller: prefixCtrl});
    $routeProvider.when('/en_US/browse/:firstLetter', {templateUrl: '/partials/prefix.html', controller: prefixCtrl});
    $routeProvider.when('/zh_TW/browse/:firstLetter', {templateUrl: '/partials/prefix.html', controller: prefixCtrl});
    $routeProvider.when('/zh_CN/browse/:firstLetter', {templateUrl: '/partials/prefix.html', controller: prefixCtrl});
    $routeProvider.when('/browse/:firstLetter/:word', {templateUrl: '/partials/word.html', controller: wordCtrl});
    $routeProvider.when('/en_US/browse/:firstLetter/:word', {templateUrl: '/partials/word.html', controller: wordCtrl});
    $routeProvider.when('/zh_TW/browse/:firstLetter/:word', {templateUrl: '/partials/word.html', controller: wordCtrl});
    $routeProvider.when('/zh_CN/browse/:firstLetter/:word', {templateUrl: '/partials/word.html', controller: wordCtrl});
    $routeProvider.otherwise({redirectTo: '/'});
  }]).
  run(['$rootScope', '$cookieStore', 'dicBooks',
  function($rootScope, $cookieStore, dicBooks) {
    // initialization (similar to main)
    $rootScope.message = '';

    // initialize setting
    $rootScope.isShowSetting = false;

    var setting = $cookieStore.get('setting');
    if (setting) {
      $rootScope.setting = setting;
    } else {
      $rootScope.setting = {
        'isShowWordPreview': false,
        'toTraditionalCht': true,
        'p2en': true,
        'p2ja': true,
        'p2zh': true,
        'dicLangOrder': 'hdr' 
      };
    }

    $rootScope.$watch('setting.isShowWordPreview', storeSettingInCookie);
    $rootScope.$watch('setting.toTraditionalCht', storeSettingInCookie);
    $rootScope.$watch('setting.p2en', storeSettingInCookie);
    $rootScope.$watch('setting.p2ja', storeSettingInCookie);
    $rootScope.$watch('setting.p2zh', storeSettingInCookie);
    $rootScope.$watch('setting.dicLangOrder', storeSettingInCookie);
    function storeSettingInCookie() { $cookieStore.put('setting', $rootScope.setting); }

    if ($rootScope.i18nLocale === 'zh_CN')
      $rootScope.setting.toTraditionalCht = false;

    // get width of document
    $rootScope.docWidth = document.getElementById('allContainer').offsetWidth;

    $rootScope.booksIndex = dicBooks.dicIndex;
  }]);

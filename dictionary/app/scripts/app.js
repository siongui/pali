'use strict';

angular.module('paliDictionary', ['ngCookies', 'pali.wordJson', 'pali.dicBooks', 'pali.dropdown', 'pali.expOrder', 'pali.wordSearch', 'paliDictionary.directives', 'pali.i18n']).
  config(['$locationProvider', function($locationProvider) {
    $locationProvider.html5Mode(true);
  }]).
  config(['$routeProvider', 'i18nProvider',
      function($routeProvider, i18nProvider) {

    $routeProvider.when('/', {template: '<br />', controller: noopCtrl});

    for (var i=0; i < i18nProvider.locales.length; i++) {
      var locale = i18nProvider.locales[i];

      var pat1 = '/' + locale + '/';
      $routeProvider.when(pat1, {template: '<br />', controller: noopCtrl});

      var pat2 = '/' + locale + '/browse/:firstLetter';
      $routeProvider.when(pat2, {templateUrl: '/partials/prefix.html', controller: prefixCtrl});

      var pat3 = '/' + locale + '/browse/:firstLetter/:word';
      $routeProvider.when(pat3, {templateUrl: '/partials/word.html', controller: wordCtrl});
    }

    $routeProvider.when('/about', {templateUrl: '/partials/about.html', controller: noopCtrl});
    $routeProvider.when('/browse/noSuchWord', {template: '<br />', controller: noSuchWordCtrl});
    $routeProvider.when('/browse/:firstLetter', {templateUrl: '/partials/prefix.html', controller: prefixCtrl});
    $routeProvider.when('/browse/:firstLetter/:word', {templateUrl: '/partials/word.html', controller: wordCtrl});
    $routeProvider.otherwise({redirectTo: '/'});
  }]).
  run(['$rootScope', '$cookieStore', 'dicBooks',
  function($rootScope, $cookieStore, dicBooks) {
    // initialization (similar to main)
    $rootScope.message = '';

    // initialize setting
    $rootScope.isShowSetting = false;

    var setting = $cookieStore.get('setting2');
    if (setting) {
      $rootScope.setting = setting;
    } else {
      $rootScope.setting = {
        'isShowWordPreview': false,
        'p2en': true,
        'p2ja': true,
        'p2zh': true,
        'p2vi': true,
        'p2my': true,
        'dicLangOrder': 'hdr' 
      };
    }

    $rootScope.$watch('setting.isShowWordPreview', storeSettingInCookie);
    $rootScope.$watch('setting.p2en', storeSettingInCookie);
    $rootScope.$watch('setting.p2ja', storeSettingInCookie);
    $rootScope.$watch('setting.p2zh', storeSettingInCookie);
    $rootScope.$watch('setting.p2vi', storeSettingInCookie);
    $rootScope.$watch('setting.p2my', storeSettingInCookie);
    $rootScope.$watch('setting.dicLangOrder', storeSettingInCookie);
    function storeSettingInCookie() { $cookieStore.put('setting2', $rootScope.setting); }

    // get width of document
    $rootScope.docWidth = document.getElementById('allContainer').offsetWidth;

    $rootScope.booksIndex = dicBooks.dicIndex;
  }]);

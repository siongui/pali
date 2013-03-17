'use strict';


angular.module('paliTipitaka', ['paliTipitaka.services', 'paliTipitaka.directives', 'pali.i18n', 'pali.xml', 'pali.tooltip']).
  config(['$locationProvider', function($locationProvider) {
    $locationProvider.html5Mode(true);
  }]).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/', {templateUrl: '/partials/about.html', controller: noopCtrl});
    $routeProvider.when('/en_US/', {templateUrl: '/partials/about.html', controller: noopCtrl});
    $routeProvider.when('/zh_TW/', {templateUrl: '/partials/about.html', controller: noopCtrl});
    $routeProvider.when('/zh_CN/', {templateUrl: '/partials/about.html', controller: noopCtrl});
    $routeProvider.when('/canon', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.when('/canon/:path1', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.when('/canon/:path1/:path2', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.when('/canon/:path1/:path2/:path3', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.when('/canon/:path1/:path2/:path3/:path4', {templateUrl: '/partials/canon.html', controller: canonCtrl});
    $routeProvider.when('/canon/:path1/:path2/:path3/:path4/:path5', {templateUrl: '/partials/canon.html', controller: canonCtrl});
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
      $rootScope.leftsideUrl = '/partials/devlinks.html';
    } else {
      $rootScope.isDevServer = false;
      $rootScope.leftsideUrl = '/partials/buttons.html';
      if ($location.search()['track'] !== 'no') {
        /* Load Google Analytics Code */
        $rootScope.analyticsUrl = '/partials/analytics.html';
      }
    }
  }]);

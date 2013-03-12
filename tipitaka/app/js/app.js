'use strict';


angular.module('paliTipitaka', ['paliTipitaka.services', 'paliTipitaka.directives', 'pali.i18n', 'pali.xml']).
  config(['$locationProvider', function($locationProvider) {
    $locationProvider.html5Mode(true);
  }]).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/', {template: '<br />', controller: noopCtrl});
    $routeProvider.when('/en_US/', {template: '<br />', controller: noopCtrl});
    $routeProvider.when('/zh_TW/', {template: '<br />', controller: noopCtrl});
    $routeProvider.when('/zh_CN/', {template: '<br />', controller: noopCtrl});
    $routeProvider.otherwise({redirectTo: '/'});
  }]).
  run(['$rootScope', '$location', '$document', 'i18nserv', 'resizableViews', function($rootScope, $location, $document, i18nserv, resizableViews) {
    // initialize resizable views
    resizableViews.initViews('treeview', 'viewwrapper', 'viewarrow', 'viewseparator', 'mainview');

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
      $rootScope.leftsideUrl = '/partials/devlinks.html';
    } else {
      $rootScope.leftsideUrl = '/partials/buttons.html';
      if ($location.search()['track'] !== 'no') {
        /* Load Google Analytics Code */
        $rootScope.analyticsUrl = '/partials/analytics.html';
      }
    }
  }]);

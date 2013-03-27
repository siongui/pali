'use strict';

angular.module('paliDictionary', ['paliDictionary.directives', 'pali.filters', 'pali.services', 'pali.i18n']).
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
  run(['$rootScope', '$location', function($rootScope, $location) {
    // initialization (similar to main)
  }]);

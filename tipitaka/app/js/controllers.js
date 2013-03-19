'use strict';

/* Controllers */


function canonCtrl($scope, $location, tvServ, paliXml, htmlDoc2View) {
  var info = tvServ.getInfo($location.path());
  if (!info.hasOwnProperty('action')) {
    // not leaf node => shows only links
    $scope.nodes = info;
    return;
  }

  // leaf node => contains pali texts
  var action = info['action'];
  var text = info['text'];
  $scope.text = text;
  $scope.isShowLoading = true;

  var promise = paliXml.get(action);
  promise.then(function(htmlDoc) {
    $scope.isShowLoading = false;
    $scope.xmlDoms = htmlDoc2View.getView(htmlDoc);

  }, function(reason) {
    // TODO: error handling here
    $scope.isShowLoading = false;
    console.log(reason);
  });
}
canonCtrl.$inject = ['$scope', '$location', 'tvServ', 'paliXml', 'htmlDoc2View'];


function infoCtrl($scope, $location, i18nTpkServ) {
  // setup translation links
  $scope.showCanon = function(path) { $location.path(path); };
  $scope.showTranslation = function(path, locale, translator) 
    { $location.path(path + '/' + locale + '/' + translator); };
  $scope.showContrastReading = function(path, locale, translator) 
    { $location.path(path + '/' + locale + '/' + translator + '/ContrastReading'); };

  $scope.localeTranslations = i18nTpkServ.getLocaleTranslations();
}
infoCtrl.$inject = ['$scope', '$location', 'i18nTpkServ'];


function translationCtrl($scope, $location, $routeParams, i18nTpkServ, paliXml) {
  $scope.isShowLoading = true;
  var url = i18nTpkServ.getTranslationUrl($location.path(), $routeParams.canonPath, $routeParams.translator);

  paliXml.getUrl(url).then( function(htmlDoc) {
    $scope.isShowLoading = false;
    $scope.xmlDoms = angular.element(htmlDoc.getElementsByTagName('body')[0].cloneNode(true));
  }, function(reason) {
    // TODO: error handling here
    $scope.isShowLoading = false;
    console.log(reason);
  });
}
translationCtrl.$inject = ['$scope', '$location', '$routeParams', 'i18nTpkServ', 'paliXml'];


function contrastReadingCtrl($scope, $location, i18nTpkServ) {
}
contrastReadingCtrl.$inject = ['$scope', '$location', 'i18nTpkServ'];


'use strict';

/* Controllers */


function canonCtrl($scope, $location, tvServ, paliXml, htmlDoc2View, i18nTpkServ) {
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
    $scope.localeTranslations = i18nTpkServ.getI18nLinks(action);
    if (angular.isDefined($scope.localeTranslations))
      $scope.isTranslationAvailableLinks = true;
  }, function(reason) {
    // TODO: error handling here
    $scope.isShowLoading = false;
    console.log(reason);
  });
}
canonCtrl.$inject = ['$scope', '$location', 'tvServ', 'paliXml', 'htmlDoc2View', 'i18nTpkServ'];


function infoCtrl($scope, $location, i18nTpkServ) {
  // setup translation links
  $scope.localeTranslations = i18nTpkServ.getLocaleTranslations();
}
infoCtrl.$inject = ['$scope', '$location', 'i18nTpkServ'];


function translationCtrl($scope, $location, $routeParams, i18nTpkServ, paliXml) {
  $scope.isShowLoading = true;
  var locale = $location.path().split('/').reverse()[1];
  var url = i18nTpkServ.getTranslationXmlUrl($routeParams.canonPath, locale, $routeParams.translator);

  paliXml.getUrl(url).then( function(htmlDoc) {
    $scope.isShowLoading = false;
    $scope.isShowOriPaliLink = true;
    $scope.oriPaliLink = '/canon/' + $routeParams.canonPath;
    $scope.xmlDoms = angular.element(htmlDoc.getElementsByTagName('body')[0].cloneNode(true));
  }, function(reason) {
    // TODO: error handling here
    $scope.isShowLoading = false;
    console.log(reason);
  });
}
translationCtrl.$inject = ['$scope', '$location', '$routeParams', 'i18nTpkServ', 'paliXml'];


function contrastReadingCtrl($scope, $location, $routeParams, $q, tvServ, i18nTpkServ, paliXml, htmlDoc2View) {
  $scope.isShowLoading = true;
  var locale = $location.path().split('/').reverse()[2];
  var url = i18nTpkServ.getTranslationXmlUrl($routeParams.canonPath, locale, $routeParams.translator);

  var info = tvServ.getInfo('/canon/' + $routeParams.canonPath);
  $scope.text = info.text;
  var promise = paliXml.get(info.action);
  var promiseTrans = paliXml.getUrl(url);

  $q.all([promise, promiseTrans]).then( function(htmlDocArray) {
    var oriHtmlDoc = htmlDocArray[0];
    var transHtmlDoc = htmlDocArray[1];
    $scope.xmlDoms = htmlDoc2View.getContrastReadingView(oriHtmlDoc, transHtmlDoc);
    $scope.isShowLoading = false;
    $scope.isShowOriPaliLink = true;
    $scope.oriPaliLink = '/canon/' + $routeParams.canonPath;
  }, function(reason) {
    // TODO: error handling here
    $scope.isShowLoading = false;
    console.log(reason);
  });
}
contrastReadingCtrl.$inject = ['$scope', '$location', '$routeParams', '$q', 'tvServ', 'i18nTpkServ', 'paliXml', 'htmlDoc2View'];


'use strict';

/* Controllers */


function canonCtrl($scope, pathInfo, paliXml, htmlDoc2View, i18nTpkServ) {
  var pInfo = pathInfo.getInfoFromPath();

  $scope.text = pInfo.tvInfo['text'];
  $scope.pathBreadcrumbs = pInfo.tvInfo.pathBreadcrumbs;

  if (!pInfo.tvInfo.hasOwnProperty('action')) {
    // not leaf node => shows only links
    $scope.nodes = pInfo.tvInfo.childNodesInfo;
    return;
  }

  // leaf node => contains pali texts
  $scope.isShowLoading = true;
  paliXml.get(pInfo.tvInfo['action']).then(function(htmlDoc) {
    $scope.isShowLoading = false;
    $scope.xmlDoms = htmlDoc2View.getView(htmlDoc);
    $scope.localeTranslations = i18nTpkServ.getI18nLinks(pInfo.tvInfo['action']);
    if (angular.isDefined($scope.localeTranslations)) {
      $scope.isTranslationAvailableLinks = true;
    }
  }, function(reason) {
    // TODO: error handling here
    $scope.isShowLoading = false;
    console.log(reason);
  });
}
canonCtrl.$inject = ['$scope', 'pathInfo', 'paliXml', 'htmlDoc2View', 'i18nTpkServ'];


function infoCtrl($scope, $http, $compile) {
  var data = { userLocale: $scope.i18nLocale };
  if (angular.isDefined($scope.urlLocale))
    data.urlLocale = $scope.urlLocale;
  else
    data.urlLocale = null;

  $http.post('/html/MainPage', JSON.stringify(data)).
    success(function(data, status, headers, config) {
      $scope.xmlDoms = $compile(data)($scope);
    }).error(function(data, status, headers, config) {
      // TODO: error handling
    });
}
infoCtrl.$inject = ['$scope', '$http', '$compile'];


function translationCtrl($scope, pathInfo, paliXml) {
  $scope.isShowLoading = true;

  var pInfo = pathInfo.getInfoFromPath();
  $scope.text = pInfo.tvInfo['text'];
  $scope.pathBreadcrumbs = pInfo.tvInfo.pathBreadcrumbs;
  $scope.paliTextPath = pInfo.paliTextPath;
  $scope.xmlLocaleTranslationInfo = pInfo.xmlLocaleTranslationInfo;

  paliXml.getUrl(pInfo.translationUrl).then( function(htmlDoc) {
    $scope.isShowLoading = false;
    $scope.isShowOriPaliLink = true;
    $scope.xmlDoms = angular.element(htmlDoc.getElementsByTagName('body')[0].cloneNode(true));
  }, function(reason) {
    // TODO: error handling here
    $scope.isShowLoading = false;
    console.log(reason);
  });
}
translationCtrl.$inject = ['$scope', 'pathInfo', 'paliXml'];


function contrastReadingCtrl($scope, $q, pathInfo, paliXml, htmlDoc2View) {
  $scope.isShowLoading = true;

  var pInfo = pathInfo.getInfoFromPath();
  $scope.text = pInfo.tvInfo['text'];
  $scope.pathBreadcrumbs = pInfo.tvInfo.pathBreadcrumbs;
  $scope.paliTextPath = pInfo.paliTextPath;
  $scope.xmlLocaleTranslationInfo = pInfo.xmlLocaleTranslationInfo;

  var promise = paliXml.get(pInfo.tvInfo['action']);
  var promiseTrans = paliXml.getUrl(pInfo.translationUrl);

  $q.all([promise, promiseTrans]).then( function(htmlDocArray) {
    var oriHtmlDoc = htmlDocArray[0];
    var transHtmlDoc = htmlDocArray[1];
    $scope.xmlDoms = htmlDoc2View.getContrastReadingView(oriHtmlDoc, transHtmlDoc);
    $scope.isShowLoading = false;
    $scope.isShowOriPaliLink = true;
  }, function(reason) {
    // TODO: error handling here
    $scope.isShowLoading = false;
    console.log(reason);
  });
}
contrastReadingCtrl.$inject = ['$scope', '$q', 'pathInfo', 'paliXml', 'htmlDoc2View'];


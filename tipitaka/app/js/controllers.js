'use strict';

/* Controllers */


function canonCtrl($scope, $http, $compile, pathInfo, htmlDoc2View) {
  var pInfo = pathInfo.getInfoFromPath();

  $scope.text = pInfo.tvInfo['text'];
  $scope.pathBreadcrumbs = pInfo.tvInfo.pathBreadcrumbs;

  if (!pInfo.tvInfo.hasOwnProperty('action')) {
    // not leaf node => shows only links
    $scope.nodes = pInfo.tvInfo.childNodesInfo;
    return;
  }

  // leaf node => contains pali texts
  var data = { userLocale: $scope.i18nLocale,
               reqPath: pInfo.reqPath,
               paliTextPath: pInfo.paliTextPath };
  if (angular.isDefined($scope.urlLocale))
    data.urlLocale = $scope.urlLocale;
  else
    data.urlLocale = null;

  $http.post('/html/CanonPage', JSON.stringify(data)).
    success(function(data, status, headers, config) {
      $scope.isShowLoading = false;
      $scope.xmlDoms = htmlDoc2View.markPaliWord($compile(data.html)($scope));
      document.title = data.title;
    }).error(function(data, status, headers, config) {
      // TODO: error handling
      $scope.isShowLoading = false;
    });
}
canonCtrl.$inject = ['$scope', '$http', '$compile', 'pathInfo', 'htmlDoc2View'];


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


function translationCtrl($scope, $http, pathInfo) {
  $scope.isShowLoading = true;

  var pInfo = pathInfo.getInfoFromPath();
  $scope.text = pInfo.tvInfo['text'];
  $scope.pathBreadcrumbs = pInfo.tvInfo.pathBreadcrumbs;

  var data = { userLocale: $scope.i18nLocale,
               reqPath: pInfo.reqPath,
               paliTextPath: pInfo.paliTextPath,
               translationLocale: pInfo.translationLocale,
               translator: pInfo.translator };
  if (angular.isDefined($scope.urlLocale))
    data.urlLocale = $scope.urlLocale;
  else
    data.urlLocale = null;

  $http.post('/html/TranslationPage', JSON.stringify(data)).
    success(function(data, status, headers, config) {
      $scope.isShowLoading = false;
      $scope.xmlDoms = angular.element(data.html);
      document.title = data.title;
    }).error(function(data, status, headers, config) {
      // TODO: error handling
      $scope.isShowLoading = false;
    });
}
translationCtrl.$inject = ['$scope', '$http', 'pathInfo'];


function contrastReadingCtrl($scope, $http, pathInfo, htmlDoc2View) {
  $scope.isShowLoading = true;

  var pInfo = pathInfo.getInfoFromPath();
  $scope.text = pInfo.tvInfo['text'];
  $scope.pathBreadcrumbs = pInfo.tvInfo.pathBreadcrumbs;

  var data = { userLocale: $scope.i18nLocale,
               reqPath: pInfo.reqPath,
               paliTextPath: pInfo.paliTextPath,
               translationLocale: pInfo.translationLocale,
               translator: pInfo.translator };
  if (angular.isDefined($scope.urlLocale))
    data.urlLocale = $scope.urlLocale;
  else
    data.urlLocale = null;

  $http.post('/html/ContrastReadingPage', JSON.stringify(data)).
    success(function(data, status, headers, config) {
      $scope.isShowLoading = false;
      $scope.xmlDoms = htmlDoc2View.markCRPaliWord(data.html);
      document.title = data.title;
    }).error(function(data, status, headers, config) {
      // TODO: error handling
      $scope.isShowLoading = false;
    });
}
contrastReadingCtrl.$inject = ['$scope', '$http', 'pathInfo', 'htmlDoc2View'];


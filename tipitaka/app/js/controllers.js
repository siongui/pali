'use strict';

/* Controllers */


function canonCtrl($scope, $location, tvServ, paliXml, htmlDoc2View) {
  var info = tvServ.getInfo($location.path());
  if (info.hasOwnProperty('action')) {
    var action = info['action'];
    var text = info['text'];
    $scope.text = text;
  } else {
    $scope.nodes = info;
    return;
  }

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


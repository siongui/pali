'use strict';

/* Controllers */


function canonCtrl($scope, $routeParams, paliXml, htmlDoc2View) {
  var action = $scope.action;
  var text = $scope.text;

  if (angular.isUndefined(action) || angular.isUndefined(text)) {
    console.log($routeParams);
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
canonCtrl.$inject = ['$scope', '$routeParams', 'paliXml', 'htmlDoc2View'];


function noopCtrl($scope) {
}
noopCtrl.$inject = ['$scope'];


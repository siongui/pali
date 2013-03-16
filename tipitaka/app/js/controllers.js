'use strict';

/* Controllers */


function canonCtrl($scope, $location, tvServ, paliXml, htmlDoc2View) {
  var action = $scope.action;
  var text = $scope.text;

  if (angular.isUndefined(action) || angular.isUndefined(text)) {
    var info = tvServ.getInfo($location.path());
    if (info.hasOwnProperty('action')) {
      action = info['action'];
      text = info['text'];
      $scope.action = action;
      $scope.text = action;
    } else {
      $scope.nodes = info;
      return;
    }
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


function noopCtrl($scope) {
}
noopCtrl.$inject = ['$scope'];


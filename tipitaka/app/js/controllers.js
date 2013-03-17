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


function noopCtrl($scope) {
}
noopCtrl.$inject = ['$scope'];


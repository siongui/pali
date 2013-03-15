'use strict';

/* Controllers */


function canonCtrl($scope, paliXml, htmlDoc2View) {
  $scope.mainviewElm = angular.element(document.getElementById('mainview'));
  var action = $scope.action;
  var text = $scope.text;

  if (angular.isUndefined(action) || angular.isUndefined(text))
    return;

  $scope.mainviewElm.children().remove();
  $scope.mainviewElm.append(angular.element('<span>Loading ' + text + ' ...</span>'));

  var promise = paliXml.get(action);
  promise.then(function(htmlDoc) {
    $scope.mainviewElm.children().remove();
    $scope.mainviewElm.append(htmlDoc2View.getView(htmlDoc));

  }, function(reason) {
    // TODO: error handling here
    console.log(reason);
  });
}
canonCtrl.$inject = ['$scope', 'paliXml', 'htmlDoc2View'];


function noopCtrl($scope) {
}
noopCtrl.$inject = ['$scope'];


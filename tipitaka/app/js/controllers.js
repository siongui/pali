'use strict';

/* Controllers */


function mainCtrl($scope, paliXml) {
  $scope.actionHandler = function(action) {
    var promise = paliXml.get(action);

    promise.then(function(htmlDoc) {
      console.log(htmlDoc);

    }, function(reason) {
      // TODO: error handling here
      console.log(reason);
    });
  };
}
mainCtrl.$inject = ['$scope', 'paliXml'];


function noopCtrl($scope) {
}
noopCtrl.$inject = ['$scope'];


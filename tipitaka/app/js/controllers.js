'use strict';

/* Controllers */


function mainCtrl($scope, paliXml) {
  $scope.mainviewElm = angular.element(document.getElementById('mainview'));

  $scope.actionHandler = function(action, text) {
    $scope.mainviewElm.children().remove();
    $scope.mainviewElm.append(angular.element('<span>Loading ' + text + ' ...</span>'));

    var promise = paliXml.get(action);
    promise.then(function(htmlDoc) {
      $scope.mainviewElm.children().remove();
      /* cloneNode() is important. otherwise the second time nothing will show up */
      $scope.mainviewElm.append(angular.element(htmlDoc.getElementsByTagName('body')[0].cloneNode(true)));

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


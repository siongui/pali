'use strict';

/* Controllers */


function mainCtrl($scope, xhrXml) {
  var xsltPath = '/romn/cscd/tipitaka-latn.xsl';

  $scope.actionHandler = function(action) {
    var promise = xhrXml.get(action);

    promise.then(function(responseXML) {
      console.log(responseXML);

    }, function(reason) {
      // TODO: error handling here
      console.log(reason);
    });
  };
}
mainCtrl.$inject = ['$scope', 'xhrXml'];


function noopCtrl($scope) {
}
noopCtrl.$inject = ['$scope'];


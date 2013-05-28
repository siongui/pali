'use strict';

/* Services */


angular.module('pali.wordJson', []).
  factory('paliWordJson', ['$http', function($http) {

    function get(word) {
      var url = '/wordJson/' + word;
      return $http.get(url, {cache: true});
    }

    return { get: get };
  }]);

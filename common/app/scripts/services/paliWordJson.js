'use strict';

/* Services */


angular.module('pali.wordJson', []).
  factory('paliWordJson', ['$http', function($http) {

    function get(word) {
      //var url = '/wordJson/' + word;
      var url = "https://siongui.github.io/xemaauj9k5qn34x88m4h/" + word + ".json";
      return $http.get(url, {cache: true});
    }

    return { get: get };
  }]);

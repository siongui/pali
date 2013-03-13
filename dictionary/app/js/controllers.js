'use strict';

/* Controllers */


function mainCtrl($scope) {
  $scope.message = '';

  // initialize setting
  $scope.isShowSetting = false;
  $scope.setting = {
    'isShowWordPreview': false,
    'toTraditionalCht': true,
    'p2en': true,
    'p2ja': true,
    'p2zh': true,
    'dicLangOrder': 'hdr' 
  };

  if ($scope.i18nLocale === 'zh_CN')
    $scope.setting.toTraditionalCht = false;
}
mainCtrl.$inject = ['$scope'];


function noopCtrl($scope, i18nserv) {
  $scope.$parent.message = '';
  // set title of html document
  // FIXME: don't access document directly?
  document.title = i18nserv.gettext('Pali Dictionary | Pāli to English, Chinese, Japanese Dictionary', $scope.i18nLocale);
}
noopCtrl.$inject = ['$scope', 'i18nserv'];


function noSuchWordCtrl($scope) {
  $scope.$parent.message = 'noSuchWord';
}
noSuchWordCtrl.$inject = ['$scope'];


function prefixCtrl($scope, $route, paliIndexes, i18nserv) {
  $scope.prefix = $route.current.params.firstLetter;
  // set title of html document
  // FIXME: don't access document directly?
  document.title = i18nserv.gettext('Words Start with', $scope.i18nLocale) + ' ' + $scope.prefix + ' - '
    + i18nserv.gettext('Pali Dictionary | Pāli to English, Chinese, Japanese Dictionary', $scope.i18nLocale);

  var words = paliIndexes.getWordsStartsWithPrefix($route.current.params.firstLetter);
  if (angular.isUndefined(words))
    return;
  else
    $scope.isShowPrefixWords = true;

  var wordGroups = []
  for (var i = 0 ; i< words.length; i++ ) {
    if ( i % 4 == 0) wordGroups.push([]);
    wordGroups[wordGroups.length -1].push(words[i]);
  }
  $scope.wordGroups = wordGroups;
}
prefixCtrl.$inject = ['$scope', '$route', 'paliIndexes', 'i18nserv'];


function wordCtrl($scope, $route, paliJson, i18nserv) {
  $scope.$parent.message = 'lookingUp';
  $scope.data = undefined;
  $scope.word = $route.current.params.word;
  // set title of html document
  // FIXME: don't access document directly?
  document.title = $scope.word + ' - ' + i18nserv.gettext('Definition and Meaning', $scope.i18nLocale) + ' - '
    + i18nserv.gettext('Pali Dictionary | Pāli to English, Chinese, Japanese Dictionary', $scope.i18nLocale);

  var promise = paliJson.get($scope.word);
  promise.then(function(jsonData) {
    $scope.$parent.message = '';
    $scope.data = jsonData;
  }, function(reason) {
    $scope.$parent.message = 'netError';
  });
}
wordCtrl.$inject = ['$scope', '$route', 'paliJson', 'i18nserv'];

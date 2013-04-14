'use strict';

/* Directives */


angular.module('paliDictionary.directives', ['paliDictionary.directives-event']).
  directive('paliInput', function() {
    return {
      restrict: 'A',
      templateUrl: '/partials/input.html',
      replace: true,
      scope: {setting: '='},
      link: function(scope, elm, attrs) {
        scope.prefix = function(word, paliWord) {
          return word.content.slice(0, paliWord.length);
        };
        scope.suffix = function(word, paliWord) {
          return word.content.slice(paliWord.length);
        };
      }
    };
  }).
  directive('autoSuggest', ['paliIndexes', '$location', 'paliJson', 'palidic', '$rootScope', function(paliIndexes, $location, paliJson, palidic, $rootScope) {
    return {
      restrict: 'A',
      require: 'ngModel',
      link: function(scope, elm, attrs, ngModelCtrl) {
        // initialize index for selection of suggested words
        var currentSelectedWordIndex = -1;
        var paths = $location.path().split('/');
        if (paths.length === 4) scope[attrs.ngModel] = paths[3];

        scope.lookupWord = function(opt_dicWordExp) {
          $rootScope.opt_dicWordExp = opt_dicWordExp;
          // Remove whitespace in the beginning and end of user input string
          var word = ngModelCtrl.$viewValue.replace(/(^\s+)|(\s+$)/g, "");
          if (paliIndexes.isValidPaliWord(word)) {
            $location.path($rootScope.urlLocaleInPath + '/browse/' + word[0] + '/' + word);
          } else {
            $location.path('/browse/noSuchWord');
          }
        };

        scope.addLtr = function(letter, paliWord) {
          if (angular.isUndefined(ngModelCtrl.$viewValue))
            scope[attrs.ngModel] = letter;
          else
            scope[attrs.ngModel] = ngModelCtrl.$viewValue + letter;
          updateSuggestion(scope[attrs.ngModel]);
          elm.focus();
        };

        // set min-width of suggestion menu
        var width = parseInt(elm.css('paddingLeft').replace('px', '')) +
                    parseInt(elm.css('paddingRight').replace('px', '')) +
                    parseInt(elm.css('width').replace('px', ''));
        scope.suggestMenuStyle = {minWidth: width + 'px', maxWidth: elm.prop('offsetWidth') + 'px'};

        // set position of suggestion preview
        var suggestionMenu = angular.element(document.getElementById('suggestion-menu'));
        scope.suggestPreviewStyle = function() {
          return {'left': suggestionMenu.prop('offsetLeft') +
                          suggestionMenu.prop('offsetWidth') +
                          1 + 'px'};
        };

        // set keypad position
        var btnkeypad = angular.element(document.getElementById('btn-keypad'));
        scope.keypadStyle = {'left': btnkeypad.prop('offsetLeft') + 'px'};

        // if mouse enters the suggested word in suggestion menu
        scope.mouseenter = function(word) {
          if (currentSelectedWordIndex > -1 &&
              currentSelectedWordIndex < scope.matchedWords.length) {
            scope.matchedWords[currentSelectedWordIndex].selected = false;
          }
          currentSelectedWordIndex = word.index;
          word.selected = true;

          scope[attrs.ngModel] = word.content;
        };

        // although the name of this function is "click"
        // it is actually a callback function of mousedown event.
        // why not use click event? cuz click fires after blur
        // while mousedown fires before blur
        scope.suggestedWordClicked = function(word) {
          scope.matchedWords = [];
        };

        // If the viewValue of 'paliWord' ngModel changes, i.e.,
        // If user changes the input element value
        ngModelCtrl.$parsers.push(updateSuggestion);

        attrs['paliKeydown'] = {
          'RETURN': function() {
            scope.matchedWords = [];
            scope.lookupWord();
          },
          'ESC': function() {
            if (scope.isShowSuggest() === false) {
              // clear user input if no suggestion menu and ESC key pressed
              scope[attrs.ngModel] = '';
              scope.matchedWords = [];
              return;
            }
            scope[attrs.ngModel] = scope.originalPaliWord;
            scope.matchedWords = [];
          },
          'UP': function() {
            if (scope.isShowSuggest() === false) {
              if (scope[attrs.ngModel] !== '') {
                // If there is no suggestion menu and user input is not empty
                updateSuggestion(ngModelCtrl.$viewValue);
              }
              return;
            }

            currentSelectedWordIndex -= 1;

            if (currentSelectedWordIndex === -2) {
              currentSelectedWordIndex = scope.matchedWords.length -1;
              scope.matchedWords[currentSelectedWordIndex].selected = true;
              scope[attrs.ngModel] = scope.matchedWords[currentSelectedWordIndex].content;
            } else if (currentSelectedWordIndex === -1) {
              scope.matchedWords[currentSelectedWordIndex + 1].selected = false;
              scope[attrs.ngModel] = scope.originalPaliWord;
            } else {
              scope.matchedWords[currentSelectedWordIndex].selected = true;
              scope[attrs.ngModel] = scope.matchedWords[currentSelectedWordIndex].content;
              if (currentSelectedWordIndex < (scope.matchedWords.length -1) )
                scope.matchedWords[currentSelectedWordIndex + 1].selected = false;
            }
          },
          'DOWN': function() {
            if (scope.isShowSuggest() === false) {
              if (scope[attrs.ngModel] !== '') {
                // If there is no suggestion menu and user input is not empty
                updateSuggestion(ngModelCtrl.$viewValue);
              }
              return;
            }

            currentSelectedWordIndex += 1;

            if (currentSelectedWordIndex === scope.matchedWords.length) {
              currentSelectedWordIndex = -1;
              scope[attrs.ngModel] = scope.originalPaliWord;
              scope.matchedWords[scope.matchedWords.length -1].selected = false;
            } else {
              scope.matchedWords[currentSelectedWordIndex].selected = true;
              scope[attrs.ngModel] = scope.matchedWords[currentSelectedWordIndex].content;
              if (currentSelectedWordIndex > 0)
                scope.matchedWords[currentSelectedWordIndex - 1].selected = false;
            }
          }
        };

        function updateSuggestion(viewValue) {
          scope.originalPaliWord = viewValue;

          // convert array of strings to array of objects
          scope.matchedWords = [];
          var index = 0;
          angular.forEach(paliIndexes.prefixMatch(viewValue), function(word) {
            this.push({content: word, selected: false, index: index});
            index++;
          }, scope.matchedWords);

          // reset index
          currentSelectedWordIndex = -1;
        }

        scope.isShowSuggest = function() {
          return angular.isArray(scope.matchedWords)
              && (scope.matchedWords.length > 0)
              && scope.isPaliInputFocused;
        };

        scope.currentSelectedWord = function() {
          if (scope.isShowSuggest()) {
            if (currentSelectedWordIndex !== -1)
              return scope.matchedWords[currentSelectedWordIndex].content;
          }
          return undefined;
        };

        scope.$watch('currentSelectedWord()', function(newValue, oldValue) {
          if (scope.setting.isShowWordPreview && angular.isDefined(newValue)) {
            var promise = paliJson.get(newValue);
            promise.then(function(jsonData) {
              scope.dicWordExps = jsonData;
            }, function(reason) {
              // fail to get json, pass
            });
          }
        });

        scope.shortDicName = palidic.shortName;
        scope.shortDicExp = palidic.shortExp;

        scope.isShowPreview = function() {
          return scope.setting.isShowWordPreview
              && scope.isShowSuggest()
              && angular.isDefined(scope.currentSelectedWord());
        };

        elm[0].focus();
      }
    }
  }]);

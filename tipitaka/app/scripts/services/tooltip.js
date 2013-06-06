'use strict';

/* Services */


angular.module('pali.tooltip', ['pali.mouseEnterLeave', 'pali.wordJson', 'pali.shortExp', 'pali.dicBooks']).
  factory('tooltip', ['$rootScope', '$compile', function($rootScope, $compile) {
    // init tooltip
    var scope = $rootScope.$new(true);
    var isMouseInTooltip = false;
    scope.onmouseenter = function() {
      // mouse enters tooltip
      isMouseInTooltip = true;
    };
    scope.onmouseleave = function() {
      // mouse leaves tooltip
      isMouseInTooltip = false;
      hide();
    };
    var _left = 0;
    var _top = 0;

    // keyword: css long word force line break
    // http://webdesignerwall.com/tutorials/word-wrap-force-text-to-wrap
    // Wait for correct ng-mouseenter and ng-mouseleave
    // https://github.com/angular/angular.js/pull/2134
    var tooltip = $compile('<div style="position: absolute; left: -9999px; background-color: #CCFFFF; border-radius: 10px; font-family: Tahoma, Arial, serif; word-wrap: break-word;" mouseenter="onmouseenter()" mouseleave="onmouseleave()"></div>')(scope);
    tooltip.css('max-width', viewWidth() + 'px');

    // append tooltip to the end of body element
    angular.element(document.getElementsByTagName('body')[0]).append(tooltip);

    // FIXME: why -32 here?
    function viewWidth() { return (window.innerWidth || document.documentElement.clientWidth) - 32; }

    function setContent(content) {
      tooltip.children().remove();
      if (angular.isUndefined(content)) {
        throw 'In tooltip: content undefined!';
      } else if (angular.isString(content)) {
        tooltip.html(content);
      } else {
        tooltip.append(content);
      }
    }

    function setPosition(position) {
      _left = parseInt(position.left.replace('px', ''));
      _top = parseInt(position.top.replace('px', ''));
    }

    function show() {
      // move tooltip to the right (don't cross the right side of browser inner window)
      var _right = _left + tooltip.prop('offsetWidth');
      if ( _right > viewWidth() )
        _left -= (_right - viewWidth());

      tooltip.css('left', _left + 'px');
      tooltip.css('top', _top + 'px');
    }

    function hide() {
      if (!isMouseInTooltip)
        tooltip.css('left', '-9999px');
    }

    var serviceInstance = {
      viewWidth: viewWidth,
      isHidden: function() {return (tooltip.css('left') === '-9999px');},
      getLeftSpace: function() {return _left;},
      getRightSpace: function() {return viewWidth() - _left - tooltip.prop('offsetWidth');},
      setContent: setContent,
      setPosition: setPosition,
      show: show,
      hide: hide
    };
    return serviceInstance;
  }]).

  factory('tooltipHandler', ['$rootScope', '$compile', '$templateCache', 'tooltip', 'paliWordJson', 'dicBooks', 'shortExp', 'wordSearch',
      function($rootScope, $compile, $templateCache, tooltip, paliWordJson, dicBooks, shortExp, wordSearch) {
    // require 'pali.filters' module
    var scope = $rootScope.$new(true);

    scope.booksIndex = dicBooks.dicIndex;
    scope.getShortExp = shortExp.get;

    scope.wordUrl = function(word) {
      if (!angular.isString(word)) return;
      var url = 'http://palidictionary.appspot.com/browse/' + word[0] + '/' + word;
      if ($rootScope.isDevServer) url += '?track=no';
      return url;
    }
    scope.redirectToDicSite = function(url) {
      // http://stackoverflow.com/questions/4907843/open-url-in-new-tab-using-javascript
      window.open(url, '_blank').focus();
    };

    scope.isTooltipHidden = function() {return tooltip.isHidden();};
    scope.$watch('isTooltipHidden()', function() {
      scope.isShowRight = false;
      scope.isNetErr = false;
      scope.currentPossibleWord = undefined;
    });
    scope.$watch('currentPossibleWord', function(newValue) {
      if (angular.isUndefined(newValue)) return;
      scope.isNetErr = false;
      paliWordJson.get(newValue).
        success( function(data, status, headers, config) {
          // get jsonData successfully
          scope.rightDicWordExps = data;
          scope.currentPossibleWordString = newValue;
          if (tooltip.getRightSpace() !== 0)
            scope.currentPossibleWordPreviewStyle = {
              width: tooltip.getRightSpace() + 'px'
            };
          scope.isShowRight = true;
        }).
        error( function(data, status, headers, config) {
          // fail to get word jsonData
          scope.isNetErr = true;
        });
    });

    scope.setting = $rootScope.setting;
    var tooltipContent = $compile($templateCache.get('/partials/tooltipContent.html'))(scope);
    scope.shortExpStyle = {width: Math.floor(tooltip.viewWidth()/2) + 'px'};
    tooltip.setContent(tooltipContent);

    function showContent(word, tooltipPosition) {
      // FIXME: use $rootScope.setting here?
      scope.setting = $rootScope.setting;
      tooltip.setPosition(tooltipPosition);

      // TODO: pre-process word (toLowerCase() etc.) here?
      scope.currentSelectedWord = word;
      scope.isShortExp = false;
      scope.isNoSuchWord = false;
      scope.isNetErr = false;
      scope.isPossibleWords = false;
      scope.isLookingUp = true;

      if (wordSearch.isValidPaliWord(word)) {
        paliWordJson.get(word).
          success( function(data, status, headers, config) {
            // get jsonData successfully
            scope.isLookingUp = false;
            scope.isShortExp = true;
            scope.dicWordExps = data;
            setTimeout(function(){tooltip.show();}, 10);
          }).
          error( function(data, status, headers, config) {
            // fail to get word jsonData
            scope.isLookingUp = false;
            scope.isNetErr = true;
            setTimeout(function(){tooltip.show();}, 10);
          });
      } else {
        var result = wordSearch.possibleWords(word);
        if (result) {
          scope.isLookingUp = false;
          scope.isPossibleWords = true;
          scope.paliWord = result[0];
          scope.possibleWords = result[1];
        } else {
          scope.isLookingUp = false;
          scope.isNoSuchWord = true;
        }
      }
      setTimeout(function(){tooltip.show();}, 10);
    }

    function hideContent() {
      tooltip.hide();
    }

    var serviceInstance = {
      showContent: showContent,
      hideContent: hideContent
    };
    return serviceInstance;
  }]).

  directive('possibleWords', ['wordSearch', function(wordSearch) {
    return {
      restrict: 'A',
      require: 'ngModel',
      link: function(scope, elm, attrs, ngModelCtrl) {
        // If the viewValue of 'paliWord' ngModel changes, i.e.,
        // If user changes the input element value
        ngModelCtrl.$parsers.push(updatePossibleWords);

        function updatePossibleWords(viewValue) {
          scope.possibleWords = wordSearch.autoSuggestedWords(viewValue);
        }
      }
    };
  }]);

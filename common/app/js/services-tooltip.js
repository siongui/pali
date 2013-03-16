'use strict';

/* Services */


angular.module('pali.tooltip', []).
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
      tooltip.css('display', 'none');
    };

    // Wait for correct ng-mouseenter and ng-mouseleave
    // https://github.com/angular/angular.js/pull/2134
    var tooltip = $compile('<div style="position: absolute; display: none; background-color: #CCFFFF; border-radius: 10px; padding: .5em; font-family: Tahoma, Arial, serif;" mouseenter="onmouseenter()" mouseleave="onmouseleave()"></div>')(scope);

    // append tooltip to the end of body element
    angular.element(document.getElementsByTagName('body')[0]).append(tooltip);

    function adjustTooltipRatio() {
      // offsetWidth and offsetHeight will be 0 if no delay
      setTimeout( function() {
        var width = tooltip.prop('offsetWidth');
        var height = tooltip.prop('offsetHeight');
        if (height/width > 2) {
          //console.log('too tall! width: ' + width + ', height: ' + height);
          var newLeft = parseInt(tooltip.css('left').replace('px', '')) - height / 2;
          if (newLeft < 0) newLeft = 0;
          tooltip.css('left', Math.floor(newLeft) + 'px');
        }
      }, 10);
    }

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
      tooltip.css('left', position.left);
      tooltip.css('top', position.top);
    }

    function show(isAdjustRatio) {
      tooltip.css('display', '');
      if (isAdjustRatio !== false)
        adjustTooltipRatio();
    }

    function hide() {
      if (!isMouseInTooltip)
        tooltip.css('display', 'none');
    }

    var serviceInstance = {
      setContent: setContent,
      setPosition: setPosition,
      show: show,
      hide: hide
    };
    return serviceInstance;
  }]).

  factory('tooltipHandler', ['$rootScope', '$compile', '$templateCache', 'tooltip', 'paliJson', 'paliIndexes', 'palidic',
                      function($rootScope, $compile, $templateCache, tooltip, paliJson, paliIndexes, palidic) {
    // require 'pali.filters' module
    var scope = $rootScope.$new(true);
    scope.shortDicName = palidic.shortName;
    scope.shortDicExp = palidic.shortExp;
    scope.wordUrl = function(word) {
      if (!angular.isString(word)) return;
      var url = 'http://palidictionary.appspot.com/browse/' + word[0] + '/' + word;
      if ($rootScope.isDevServer) url += '?track=no';
      return url;
    }
    scope.setting = $rootScope.setting;
    var tooltipContent = $compile($templateCache.get('/partials/tooltipContent.html'))(scope);
    tooltip.setContent(tooltipContent);

    function showContent(word, tooltipPosition) {
      // FIXME: use $rootScope.setting here?
      scope.setting = $rootScope.setting;
      tooltip.setPosition(tooltipPosition);
      tooltip.show(false);

      // TODO: pre-process word (toLowerCase() etc.) here?
      scope.currentSelectedWord = word;
      scope.isShortExp = false;
      scope.isNoSuchWord = false;
      scope.isNetErr = false;
      scope.isPossibleWords = false;
      scope.isLookingUp = true;

      if (paliIndexes.isValidPaliWord(word)) {
        paliJson.get(word).then( function(jsonData) {
          // get jsonData successfully via xhr CORS
          scope.isLookingUp = false;
          scope.isShortExp = true;
          scope.dicWordExps = jsonData;
          tooltip.show(true);
        }, function(reason) {
          // fail to get word via xhr CORS
          scope.isLookingUp = false;
          scope.isNetErr = true;
        });
      } else {
        var possibleWords = paliIndexes.possibleWords(word);
        if (possibleWords) {
          scope.isLookingUp = false;
          scope.isPossibleWords = true;
          scope.possibleWords = possibleWords;
        } else {
          scope.isLookingUp = false;
          scope.isNoSuchWord = true;
        }
      }
      scope.$apply();
    }

    function hideContent() {
      tooltip.hide();
    }

    var serviceInstance = {
      showContent: showContent,
      hideContent: hideContent
    };
    return serviceInstance;
  }]);

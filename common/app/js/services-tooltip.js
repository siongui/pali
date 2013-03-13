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

    function adjustTooltipRatio(content) {
      // offsetWidth and offsetHeight will be 0 if no delay
      setTimeout( function() {
        var width = tooltip.prop('offsetWidth');
        var height = tooltip.prop('offsetHeight');
        if (height/width > 2) {
          //console.log('too tall! width: ' + width + ', height: ' + height);
          var newLeft = parseInt(tooltip.css('left').replace('px', '')) - height / 2;
          if (newLeft < 0) newLeft = 0;
          tooltip.css('left', Math.floor(newLeft) + 'px');
          // append something to force re-drawing tooltip
          tooltip.append(angular.element('<span> </span>'));
        }
      }, 10);
    }

    function show(position, content, isAdjustRatio) {
      // set tooltip position
      tooltip.css('left', position.left);
      tooltip.css('top', position.top);
      // remove content in tooltip
      tooltip.children().remove();
      // set content of tooltip
      if (angular.isUndefined(content)) {
        throw 'In tooltip: content undefined!';
      } else if (angular.isString(content)) {
        tooltip.html(content);
      } else {
        tooltip.append(content);
      }
      // show tooltip
      tooltip.css('display', '');
      if (isAdjustRatio === false)
        return;
      adjustTooltipRatio(content);
    }

    function hide() {
      if (!isMouseInTooltip)
        tooltip.css('display', 'none');
    }

    var serviceInstance = { show: show, hide: hide };
    return serviceInstance;
  }]);

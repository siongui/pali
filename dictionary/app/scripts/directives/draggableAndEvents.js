'use strict';

/* Directives */


angular.module('paliDictionary.directives-event', []).
  directive('paliDraggable', ['$document' , function($document) {
   /**
    * @see https://github.com/siongui/palidictionary/blob/master/static/js/draggable.js
    * @see http://docs.angularjs.org/guide/compiler 
    */ 
   return {
      restrict: 'A',
      link: function(scope, elm, attrs) {
        var startX, startY, initialMouseX, initialMouseY;
        elm.css({position: 'absolute'});

        elm.bind('mousedown', function($event) {
          startX = elm.prop('offsetLeft');
          startY = elm.prop('offsetTop');
          initialMouseX = $event.clientX;
          initialMouseY = $event.clientY;
          $document.bind('mousemove', mousemove);
          $document.bind('mouseup', mouseup);
          return false;
        });
 
        function mousemove($event) {
          var dx = $event.clientX - initialMouseX;
          var dy = $event.clientY - initialMouseY;
          elm.css({
            top:  startY + dy + 'px',
            left: startX + dx + 'px'
          });
          return false;
        }
 
        function mouseup() {
          $document.unbind('mousemove', mousemove);
          $document.unbind('mouseup', mouseup);
        }
      }
    };
  }]).
  directive('paliKeydown', ['$window', function($window) {
    return {
      restrict: 'A',
      link: function(scope, elm, attrs) {
        /**
         * Keys code numbers.
         * @const
         * @enum {number}
         * @private
         */
        var KeyCode = {
          TAB:     9,
          RETURN: 13,
          ESC:    27,
          UP:     38,
          DOWN:   40
        };

        elm.bind('keydown', function(e) {
          if (!angular.isObject(attrs['paliKeydown'])) return;

          var evt = e || $window.event;
          var code = evt.keyCode || evt.which;

          for (var key in KeyCode) {
            if (code === KeyCode[key] &&
                !angular.isUndefined(attrs['paliKeydown'][key]) ) {
              // https://gist.github.com/siongui/a8d9a9003772315e2cba
              if (scope.$root.$$phase)
                scope.$eval(attrs['paliKeydown'][key]);
              else
                scope.$apply(attrs['paliKeydown'][key]);
              break;
            }
          }
        });
      }
    }
  }]).
  directive('paliBlur', function() {
    return {
      restrict: 'A',
      link: function(scope, elm, attrs) {
        elm.bind('blur', function(e) {
          // https://gist.github.com/siongui/a8d9a9003772315e2cba
          if (scope.$root.$$phase)
            scope.$eval(attrs['paliBlur']);
          else
            scope.$apply(attrs['paliBlur']);
        });
      }
    }
  }).
  directive('paliFocus', function() {
    return {
      restrict: 'A',
      link: function(scope, elm, attrs) {
        elm.bind('focus', function(e) {
          // https://gist.github.com/siongui/a8d9a9003772315e2cba
          if (scope.$root.$$phase)
            scope.$eval(attrs['paliFocus']);
          else
            scope.$apply(attrs['paliFocus']);
        });
      }
    }
  });

'use strict';

/* Directives */


angular.module('pali.dropdown', []).
  directive('dropdown', ['$document', function($document) {
  // @see http://stackoverflow.com/questions/14574365/angularjs-dropdown-directive-hide-when-clicked-outisde
    return {
      restrict: 'A',
      replace: true,
      transclude: true,
      scope: {
        classmenu: '@',
        classlink: '@',
        linktext: '@'
      },
      template: '<span ng-init="isShowMenu = false">' +
                  '<a ng-click="isShowMenu = !isShowMenu" ng-class="classlink" href="javascript:void(0);">{{linktext}}</a>' +
                  '<span ng-show="isShowMenu" ng-click="isShowMenu = false" ng-class="classmenu" ng-style="menuStyle" ng-transclude></span>' +
                '</span>',
      link: function(scope, elm, attrs) {
        scope.menuStyle = { 'position': 'absolute' };

        elm.bind('mousedown', function() {
          // mousedown event is called earlier than click event
          scope.menuStyle['left'] =  elm.prop('offsetLeft') + 'px';
          scope.menuStyle['top'] =  (elm.prop('offsetTop') + elm.prop('offsetHeight') + 5) + 'px';
        });

        elm.bind('click', function(event) {
          event.stopPropagation();
        });

        $document.bind('click', function(e) {
          scope.isShowMenu = false;
          scope.$apply();
        });
      }
    };
  }]);

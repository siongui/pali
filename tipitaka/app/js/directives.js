'use strict';

/* Directives */


angular.module('paliTipitaka.directives', []).
  directive('treeview', ['$compile', function($compile) {
    return {
      restrict: 'A',
      link: function(scope, elm, attrs) {
        if (!angular.isObject(treeviewAllJson)) throw 'no treeviewAllJson';

        scope.leafNodeClicked = function(action, text) {
          scope.actionHandler(action, text);
        };

        // show only tipitaka, no commentaries and sub-commentaries
        elm.append(traverseTreeviewData(treeviewAllJson['child'][0]));

        function traverseTreeviewData(node) {
          if (node['child']) {
            // not leaf node, keys: 'text', 'child'
            var element = angular.element('<div class="item"></div>');
            var sign = angular.element('<span>+</span>');
            var text = angular.element('<span class="treeNode">'+ node['text'] + '</span>');
            element.append(sign);
            element.append(text);

            var container = $compile('<div class="childrenContainer"></div>')(scope);
            for (var i=0; i<node['child'].length; i++)
              container.append(traverseTreeviewData(node['child'][i]));
            container.css('display', 'none');

            text.bind('click', function() {
              if (container.css('display') === 'none') {
                container.css('display', '');
                sign.html('-');
              } else {
                container.css('display', 'none');
                sign.html('+');
              }
            });

            if (node['text'] === 'Tipiṭaka (Mūla)') {
               container.css('display', '');
               sign.html('-');
            }

            var all = angular.element('<div></div>');
            all.append(element);
            all.append(container);
            return all;
          } else {
            // leaf node, keys: 'text', 'action'
            var element = $compile('<div class="item" ng-click="leafNodeClicked(' +
                                   "'" + node['action'] + "', '" + node['text'] + "'" +
                                   ')"><span class="treeNode">' +
                                   node['text'] +'</span></div>')(scope);
            return element;
          }
        }
      }
    };
  }]);

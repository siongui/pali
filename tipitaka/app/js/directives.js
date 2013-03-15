'use strict';

/* Directives */


angular.module('paliTipitaka.directives', []).
  directive('treeview', ['$compile', '$location', function($compile, $location) {
    return {
      restrict: 'A',
      link: function(scope, elm, attrs) {
        if (!angular.isObject(treeviewAllJson)) throw 'no treeviewAllJson';

        scope.leafNodeClicked = function(action, text, path) {
          scope.action = action;
          scope.text = text;
          $location.path(path);
        };

        // show only tipitaka, no commentaries and sub-commentaries
        elm.append(traverseTreeviewData(treeviewAllJson['child'][0], '/canon'));

        function traverseTreeviewData(node, path) {
          if (node['child']) {
            // not leaf node, keys: 'text', 'child', 'url'
            var element = angular.element('<div class="item"></div>');
            var sign = angular.element('<span>+</span>');
            var text = angular.element('<span class="treeNode">'+ node['text'] + '</span>');
            element.append(sign);
            element.append(text);

            var childrenContainer = $compile('<div class="childrenContainer"></div>')(scope);
            for (var i=0; i<node['child'].length; i++) {
              var child = node['child'][i];
              var childPath = path + '/' + child['url'];
              childrenContainer.append(traverseTreeviewData(child, childPath));
            }
            childrenContainer.css('display', 'none');

            text.bind('click', function() {
              if (childrenContainer.css('display') === 'none') {
                childrenContainer.css('display', '');
                sign.html('-');
              } else {
                childrenContainer.css('display', 'none');
                sign.html('+');
              }
            });

            if (node['text'] === 'Tipiṭaka (Mūla)') {
               childrenContainer.css('display', '');
               sign.html('-');
            }

            var all = angular.element('<div></div>');
            all.append(element);
            all.append(childrenContainer);
            return all;
          } else {
            // leaf node, keys: 'text', 'action', 'url'
            var element = $compile('<div class="item" ng-click="leafNodeClicked(' +
                                   "'" + node['action'] + "', '" + node['text'] + "', '" + path + "'" +
                                   ')"><span class="treeNode">' +
                                   node['text'] +'</span></div>')(scope);
            return element;
          }
        }
      }
    };
  }]).

  directive('bindXmlDoms', [function() {
    return {
      restrict: 'A',
      link: function(scope, elm, attrs) {
        scope.$watch('xmlDoms', function(newValue) {
          elm.children().remove();
          elm.append(newValue);
        });
      }
    };
  }]);

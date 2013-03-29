'use strict';

/* Directives */


angular.module('paliTipitaka.directives', []).
  directive('treeview', ['$compile', '$location', '$rootScope', 'tvServ', 'i18nTpkServ', function($compile, $location, $rootScope, tvServ, i18nTpkServ) {
    return {
      restrict: 'A',
      link: function(scope, elm, attrs) {

        scope.leafNodeClicked = function(action, text, path) {
          scope.action = action;
          scope.text = text;
          $location.path(path);
        };

        scope.translateNodeText = function(text) {
          return i18nTpkServ.translateText2(text, $rootScope.i18nLocale);
        }

        // show only tipitaka, no commentaries and sub-commentaries
        var tpkNode = traverseTreeviewData(tvServ.tipitakaRootNode, tvServ.tipitakaRootNodePath);
        tpkNode[0].lastChild.style.display = '';
        elm.append(tpkNode);

        function traverseTreeviewData(node, path) {
          var text = node['text'];
          if (node['child']) {
            // not leaf node, keys: 'text', 'child', 'subpath'
            var element = angular.element('<div class="item"></div>');
            var sign = angular.element('<span>+</span>');
            var textElm = $compile('<span class="treeNode">{{ translateNodeText("'+ text + '") }}</span>')(scope);
            element.append(sign);
            element.append(textElm);

            var childrenContainer = $compile('<div class="childrenContainer"></div>')(scope);
            for (var i=0; i<node['child'].length; i++) {
              var child = node['child'][i];
              var childPath = path + '/' + child['subpath'];
              childrenContainer.append(traverseTreeviewData(child, childPath));
            }
            childrenContainer.css('display', 'none');

            textElm.bind('click', function() {
              if (childrenContainer.css('display') === 'none') {
                childrenContainer.css('display', '');
                sign.html('-');
              } else {
                childrenContainer.css('display', 'none');
                sign.html('+');
              }
            });

            var all = angular.element('<div></div>');
            all.append(element);
            all.append(childrenContainer);
            return all;
          } else {
            // leaf node, keys: 'text', 'action', 'subpath'
            var element = $compile('<div class="item" ng-click="leafNodeClicked(' +
                                   "'" + node['action'] + "', '" + text + "', '" + path + "'" +
                                   ')"><span class="treeNode">' +
                                   '{{ translateNodeText("' + text +'") }}</span></div>')(scope);
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

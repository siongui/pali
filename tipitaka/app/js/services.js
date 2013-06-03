'use strict';

/* Services */


angular.module('paliTipitaka.services', ['pali.services', 'pali.filters', 'paliTipitaka.i18nTpk', 'pali.treeviewAllJson']).
  factory('tvServ', ['treeviewAllJson', function(treeviewAllJson) {

    function getInfo(path) {
      // find the node corresponds to the path
      var node = treeviewAllJson.all;
      var pathBreadcrumbs = [];
      var pathArray = path.split('/');
      if (pathArray.length < 2) {
        throw 'impossible path: ' + path;
      } else {
        for (var i=1; i<pathArray.length; i++) {
          var pathi = pathArray[i];
          for (var j=0; j<node['child'].length; j++) {
            if (node['child'][j]['subpath'] === pathi) {
              node = node['child'][j];
              if (pathBreadcrumbs.length === 0)
                var bcPath = '/' + node['subpath'];
              else
                var bcPath = pathBreadcrumbs[pathBreadcrumbs.length - 1].path + '/' + node['subpath'];
              pathBreadcrumbs.push({ text: node['text'], path: bcPath });
              break;
            }
          }
        }
      }

      // node found. build information
      if (node.hasOwnProperty('action')) {
        return {'action': node['action'], 'text': node['text'], 'pathBreadcrumbs': pathBreadcrumbs};
      } else {
        var childNodesInfo = [];
        for (var i=0; i<node['child'].length; i++) {
          childNodesInfo.push({
            'text': node['child'][i]['text'],
            'path': path + '/' + node['child'][i]['subpath']
          });
        }
        return { childNodesInfo: childNodesInfo, pathBreadcrumbs: pathBreadcrumbs, 'text': node['text'] };
      }
    }

    var serviceInstance = {
      getInfo: getInfo,
      allPali: treeviewAllJson.all
    };
    return serviceInstance;
  }]);

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
  }]).

  factory('pathInfo', ['$location', '$routeParams', 'tvServ', function($location, $routeParams, tvServ) {
    function getInfoFromPath() {
      var pathInfo = { reqPath: $location.path() };
      var subpathes = $location.path().split('/');

      // check if this is 'contrast reading' or 'translation' page
      if (angular.isDefined($routeParams.translator)) {
        // This is 'contrast reading' or 'translation' page
        if (subpathes[subpathes.length - 1] === 'ContrastReading') {
          // contrast reading page (contrastReadingCtrl)
          subpathes.pop();
          pathInfo.translator = subpathes.pop(); //pathInfo.translator = $routeParams.translator;
          pathInfo.translationLocale = subpathes.pop();
        } else {
          // translation page (translationCtrl)
          pathInfo.translator = subpathes.pop(); //pathInfo.translator = $routeParams.translator;
          pathInfo.translationLocale = subpathes.pop();
        }
      }

      pathInfo.paliTextPath = '';
      subpathes.shift();
      // get urlLocale if any
      if (subpathes[0] === 'en_US' ||
          subpathes[0] === 'zh_TW' ||
          subpathes[0] === 'zh_CN') {
        pathInfo.urlLocale = subpathes.shift();
      }

      for (var i=0; i<subpathes.length; i++)
        pathInfo.paliTextPath += ('/' + subpathes[i]);

      pathInfo.tvInfo = tvServ.getInfo(pathInfo.paliTextPath);

      return pathInfo;
    }

    return { getInfoFromPath: getInfoFromPath };
  }]);

'use strict';

/* Services */


angular.module('pali.pathInfo', []).
  factory('pathInfo', ['$location', '$routeParams', 'tvServ',
               function($location, $routeParams, tvServ) {
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
          subpathes[0] === 'fr_FR' ||
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

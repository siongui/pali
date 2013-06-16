'use strict';

/* Services */


angular.module('pali.pathInfo', []).
  factory('pathInfo', ['$location', '$routeParams', 'tvServ', 'i18nSetting',
               function($location, $routeParams, tvServ, i18nSetting) {
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
      for (var i=0; i < i18nSetting.locales.length; i++) {
        var locale = i18nSetting.locales[i];
        if (subpathes[0] === locale) {
          pathInfo.urlLocale = subpathes.shift();
          break;
        }
      }

      for (var i=0; i<subpathes.length; i++)
        pathInfo.paliTextPath += ('/' + subpathes[i]);

      pathInfo.tvInfo = tvServ.getInfo(pathInfo.paliTextPath);

      return pathInfo;
    }

    return { getInfoFromPath: getInfoFromPath };
  }]);

'use strict';

/* Services */


angular.module('paliTipitaka.services', ['pali.services', 'pali.filters', 'pali.jqlext', 'paliTipitaka.i18nTpk', 'pali.treeviewAllJson']).
  factory('htmlDoc2View', ['paliString', function(paliString) {
    /**
     * wrap all words in the element
     * @param {DOM element} FIXME: is this HTML or XML dom element?
     */
    function wrapWordsInElement(xmlElement) {
      // 1: element node
      if (xmlElement.nodeType == 1) {
        for (var i=0; i<xmlElement.childNodes.length; i++)
          // recursively call self to process
          wrapWordsInElement(xmlElement.childNodes[i]);
        return;
      }

      // 3: text node
      if (xmlElement.nodeType == 3) {
        var string = xmlElement.nodeValue;
        if (string.replace(/\s*/, '') !== '')
          // string is not whitespace
          xmlElement.parentNode.replaceChild(paliString.toDom(string), xmlElement);
        return;
      }

      console.log('In end of wrapWordsInElement: ');
      console.log(xmlElement);
    }

    /**
     * make pali words lookup-able.
     * @param {jqLite DOM element}
     * @return {jqLite DOM element}
     */
    function markPaliWord(canonPageDom) {
      /* FIXME: cloneNode() here? */
      var pElems = canonPageDom[0].getElementsByTagName('p');
      for (var i=0; i<pElems.length; i++)
        wrapWordsInElement(pElems[i]);
      return canonPageDom;
    }

    function markCRPaliWord(htmlString) {
      /* FIXME: cloneNode() here? */
      var jqLiteDom = angular.element(htmlString);
      var trElems = jqLiteDom[0].getElementsByTagName('tr');
      for (var i=0; i<trElems.length; i++)
        wrapWordsInElement(trElems[i].cells[0]);
      return jqLiteDom;
    }

    var serviceInstance = { markPaliWord: markPaliWord,
                            markCRPaliWord: markCRPaliWord };
    return serviceInstance;
  }]).

  factory('paliString', ['$rootScope', 'jqlext', 'tooltipHandler', 'wordSearch',
                function($rootScope, jqlext, tooltipHandler, wordSearch) {
    // when user's mouse hovers over words, delay a period of time before look up.
    var DELAY_INTERVAL = 1000; // ms

    var isMouseInWord = false;

    function onWordMouseOver(e) {
      isMouseInWord = true;
      this.style.color = 'red';
      if (!$rootScope.setting.showTooltip) return;

      setTimeout(angular.bind(this, function() {
        // 'this' keyword here refers to raw dom element
        if (this.style.color === 'red') {
          // mouse is still on word
          var tooltipPosition = {
            'left': (jqlext.offset(this).left + 'px'),
            'top': (jqlext.offset(this).top + this.offsetHeight + 'px')
          };

          var word = this.innerHTML.toLowerCase();
          tooltipHandler.showContent(word, tooltipPosition);
          $rootScope.$apply();
        }
      }), DELAY_INTERVAL);
    }

    function onWordMouseOut(e) {
      isMouseInWord = false;
      this.style.color = '';
      if (!$rootScope.setting.showTooltip) return;

      setTimeout(angular.bind(this, function() {
        if (!isMouseInWord) {
          tooltipHandler.hideContent();
          $rootScope.$apply();
        }
      }), DELAY_INTERVAL);
    }

    function onWordDbclick(e) {
      var word = this.innerHTML.toLowerCase();
      if (!wordSearch.isValidPaliWord(word)) return;
      var url = 'http://palidictionary.appspot.com/browse/' + word[0] + '/' + word;
      if ($rootScope.isDevServer) url += '?track=no';
      window.open(url);
    }

    function toDom(string) {
      // wrap all pali words in span
      var spanContainer = htmlStr2Dom(markInSpan(string));
      for (var i=0; i<spanContainer.childNodes.length; i++) {
        var node = spanContainer.childNodes[i];
        var tagName = node.tagName;
        if (tagName && tagName.toLowerCase() === 'span') {
          node.onmouseover = onWordMouseOver;
          node.onmouseout = onWordMouseOut;
          node.ondblclick = onWordDbclick;
        }
      }
      return spanContainer;
    }

    function htmlStr2Dom(string) {
      // @see http://stackoverflow.com/questions/3103962/converting-html-string-into-dom-elements
      // @see http://stackoverflow.com/questions/888875/how-to-parse-html-from-javascript-in-firefox
      var spanContainer = document.createElement('span');
      spanContainer.innerHTML = string;
      return spanContainer;
    }

    function markInSpan(string) {
      return string.replace(/[AaBbCcDdEeGgHhIiJjKkLlMmNnOoPpRrSsTtUuVvYyĀāĪīŪūṀṁṂṃŊŋṆṇṄṅÑñṬṭḌḍḶḷ]+/g, '<span>$&</span>');
    }

    var serviceInstance = { toDom: toDom };
    return serviceInstance;
  }]).

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

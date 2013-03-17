'use strict';

/* Services */


angular.module('paliTipitaka.services', ['pali.services', 'pali.filters', 'pali.directives', 'pali.jqlext', 'paliTipitaka.i18nTpk']).
  factory('resizableViews', ['$document', function($document) {
    var leftView, viewwrapper, arrow, separator, rightView;
    var startLeftViewWidth, startRightViewWidth, initialMouseX;

    function initViews(allContainerId, leftViewId, viewwrapperId, arrowId, separatorId, rightViewId) {
      leftView    = angular.element(document.getElementById(leftViewId));
      viewwrapper = angular.element(document.getElementById(viewwrapperId));
      arrow       = angular.element(document.getElementById(arrowId));
      separator   = angular.element(document.getElementById(separatorId));
      rightView   = angular.element(document.getElementById(rightViewId));

      var width = document.getElementById(allContainerId).offsetWidth;
      var leftViewWidth = 250; //px
      var viewwrapperWidth = 7; //px
      var rightViewWidth = width - leftViewWidth - viewwrapperWidth;

      // set default width
      leftView.css(   'width', leftViewWidth    + 'px');
      rightView.css(  'width', rightViewWidth   + 'px');
      viewwrapper.css('width', viewwrapperWidth + 'px');

      arrow.bind('click', function() {
        var lwidth = parseInt(leftView.css('width').replace('px', ''));
        var rwidth = parseInt(rightView.css('width').replace('px', ''));
        leftView.css('width', '0');
        rightView.css('width', lwidth + rwidth + 'px');
      });

      separator.bind('mousedown', function($event) {
        $event.preventDefault();
        startLeftViewWidth = parseInt(leftView.css('width').replace('px', ''));
        startRightViewWidth = parseInt(rightView.css('width').replace('px', ''));
        initialMouseX = $event.clientX;
        $document.bind('mousemove', mousemove);
        $document.bind('mouseup', mouseup);
        return false;
      });
    }

    function mousemove($event) {
      // calculate the delta of mouse cursor movement
      var dx = $event.clientX - initialMouseX;

      var newlw = startLeftViewWidth + dx;
      if (newlw < 0) {
        leftView.css('width', '0');
        rightView.css('width', startLeftViewWidth + startRightViewWidth + 'px');
        return false;
      }

      var newrw = startRightViewWidth - dx;
      if (newrw < 0) {
        leftView.css('width', startLeftViewWidth + startRightViewWidth + 'px');
        rightView.css('width', '0');
        return false;
      }

      leftView.css('width', newlw + 'px');
      rightView.css('width', newrw + 'px');
      return false;
    }

    function mouseup() {
      $document.unbind('mousemove', mousemove);
      $document.unbind('mouseup', mouseup);
    }

    var serviceInstance = { initViews: initViews };
    return serviceInstance;
  }]).

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

    function getView(htmlDoc) {
      /* cloneNode() is important. otherwise the second time nothing will show up */
      var body = htmlDoc.getElementsByTagName('body')[0].cloneNode(true);
      for (var i=0; i<body.childNodes.length; i++) {
        wrapWordsInElement(body.childNodes[i]);
      }

      return angular.element(body);
    }

    var serviceInstance = { getView: getView };
    return serviceInstance;
  }]).

  factory('paliString', ['$rootScope', 'jqlext', 'tooltipHandler', 'paliIndexes',
                function($rootScope, jqlext, tooltipHandler, paliIndexes) {
    // when user's mouse hovers over words, delay a period of time before look up.
    var DELAY_INTERVAL = 1000; // ms

    function onWordMouseOver(e) {
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
        }
      }), DELAY_INTERVAL);
    }

    function onWordMouseOut(e) {
      this.style.color = '';
      if (!$rootScope.setting.showTooltip) return;

      setTimeout(angular.bind(this, function() {
        tooltipHandler.hideContent();
      }), DELAY_INTERVAL);
    }

    function onWordDbclick(e) {
      var word = this.innerHTML.toLowerCase();
      if (!paliIndexes.isValidPaliWord(word)) return;
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

  factory('tvServ', ['i18nTpk', function(i18nTpk) {
    if (!angular.isObject(treeviewAllJson)) throw 'no treeviewAllJson';

    function getInfo(path) {
      // find the node corresponds to the path
      var node;
      var pathArray = path.split('/');
      if (pathArray.length < 2) {
        throw 'impossible path: ' + path;
      } else if (pathArray.length === 2) {
        node = treeviewAllJson['child'][0];
      } else {
        node = treeviewAllJson['child'][0];
        for (var i=2; i<pathArray.length; i++) {
          var pathi = pathArray[i];
          for (var j=0; j<node['child'].length; j++) {
            if (node['child'][j]['url'] === pathi) {
              node = node['child'][j];
              break;
            }
          }
        }
      }

      // node found. build information
      if (node.hasOwnProperty('action')) {
        return {'action': node['action'], 'text': node['text']};
      } else {
        var childNodesInfo = [];
        for (var i=0; i<node['child'].length; i++) {
          childNodesInfo.push({
            'text': node['child'][i]['text'],
            'path': path + '/' + node['child'][i]['url']
          });
        }
        return childNodesInfo;
      }
    }

    function basename(str) { return str.split('/').reverse()[0]; }

    function recursiveBuildPath(node, pathPrefix, xmlName) {
      var path = pathPrefix + '/' + node['url'];
      if (path === '/canon/tipiṭaka (mūla)') path = '/canon';
      if (node.hasOwnProperty('action')) {
        if (basename(node['action']) === xmlName)
          return path;
      } else {
        for (var i=0; i<node['child'].length; i++) {
          var result = recursiveBuildPath(node['child'][i], path, xmlName);
          if (angular.isString(result))
            return result;
        }
      }
    }

    function xmlName2Path(xmlName) {
      var node = treeviewAllJson['child'][0];
      var pathPrefix = '/canon';
      return recursiveBuildPath(node, pathPrefix, xmlName);
    }

    function getLocaleTranslations() {
      var localeTranslations = [];
      for (var locale in i18nTpk.translationInfo) {
        var localeTranslation = {};
        localeTranslation.locale = locale;
        localeTranslation.translations = [];
        for (var xmlName in i18nTpk.translationInfo[locale]['canon']) {
          var translation = {};
          translation.path = xmlName2Path(xmlName);
          translation.canonName = i18nTpk.canonName[xmlName]['pali'];
          translation.translatorCode = i18nTpk.translationInfo[locale]['canon'][xmlName];
          translation.translator =  i18nTpk.translationInfo[locale]['source'][translation.translatorCode][0];
          localeTranslation.translations.push(translation);
        }
        localeTranslations.push(localeTranslation);
      }
      return localeTranslations;
    }

    var serviceInstance = {
      getLocaleTranslations: getLocaleTranslations,
      getInfo: getInfo,
      tipitakaRootNode: treeviewAllJson['child'][0],
      tipitakaRootNodePath: '/canon'
    };
    return serviceInstance;
  }]);

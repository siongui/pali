'use strict';

/* Services */


angular.module('paliTipitaka.services', ['pali.services', 'pali.filters', 'pali.directives']).
  factory('resizableViews', ['$document', function($document) {
    var leftView, viewwrapper, arrow, separator, rightView;
    var startLeftViewWidth, startRightViewWidth, initialMouseX;

    function initViews(leftViewId, viewwrapperId, arrowId, separatorId, rightViewId) {
      leftView    = angular.element(document.getElementById(leftViewId));
      viewwrapper = angular.element(document.getElementById(viewwrapperId));
      arrow       = angular.element(document.getElementById(arrowId));
      separator   = angular.element(document.getElementById(separatorId));
      rightView   = angular.element(document.getElementById(rightViewId));

      // set default width
      var docWidth = $document.prop('width');
      leftView.css('width', '250px');
      rightView.css('width', (docWidth - 300 - 7 - 10) + 'px');
      viewwrapper.css('width', '7px');

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

  factory('paliXml', ['$q', '$cacheFactory', 'xhrXml', 'xslt', function($q, $cacheFactory, xhrXml, xslt) {
    var cache = $cacheFactory('paliXml');
    var xsltPath = '/romn/tipitaka-latn.xsl';

    function get(action) {
      var url = '/romn/' + action;
      var xsltDoc = cache.get(xsltPath);
      if (xsltDoc) {
        var htmlDoc = cache.get(url);
        if (htmlDoc) {
          var deferred = $q.defer();
          deferred.resolve(htmlDoc);
          return deferred.promise;
        } else {
          return xhrXml.get(url).then(function(responseXML) {
            var htmlDoc = xslt.transform(responseXML, xsltDoc);
            cache.put(url, htmlDoc);
            return htmlDoc;
          }, function(reason) {return reason;});
        }
      } else {
        var promise = $q.all([xhrXml.get(xsltPath), xhrXml.get(url)]);
        return promise.then(function(xsltXmlArray) {
          xsltDoc = xsltXmlArray[0];
          cache.put(xsltPath, xsltDoc);
          var htmlDoc = xslt.transform(xsltXmlArray[1], xsltDoc);
          cache.put(url, htmlDoc);
          return htmlDoc;
        }, function(reason) {return reason;});

      }
    }

    var serviceInstance = { get: get };
    return serviceInstance;
  }]).

  factory('xslt', [function() {
    function transform(xmlDoc, xsltDoc) {
      // transform xml using xslt.
      // @see http://www.w3schools.com/xsl/xsl_client.asp
      // @see http://stackoverflow.com/questions/5722410/how-can-i-use-javascript-to-transform-xml-xslt
      var transformedXML;

      if (window.XSLTProcessor) {
        transformedXML = new XSLTProcessor();
        transformedXML.importStylesheet(xsltDoc);
        transformedXML = transformedXML.transformToDocument(xmlDoc);
      } else {
        // for IE
        transformedXML = new ActiveXObject("MSXML2.DOMDocument");
        xmlDoc.transformNodeToObject(xsltDoc, transformedXML);
      }

      return transformedXML;
    }

    var serviceInstance = { transform: transform };
    return serviceInstance;
  }]).

  factory('xhrXml', ['$q', '$rootScope', function($q, $rootScope) {
    function get(url) {
      var deferred = $q.defer();

      var xmlhttp;

      if (window.XMLHttpRequest)
        xmlhttp=new XMLHttpRequest();
      else
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");

      xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4) {
          if (xmlhttp.status == 200) {
            deferred.resolve(xmlhttp.responseXML);
          } else {
            deferred.reject(xmlhttp.status);
          }
          $rootScope.$apply();
        }
      };

      xmlhttp.open("GET", url, true);
      xmlhttp.send();

      return deferred.promise;
    }

    var serviceInstance = { get: get };
    return serviceInstance;
  }]).

  factory('htmlDoc2View', ['paliwords', function(paliwords) {
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
          xmlElement.parentNode.replaceChild(paliwords.toDom(string), xmlElement);
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

  factory('paliwords', ['$rootScope' , '$compile', 'htmlString2Dom', 'tooltip', 'xhrCors', 'paliIndexes', 'palidic',
                function($rootScope, $compile, htmlString2Dom, tooltip, xhrCors, paliIndexes, palidic) {
    // when user's mouse hovers over words, delay a period of time before look up.
    var DELAY_INTERVAL = 1000; // ms

    var noSuchWord = $compile('<span>{{_("No Such Word")}}</span>')($rootScope);

    var scope = $rootScope.$new(true);
    scope.setting = $rootScope.setting;
    $rootScope.$watch('setting', function(newValue) {
      scope.setting = newValue;
    });
    scope.shortDicName = palidic.shortName;
    scope.shortDicExp = palidic.shortExp;
    var shortDicNameExps = $compile('<div><span style="color: GoldenRod; font-weight: bold; font-size: 1.5em; margin: .5em; text-decoration: none;">{{currentSelectedWord}}</span><div ng-repeat="dicWordExp in dicWordExps | removeFuzzyMatch: currentSelectedWord | zhConvert: setting | dicLangSelect: setting | dicOrder: setting"><span style="color: red;">{{shortDicName(dicWordExp)}}</span><span ng-bind-html-unsafe="shortDicExp(dicWordExp)"></span></div></div>')(scope);

    function showShortExplanationInTooltip(rawWordSpanDom) {
      var word = rawWordSpanDom.innerHTML;
      if (paliIndexes.isValidPaliWord(word)) {
        xhrCors.get(word).then( function(jsonData) {
          // get jsonData successfully by xhr CORS
          scope.dicWordExps = jsonData;
          scope.currentSelectedWord = word;
          setTimeout( function() {
            // delay is important here! wait AngularJS to digest!
            tooltip.show(rawWordSpanDom, shortDicNameExps);
          });
        }, function(reason) {
          // fail to get word via xhr CORS
          tooltip.show(rawWordSpanDom, noSuchWord);
        });
        $rootScope.$apply();
      } else {
        // not a word present in indexes
        tooltip.show(rawWordSpanDom, noSuchWord);
      }
    }

    function onWordMouseOver(e) {
      this.style.color = 'red';
      if (!$rootScope.setting.showTooltip) return;

      setTimeout(angular.bind(this, function() {
        // 'this' keyword here refers to raw dom element
        if (this.style.color === 'red') {
          // mouse is still on word
          showShortExplanationInTooltip(this);
        }
      }), DELAY_INTERVAL);
    }

    function onWordMouseOut(e) {
      this.style.color = '';
      if (!$rootScope.setting.showTooltip) return;

      setTimeout(angular.bind(this, function() {
        tooltip.hide();
      }), DELAY_INTERVAL);
    }

    function toDom(string) {
      // wrap all pali words in span
      var spanContainer = htmlString2Dom.string2dom(markInSpan(string));
      for (var i=0; i<spanContainer.childNodes.length; i++) {
        var node = spanContainer.childNodes[i];
        var tagName = node.tagName;
        if (tagName && tagName.toLowerCase() === 'span') {
          node.onmouseover = onWordMouseOver;
          node.onmouseout = onWordMouseOut;
          //node.ondblclick = onWordDbclick;
        }
      }
      return spanContainer;
    }

    function markInSpan(string) {
      return string.replace(/[AaBbCcDdEeGgHhIiJjKkLlMmNnOoPpRrSsTtUuVvYyĀāĪīŪūṀṁṂṃŊŋṆṇṄṅÑñṬṭḌḍḶḷ]+/g, '<span>$&</span>');
    }

    var serviceInstance = { toDom: toDom };
    return serviceInstance;
  }]).

  factory('htmlString2Dom', [function() {
    /**
     * @see http://stackoverflow.com/questions/3103962/converting-html-string-into-dom-elements
     * @see http://stackoverflow.com/questions/888875/how-to-parse-html-from-javascript-in-firefox
     */
    function string2dom(string) {
      var spanContainer = document.createElement('span');
      spanContainer.innerHTML = string;
      return spanContainer;
    }

    var serviceInstance = { string2dom: string2dom };
    return serviceInstance;
  }]).

  factory('offset', [function() {
    function offset(elm) {
      if (window.jQuery)
        return elm.offset();

      var rawDom = elm[0];
      /**
       * getBoundingClientRect method
       * @see http://help.dottoro.com/ljvmcrrn.php
       */
      var _x = 0;
      var _y = 0;
      var body = document.documentElement || document.body;
      var scrollX = window.pageXOffset || body.scrollLeft;
      var scrollY = window.pageYOffset || body.scrollTop;
      _x = rawDom.getBoundingClientRect().left + scrollX;
      _y = rawDom.getBoundingClientRect().top + scrollY;
      return { left: _x, top:_y };
    }

    var serviceInstance = { get: offset };
    return serviceInstance;
  }]).

  factory('tooltip', ['$rootScope', '$compile', 'offset', function($rootScope, $compile, offset) {
    var scope = $rootScope.$new(true);
    var isMouseInTooltip = false;
    scope.onmouseenter = function() {
      // mouse enters tooltip
      isMouseInTooltip = true;
    };
    scope.onmouseleave = function() {
      // mouse leaves tooltip
      isMouseInTooltip = false;
      tooltip.css('display', 'none');
    };
    var tooltip = $compile('<div style="position: absolute; display: none; background-color: #CCFFFF; border-radius: 10px; padding: .5em; font-family: Tahoma, Arial, serif;" mouseenter="onmouseenter()" mouseleave="onmouseleave()"></div>')(scope);

    // append tooltip to the end of body element
    angular.element(document.getElementsByTagName('body')[0]).append(tooltip);

    /**
     * @param {DOM element | angular element}
     * @return {angular element}
     */
    function getAngularElement(element) {
      if (element[0])
        // this is element wrapped with AngularJS jqLite
        return element;
      else
        // raw dom element, wrap it with jqLite
        return angular.element(element);
    }

    function setTooltipPosition(elm) {
      tooltip.css('left', offset.get(elm).left + 'px');
      tooltip.css('top', offset.get(elm).top + elm.prop('offsetHeight') + 'px');
    }

    function adjustTooltipRatio(content) {
      // offsetWidth and offsetHeight will be 0 if no delay
      setTimeout( function() {
        var width = tooltip.prop('offsetWidth');
        var height = tooltip.prop('offsetHeight');
        if (height/width > 2) {
          //console.log('too tall! width: ' + width + ', height: ' + height);
          var newLeft = parseInt(tooltip.css('left').replace('px', '')) - height / 2;
          if (newLeft < 0) newLeft = 0;
          tooltip.css('left', Math.floor(newLeft) + 'px');
          // make browser to re-draw
          tooltip.children().remove();
          if (angular.isUndefined(content)) {
            throw 'In tooltip: content undefined!';
          } else if (angular.isString(content)) {
            tooltip.html(content);
          } else {
            tooltip.append(content);
          }
        }
      }, 10);
    }

    function show(element, content) {
      setTooltipPosition(getAngularElement(element));
      tooltip.children().remove();
      if (angular.isUndefined(content)) {
        throw 'In tooltip: content undefined!';
      } else if (angular.isString(content)) {
        tooltip.html(content);
      } else {
        tooltip.append(content);
      }
      tooltip.css('display', '');
      adjustTooltipRatio(content);
    }

    function hide() {
      if (!isMouseInTooltip)
        tooltip.css('display', 'none');
    }

    var serviceInstance = { show: show, hide: hide };
    return serviceInstance;
  }]);

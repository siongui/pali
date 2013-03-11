'use strict';

/* Services */


angular.module('paliTipitaka.services', []).
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

  factory('htmlDoc2View', ['paliwords', 'htmlString2Dom', function(paliwords, htmlString2Dom) {
    function onWordMouseOver(e) {
      this.style.color = 'red';
//      if (!document.getElementById('showTooltip').checked) return;

//      setTimeout(Lookup.getLookupResult.bind(this),
//                 Lookup.DELAY_INTERVAL);
    }

    function onWordMouseOut(e) {
      this.style.color = '';
//      if (!document.getElementById('showTooltip').checked) return;

//      setTimeout(Lookup.delayedCloseTooltip,
//                 Lookup.DELAY_INTERVAL);
    }

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
        // wrap all words in span here
        var spanContainer = htmlString2Dom.string2dom(paliwords.markInSpan(xmlElement.nodeValue));
        for (var i=0; i<spanContainer.childNodes.length; i++) {
          if (spanContainer.childNodes[i].tagName && spanContainer.childNodes[i].tagName.toLowerCase() === 'span') {
            spanContainer.childNodes[i].onmouseover = onWordMouseOver;
            spanContainer.childNodes[i].onmouseout = onWordMouseOut;
            //spanContainer.childNodes[i].ondblclick = onWordDbclick;
          }
        }

        xmlElement.parentNode.replaceChild(spanContainer, xmlElement);
        return;
      }

      console.log('In end of wrapWordsInElement');
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

  factory('paliwords', [function() {
    function markInSpan(string) {
      return string.replace(/[AaBbCcDdEeGgHhIiJjKkLlMmNnOoPpRrSsTtUuVvYyĀāĪīŪūṀṁṂṃŊŋṆṇṄṅÑñṬṭḌḍḶḷ]+/g, '<span>$&</span>');
    }

    var serviceInstance = { markInSpan: markInSpan };
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
  }]);

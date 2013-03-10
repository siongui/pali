'use strict';

/* Services */


angular.module('paliTipitaka.services', []).
  factory('resizableViews', ['$document', function($document) {
    var leftView, arrow, separator, rightView;
    var startLeftViewWidth, startRightViewWidth, initialMouseX;

    function initViews(leftViewId, arrowId, separatorId, rightViewId) {
      leftView  = angular.element(document.getElementById(leftViewId));
      arrow     = angular.element(document.getElementById(arrowId));
      separator = angular.element(document.getElementById(separatorId));
      rightView = angular.element(document.getElementById(rightViewId));

      // set default width
      var docWidth = $document.prop('width');
      leftView.css('width', '300px');
      rightView.css('width', (docWidth - 300 - 7 -10) + 'px');

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

    var serviceInstance = {
      initViews: initViews
    };

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

    var serviceInstance = {
      get: get
    };

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

    var serviceInstance = {
      transform: transform
    };

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

    var serviceInstance = {
      get: get
    };

    return serviceInstance;
  }]);

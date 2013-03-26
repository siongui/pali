'use strict';

/* Services */


angular.module('pali.xml', []).
  factory('paliXml', ['$q', '$cacheFactory', 'xhrXml', 'xslt', function($q, $cacheFactory, xhrXml, xslt) {
    var cache = $cacheFactory('paliXml');
    var xsltPath = '/romn/cscd/tipitaka-latn.xsl';

    function get(action) {
      var url = '/romn/' + action;
      return getUrl(url);
    }

    function getUrl(url) {
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

    var serviceInstance = { get: get, getUrl: getUrl };
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
  }]);

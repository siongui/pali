/**
 * @fileoverview base utility which provides common functionality
 */


var pali = pali || {}; // Identifies this file as the base.


/**
 * Do nothing. Only to show the dependency.
 *
 * @param {string} name The namespace to include.
 */
pali.require = function(name) {};


/**
 * Cross-browser addEventListener function.
 *
 * @param {DOM element} element The element to add event listener.
 * @param {string} evt The event to be listened.
 * @param {function} fn The callback function when event occurs.
 */
pali.addEventListener = function(element, evt, fn) {
  if (window.addEventListener) {
    /* W3C compliant browser */
    element.addEventListener(evt, fn, false);
  } else {
    /* IE */
    element.attachEvent('on' + evt, fn);
  }
};


/**
 * Cross-browser removeEventListener function.
 *
 * @param {DOM element} element The element to remove event listener.
 * @param {string} evt The event to be un-listened.
 * @param {function} fn The callback function when event occurs.
 */
pali.removeEventListener = function(element, evt, fn) {
  if (window.removeEventListener) {
    /* W3C compliant browser */
    element.removeEventListener(evt, fn, false);
  } else {
    /* IE */
    element.detachEvent('on' + evt, fn);
  }
};


/**
 * The string starts with prefix?
 * @param {string} string The string starts with prefix?
 * @param {string} prefix The string starts with prefix?
 * @return {boolean} true if string starts with prefix, otherwise false
 */
pali.startswith = function(string, prefix) {
  return string.indexOf(prefix) == 0;
};


/**
 * The string ends with suffix?
 * @param {string} string The string ends with suffix?
 * @param {string} suffix The string ends with suffix?
 * @return {boolean} true if string ends with suffix, otherwise false
 */
pali.endswith = function(string, suffix) {
  // JavaScript endswith
  // @see http://stackoverflow.com/questions/280634/endswith-in-javascript
  // @see http://www.w3schools.com/jsref/jsref_indexof.asp
  return string.indexOf(suffix, string.length - suffix.length) != -1;
};


/**
 * JavaScript version of basename in Python os library
 * @param {string} path Example: a/b/c/d
 * @return {string} Example: d
 */
pali.basename = function(path) {
  var array = path.split('/');
  return array[array.length - 1];
}


/**
 * Get xml file via HTTP GET
 * @param {string} url The url of xml file
 * @param {function} callback The callback function to process responseXML
 */
pali.httpGetXml = function(url, callback) {
  var xmlhttp;

  if (window.XMLHttpRequest)
    xmlhttp=new XMLHttpRequest();
  else
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");

  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4) {
      if (xmlhttp.status == 200)
        callback(xmlhttp.responseXML, url);
      else
        alert('fail to get ' + url);
    }
  };

  xmlhttp.open("GET", url, true);
  xmlhttp.send();
};


/**
 * Cross-browser get DOM element position function.
 *
 * @param {DOM element} el The element of which to get the position
 * @return {Object} The top and left position of DOM element
 * @see Dynamically retrieve Html element (X,Y) position with JavaScript
 *      http://stackoverflow.com/questions/442404/dynamically-retrieve-html-element-x-y-position-with-javascript
 * @see Window size and scrolling
 *      http://www.howtocreate.co.uk/tutorials/javascript/browserwindow
 * @see scrollLeft property
 *      http://help.dottoro.com/ljcjgrml.php
 * @see jQuery source code: src/offset.js
 *      https://github.com/jquery/jquery/blob/master/src/offset.js
 * @see How to get iframe scroll position in IE using Java Script?
 *      http://stackoverflow.com/questions/2347491/how-to-get-iframe-scroll-position-in-ie-using-java-script
 */
pali.getOffset = function(el) {
  var oriEl = el;
  var _x = 0;
  var _y = 0;
  var offsetX = 0;
  var offsetY = 0;
  var scrollX = 0;
  var scrollY = 0;

  while( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
    offsetX += el.offsetLeft;
    offsetY += el.offsetTop;
    scrollX += el.scrollLeft;
    scrollY += el.scrollTop;
    el = el.offsetParent;
  }

  /**
   * getBoundingClientRect method
   * @see http://help.dottoro.com/ljvmcrrn.php
   */
  if (oriEl.getBoundingClientRect) {
    /* FIXME: should take margin-left and margin-top into consideration */
    var body = document.documentElement || document.body;
    scrollX = window.pageXOffset || body.scrollLeft;
    scrollY = window.pageYOffset || body.scrollTop;
    _x = oriEl.getBoundingClientRect().left + scrollX;
    _y = oriEl.getBoundingClientRect().top + scrollY;
  } else {
    /* FIXME: code in this else clause maybe not correct? */
    _x = offsetX - scrollX;
    _y = offsetY - scrollY;
  }
  return { top: _y, left: _x };
};


/**
 * check if element is targer or the parent of target
 * @param {DOM Element} target
 * @param {DOM Element} element
 * @return {boolean} Return true if element is target or the parent of target
 *                   else return false.
 */
pali.checkParent = function(target, element) {
  // Chrome and Firefox use parentNode, while Opera use offsetParent
  while(target.parentNode) {
    if( target == element ) return true;
    target = target.parentNode;
  }
  while(target.offsetParent) {
    if( target == element ) return true;
    target = target.offsetParent;
  }
  return false;
};


/**
 * Cross-browser add mouse enter event listener. The mouse enter event only 
 * fired if mouse enters the element, not fired if mouse enters child element(s)
 * of the registered element.
 *
 * @param {DOM element} element The element to add mouse enter event listener.
 * @param {function} fn The callback function when the mouse enter event occurs.
 */
pali.addMouseEnterEventListener = function(element, fn) {
  var wrapper = function(e) {
    var evt = e || window.event;
    var targetElement = evt.target || evt.srcElement;

    // check if mouse moves inside the element, if yes, return.
    var relTarg = evt.relatedTarget || evt.fromElement;
    if (pali.checkParent(relTarg, element)) return;

    setTimeout(fn, 0);
  };

  pali.addEventListener(element, 'mouseover', wrapper);
};


/**
 * Cross-browser add mouse leave event listener. The mouse leave event only 
 * fired if mouse leaves the element, not fired if mouse leaves child element(s)
 * of the registered element.
 *
 * @param {DOM element} element The element to add mouse leave event listener.
 * @param {function} fn The callback function when the mouse leave event occurs.
 */
pali.addMouseLeaveEventListener = function(element, fn) {
  var wrapper = function(e) {
    var evt = e || window.event;
    var targetElement = evt.target || evt.srcElement;

    // check if mouse moves inside the element, if yes, return.
    var relTarg = evt.relatedTarget || evt.toElement;
    if (pali.checkParent(relTarg, element)) return;

    setTimeout(fn, 0);
  };

  pali.addEventListener(element, 'mouseout', wrapper);
};


/**
 * Remove all children of a DOM element (node)
 * @param {DOM element}
 **/
pali.removeAllChildren = function(element) {
  while (element.hasChildNodes())
    element.removeChild(element.lastChild);
};


/**
 * keyword: javascript get url parameter 
 * http://stackoverflow.com/questions/979975/how-to-get-the-value-from-url-parameter
 * http://stackoverflow.com/questions/1403888/get-url-parameter-with-jquery
 * http://papermashup.com/read-url-get-variables-withjavascript/
 */
window['queryURL'] = (function() {
  // This function is anonymous, is executed immediately and the return value is assigned to queryURL
  var queryPairs = {};
  if (!window.location.search) {return queryPairs;}
  var variables = window.location.search.substring(1).split("&");
  for (var i=0; i < variables.length; i++) {
    /* http://stackoverflow.com/questions/747641/what-is-the-difference-between-decodeuricomponent-and-decodeuri */
    var pair = decodeURIComponent(variables[i]).split("=");
    if (pair.length != 2) {console.log('strange query string: '+variables[i]);continue;}
    if (typeof pair[0] == "undefined") {
      continue;
    } else if (typeof pair[0] == null) {
      continue;
    } else {
      queryPairs[pair[0]] = pair[1];
    }
  }
  return queryPairs;
})();


/*                              width: 80                                     */

/**
 * The following code is for adding bind() to IE8.
 * @see https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/Function/bind
if (!Function.prototype.bind) {
  Function.prototype.bind = function (oThis) {
    if (typeof this !== "function") {
      // closest thing possible to the ECMAScript 5 internal IsCallable function
      throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
    }
 
    var aArgs = Array.prototype.slice.call(arguments, 1), 
        fToBind = this, 
        fNOP = function () {},
        fBound = function () {
          return fToBind.apply(this instanceof fNOP && oThis
                                 ? this
                                 : oThis,
                               aArgs.concat(Array.prototype.slice.call(arguments)));
        };
 
    fNOP.prototype = this.prototype;
    fBound.prototype = new fNOP();
 
    return fBound;
  };
}
 */

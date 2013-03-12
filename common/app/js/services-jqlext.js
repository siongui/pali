'use strict';

/* Services */


angular.module('pali.jqlext', []).
  factory('jqlext', [function() {
    function offset(elm) {
      if (window.jQuery)
        return elm.offset();

      var rawDom = toRawDomElement(elm);
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

    function isJqlElement(elm) {
      if (elm[0]) return true;
      else return false;
    }

    function toJqlElement(elm) {
      if (isJqlElement(elm)) return elm;
      else return angular.element(elm);
    }

    function toRawDomElement(elm) {
      if (isJqlElement(elm)) return elm[0];
      else return elm[0];
    }

    var serviceInstance = {
      offset: offset,
      isJqlElement: isJqlElement,
      toJqlElement: toJqlElement,
      toRawDomElement: toRawDomElement
    };
    return serviceInstance;
  }]);

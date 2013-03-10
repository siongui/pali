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
  }]);

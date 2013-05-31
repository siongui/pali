/**
 * @fileoverview Adjust the width of two column views
 */

pali.require('base');

/**
 * Make two column views re-sizable by moving separator or click arrow
 * @param {string} idLeftView
 * @param {string} idArrow
 * @param {string} idSeparator
 * @param {string} idRightView
 */
MovableCol = function(idLeftView, idArrow, idSeparator, idRightView) {
  // @see http://code.google.com/p/pali/source/browse/static/js/draggable.js
  this.leftView_ = document.getElementById(idLeftView);
  if (!this.leftView_) throw 'left view error';

  this.arrow_ = document.getElementById(idArrow);
  if (!this.arrow_) throw 'arrow error';

  this.separator_ = document.getElementById(idSeparator);
  if (!this.separator_) throw 'separator error';

  this.rightView_ = document.getElementById(idRightView);
  if (!this.rightView_) throw 'right view error';

  // minimize left view when the arrow is clicked
  this.arrow_.onclick = function() {
    var lwidth = parseInt(this.leftView_.style.width.replace('px', ''));
    var rwidth = parseInt(this.rightView_.style.width.replace('px', ''));
    rwidth += lwidth;
    this.leftView_.style.width = '0';
    this.rightView_.style.width = rwidth + 'px';
  }.bind(this);

  this.eventHandlers_ = {
    'startMouseDraggable': this.startMouseDraggable.bind(this),
    'mouseDrag'          : this.mouseDrag.bind(this),
    'releaseElement'     : this.releaseElement.bind(this)
  };

  this.startLeftViewWidth_ = undefined;
  this.startrightViewWidth_ = undefined;
  this.initialMouseX_ = undefined;

  // start to listen to mouse down event of draggable element
  pali.addEventListener(this.separator_, 'mousedown',
                    this.eventHandlers_['startMouseDraggable']);
};

MovableCol.prototype.startMouseDraggable = function(e) {
  var evt = e || window.event; // For IE compatible

  if (evt.preventDefault) evt.preventDefault();
  if (evt.stopPropagation) evt.stopPropagation();
  if (window.event) evt.returnValue = false; // IE version of preventDefault

  // In case mouse move and up event have been previously registered
  this.releaseElement();

  this.startLeftViewWidth_ = parseInt(this.leftView_.style.width.replace('px', ''));
  this.startrightViewWidth_ = parseInt(this.rightView_.style.width.replace('px', ''));
  this.initialMouseX_ = evt.clientX;

  pali.addEventListener(document, 'mousemove',
                    this.eventHandlers_['mouseDrag']);
  pali.addEventListener(document, 'mouseup',
                    this.eventHandlers_['releaseElement']);

  return false;
};

MovableCol.prototype.mouseDrag = function(e) {
  var evt = e || window.event; // For IE compatible

  if (evt.preventDefault) evt.preventDefault();
  if (evt.stopPropagation) evt.stopPropagation();
  if (window.event) evt.returnValue = false; // IE version of preventDefault

  // calculate the delta of mouse cursor movement
  var dX = evt.clientX - this.initialMouseX_;

  this.setPosition(dX);

  // suppress the default action of mouse event
  return false;
};

MovableCol.prototype.setPosition = function(dx) {
  var newlw = this.startLeftViewWidth_ + dx;
  if (newlw < 0) {
    this.leftView_.style.width = '0';
    this.rightView_.style.width = this.startLeftViewWidth_ + this.startrightViewWidth_ + 'px';
    return;
  }

  var newrw = this.startrightViewWidth_ - dx;
  if (newrw < 0) {
    this.leftView_.style.width = this.startLeftViewWidth_ + this.startrightViewWidth_ + 'px';
    this.rightView_.style.width = '0';
    return;
  }

  this.leftView_.style.width = newlw + 'px';
  this.rightView_.style.width = newrw + 'px';
};


MovableCol.prototype.releaseElement = function(e) {
  pali.removeEventListener(document, 'mousemove',
                       this.eventHandlers_['mouseDrag']);
  pali.removeEventListener(document, 'mouseup',
                       this.eventHandlers_['releaseElement']);
};

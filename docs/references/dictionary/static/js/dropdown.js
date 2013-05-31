/**
 * @fileoverview Google Code style dropdown menu
 *
 * References:
 * hide popup div when clicking outside the div
 * @see http://www.webdeveloper.com/forum/showthread.php?t=98973
 * Event accessing
 * @see http://www.quirksmode.org/js/events_access.html
 * Event properties
 * @see http://www.quirksmode.org/js/events_properties.html
 */


pali.require("base");


/**
 * Class to make a dropdown menu.
 *
 * @param {string} dropdownId The id of DOM element to toggle menu div.
 * @param {string} dropdownMenuDivId The id of DOM element of menu div.
 * @constructor
 */
pali.Dropdown = function(dropdownId, dropdownMenuDivId) {
  /**
   * The DOM element to toggle menu div.
   * @const
   * @type {DOM Element}
   * @private
   */
  this.dropdown_ = document.getElementById(dropdownId);
  if (!this.dropdown_) throw "pali.Dropdown.NoDropdown";

  /**
   * The DOM element of menu div.
   * @const
   * @type {DOM Element}
   * @private
   */
  this.dropdownMenuDiv_ = document.getElementById(dropdownMenuDivId);
  if (!this.dropdownMenuDiv_) throw "pali.Dropdown.NoDropdownMenuDiv";

  /**
   * Passing this.startMouseDraggable.bind(this) directly to addEventListener
   * and removeEventListener is WRONG because this is actually passing an
   * anonymous function as argument, which has no effect on removeEventListener.
   * The workaround is as below. Use an event handler object to wrap functions.
   * @see http://stackoverflow.com/questions/4386300/javascript-dom-how-to-remove-all-events-of-a-dom-object
   * @see https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Function/bind
   * @const
   * @enum {function}
   */
  this.eventHandlers_ = {
    'onDocumentClick': this.onDocumentClick.bind(this)
  };

  // listen to document click event
  pali.addEventListener(document, 'click',
                        this.eventHandlers_['onDocumentClick']);
};


/**
 * listen to document click event.
 * @param {Object} e The event object passed by browser automatically in W3C-
 *                   compliant browser. For IE, use 'e || window.event'.
 * @private
 */
pali.Dropdown.prototype.onDocumentClick = function(e) {
  var evt = e || window.event; // For IE compatible
  var target = evt.target || evt.srcElement; // For IE compatible

  if (!pali.checkParent(target, this.dropdownMenuDiv_)) {
    // click outside the dropdown menu
    if (pali.checkParent(target, this.dropdown_)) {
      // click outside the dropdown menu
      // AND
      // click on the dropdown link
      if (this.dropdownMenuDiv_.style.display == "none") {
        // click outside the dropdown menu
        // AND
        // click on the dropdown link
        // AND
        // the dropdown menu is invisible
        this.dropdownMenuDiv_.style.left =
          pali.getOffset(this.dropdown_).left +"px";
        this.dropdownMenuDiv_.style.top =
          (pali.getOffset(this.dropdown_).top + this.dropdown_.offsetHeight +3)
          +"px";
        this.dropdownMenuDiv_.style.display = "block";
      } else {
        // click outside the dropdown menu
        // AND
        // click on the dropdown link
        // AND
        // the dropdown menu is visible
        this.dropdownMenuDiv_.style.display = "none";}
    } else {
      // click outside the dropdown menu
      // AND
      // click outside the dropdown link
      this.dropdownMenuDiv_.style.display = "none";
    }
  }
};

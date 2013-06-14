/**
 * @fileoverview Implement a simple custom event library.
 */

/**
 * A simple custom event object for add, dispatch, and remove custom events
 */
var PaliCustomEvent = {};

/**
 * type <-> handlers mapping object
 * example: object[type] = [handler1, handler2, ... ]
 * where type is defined in PaliCustomEvent.CUSTOM_EVENT_TYPE
 * @type {object}
 */
PaliCustomEvent.typeHandlers_ = {};

/**
 * Add custom event
 * @param {string} type The custom event type. The type should be defined in
                        PaliCustomEvent.CUSTOM_EVENT_TYPE before being used to
                        prevent conflicts.
 * @param {function} fn The handler function to be executed when event occurs.
 * @return {boolean} True if success. Otherwise false.
 */
PaliCustomEvent.addCustomEvent = function(type, fn) {
  // TODO: check whether type exist in PaliCustomEvent.CUSTOM_EVENT_TYPE
  if (typeof fn != 'function') {
    console.log('fn is not a function');
    //return false;
  }

  if (typeof PaliCustomEvent.typeHandlers_[type] == 'undefined') {
    // there is no event handler of this type, create empty array to store
    // functions
    PaliCustomEvent.typeHandlers_[type] = [];
  }
  PaliCustomEvent.typeHandlers_[type].push(fn);

  return true;
};

/**
 * Dispatch custom event(s)
 * @param {string} type The custom event type of which events to be executed.
 */
PaliCustomEvent.dispatchCustomEvent = function(type) {
  // TODO: check whether type exist in PaliCustomEvent.CUSTOM_EVENT_TYPE
  if (typeof PaliCustomEvent.typeHandlers_[type] == 'undefined') return;
  for (var i=0; i < PaliCustomEvent.typeHandlers_[type].length; i++) {
    // fire events of 'type'
    try {
      setTimeout(PaliCustomEvent.typeHandlers_[type][i], 0);
    } catch (err) {}
  }
};

/**
 * Remove custom event
 * @param {string} type The custom event type. The type should be defined in
                        PaliCustomEvent.CUSTOM_EVENT_TYPE before being used to
                        prevent conflicts.
 * @param {function} fn The handler function to be removed.
 * @return {boolean} True if success. Otherwise false.
 */
PaliCustomEvent.removeCustomEvent = function(type, fn) {
  // TODO: check whether type exist in PaliCustomEvent.CUSTOM_EVENT_TYPE
  if (typeof PaliCustomEvent.typeHandlers_[type] == 'undefined') return;
  // iterate through all hanlder of the type
  for (var i=0; i < PaliCustomEvent.typeHandlers_[type].length; i++) {
    // remove the handler if matched with input function
    if (fn == PaliCustomEvent.typeHandlers_[type][i])
      PaliCustomEvent.typeHandlers_[type].splice(i, 1);
  }
};

PaliCustomEvent.CUSTOM_EVENT_TYPE = {
  ON_SUGGESTION_MENU_CLOSED: 1
};

"use strict";

// A value with YOUR-... or example.com in it means "not set yet"
function isPlaceholder(value) {
  return !value || /YOUR-|example\.com/i.test(value);
}


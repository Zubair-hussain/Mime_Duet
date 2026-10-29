"use strict";

// A value with YOUR-... or example.com in it means "not set yet"
function isPlaceholder(value) {
  return !value || /YOUR-|example\.com/i.test(value);
}

// Fill in the name and the links from config.js. Links that are not set yet stay hidden.
function applyConfig() {
  const config = window.SITE_CONFIG || {};
  document.querySelectorAll("[data-config-text]").forEach((element) => {
    const value = config[element.dataset.configText];
    if (!isPlaceholder(value)) {
      element.textContent = value;
    }
  });
  document.querySelectorAll("[data-config-href]").forEach((element) => {
    const value = config[element.dataset.configHref];
    if (isPlaceholder(value)) {
      element.hidden = true;
    } else {
      element.href = value;
    }
  });
  document.querySelectorAll("[data-config-mailto]").forEach((element) => {
    const value = config[element.dataset.configMailto];
    if (isPlaceholder(value)) {
      element.hidden = true;
    } else {
      element.href = "mailto:" + value;
    }
  });
  const clone = document.getElementById("code-clone");
  if (clone && !isPlaceholder(config.githubUrl)) {
    const folder = config.githubUrl.split("/").pop();
    clone.textContent = "git clone " + config.githubUrl + ".git\ncd " + folder;
  }
}


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

// Copy buttons for the code samples
function setupCopyButtons() {
  document.querySelectorAll(".copy").forEach((button) => {
    button.addEventListener("click", async () => {
      const source = document.getElementById(button.dataset.copy);
      if (!source || !navigator.clipboard) {
        return;
      }
      await navigator.clipboard.writeText(source.textContent);
      button.textContent = "Copied";
      window.setTimeout(() => {
        button.textContent = "Copy";
      }, 1600);
    });
  });
}

// Fade sections in as they scroll into view
function setupReveal() {
  const items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    items.forEach((item) => item.classList.add("is-visible"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  items.forEach((item) => observer.observe(item));
}


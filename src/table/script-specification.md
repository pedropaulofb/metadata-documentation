<script>
(function () {
  "use strict";

  function enhanceAppearance() {
    var control = document.getElementById("spec-appearance");
    if (!control) return;

    // Reuse Bikeshed's inline theme rules and the local palette together,
    // without duplicating their colors. System restores the original queries.
    var themeRules = [];
    function collectThemeRules(rules) {
      Array.from(rules).forEach(function (rule) {
        if (rule.type === CSSRule.MEDIA_RULE) {
          var match = rule.media.mediaText.match(/^\(prefers-color-scheme:\s*(light|dark)\)$/);
          if (match) {
            themeRules.push({ media: rule.media, original: rule.media.mediaText, scheme: match[1] });
          }
        }
        if (rule.cssRules) collectThemeRules(rule.cssRules);
      });
    }
    document.querySelectorAll("style").forEach(function (style) {
      if (style.sheet) collectThemeRules(style.sheet.cssRules);
    });

    function applyAppearance(mode) {
      themeRules.forEach(function (rule) {
        rule.media.mediaText = mode === "system" ? rule.original : (rule.scheme === mode ? "all" : "not all");
      });
      document.documentElement.style.colorScheme = mode === "system" ? "light dark" : mode;
    }

    var storageKey = "health-ri-spec-appearance";
    try {
      var savedMode = localStorage.getItem(storageKey);
      if (savedMode === "light" || savedMode === "dark") control.value = savedMode;
    } catch (error) {
      // The selector still works when browser storage is unavailable.
    }
    applyAppearance(control.value);
    control.parentElement.hidden = false;
    control.addEventListener("change", function () {
      applyAppearance(control.value);
      try {
        localStorage.setItem(storageKey, control.value);
      } catch (error) {
        // Remembering the preference is optional.
      }
    });
  }

  function enhanceSectionHighlight(toc) {
    var main = document.querySelector("main");
    var sections = [];
    toc.querySelectorAll('a[href^="#"]').forEach(function (link) {
      var heading = document.getElementById(link.getAttribute("href").slice(1));
      if (main && heading && main.contains(heading)) {
        sections.push({ link: link, heading: heading });
      }
    });
    var active = null;
    var pending = null;

    function updateCurrentSection() {
      pending = null;
      var current = null;
      var readingLine = Math.min(120, window.innerHeight * 0.2);
      for (var i = 0; i < sections.length; i++) {
        if (sections[i].heading.getBoundingClientRect().top > readingLine) break;
        current = sections[i];
      }
      // Short final sections may never reach the reading line before page end.
      if (window.scrollY > 0 && window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) {
        current = sections[sections.length - 1] || null;
      }
      if (current === active) return;
      if (active) active.link.removeAttribute("aria-current");
      active = current;
      if (active) active.link.setAttribute("aria-current", "location");
    }

    function scheduleUpdate() {
      if (pending === null) pending = window.setTimeout(updateCurrentSection, 50);
    }

    window.addEventListener("scroll", scheduleUpdate, { passive: true });
    window.addEventListener("resize", scheduleUpdate);
    window.addEventListener("hashchange", scheduleUpdate);
    window.addEventListener("load", scheduleUpdate);
    updateCurrentSection();
    return scheduleUpdate;
  }

  function enhanceSpecificationLayout() {
    enhanceAppearance();
    // Keep horizontal scrolling local to tables on narrow screens.
    document.querySelectorAll("main table").forEach(function (table) {
      var wrapper = document.createElement("div");
      wrapper.className = "spec-table-wrap";
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    });

    var toc = document.getElementById("toc");
    if (!toc) return;
    var updateSectionHighlight = enhanceSectionHighlight(toc);

    var desktop = window.matchMedia("screen and (min-width: 78em)");
    var root = document.documentElement;
    var minimumWidth = 220;
    var maximumWidth = 480;
    var width = parseFloat(getComputedStyle(root).getPropertyValue("--spec-toc-width")) || 300;
    var activePointer = null;
    var startX = 0;
    var startWidth = width;
    var separator = document.createElement("div");
    separator.id = "spec-toc-resizer";
    separator.setAttribute("role", "separator");
    separator.setAttribute("aria-label", "Table of contents width");
    separator.setAttribute("aria-orientation", "vertical");
    separator.setAttribute("aria-controls", "toc");
    separator.setAttribute("aria-valuemin", minimumWidth);
    separator.setAttribute("aria-valuemax", maximumWidth);
    toc.insertAdjacentElement("afterend", separator);

    function setWidth(value) {
      width = Math.round(Math.min(maximumWidth, Math.max(minimumWidth, value)));
      root.style.setProperty("--spec-toc-width", width + "px");
      separator.setAttribute("aria-valuenow", width);
      separator.setAttribute("aria-valuetext", width + " pixels");
      updateSectionHighlight();
    }

    function stopResizing() {
      if (activePointer !== null && separator.hasPointerCapture(activePointer)) {
        separator.releasePointerCapture(activePointer);
      }
      activePointer = null;
      if (document.body.classList.contains("spec-resizing")) {
        document.body.classList.remove("spec-resizing");
      }
    }

    function updateSidebar() {
      var enabled = desktop.matches && !document.body.classList.contains("toc-inline");
      separator.hidden = !enabled;
      separator.tabIndex = enabled ? 0 : -1;
      if (!enabled) stopResizing();
      updateSectionHighlight();
    }

    separator.addEventListener("pointerdown", function (event) {
      if (separator.hidden || event.button !== 0) return;
      event.preventDefault();
      separator.focus();
      activePointer = event.pointerId;
      startX = event.clientX;
      startWidth = width;
      separator.setPointerCapture(activePointer);
      document.body.classList.add("spec-resizing");
    });

    separator.addEventListener("pointermove", function (event) {
      if (event.pointerId === activePointer) {
        setWidth(startWidth + event.clientX - startX);
      }
    });

    separator.addEventListener("pointerup", stopResizing);
    separator.addEventListener("pointercancel", stopResizing);
    separator.addEventListener("lostpointercapture", stopResizing);

    separator.addEventListener("keydown", function (event) {
      if (separator.hidden) return;
      var value;
      if (event.key === "ArrowLeft") value = width - 10;
      else if (event.key === "ArrowRight") value = width + 10;
      else if (event.key === "Home") value = minimumWidth;
      else if (event.key === "End") value = maximumWidth;
      else return;
      event.preventDefault();
      setWidth(value);
    });

    if (desktop.addEventListener) desktop.addEventListener("change", updateSidebar);
    else desktop.addListener(updateSidebar);
    window.addEventListener("resize", updateSidebar);
    new MutationObserver(updateSidebar).observe(document.body, { attributes: true, attributeFilter: ["class"] });
    setWidth(width);
    updateSidebar();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enhanceSpecificationLayout);
  } else {
    enhanceSpecificationLayout();
  }
})();
</script>

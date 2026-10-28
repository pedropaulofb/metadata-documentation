<script>
(function () {
  "use strict";

  function enhanceSpecificationLayout() {
    // Keep horizontal scrolling local to tables on narrow screens.
    document.querySelectorAll("main table").forEach(function (table) {
      var wrapper = document.createElement("div");
      wrapper.className = "spec-table-wrap";
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    });

    var toc = document.getElementById("toc");
    if (!toc) return;

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

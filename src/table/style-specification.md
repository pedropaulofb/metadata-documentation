<style>
/* Applied after the included table styles so every table shares one layout. */
:root {
  --spec-toc-width: 300px;
  --spec-page-bg: #fff;
  --spec-heading: #1c4078;
  --spec-border: #d5dee8;
  --spec-table-bg: #fff;
  --spec-table-text: #202938;
  --spec-table-head: #e8f0f8;
  --spec-table-stripe: #f7f9fc;
  --spec-table-hover: #edf3fa;
  --spec-sidebar-bg: #f5f7fa;
  --spec-focus: #245ca6;
}

/* Override Bikeshed's page background without duplicating its color palette. */
html:root {
  --bg: var(--spec-page-bg);
}

@media (prefers-color-scheme: dark) {
  :root {
    --spec-page-bg: #10151d;
    --spec-heading: #a9caff;
    --spec-border: #455365;
    --spec-table-bg: #151c26;
    --spec-table-text: #e5eaf1;
    --spec-table-head: #26384f;
    --spec-table-stripe: #1c2633;
    --spec-table-hover: #293b52;
    --spec-sidebar-bg: #111822;
    --spec-focus: #a9caff;
  }
}

body .head h1,
body .head h2,
body main :is(h2, h3, h4),
body #toc h2,
body:not(.toc-inline) #toc h2,
body.toc-sidebar #toc h2 {
  color: var(--spec-heading);
}

body .head #profile-and-date {
  margin-bottom: 0;
}

body .head .spec-brand {
  margin: 1rem 0 1.5rem;
}

body .head .spec-logo {
  display: block;
  width: 450px;
  max-width: 100%;
  height: auto;
  background: transparent;
}

body .head .spec-logo-white {
  display: none;
}

/* These rules also follow the Appearance selector's manual overrides. */
@media (prefers-color-scheme: dark) {
  body .head .spec-logo-blue {
    display: none;
  }

  body .head .spec-logo-white {
    display: block;
  }
}

body .head .spec-appearance:not([hidden]) {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0 0 0.75rem;
}

#spec-appearance {
  font: inherit;
  color: var(--spec-table-text);
  background: var(--spec-table-bg);
  border: 1px solid var(--spec-border);
  border-radius: 0.25rem;
  padding: 0.3rem 0.5rem;
}

#spec-appearance:focus-visible {
  outline: 2px solid var(--spec-focus);
  outline-offset: 2px;
}

body .head dl {
  display: grid;
  grid-template-columns: minmax(10rem, 13rem) minmax(0, 1fr);
  gap: 0.4rem 1.25rem;
  align-items: baseline;
}

body .head dl dt {
  grid-column: 1;
  margin: 0;
}

body .head dl dd,
body .head dl dd + dd {
  grid-column: 2;
  margin: 0;
  overflow-wrap: anywhere;
}

/* Tighten only consecutive editor rows within the metadata grid. */
body .head dl dd.editor + dd.editor {
  margin-top: -0.25rem;
}

body main > p,
body main > ul,
body main > ol,
body .p-summary {
  box-sizing: border-box;
  max-width: 80ch;
}

body main h2 {
  margin-top: 3rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--spec-border);
  font-size: 1.6rem;
  font-weight: 600;
}

body main h3 {
  margin-top: 2.25rem;
}

body main h4 {
  margin-top: 1.75rem;
}

body main :is(h2, h3, h4) {
  margin-bottom: 1rem;
}

body main table,
body main table[class] {
  box-sizing: border-box;
  width: 100%;
  max-width: none;
  table-layout: fixed;
  margin: 1.25rem 0 2rem;
  font-size: 0.9375rem;
  line-height: 1.45;
  color: var(--spec-table-text);
  background: var(--spec-table-bg);
}

body main table th,
body main table td,
body main table[class] th,
body main table[class] td {
  box-sizing: border-box;
  padding: 0.4rem 0.625rem;
  border: 1px solid var(--spec-border);
  font-size: 0.9375rem;
  line-height: 1.45;
  text-align: left;
  vertical-align: top;
  overflow-wrap: anywhere;
}

/* The existing class-summary rules use !important; keep their borderless style. */
body main table.no-style,
body main table.no-style th,
body main table.no-style td {
  font-size: 0.9375rem !important;
  line-height: 1.45 !important;
}

body main table.no-style th,
body main table.no-style td {
  padding: 0.4rem 0.625rem !important;
}

body main table thead th {
  position: sticky;
  top: 0;
  z-index: 1;
  background: var(--spec-table-head);
  color: var(--spec-table-text);
  box-shadow: 0 1px 0 var(--spec-border);
}

body main table.no-style thead th {
  position: static;
  box-shadow: none;
  color: var(--spec-heading);
}

body main table tbody tr:nth-child(even) {
  background: var(--spec-table-stripe);
}

body main table tbody tr:hover {
  background: var(--spec-table-hover);
}

body main table a {
  overflow-wrap: anywhere;
  word-break: normal;
  hyphens: none;
}

/* Six-column property tables share proportions; cardinality keeps a readable width. */
body main table.dataframe tbody td:first-child {
  font-weight: 600;
}

body main table.dataframe tbody td:nth-child(3),
body main table.dataframe tbody td:nth-child(4) {
  font-family: ui-monospace, "SFMono-Regular", Consolas, "Liberation Mono", monospace;
}

body main table.dataframe th:nth-child(1) { width: 14%; }
body main table.dataframe th:nth-child(2) { width: 24%; }
body main table.dataframe th:nth-child(3) { width: 17%; }
body main table.dataframe th:nth-child(4) { width: 12%; }
body main table.dataframe th:nth-child(5) { width: 8rem; }

body main table.no-style th:nth-child(1) { width: 15%; }
body main table.no-style th:nth-child(2) { width: 30%; }
body main table.no-style th:nth-child(3) { width: 35%; }
body main table.larger-font th:first-child { width: 25%; }
body main table:not([class]) th:nth-child(1) { width: 21%; }
body main table:not([class]) th:nth-child(2) { width: 19%; }
body main table:not([class]) th:nth-child(3) { width: 27%; }

.spec-table-wrap {
  width: 100%;
  margin: 1.25rem 0 2rem;
}

body main .spec-table-wrap > table {
  margin: 0;
}

body #toc {
  font-size: 0.9375rem;
  line-height: 1.45;
}

body #toc > .toc > li > a {
  font-weight: 600;
}

body #toc .toc li {
  margin-top: 0.35rem;
  margin-bottom: 0.35rem;
}

@media screen {
  /* Bikeshed's ToC links use display: contents, so style the visible label. */
  body #toc a[aria-current="location"] > .content {
    background: var(--spec-table-head);
    box-shadow: -3px 0 0 var(--spec-focus);
  }
}

#spec-toc-resizer {
  display: none;
}

@media screen and (min-width: 78em) {
  body.toc-inline {
    max-width: none;
    margin: 0;
    padding-right: 2rem;
  }

  body:not(.toc-inline) {
    max-width: none;
    margin: 0;
    padding-left: calc(var(--spec-toc-width) + 3rem);
    padding-right: 2rem;
  }

  body:not(.toc-inline) #toc {
    box-sizing: border-box;
    width: var(--spec-toc-width);
    max-width: none;
    padding-right: 1.25rem;
    background: var(--spec-sidebar-bg);
  }

  body:not(.toc-inline) #spec-toc-resizer:not([hidden]) {
    display: block;
    position: fixed;
    top: 0;
    bottom: 0;
    left: calc(var(--spec-toc-width) - 6px);
    width: 12px;
    z-index: 2;
    cursor: col-resize;
    touch-action: none;
  }

  #spec-toc-resizer::after {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 5px;
    width: 2px;
    background: var(--spec-border);
  }

  #spec-toc-resizer:hover::after,
  #spec-toc-resizer:focus-visible::after,
  body.spec-resizing #spec-toc-resizer::after {
    background: var(--spec-focus);
  }

  #spec-toc-resizer:focus-visible {
    outline: 2px solid var(--spec-focus);
    outline-offset: -2px;
  }

  body.spec-resizing,
  body.spec-resizing * {
    cursor: col-resize !important;
    user-select: none;
  }
}

@media screen and (max-width: 50em) {
  body .head dl {
    display: block;
  }

  body .head dl dt {
    margin-top: 0.8rem;
  }

  body .head dl dd {
    margin-top: 0.25rem;
  }

  body .head dl dd.editor + dd.editor {
    margin-top: 0;
  }

  .spec-table-wrap {
    overflow-x: auto;
  }

  body main .spec-table-wrap > table.dataframe {
    min-width: 44rem;
  }

  body main table thead th {
    position: static;
  }
}

@media print {
  :root {
    --spec-page-bg: #fff;
    --spec-heading: #1c4078;
    --spec-border: #aab5c3;
  }

  body {
    color: #000;
    background: #fff;
  }

  body .head .spec-logo-blue {
    display: block;
  }

  body .head .spec-logo-white {
    display: none;
  }

  #spec-toc-resizer,
  body .head .spec-appearance {
    display: none !important;
  }

  body main table thead th {
    position: static;
  }

  body main table,
  body main table thead th,
  body main table th,
  body main table td {
    color: #000;
    background: #fff;
  }

  body a[href],
  body #toc a {
    color: #034575;
    text-decoration-color: currentColor;
  }
}
</style>

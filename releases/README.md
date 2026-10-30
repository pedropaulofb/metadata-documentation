# Published specification snapshots

Version folders contain rendered documentation and the images required to display
it. They are HTML specifications, not metadata-model or SHACL releases.

## v2.0.3 provenance

- Published HTML: `Health-RI/metadata-documentation`, `gh-pages` commit
  [`cb47a264dfb008d39bdb954bf5f70f21229ccfc0`](https://github.com/Health-RI/metadata-documentation/commit/cb47a264dfb008d39bdb954bf5f70f21229ccfc0).
- Original source: commit
  [`8e0e7227fe33a8c716f3a15245888671db0d7126`](https://github.com/Health-RI/metadata-documentation/commit/8e0e7227fe33a8c716f3a15245888671db0d7126),
  identified in the deployment commit as the v2.0.3 update.
- Publication date: 2 July 2026, preserved from the published HTML.
- `HRI_Logo.png` and `HRI_metadata_p2.png` are copied byte-for-byte from that
  original source commit.
- The only HTML changes replace three image/link references to the changing
  `main` branch with relative `images/` paths. The published text, tables,
  publication metadata, and styling remain unchanged.

## Build and retain snapshots

Install Bikeshed 7.2.0 and run from the repository root:

```bash
python src/python/build_specification_site.py
```

The command creates a new `_site/` directory containing:

```text
index.html
src/images/...
releases/v2.1.0/index.html
releases/v2.1.0/src/images/...
releases/v2.0.3/index.html
releases/v2.0.3/images/...
```

`_site/index.html` and the current version's `index.html` are identical. The
current version comes from the versioned documentation PID in `index.bs` and must
agree with `Status Text`. `Previous Version` must identify an available snapshot.
The generator does not read, select, or modify an Excel workbook.

Use `--output PATH` to choose a fresh output directory. Existing output is never
overwritten. Running the script by its absolute path also works from another
working directory.

To retain previously published snapshots, supply a checkout of the published site:

```bash
python src/python/build_specification_site.py --published-site PATH_TO_PUBLISHED_SITE
```

Existing version folders are retained byte-for-byte. Conflicting snapshots or a
changed build of an already published version cause a failure. Publishing changed
content requires a new documentation version and updated publication metadata;
published snapshots must not be overwritten.

The publication workflow builds and uploads this directory for PRs targeting
`main` or `v2.1`. Deployment remains restricted to pushes to the upstream
`Health-RI/metadata-documentation` repository's `main` branch. It publishes all
three pages and their assets to the existing `gh-pages` branch while retaining
older snapshots and other existing site files.

The versioned w3id routes must also be accepted in `perma-id/w3id.org` before the
new version-specific PIDs resolve. Creating these files does not activate those
redirects or publish a release.

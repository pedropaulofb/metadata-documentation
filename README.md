# Health-RI Metadata Documentation

This repository contains the source files, generated documentation fragments, and publication workflow for the **Health-RI Metadata Model documentation**.

The published documentation describes the Health-RI Core Metadata Schema for the **National Health Data Catalogue**.

| Resource                 | Link                                                                                              |
|--------------------------|---------------------------------------------------------------------------------------------------|
| Published specification  | [health-ri.github.io/metadata-documentation](https://health-ri.github.io/metadata-documentation/) |
| Related model repository | [Health-RI/health-ri-metadata](https://github.com/Health-RI/health-ri-metadata)                   |
| Repository issue tracker | [health-ri-metadata issues](https://github.com/Health-RI/health-ri-metadata/issues)              |

---

## Purpose

This repository is used to maintain and publish the human-readable technical specification of the Health-RI Core Metadata Schema.

It contains:

* the main Bikeshed source file  
* manually maintained explanatory chapters  
* manually maintained class descriptions  
* an Excel workbook used as structured source material for generated property tables  
* a JSON configuration file for controlled vocabulary mappings, requirement lookups, and property links  
* a Python script that converts Excel content into HTML table fragments  
* generated property-table fragments included by Bikeshed  
* GitHub Actions configuration for publication to GitHub Pages  

This repository is primarily intended for **internal use** by documentation maintainers, metadata model maintainers, and technical contributors working on the specification website.

It is **not** the main repository for Health-RI metadata model artifacts.  
Model-level artifacts, SHACL shapes, releases, and **all issue tracking (including documentation issues)** are maintained in: https://github.com/Health-RI/health-ri-metadata

---

## Useful resources 

The Health-RI metadata ecosystem uses multiple repositories, tools, and publication targets.

| Resource | Role | Description |
|----------|------|------------|
| https://github.com/Health-RI/metadata-documentation | Documentation repository | Bikeshed source, Markdown chapters, class descriptions, generated property tables, and publication workflow |
| https://github.com/Health-RI/health-ri-metadata | Main metadata repository | Core metadata schema artifacts, SHACL shapes, releases, and all issue tracking (including documentation issues) |
| https://health-ri.github.io/metadata-documentation/ | Published specification | Rendered HTML documentation |
| https://doi.org/10.5281/zenodo.15395604 | DOI record | Citable archival record |
| https://speced.github.io/bikeshed/ | Bikeshed documentation | Documentation for the Bikeshed tool |
| https://www.w3.org/TR/vocab-dcat-3/ | DCAT 3 | W3C Data Catalog Vocabulary |
| https://docs.geostandaarden.nl/dcat/dcat-ap-nl30/ | DCAT-AP NL 3.0 | Dutch DCAT application profile |
| https://healthdataeu.pages.code.europa.eu/healthdcat-ap/ | HealthDCAT-AP | Health domain DCAT profile |

In short (how to use these):

- use this repository to edit, build, and publish the technical specification  
- use the metadata repository for schema artifacts and all issue tracking  
- use the published specification for reading and reference  

---

## Repository structure and source-of-truth

Different parts of the specification are maintained in different locations.

| Content | Location | Generated | Usage / Notes |
|--------|----------|-----------|----------------|
| Specification structure and configuration | `index.bs` | No | Controls document structure and includes other content |
| Narrative chapters | `src/chapter/*.md` | No | Edit for explanatory documentation |
| Class descriptions | `src/class/*.md` | No | Edit for class-level documentation |
| Property definitions (labels, URIs, cardinality, etc.) | `src/excel/HealthRI_v*.xlsx` | Partly | Edit here; regenerate property tables afterwards |
| Property tables | `src/property/*.html` | Yes | Generated from Excel; do not edit manually |
| Table styling | `src/table/*.md` | No | Styling fragments |
| Images and diagrams | `src/images/` | No | Visual assets |
| Generator scripts | `src/python/` | No | Contains Excel-to-HTML generator |
| Publication workflow | `.github/workflows/publish.yml` | No | GitHub Actions build and deploy process |
| Documentation site (deployment) | `gh-pages` branch | Yes | Published documentation output |
| Rendered HTML file | `index.html` | Yes | Generated output; do not edit manually |
| Saved specification versions | `releases/vX.Y.Z/` | Yes | Commit each published HTML specification and its images here |
| Repository overview | `README.md` | No | Maintainer documentation |

### Maintenance rules

- Edit the upstream source, not generated output  
- Do not manually edit `index.html`  
- Do not manually edit generated `src/property/*.html` unless explicitly justified  
- Treat the Excel workbook as the source of truth for property metadata  
- Regenerate tables only when the Excel workbook changes  
- Publication is handled via GitHub Actions, not manual HTML edits  

---

## Build and publication pipeline

The documentation workflow has two related but distinct parts:

1. Property-table generation (when the Excel workbook changes)  

```mermaid
flowchart LR
    A{"Excel workbook changed?"}
    A -- "Yes" --> B["Edit versioned workbook<br/>src/excel/HealthRI_v*.xlsx"]
    A -- "No" --> F["Do not regenerate property tables"]

    B --> C["Run generator from src/python<br/>python Excel_To_Html.py"]
    C --> D["Regenerate property tables<br/>src/property/*.html"]
    D --> E["Review generated diff"]
    E --> G["Commit workbook and generated table changes"]
```

2. Specification rendering and publication  

```mermaid
flowchart TD
    start["Contributor edits repository content"]

    start --> changeType{"What changed?"}

    changeType -->|"Narrative text"| chapters["Edit src/chapter/*.md"]
    changeType -->|"Class description"| classes["Edit src/class/*.md"]
    changeType -->|"Specification structure"| bikeshed["Edit index.bs"]
    changeType -->|"Property metadata"| workbook["Edit current workbook<br/>src/excel/HealthRI_v*.xlsx"]
    changeType -->|"Images or styles"| assets["Edit src/images/ or src/table/"]

    workbook --> generator["Run generator from src/python<br/>python Excel_To_Html.py"]
    generator --> generatedTables["Regenerated property tables<br/>src/property/*.html"]

    chapters --> validate["Local build and testing"]
    classes --> validate
    bikeshed --> validate
    assets --> validate
    generatedTables --> validate

    validate --> pr["Open pull request targeting main"]
    pr --> ciPr["GitHub Actions validation<br/>w3c/spec-prod"]

    ciPr --> review{"Review outcome"}
    review -->|"Changes requested"| start
    review -->|"Approved"| main["Merge to main"]

    main --> ciMain["GitHub Actions publication run"]
    ciMain --> ghpages["Deploy rendered specification<br/>to gh-pages"]
    ghpages --> site["Published documentation site"]
```

---

## Local build and testing

The production publication workflow is automated through GitHub Actions. Local builds are useful to test and preview changes before opening or merging a pull request.

Install Bikeshed:

```bash
pipx install bikeshed
bikeshed update
```

Build locally:

```bash
bikeshed spec index.bs index.html
```

Dry-run (no output):

```bash
bikeshed --dry-run spec index.bs
```

Use this local build process to:

- verify that the specification renders correctly  
- catch errors or warnings early  
- test changes before submitting a pull request  

Do not manually edit the generated `index.html`.

---

## Publication

The documentation is published at:

https://health-ri.github.io/metadata-documentation/

### Save each published specification

Before publishing a version, save its generated HTML and required images in
`releases/vX.Y.Z/` and commit that folder with the release. Keep previous version
folders available when preparing the next version.

Continue using the existing Excel-to-HTML and Bikeshed commands. For example,
after v2.1.0 has been published, prepare v2.2.0 as follows:

1. Update the workbook and related sources. Regenerate property tables when the
   workbook changes, selecting the intended input explicitly:

   ```bash
   python src/python/Excel_To_Html.py --excel src/excel/your-workbook.xlsx
   ```

2. Update `index.bs`: set the new `Status Text` version and actual publication
   `Date`; set `URL` and `Canonical URL` to
   `https://w3id.org/health-ri/metadata/docs/v2.2.0`; and set `Previous Version` to
   `https://w3id.org/health-ri/metadata/docs/v2.1.0`. Keep `TR` as
   `https://w3id.org/health-ri/metadata/docs`. Keep the UML heading and diagram
   reference consistent with the release version.

3. Create `releases/v2.2.0/src/images/`, generate the HTML into that version's
   `index.html`, and copy its images while preserving their relative paths.
   This PowerShell example copies the image folder so the saved specification
   does not depend on future changes to the current images:

   ```powershell
   New-Item -ItemType Directory -Force releases/v2.2.0/src/images | Out-Null
   bikeshed spec index.bs releases/v2.2.0/index.html
   Copy-Item src/images/* releases/v2.2.0/src/images/
   ```

4. Open the saved `index.html` and check its tables, links, and images. Commit the
   saved version folder together with the source changes and regenerated property
   tables. You may still generate a local preview with the usual command:

   ```bash
   bikeshed spec index.bs preview-v2.2.0.html
   ```

The workflow continues to generate the latest page with `w3c/spec-prod`. After a
push to upstream `main`, an additional step copies the committed `releases/`
folders and current `src/images/` to GitHub Pages, retaining existing site files.
The workflow does not regenerate the saved version folders or the property
tables. Regenerate the current version's saved HTML and recopy its images when
finalizing the publication; generating a preview alone does not update it.

The v2.1.0 snapshot included here retains the preview date in `index.bs`. Set the
actual publication date and regenerate that snapshot before publishing v2.1.0.
Version-specific documentation PIDs also require the separately proposed w3id
redirects to be active. Their generic version rule needs no update for each
future release.

### Historical v2.0.3 snapshot

The saved v2.0.3 HTML comes from the published `gh-pages` commit
[`cb47a264dfb008d39bdb954bf5f70f21229ccfc0`](https://github.com/Health-RI/metadata-documentation/commit/cb47a264dfb008d39bdb954bf5f70f21229ccfc0),
which identifies source commit
[`8e0e7227fe33a8c716f3a15245888671db0d7126`](https://github.com/Health-RI/metadata-documentation/commit/8e0e7227fe33a8c716f3a15245888671db0d7126)
as the v2.0.3 update. Its two images are copied unchanged from that source commit.
The only HTML edits replace three references to those images on the changing
`main` branch with local `images/` paths. Its original text, tables, publication
metadata, styling, and 2 July 2026 publication date are preserved.

If changes are not visible:

- check the GitHub Actions workflow runs and confirm they completed successfully  
- verify that the changes were merged into the `main` branch  
- check the `gh-pages` branch to confirm the updated content was deployed  
- check that the saved `releases/vX.Y.Z/index.html` and its images were committed
- refresh the page and clear your browser cache if necessary  

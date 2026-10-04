# Health-RI Metadata Documentation

This repository contains the source files, generated documentation fragments, and publication workflow for the **Health-RI Metadata Model documentation**.

The published documentation describes the Health-RI Core Metadata Schema for the **National Health Data Catalogue**.

| Resource                 | Link                                                                                              |
|--------------------------|---------------------------------------------------------------------------------------------------|
| Published specification  | [health-ri.github.io/metadata-documentation](https://health-ri.github.io/metadata-documentation/) |
| Related model repository | [Health-RI/health-ri-metadata](https://github.com/Health-RI/health-ri-metadata)                   |
| Repository issue tracker | [health-ri-metadata issues](https://github.com/Health-RI/health-ri-metadata/issues)              |

---

## Forthcoming release

The candidate is maintained on `v2.1`. See [RELEASING.md](RELEASING.md) for the current source list, pinned build environment, validation, publication behavior and coordinated release checklist. The released workbook is supplemented by `src/next-release-properties.json` and `src/property-overrides.json`; it is not the complete candidate source by itself.

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
| Repository overview | `README.md` | No | Maintainer documentation |

### Maintenance rules

- Edit the upstream source, not generated output  
- Do not manually edit `index.html`  
- Do not manually edit generated `src/property/*.html` unless explicitly justified  
- Treat the Excel workbook plus the documented JSON additions/corrections as the source of truth for candidate property metadata
- Regenerate tables when the workbook, JSON additions/corrections, link configuration or generator changes
- Publication is handled via GitHub Actions, not manual HTML edits  

---

## Build and publication pipeline

The documentation workflow has two related but distinct parts:

1. Property-table generation (when a property source changes)  

```mermaid
flowchart LR
    A{"Property source changed?"}
    A -- "Yes" --> B["Edit workbook or JSON additions/corrections"]
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
    pr --> ciPr["GitHub Actions validation<br/>source tests and Bikeshed"]

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

If changes are not visible:

- check the GitHub Actions workflow runs and confirm they completed successfully  
- verify that the changes were merged into the `main` branch  
- check the `gh-pages` branch to confirm the updated content was deployed  
- ensure that regenerated `src/property/*.html` files were included in the source commit; `index.html` is built and deployed by CI
- refresh the page and clear your browser cache if necessary  

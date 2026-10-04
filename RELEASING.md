# Build and release the documentation

`main` publishes the released specification. `v2.1` is the existing upstream
candidate branch; its name does not by itself assign the final release number.
PRs and candidate pushes build a preview only. A successful push build on `main`
publishes that exact HTML artifact to the existing `gh-pages` publication branch.
No schema or vocabulary repository is written by the workflow.

## Sources and regeneration

- `src/excel/HealthRI_v2.0.3.xlsx`: released property source, retained unchanged.
- `src/next-release-properties.json`: new Dataset-property source, copied from the
  schema repository's `Documents/next-release-properties.json`.
- `src/property-overrides.json`: explicit next-release corrections to workbook rows.
  Retention text comes from schema `develop` commit `acec135`; the endpoint URI
  spelling correction matches the already-correct SHACL (upstream issue #267).
- `src/python/links.json`: controlled-vocabulary and term links.
- `src/chapter`, `src/class` and `index.bs`: maintained narrative and structure.
- `src/property/*.html`: generated; do not edit directly.

The workbook alone is not the complete candidate model. Keep the addendum with it.
When the workbook is revised later, deliberately reconcile these overlays; the
generator rejects duplicate additions and unmatched correction targets.

```bash
python -m pip install -r requirements.txt
python src/python/Excel_To_Html.py
python -m unittest discover -s tests -v
python scripts/check_release_alignment.py /path/to/health-ri-metadata
bikeshed spec index.bs index.html
```

Use Python 3.12. Generator paths are independent of the working directory. Commit
the reviewed source and generated-table changes together. `index.html` is a build
artifact and is not committed on the source branch. CI compares regenerated tables
byte for byte. Direct build dependencies are pinned; transitive dependencies and
Bikeshed reference data are not fully locked.

## Coordinated release checklist

1. Review the schema `develop` candidate and documentation `v2.1` together. Run the
   offline alignment check against the exact proposed schema checkout.
2. Resolve existing model/documentation ambiguities before claiming complete
   conformance. In particular, Distribution title and Catalog dataset-membership cardinalities differ, and the
   existing Distribution `healthdcatap:retentionperiod` spelling is distinct from
   Dataset `healthdcatap:retentionPeriod`. This change preserves those existing IRIs.
3. Assign the schema release number/date, update the draft notice and historical
   diagram description as appropriate, and record vocabulary v0.4.1 adoption.
4. Record the schema and documentation commit SHAs in the schema release notes.
5. Publish the schema release via its normal `develop` → `master` process and merge
   the matching documentation to `main` in coordination. There is no automatic
   cross-repository release event: it would need a selected documentation revision
   and an agreed publication policy. No long-lived cross-repository token is needed.
6. Verify the published site and the machine-readable release links. In a failure,
   inspect the build/publish job, correct the source and push the corrected commit.

## Manual activation

- Enable Actions on a fork if disabled. Candidate builds require no secrets.
- Keep Pages configured to publish from `gh-pages` at its root. This retains the
  existing hosting model; do not switch to a different source without a deliberate
  deployment migration.
- Permit `GITHUB_TOKEN` contents-write for the `publish` job and permit its update
  of the generated `gh-pages` branch. No write permission is requested for PR builds.
- Review branch protections/required checks for both `main` and `v2.1`; settings
  were not changed by this task.

The publication job uses `w3c/spec-prod@v2` in static mode to deploy the HTML already
validated by the build job. Existing Pages branch behavior is retained. Schema
tags alone do not deploy documentation.

# Forthcoming minor release {#forthcoming-minor-release}

**Draft — not yet a published schema release.** The final schema version and date
remain to be assigned. The existing diagram describes v2.0.3 and does not show the
new optional properties.

The Dataset table includes five optional, repeatable additions: `dct:alternative`,
`dcat:landingPage`, `dct:provenance`, `hri:healthConditionOfInterest` and
`hri:anatomicalLocationCovered`. Existing properties are retained. No migration is
required by these additions.

Here `hri` denotes `https://w3id.org/health-ri/metadata-vocabulary#`.
The two Health-RI terms are defined by
[Health-RI Metadata Vocabulary v0.4.1](https://w3id.org/health-ri/metadata-vocabulary/v0.4.1).
A [pinned repository copy](https://github.com/pedropaulofb/health-ri-metadata-vocabulary/blob/0a06931f250954443edd62d930547bf02bd77711/vocabulary/versioned/health-ri-metadata-vocabulary-v0.4.1.ttl) is also available.
Both apply to `dcat:Dataset` and have cardinality `0..n` in this candidate.

Health-condition values identify suitable SNOMED CT or ICD-10 concepts and are
typed as `skos:Concept` in the metadata graph. They describe dataset-level subject
matter, not diagnoses of individual participants. Anatomical values are SNOMED CT
anatomical classes: Anatomical structure (91723000) or a direct or indirect subclass.
They require no `skos:Concept` typing and describe aggregate coverage, without linking
particular body sites to modalities, data categories or samples.

## Validation of the additions {#validation-of-additions}

The core shapes register these optional properties descriptively. Existing core
constraints are unchanged. Core SHACL conformance alone does not validate the new
properties' intended value forms or terminology membership.

The schema repository supplies a separate, opt-in validator using the vocabulary's
non-normative shapes. It checks health-condition identifier formats and Concept
typing, and anatomical SNOMED identifier formats and hierarchy paths. Anatomical
checks require independently trusted SNOMED hierarchy evidence. The vocabulary's
OWL Full range entails subclass membership but does not establish authoritative
terminology membership. Do not use that inference as validation evidence.

The checks cannot establish concept existence, activity, or clinical suitability.
Requiring them as part of core conformance needs a separate compatibility decision.
See the schema repository's
[release draft and validation instructions](https://github.com/Health-RI/health-ri-metadata/blob/develop/Documents/next-release.md).

## Non-normative example {#hri-property-example}

This fragment illustrates the additions; it is not a complete catalogue record.

```turtle
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix hri: <https://w3id.org/health-ri/metadata-vocabulary#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<https://example.org/dataset> a dcat:Dataset ;
    hri:healthConditionOfInterest <http://snomed.info/id/22298006> ;
    hri:anatomicalLocationCovered <http://snomed.info/id/91723000> .

<http://snomed.info/id/22298006> a skos:Concept .
```

The anatomical root is used only to keep this example independent of a terminology
download. Choose the appropriate, more specific anatomical coverage for real data.

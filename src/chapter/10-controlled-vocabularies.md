# Controlled Vocabularies 

In this section, properties are listed for which specific values are expected. These values are typically taken from controlled vocabularies, but may also come from defined ontologies, authority tables, or prescribed value lists (such as licenses or identifier schemes).

Using these predefined sources ensures consistency and interoperability across datasets and catalogues.

The requirements are grouped into three categories:

* **MUST**: the value for the property must be selected from the specified vocabulary or list.
* **AT LEAST 1**: at least one of the provided values must come from the specified vocabulary (additional values from other sources may be included where relevant).
* **MAY**: the use of the specified vocabulary is optional, but recommended when applicable.

The tables below list the relevant properties, the classes they apply to, the expected vocabularies, and additional usage notes to support correct implementation.

## Terminology bindings for the new optional properties {#new-property-terminology}

The following bindings describe intended usage in Health-RI Metadata Vocabulary
v0.4.1. Both properties are optional and repeatable on `dcat:Dataset`. Their
suggested validation checks are opt-in and are not added to core conformance.

| Property | Intended values | Validation limits |
|---|---|---|
| `hri:healthConditionOfInterest` | Suitable SNOMED CT or ICD-10 concept IRIs, typed `skos:Concept` | Identifier-pattern and typing checks do not establish existence, activity or clinical suitability. |
| `hri:anatomicalLocationCovered` | SNOMED CT Anatomical structure (91723000) or a direct or indirect subclass, identified by IRI; no `skos:Concept` typing required | Hierarchy checks need separately trusted SNOMED evidence. OWL Full range entailment is not terminology validation. |

See [validation of the additions](#validation-of-additions) for details. These
bindings do not replace or restrict values of any existing property.

## Properties with controlled vocabularies that **MUST** be used for the listed properties

<table>
  <thead>
    <tr>
      <th>Property URI</th>
      <th>Used for Class</th>
      <th>Controlled Vocabulary</th>
      <th>Usage Note</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>dct:accessRights</td>
      <td>Dataset</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/access-right">
          http://publications.europa.eu/resource/authority/access-right
        </a>
      </td>
      <td>The EU authority table, containing values for access rights of the Dataset. You can choose between the values PUBLIC, NON_PUBLIC and RESTRICTED, even though in the vocabulary itself more values are included. Depending on the value that is choosed here, one of the three different versions of HealthDCAT-AP will be used.</td>
    </tr>

    <tr>
      <td>dct:accrualPeriodicity</td>
      <td>Dataset</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/frequency">
          http://publications.europa.eu/resource/authority/frequency
        </a>
      </td>
      <td>EU authority table, containing possible values to use in order to describe the frequency at which the dataset is updated.</td>
    </tr>

    <tr>
      <td>dct:language</td>
      <td>Dataset</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/language">
          http://publications.europa.eu/resource/authority/language
        </a>
      </td>
      <td>Choose the language of the dataset in the EU authority table.</td>
    </tr>

    <tr>
      <td>dpv:hasPersonalData</td>
      <td>Dataset</td>
      <td>
        <a href="https://w3c.github.io/dpv/2.0/pd/">
          https://w3c.github.io/dpv/2.0/pd/
        </a>
      </td>
      <td>For this propery, you should specify the type(s) of personal data that your dataset contains or processes. These types are defined in the DPV ontology and include classes such as dpv:Age, dpv:BirthDate and dpv:Gender. Choose the classes that describe personal data inside your Dataset.</td>
    </tr>

    <tr>
      <td>adms:status</td>
      <td>Dataset</td>
      <td>
        <a href="https://publications.europa.eu/resource/authority/dataset-status">
          https://publications.europa.eu/resource/authority/dataset-status
        </a>
      </td>
      <td>Choose the status of the dataset in the EU authority table.</td>
    </tr>

    <tr>
      <td>dcat:theme</td>
      <td>Dataset</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/data-theme">
          http://publications.europa.eu/resource/authority/data-theme
        </a>
      </td>
      <td>Choose the theme(s) of the dataset in the EU authority table. In the Health Data Catalogue, all datasets will use the theme 'HEAL' (http://publications.europa.eu/resource/authority/data-theme/HEAL), but additional values from the same vocabulary are allowed.</td>
    </tr>

    <tr>
      <td>dct:type</td>
      <td>Dataset</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/dataset-type">
          http://publications.europa.eu/resource/authority/dataset-type
        </a>
      </td>
      <td>Choose the type of the dataset in the EU authority table.</td>
    </tr>

    <tr>
      <td>dct:language</td>
      <td>Catalog</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/language">
          http://publications.europa.eu/resource/authority/language
        </a>
      </td>
      <td>Choose the language of the catalog in the EU authority table.</td>
    </tr>

    <tr>
      <td>dct:license</td>
      <td>Catalog</td>
      <td>
        <a href="https://definities.geostandaarden.nl/dcat-ap-nl/nl/">
          https://definities.geostandaarden.nl/dcat-ap-nl/nl/
        </a>
      </td>
      <td>Choose a license that is applicable to your Catalog. You can choose one from the DCAT-AP NL provided list, which uses Creative Commons licenses. If you need help choosing one, it is recommended to use the chooser tool from Creative Commons (https://creativecommons.org/chooser/).</td>
    </tr>

    <tr>
      <td>dct:spatial</td>
      <td>Agent</td>
      <td>
        <a href="https://publications.europa.eu/resource/authority/country">
          https://publications.europa.eu/resource/authority/country
        </a>
      </td>
      <td>Choose country of the Catalogue from the EU authority table.</td>
    </tr>

    <tr>
      <td>dct:identifier</td>
      <td>Agent</td>
      <td>
        <a href="https://orcid.org/">ORCID</a>,
        <a href="https://ror.org/">ROR</a>,
        <a href="https://isni.org/page/search-database/">ISNI</a>,
        <a href="https://standaarden.overheid.nl/tooi/waardelijsten/">TOOI</a>,
        <a href="https://www.wikidata.org/wiki/Wikidata:Main_Page">Wikidata</a>
      </td>
      <td>Provide an ORCID identifier for person, ROR for organization. If these are not available, it is also allowed to use ISNI, TOOI or Wikidata.</td>
    </tr>

    <tr>
      <td>healthdcatap:publishertype</td>
      <td>Agent</td>
      <td>
        <a href="https://raw.githubusercontent.com/SEMICeu/ADMS-AP/master/purl.org/ADMS_SKOS_v1.00.rdf">
          https://raw.githubusercontent.com/SEMICeu/ADMS-AP/master/purl.org/ADMS_SKOS_v1.00.rdf
        </a>
      </td>
      <td>Choose the publisher type from the ADMS publishertype list.</td>
    </tr>

    <tr>
      <td>dct:type</td>
      <td>Agent</td>
      <td>
        <a href="https://raw.githubusercontent.com/SEMICeu/ADMS-AP/master/purl.org/ADMS_SKOS_v1.00.rdf">
          https://raw.githubusercontent.com/SEMICeu/ADMS-AP/master/purl.org/ADMS_SKOS_v1.00.rdf
        </a>
      </td>
      <td>Choose the type of Agent from the ADMS publishertype list.</td>
    </tr>

    <tr>
      <td>dcat:compressFormat</td>
      <td>Distribution</td>
      <td>
        <a href="http://www.iana.org/assignments/media-types/media-types.xhtml">
          http://www.iana.org/assignments/media-types/media-types.xhtml
        </a>
      </td>
      <td>Choose the compression format of the Distribution from the IANA media type list.</td>
    </tr>

    <tr>
      <td>dct:format</td>
      <td>Distribution</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/file-type">
          http://publications.europa.eu/resource/authority/file-type
        </a>
      </td>
      <td>Choose the format of the Distribution from the EU Authority table.</td>
    </tr>

    <tr>
      <td>dct:language</td>
      <td>Distribution</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/language">
          http://publications.europa.eu/resource/authority/language
        </a>
      </td>
      <td>Choose the language of the distribution in the EU authority table.</td>
    </tr>

    <tr>
      <td>dct:license</td>
      <td>Distribution</td>
      <td>
        <a href="https://definities.geostandaarden.nl/dcat-ap-nl/nl/">
          https://definities.geostandaarden.nl/dcat-ap-nl/nl/
        </a>
      </td>
      <td>For license of Distribution, please choose between "not-open" licence for non-public data or "CC0" for public data.</td>
    </tr>

    <tr>
      <td>dcat:mediaType</td>
      <td>Distribution</td>
      <td>
        <a href="http://www.iana.org/assignments/media-types/media-types.xhtml">
          http://www.iana.org/assignments/media-types/media-types.xhtml
        </a>
      </td>
      <td>Choose the media type of the Distribution from the IANA media type list.</td>
    </tr>

    <tr>
      <td>dcat:packageFormat</td>
      <td>Distribution</td>
      <td>
        <a href="http://www.iana.org/assignments/media-types/media-types.xhtml">
          http://www.iana.org/assignments/media-types/media-types.xhtml
        </a>
      </td>
      <td>Choose the package format of the Distribution from the IANA media type list.</td>
    </tr>

    <tr>
      <td>adms:status</td>
      <td>Distribution</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/distribution-status">
          http://publications.europa.eu/resource/authority/distribution-status
        </a>
      </td>
      <td>Choose the status of the distribution from the EU authority table.</td>
    </tr>

    <tr>
      <td>dct:accrualPeriodicity</td>
      <td>Dataset Series</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/frequency">
          http://publications.europa.eu/resource/authority/frequency
        </a>
      </td>
      <td>Choose the frequency with which items are added to a collectio from the EU authority table.</td>
    </tr>

    <tr>
      <td>dct:accessRights</td>
      <td>Data Service</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/access-right">
          http://publications.europa.eu/resource/authority/access-right
        </a>
      </td>
      <td>Choose the term for the access rights of the data service from the EU authority table.</td>
    </tr>

    <tr>
      <td>dct:format</td>
      <td>Data Service</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/file-type">
          http://publications.europa.eu/resource/authority/file-type
        </a>
      </td>
      <td>Choose the format of the data service from the EU athority table.</td>
    </tr>

    <tr>
      <td>dct:language</td>
      <td>Data Service</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/language">
          http://publications.europa.eu/resource/authority/language
        </a>
      </td>
      <td>Choose the language of the data service in the EU authority table.</td>
    </tr>

    <tr>
      <td>dct:license</td>
      <td>Data Service</td>
      <td>
        <a href="https://definities.geostandaarden.nl/dcat-ap-nl/nl/">
          https://definities.geostandaarden.nl/dcat-ap-nl/nl/
        </a>
      </td>
      <td>Choose a license that is applicable to your data service. You can choose one from the DCAT-AP NL provided list, which uses Creative Commons licenses. If you need help choosing one, it is recommended to use the chooser tool from Creative Commons (https://creativecommons.org/chooser/).</td>
    </tr>

    <tr>
      <td>dcat:theme</td>
      <td>Data Service</td>
      <td>
        <a href="https://publications.europa.eu/resource/authority/data-theme">
          https://publications.europa.eu/resource/authority/data-theme
        </a>
      </td>
      <td>Choose the theme of the data service from the EU authority table.</td>
    </tr>

    <tr>
      <td>dcat:hadRole</td>
      <td>Attribution</td>
      <td>
        <a href="https://standards.iso.org/iso/19115/resources/Codelists/gml/CI_RoleCode.xml">ISO RoleCode</a>,
        <a href="https://jats4r.niso.org/credit-taxonomy/#table-1-credit-terms-and-urls">CRediT taxonomy</a>
      </td>
      <td>Choose the role of the attributed agent from either the ISO RoleCode list or from the Credit taxonomy.</td>
    </tr>

    <tr>
      <td>dcat:hadRole</td>
      <td>Relationship</td>
      <td>
        <a href="https://www.iana.org/assignments/link-relations/link-relations.xhtml">IANA Link Relations</a>,
        <a href="https://standards.iso.org/iso/19115/resources/Codelists/gml/DS_AssociationTypeCode.xml">ISO Codelist</a>
      </td>
      <td>Choose the role of the related resource from either the IANA link relations or ISO Association type code list.</td>
    </tr>

    <tr>
      <td>spdx:algorithm</td>
      <td>Checksum</td>
      <td>
        <a href="https://spdx.org/rdf/terms/#d4e2129">
          https://spdx.org/rdf/terms/#d4e2129
        </a>
      </td>
      <td>Choose one of the subclasses of spdx:ChecksumAlgorithm class to indicate the algorithm used.</td>
    </tr>
  </tbody>
</table>

## Properties with **AT LEAST 1** value from the controlled vocabularies

<table>
  <thead>
    <tr>
      <th>Property URI</th>
      <th>Used for Class</th>
      <th>Controlled Vocabulary</th>
      <th>Usage Note</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>dcat:themeTaxonomy</td>
      <td>Catalog</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/data-theme">http://publications.europa.eu/resource/authority/data-theme</a>
      </td>
      <td>Multiple taxonomies may be listed, but at least the EU Data Theme (http://publications.europa.eu/resource/authority/data-theme) must be present.</td>
    </tr>
  </tbody>
</table>

## Properties with controlled vocabularies that **MAY** be used for the listed properties

<table>
  <thead>
    <tr>
      <th>Property URI</th>
      <th>Used for Class</th>
      <th>Controlled Vocabulary</th>
      <th>Usage Note</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>dct:spatial</td>
      <td>Dataset</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/continent">http://publications.europa.eu/resource/authority/continent</a>,
        <a href="http://publications.europa.eu/resource/authority/country">http://publications.europa.eu/resource/authority/country</a>,
        <a href="http://publications.europa.eu/resource/authority/place">http://publications.europa.eu/resource/authority/place</a>,
        <a href="http://sws.geonames.org/">http://sws.geonames.org/</a>,
        <a href="https://vocabs.cbs.nl/nl/">https://vocabs.cbs.nl/nl/</a>
      </td>
      <td>For this property you can use controlled vocabularies depending on which best represents your dataset. The EU provides three relevant authority tables - for continent, country, and place, with country codes aligned to ISO standards where applicable. Your choice depends on the granularity of the geographical coverage: for example, if your dataset covers the entire Netherlands, you can use http://publications.europa.eu/resource/authority/country/NLD from the Country authority table, while for a specific city you should check the Place authority table. Since the Place table has limited coverage, you can also use Geonames, a widely used geographical database with global coverage, or CBS vocabularies, which focus on places in the Netherlands. In general, prefer EU authority URIs first, then Geonames, and finally national vocabularies for finer-grained locations.</td>
    </tr>

    <tr>
      <td>dpv:hasLegalBasis</td>
      <td>Dataset</td>
      <td>
        <a href="https://w3c.github.io/dpv/2.0/dpv/modules/legal_basis.html#vocab-legal-basis">
          https://w3c.github.io/dpv/2.0/dpv/modules/legal_basis.html#vocab-legal-basis
        </a>
      </td>
      <td>You can select one of the subclasses of dpv:LegalBasis to describe the legal basis for processing your dataset. All possible options are defined in the DPV ontology, including Consent, Contract, LegalObligation, LegitimateInterest, VitalInterest, etc. Some of these have further subclasses for more precise specification; for example, Consent can be specialized as InformedConsent → ExpressedConsent → ExplicitlyExpressedConsent. Choose the term that best reflects the legal basis applicable to your dataset.</td>
    </tr>

    <tr>
      <td>dpv:hasPurpose</td>
      <td>Dataset</td>
      <td>
        <a href="https://w3c.github.io/dpv/2.1/dpv/#vocab-purposes">
          https://w3c.github.io/dpv/2.1/dpv/#vocab-purposes
        </a>
      </td>
      <td>Choose the purposes that describe your Dataset from the DPV Purposes, which include classes such as dpv:PublicBenefit, dpv:CommercialPurpose, dpv:Marketing, and dpv:NonCommercialPurpose.</td>
    </tr>

    <tr>
      <td>dct:spatial</td>
      <td>Catalog</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/continent">http://publications.europa.eu/resource/authority/continent</a>,
        <a href="http://publications.europa.eu/resource/authority/country">http://publications.europa.eu/resource/authority/country</a>,
        <a href="http://publications.europa.eu/resource/authority/place">http://publications.europa.eu/resource/authority/place</a>,
        <a href="http://sws.geonames.org/">http://sws.geonames.org/</a>,
        <a href="https://vocabs.cbs.nl/nl/">https://vocabs.cbs.nl/nl/</a>
      </td>
      <td>For this property you can use controlled vocabularies depending on which best represents your catalogue. The EU provides three relevant authority tables - for continent, country, and place, with country codes aligned to ISO standards where applicable. Your choice depends on the granularity of the geographical coverage: for example, if your catalogue covers the entire Netherlands, you can use http://publications.europa.eu/resource/authority/country/NLD from the Country authority table, while for a specific city you should check the Place authority table. Since the Place table has limited coverage, you can also use Geonames, a widely used geographical database with global coverage, or CBS vocabularies, which focus on places in the Netherlands. In general, prefer EU authority URIs first, then Geonames, and finally national vocabularies for finer-grained locations.</td>
    </tr>

    <tr>
      <td>dct:spatial</td>
      <td>Dataset Series</td>
      <td>
        <a href="http://publications.europa.eu/resource/authority/continent">http://publications.europa.eu/resource/authority/continent</a>,
        <a href="http://publications.europa.eu/resource/authority/country">http://publications.europa.eu/resource/authority/country</a>,
        <a href="http://publications.europa.eu/resource/authority/place">http://publications.europa.eu/resource/authority/place</a>,
        <a href="http://sws.geonames.org/">http://sws.geonames.org/</a>,
        <a href="https://vocabs.cbs.nl/nl/">https://vocabs.cbs.nl/nl/</a>
      </td>
      <td>For this property you can use controlled vocabularies depending on which best represents your dataset series. The EU provides three relevant authority tables - for continent, country, and place, with country codes aligned to ISO standards where applicable. Your choice depends on the granularity of the geographical coverage: for example, if your dataset series covers the entire Netherlands, you can use http://publications.europa.eu/resource/authority/country/NLD from the Country authority table, while for a specific city you should check the Place authority table. Since the Place table has limited coverage, you can also use Geonames, a widely used geographical database with global coverage, or CBS vocabularies, which focus on places in the Netherlands. In general, prefer EU authority URIs first, then Geonames, and finally national vocabularies for finer-grained locations.</td>
    </tr>
  </tbody>
</table>

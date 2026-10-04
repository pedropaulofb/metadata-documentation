## Class Structure 
The Health-RI metadata schema builds on DCAT-AP 3.0, which defines a set of classes and properties for describing datasets, services, and related resources. To make the model easier to apply (and interoperable) across catalogues, the schema organizes its structure around two types of classes: **Main Classes** and **Supportive Classes**.

- **Main Classes** – the core entities that form the core of the catalogue.
- **Supportive Classes** – contextual entities that provide detail to the main classes.

Main classes in this structure:
- **Catalog**
- **Dataset**
- **Data Service**
- **Dataset Series**
- **Distribution**

Supportive classes in this structure:
- **Agent**
- **Kind**
- **Attribution**
- **Checksum**
- **Identifier**
- **Period of time**
- **Relationship**
- **Quality certificate**

The main classes and supportive classes together form the Health-RI Core metadata schema. 

**Please take into consideration**:
- Certain properties (e.g. `dct:publisher`, `dct:creator`, `dcat:contactPoint`) in several of the main classes refer to the supporting classes (e.g. [`foaf:Agent`](#agent), [`vcard:Kind`](#kind)). These properties link to supporting resources. The same Agent may be reused for creator and publisher, or separate Agents may be identified when their roles are fulfilled by different entities.

- It is possible that not all main classes of the metadata schema are necessary to describe your data or the structure of your data. For example, [DataService](#data-service) or [DatasetSeries](#dataset-series) might not apply to all datasets described/onboarded in the National Health Data Catalogue.

- The power of [DCAT](https://www.w3.org/TR/vocab-dcat-3/) is that it is flexible in use, giving a data holder the ability to reflect the structure of their data by using the different classes.

- We aim to collect mapping examples from different data sources [here](https://health-ri.atlassian.net/wiki/spaces/FSD/folder/736985095). Currently, this collection only holds mapping examples to v1 though.

- Please visit Confluence for general information about the [metadata schema](https://health-ri.atlassian.net/wiki/spaces/FSD/pages/279281676/4A+Metadata+mapping) and [metadata mapping](https://health-ri.atlassian.net/wiki/spaces/FSD/pages/290291734/Mapping+tutorial).


## Usage Notes on Schema / Mapping
Supportive classes are included because they form the range of properties used by the main classes [additional requirements to properties for the entity]. They enrich the main classes which are the core entities in the catalogue. Both structures are further divided into **mandatory properties** for conformance and **recommended properties** for richer metadata. 

The separation from above helps modularize metadata and makes it easier to reuse supporting elements across multiple datasets or services. It helps users to easier use those classes. To apply it:
- Start with main classes -> Identify the datasets, services, and distributions you need to describe.
- Link supportive classes –> Use them wherever the schema specifies a property range (e.g., publisher → Agent).
- Always fill mandatory properties –> Ensure your metadata is valid and interoperable.
- Check controlled vocabulary requirements -> For each property, consult [Controlled Vocabularies](#controlled-vocabularies) to determine whether a MUST, AT LEAST 1, or MAY requirement applies, as controlled vocabularies ensure consistent and interoperable values.
- Add recommended properties where possible –> Improve FAIRness and increases the overall maturity of your metadata.
- Reuse supportive entities –> E.g. if the same Agent or Identifier appears in multiple records, reference it rather than duplicating it.

The following sections describe each class in detail, including its role in the schema, its mandatory and recommended properties, and examples of how to populate them.

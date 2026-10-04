# Introduction 

## Scope and Current State of the Schema
Building on the [1st version of the metadata schema](https://github.com/Health-RI/health-ri-metadata/tree/master), version 2 aims to incorporate both [DCAT-AP NL](https://geonovum.github.io/DCAT-AP-NL30/) and the (yet-to-be-finalized) [HealthDCAT-AP](https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-6/), along with Health-RI-specific requirements for the [National Health Data Catalogue](https://catalogus.healthdata.nl/). It introduces several health-related properties (marked in blue in the UML diagram below), with suggested or required controlled vocabularies where applicable.

**Important Note:** HealthDCAT-AP has not yet been officially finalized and remains subject to change. Once its official release is published, Health-RI will reevaluate compatibility with HealthDCAT-AP. This version is based on the draft dated *16-12-2024*. In that draft, the cardinalities of HealthDCAT-AP vary depending on different access rights (public, restricted, non-public). For now, compliance is ensured with the [open version](https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-6/), using its UML diagram for reference.

Additionally, several **ELSI**-related metadata fields, as [gathered](https://health-ri.atlassian.net/wiki/spaces/HA/pages/469893133/Metadata+rondom+gebruiksvoorwaarden+en+authenticatie+autorisatie+en+ELSI+aspecten#Catalogus) by the Health-RI ELSI team, have been included in this version 2. These fields are not mandatory but will be evaluated upon implementation in the catalogue.

To indicate the **nature of the data** (e.g., whole genome sequencing or questionnaire data), we propose using `healthdcatap:healthTheme`. For **synthetic data**, use `dct:type` with the required controlled vocabulary in the `dcat:Dataset` class.

Several classes from [DCAT-AP NL](https://docs.geostandaarden.nl/dcat/dcat-ap-nl30/) and draft [HealthDCAT-AP](https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-6/) have been included but not further specified for Health-RI yet. This includes the **DataService** class, meaning that these classes can be used but are not yet tailored to specific dataholder needs for the National Health Data Catalogue.

  
## Used Prefixes
<table class="larger-font">
  <thead>
    <tr>
      <th>Prefix</th>
      <th>Namespace IRI</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>adms</td><td>http://www.w3.org/ns/adms#</td></tr>
    <tr><td>dcat</td><td>http://www.w3.org/ns/dcat#</td></tr>
    <tr><td>dcatap</td><td>http://data.europa.eu/r5r/</td></tr>
    <tr><td>dct</td><td>http://purl.org/dc/terms/</td></tr>
    <tr><td>dpv</td><td>https://w3id.org/dpv#</td></tr>
    <tr><td>dqv</td><td>http://www.w3.org/ns/dqv#</td></tr>
    <tr><td>eli</td><td>http://data.europa.eu/eli/ontology#</td></tr>
    <tr><td>hri</td><td>https://w3id.org/health-ri/metadata-vocabulary#</td></tr>
    <tr><td>foaf</td><td>http://xmlns.com/foaf/0.1/</td></tr>
    <tr><td>owl</td><td>http://www.w3.org/2002/07/owl#</td></tr>
    <tr><td>rdf</td><td>http://www.w3.org/1999/02/22-rdf-syntax-ns#</td></tr>
    <tr><td>rdfs</td><td>http://www.w3.org/2000/01/rdf-schema#</td></tr>
    <tr><td>skos</td><td>http://www.w3.org/2004/02/skos/core#</td></tr>
    <tr><td>spdx</td><td>http://spdx.org/rdf/terms#</td></tr>
    <tr><td>time</td><td>http://www.w3.org/2006/time#</td></tr>
    <tr><td>vcard</td><td>http://www.w3.org/2006/vcard/ns#</td></tr>
    <tr><td>xsd</td><td>http://www.w3.org/2001/XMLSchema#</td></tr>
    <tr><td>healthdcatap</td><td>http://healthdataportal.eu/ns/health#</td></tr>
  </tbody>
</table>

# Overview and Diagram
An overview of the metadata schema core is presented in the UML diagram below. This UML diagram showcases primary classes (entities), excluding detailed definitions such as `rdfs:label` and `rdfs:comment`. Each block represents a class and lists its attributes (properties). Where properties reference another class, their range is displayed in pink font.

If a class is linked to another class with a closed arrow, it inherits all properties from the other class (e.g., `dcat:Dataset` inherits from `dcat:Resource`). Other arrows represent relationships, including their types (e.g., `dcat:Dataset` connects to a `dcat:DatasetSeries` via `dcat:inSeries`), along with cardinalities (e.g., `dcat:Dataset` connects to zero or more `dcat:DatasetSeries`). **Mandatory relationships** are marked with dark labels, while **recommended relationships** use a lighter color.

The UML diagram separates **main classes** from **supporting classes**. While relationships between main classes are indicated by arrows, supporting class relationships are not visually connected via arrows to maintain clarity in the diagram. Instead, they can be deduced from the pink-colored property ranges listed per class.

Properties derived from draft [HealthDCAT-AP](https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-6/) (mostly within the `dcat:Dataset` class) are marked blue.

A tabular overview of all classes and properties—including their range, cardinality, controlled vocabulary (if applicable), and usage notes—is provided below. A reference sheet containing this information can be found [here](https://github.com/Health-RI/health-ri-metadata/blob/develop/Documents/Metadata_CoreGenericHealth_v2.xlsx). This sheet also documents property histories (compared to v1 of the Health-RI core metadata schema) and specifies the origins of new constraints (whether they stem from DCAT-AP v3, DCAT-AP NL, or HealthDCAT-AP).


## UML Class Diagram v2.0.3

<a href="https://raw.githubusercontent.com/Health-RI/metadata-documentation/main/src/images/HRI_metadata_p2.png" target="_blank">
  <img src="https://raw.githubusercontent.com/Health-RI/metadata-documentation/main/src/images/HRI_metadata_p2.png" alt="Health-RI Metadata Diagram" width=800 height=1100 title="diagram">
</a>

Usage directions for the properties and their associated constraints that apply in the context of this profile, and the range of properties, are listed below.
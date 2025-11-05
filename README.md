# spotifyazureproject
## Bronze Layer
### Objective
Establish the foundational Bronze layer for the Spotify Data Pipeline in Azure to store and manage raw ingested data. This layer ensures secure, structured, and version-controlled ingestion using Azure Data Factory and Logic Apps.

### Azure Resources Deployed
| Resource                        | Name                                    | Purpose                                                                                                                    |
| ------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------- |
| **Azure Data Factory (V2)**    | `df-spotifyrohan`                       | Orchestrates Spotify API ingestion and manages incremental data loads.                                                     |
| **Azure SQL Server + Database** | `rohanspotifyserver` / `spotifydbrohan` | Stores dimensional and fact tables (`DimArtist`, `DimDate`, `DimTrack`, `DimUser`,                                                                                     `FactStream`) for downstream analytics. |
| **Azure Storage Account**       | `spotifystoragerohan`                   | Hosts the **Bronze container**, storing raw JSON/Parquet data and CDC (change data                                                                                       capture) folders.                       |
| **Logic App**                   | `logicappspotifyrohan`                  | Sends automated pipeline-failure/skipped alerts via Outlook when triggered from ADF.                                             

### Implementation Highlights
Created a resource group RG-AzureProject to centrally manage all Spotify pipeline resources.

Configured ADF pipelines (incremental_ingestion, incremental_ingestion_loop) to fetch Spotify data, push to Azure SQL, and store raw data in Bronze storage.

Designed a Logic App workflow triggered by HTTP requests to send email alerts on pipeline completion.

Implemented incremental ingestion with a dynamic ForEachSpotifyRohan loop handling multiple tables and CDC updates.

Organized raw data in Azure Blob Storage → Bronze container, maintaining sub-folders for each entity and its CDC snapshot:
DimArtist, DimArtist_cdc, DimDate, DimTrack, DimUser, FactStream.

Verified end-to-end connectivity between ADF, Azure SQL, and Storage Account.

Published all ADF artifacts and merged the sub-branch into the Git main branch for full version control and CI/CD tracking.

### Technical Stack
Azure Data Factory | Azure SQL Database | Azure DataLake | Logic Apps | GitHub Integration | Incremental ETL

### Outcome
The Bronze Layer successfully stores raw Spotify data with CDC support and triggers email notifications upon pipeline execution, forming the base for upcoming Silver and Gold layers.

### Architecture Diagram
<img width="1917" height="862" alt="image" src="https://github.com/user-attachments/assets/8ef56119-0c59-4605-a5a2-0ee7f4464db7" />
<img width="1919" height="865" alt="image" src="https://github.com/user-attachments/assets/fb94022c-db51-498f-813e-0e2198141c32" />
<img width="1916" height="864" alt="image" src="https://github.com/user-attachments/assets/539a1865-3911-40db-bd54-77f16764050b" />
<img width="1611" height="911" alt="image" src="https://github.com/user-attachments/assets/3aca14e1-38f4-4e72-97c8-34e40090afdc" />
<img width="1918" height="866" alt="image" src="https://github.com/user-attachments/assets/16969775-ad8f-4eef-a11d-bf6bf734fe92" />

### ON Failure Email Alert
<img width="1515" height="732" alt="image" src="https://github.com/user-attachments/assets/95d8406b-12ab-4828-b9ea-6cdcdd8acb62" />

### Silver Layer (Cleansing + Metadata-Driven Transformation)

**Location:** src/silver/

**Objective:** Transform raw ingested data from Bronze into a structured, deduplicated, and schema-evolved Silver layer.

**Key Features**

**Unity Catalog Metastore Setup**

Created a managed Unity Catalog storage (West US 2 region)

Configured new metastore in accounts.azuredatabricks.net linked to the same region

Granted access via IAM → Storage Contributor to Databricks workspace identity

Assigned Gmail account as metastore admin

**Parameterized & Dynamic Notebooks**

Used Jinja templating to dynamically build SQL queries based on metadata parameters

Configurable parameters (table, schema, join type, etc.)

Enabled fully reusable notebooks for all dimension/fact tables

**Schema Evolution & Auto Loader**

Implemented schema evolution with cloudFiles.schemaEvolutionMode = "addNewColumns"

Configured Auto Loader for incremental data ingestion with checkpointing for idempotency

Managed CDC and deduplication using Delta operations

**Utility Functions**

Created modular utilities in utils/transformations.py for:

Dropping redundant columns

Replacing special characters

Flagging records by duration category

Imported dynamically via system path setup for reuse

**Data Quality & Performance**

Handled deduplication, null handling, and consistency checks

Wrote output to Delta format in the Silver zone (toTable("catalog.schema.table"))

### Gold Layer (Business-Ready + Declarative Pipelines)

**Objective:** Transform cleansed data into business-ready fact and dimension tables using Delta Live Tables (DLT).

**Core Highlights**

**DLT Declarative Pipelines**

Configured via resources/spotifyrohan_dab.pipeline.yml

Fully serverless, catalog-aware, and schema-scoped

Enabled automated DAG generation with transformation lineage

**Slowly Changing Dimensions (SCD Type 2)**

Implemented Auto CDC logic in Gold using DLT declarative pipeline syntax

Stored historical dimension records with effective-date logic

Applied UPSERT for fact tables (transactional updates)

**Reusable Components**

Created Python utilities for shared transformations

Added metadata-driven logic for schema and table handling

Populated business views automatically in Gold zone

**DLT Configuration**
catalog: spotify_cata
schema: gold
storage: "dbfs:/pipelines/spotifyrohan_dab_pipeline"
serverless: true
libraries:
  - notebook:
      path: ./src/gold/rohanspotify_dlt/transformations/

**Lineage Tracking**

Automatic lineage visualization in DLT UI

Business audit trail and end-to-end data flow traceable from Bronze → Gold

### CI/CD & Environment Deployment (Dev → QA → Prod)**

**Managed via:** databricks.yml and Asset Bundles

Used Databricks Asset Bundles to automate deployment across environments

Defined parameterized environment variables for catalog, schema, and workspace host

bundle.sourcePath and bundle.target automatically inject the correct config at deploy time

**Commands used:**
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle deploy -t qa
databricks bundle deploy -t prod

Each deployment linked to a unique workspace & Unity Catalog instance

### Version Control & Git Integration

Connected Databricks repo to GitHub using Linked Service

Created dedicated repo folder: spotifyazureproject

**Branched workflow:**
feature/<component_name> → rohan → main

Commits handled through Databricks Git UI → “Commit & Push”

Automated YAML + Python sync to GitHub repo

### Key Learnings & Highlights

End-to-end Azure Data Engineering solution

Advanced Databricks Unity Catalog, DLT, Auto Loader, SCD Type 2

Full CI/CD automation via Asset Bundles

Metadata-driven transformation using Jinja + Python

Data governance and security via Unity Catalog

Real-time data quality monitoring and schema evolution

Modular, reusable pipeline design

### Setup Instructions

Clone this repository into your Databricks workspace:

git clone https://github.com/<yourusername>/spotifyazureproject.git
cd spotifyazureproject/azuredabrohan

**Initialize and deploy:**

databricks bundle validate -t dev
databricks bundle deploy -t dev

**Environment targets:**

dev → Development workspace (default)
qa → Testing environment
prod → Production environment

To visualize the DLT pipeline, navigate to
Workflows → Delta Live Tables → spotifyrohan_dab_pipeline

### Summary

This project showcases advanced Azure Data Engineering & Databricks capabilities:

Scalable multi-layer architecture (Bronze → Silver → Gold)

Parameterized transformations using metadata & Jinja

Fully automated CI/CD with Databricks Asset Bundles

End-to-end governance with Unity Catalog and Azure IAM

Real-time orchestration using ADF + Logic Apps

**Outcome:** Production-grade, reusable, and governed data platform design demonstrating advanced skills in Azure Data Factory, Databricks, and modern data engineering practices.

<img width="1919" height="908" alt="image" src="https://github.com/user-attachments/assets/69f677a2-bd39-4db7-873d-c017f9a1b50a" />

<img width="1870" height="620" alt="image" src="https://github.com/user-attachments/assets/3d704f78-fb04-444e-b782-1e0f7323b5ad" />

<img width="1862" height="915" alt="image" src="https://github.com/user-attachments/assets/8e2f9d5f-37c5-4730-a207-afedb96449f1" />

<img width="997" height="460" alt="1" src="https://github.com/user-attachments/assets/e99269e0-4a82-446e-ae8d-02b1e5cccc82" />

### Architecture Overview

               ┌─────────────────────────────┐
               │ Azure Data Factory (ADF)    │
               │  - Ingest raw data from     │
               │    APIs / DB / Storage      │
               └──────────────┬──────────────┘
                              │
                              ▼
                 ┌────────────────────────┐
                 │     Bronze Layer        │
                 │  (Raw landing in ADLS)  │
                 │  - Incremental loads    │
                 │  - CDC & Backfills      │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌────────────────────────┐
                 │     Silver Layer        │
                 │  (Cleansed + Structured)│
                 │  - Auto Loader          │
                 │  - Schema Evolution     │
                 │  - Jinja Parameterized  │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌────────────────────────┐
                 │      Gold Layer         │
                 │  (Business-Ready DLT)   │
                 │  - SCD Type 2           │
                 │  - Fact & Dimension     │
                 │  - Lineage Tracking     │
                 └────────────┬────────────┘
                              │
                              ▼
           ┌────────────────────────────────────┐
           │  Azure SQL DB / Power BI Reports   │
           │  - Analytics & Visualization       │
           └────────────────────────────────────┘

               ┌────────────────────────────────┐
               │ Azure Logic Apps & Asset Bundles │
               │  - CI/CD: Dev → QA → Prod       │
               │  - Alerts, validation, & deploy │
               └────────────────────────────────┘



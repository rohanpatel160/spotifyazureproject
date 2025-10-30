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

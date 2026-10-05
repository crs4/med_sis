
<div align="center">

# Med-SIS
**Med-SIS: Soil Information System (SIS) prototype** 

[![License: GPL v3](https://img.shields.io/github/license/crs4/med_sis)](./LICENSE)

[Live app](https://soils4med.crs4.it/) 

</div>

---

## About
A **Soil Information System (SIS)** is an integrated information system designed to facilitate the storage, analysis, management and dissemination of soil data.
To assess and monitor soil health and promote sustainable soil management in the Mediterranean region, there is a pressing need to improve the availability and accessibility of soil data. 
One of the objectives of the SOILS4MED project (SOIL health monitoring and information systems FOR sustainable soil management in the MEDiterranean region) which addresses this need by designing and developing a decentralised network of country-based soil information systems.
<p> 
This network aims to improve the interoperability, management, governance, and utilization of soil data across the Mediterranean region by establishing a federated architecture of SISs, starting with the development of a harmonized data model aligned with the World Reference Base for Soil Resources (WRB 2022), alongside the implementation of core functionalities for the ingestion, integration, and management of both legacy and newly acquired soil data.
</p>
<p>
Soils4Med is a project funded by **[PRIMA](https://prima-med.org/)** - Partnership for Research and Innovation in the Mediterranean Area.
</p>
<p>
The **Med-SIS** was designed and implemented by **[CRS4](https://www.crs4.it/)** (Roberto Demontis, Eva Lorrai, Laura Muscas, Piergiorgio Palla) with the support of all project partners.
</p>

## Components
The main components of the Med-SIS are two:

| Component | Role | Stack |
|---|---|---|
| Web GIS Catalogue | Soil data management | [Geonode](https://geonode.org) |
| Back Office | Med-SIS utilities for Soil data management | [Nextjs](https://nextjs.org) | 

### Web GIs Catalogue
It is a Geonode WEB GIS catalogue for Soil data management 

- **Geonode** 5.1.0  
- **Geoserver** 2.28.4 
- **Django** 5.2.17
- **djangorestframework** 3.17.2
- **Python** 3.12

### Back Office
It is a NextJS application that use the PrimeReact REACT Diamond template

- **React** 18.3.0
- **NextJS** 15.5.15
- **Primereact** 10.2.1

---


## Getting started

### Requirenments
- **docker compose Desktop or Engine

### 0. clone the repository 
```bash
    git clone https://github.com/crs4/med_sis.git -b <your_branch>
    cd med_sis
```

### 1. copy the .env.sample file in a new file named .env 

```bash
cp .env.sample .env
```

### 2. edit the environment variables in the new .env file (see the comments in the file)

```bash
vi .env
```

### 3. inside the root directory run docker compose build

```bash
docker compose build 
```

### 3. inside the root directory run the docker compose application

```bash
docker compose up -d 
```
### 4. Access the site  

## License

The source code in this repository is licensed under the **GNU General Public
License v3.0 (GPL-3.0)** — see [`LICENSE`](./LICENSE) for the full text.

## Contact
For any question regarding the MED-SIS contact the developers at **demontis@crs4.it**.
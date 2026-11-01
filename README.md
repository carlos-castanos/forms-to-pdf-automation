# Forms to PDF Automation

A Python-based workflow automation project that integrates form responses, Excel datasets, and PDF documents to streamline recurring data processing tasks.

## Project Overview

This project automates the collection, integration, and processing of monthly form responses. It combines submitted data with a master dataset, matches records using unique identifiers, and updates corresponding PDF forms.

## Key Features

- Excel data extraction using pandas.
- Integration of form responses with a master dataset.
- Record matching using unique identifiers.
- Automated PDF form field updates.
- Monthly activity data processing.
- Automatic calculation of cumulative hours.
- PDF form preparation for a new reporting period.

## Workflow

1. **Data Input:** Read Excel files containing form responses from multiple groups.
2. **Data Integration:** Match submitted information with a master dataset using unique IDs.
3. **Data Processing:** Organize records and prepare values for PDF form fields.
4. **PDF Automation:** Update the corresponding PDF documents.
5. **Aggregation:** Calculate cumulative hours and update summary fields.

## Technologies

- Python
- pandas
- openpyxl
- pypdf
- Excel data processing
- PDF form automation

## Project Structure

- `main.py` — Main workflow orchestration.
- `respuestas.py` — Reads and structures form responses.
- `lista_maestra.py` — Loads reference data.
- `datos_publicadores.py` — Integrates datasets using unique identifiers.
- `pdf.py` — Handles PDF field updates and hour calculations.
- `limpiar_tarjetas.py` — Prepares PDF forms for a new reporting period.

## Business Value

The project reduces repetitive administrative work by connecting multiple data sources and automating document updates through a modular Python workflow.

## Data Privacy

Original personal records and documents are excluded. This repository is intended to demonstrate the automation logic using a sanitized project structure.

## Project Status

In development.

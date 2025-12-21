# oracle-of-delphi
an end-to-end ecommerce analytics solution with forecast capability

# Oracle of Delphi — Hybrid Sales Data Preparation

This repository contains the **data hybridization logic** used to prepare a realistic SME sales dataset for a sales intelligence platform.

## What this is
- Real UCL e-commerce data (1 year) used as a base
- +1 year **synthetic extension**
- Transaction-level
- Designed to simulate real client data conditions

## Why no dataset here
The final hybrid dataset exceeds GitHub size limits (>100MB).  
Instead, this repo provides the **reproducible script** used to generate it.

## Artifacts
- `hybridize_ucl_data.py` — generates the 2-year hybrid dataset

## Purpose
This step is a **hard prerequisite** for downstream work:
- Data ingestion
- Validation
- Analytics & forecasting

The output of this script serves as the input contract for the *Oracle of Delphi* project.

last updated 2025-12-21

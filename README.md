# Kaizen Talent Analytics

![Dashboard Analytics](https://images.pexels.com/photos/435063/pexels-photo-435063.jpeg)

This project is part of my application for the Netflix Analyst, Talent Analytics (Machine Learning) role. It demonstrates my ability to architect a modular, extensible, and ML-ready system for predictive hiring analytics, including talent funnel modeling, sourcing analysis, and candidate forecasting.

## Overview

The `kaizen_talent_analytics` system is designed as a self-evolving, modular Python package that integrates machine learning models and analytics components to support talent acquisition and retention strategies.

### Key Components

- **Fingerprint Engine**: Generates unique fingerprints for prompts.
- **Diff Tracker**: Logs differences between outputs for audit and analysis.
- **Goal Tracker**: Manages goals related to talent analytics workflows.
- **Session Audit**: Logs session activities for traceability.
- **Visual Loop Composer**: Parses markdown to build prompt flow graphs.
- **Predictive Models**: Abstract base and specific models for retention, time to hire, and flight risk.
- **Connectors**: Includes an ATS adapter to ingest applicant tracking system event data.

## Extensibility

This system is designed for easy integration into the existing `nexus-UF` dashboard framework and can be extended with proprietary logic, additional models, and UI components.

## Example Usage

See the example workflow in [`examples/sample_workflow.py`](examples/sample_workflow.py) for a demonstration of how to use the fingerprint engine and predictive models.

---

Thank you for reviewing this project as part of my Netflix application.

## Deployment Instructions

### Render Deployment

- Build Command:  
  `pip install -r requirements_render.txt`

- Start Command:  
  `python3 talent_insights.py`

- Render configuration is defined in `render.yaml`.

### Vercel Deployment

- Vercel is configured to deploy the Python backend using the `@vercel/python` runtime.

- The `vercel.json` file routes all requests to `talent_insights.py`.

- To deploy on Vercel, ensure you have the Vercel CLI installed and run:  
  `vercel --prod`

- Vercel will automatically detect the Python runtime and start the app accordingly.

### Notes

- Ensure environment variables and secrets are configured appropriately on both platforms.

- For local testing, you can run:  
  `python3 talent_insights.py`

- For any issues during deployment, check the platform logs for errors.

---

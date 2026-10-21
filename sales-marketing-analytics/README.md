# Sales & Marketing Analytics with Python, HubSpot and Power BI

This project follows a practical analyst workflow: start with a public sales dataset, clean and explore it in Python, prepare report-ready files, and use Power BI to turn the results into a business dashboard. An optional HubSpot connection exports CRM contacts and deals when authorized API access is available.

## Business questions

- Which months, regions and product categories bring in the most sales?
- Are strong sales also producing healthy profit?
- Which product groups are losing money?
- How do customer segments and order values compare?
- If CRM data is available, what does the HubSpot deal pipeline look like alongside sales performance?

## Tools

- **Python and pandas:** data download, cleaning, validation, aggregation and export
- **HubSpot CRM API (optional):** read-only contacts and deals export
- **Power BI Desktop:** interactive reporting and KPI visuals

## Dataset

The main dataset is the public **Sample Superstore** retail dataset hosted in a public GitHub repository: [Dataset source](https://github.com/atharvadhankarr/SampleSuperstore-Dataset).

The Python script downloads the CSV on first run. This is a sample retail dataset, not a company's private campaign data. HubSpot is a separate optional source for actual CRM pipeline information and requires your own authorized private-app token.

## Project structure

    sales-marketing-analytics/
    ├── analyze_sales.py
    ├── hubspot_export.py
    ├── requirements.txt
    ├── .gitignore
    └── powerbi/
        └── README.md

Generated data is saved under powerbi/exports/ when you run the scripts. The exports are excluded from Git to avoid publishing generated datasets or private CRM records.

## Run locally

Use Python 3.10 or newer.

    python -m venv .venv

On Windows, activate the environment and install dependencies:

    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python analyze_sales.py

The script generates sales_clean.csv, monthly_performance.csv, category_performance.csv, regional_performance.csv, product_profitability.csv, customer_summary.csv and analysis_summary.txt inside powerbi/exports/.

The summary is calculated from the dataset each time; results are not hard-coded because the source file may change.

## Optional HubSpot export

1. In HubSpot, create a private app with read-only access to the CRM objects you need.
2. Keep the token private. Do not paste it into a Python file or commit it to GitHub.
3. Set the environment variable and run the export script.

PowerShell:

    $env:HUBSPOT_ACCESS_TOKEN="your_private_app_token"
    python hubspot_export.py

macOS/Linux:

    export HUBSPOT_ACCESS_TOKEN="your_private_app_token"
    python hubspot_export.py

The script exports contact lifecycle fields and deal amount/stage/date fields to local CSV files. It only reads records; it does not create or update HubSpot data. Use only data you are authorized to access.

## Build the Power BI report

Open Power BI Desktop and import the generated CSVs using Get data → Text/CSV. The dashboard layout and suggested DAX measures are in [powerbi/README.md](powerbi/README.md).

Suggested pages:
- **Executive Overview:** sales, profit, margin, orders, monthly trend and regional/category performance
- **Product Profitability:** sub-category profit, discount patterns and loss-making items
- **Customer & Marketing:** segment performance, average order value and repeat-order patterns
- **CRM Pipeline (optional):** HubSpot deals by stage, amount, creation date and owner

Add date, region, category and segment slicers, format profit margin as a percentage, and use consistent number formatting.

## Business value

The aim is to move beyond reporting totals and give a sales or marketing team a clearer view of where revenue comes from, where profit is under pressure, and which areas deserve a closer look. Recommendations should be validated with business context before being used for real decisions.

## Limitations

- Sample Superstore is a practice dataset, not a live company's sales ledger.
- It does not contain campaign spend, impressions, clicks or attributed conversions, so it cannot calculate true marketing ROI.
- HubSpot export is optional and has not been run against a live portal in this project.
- A Power BI .pbix file is not generated automatically; the guide explains how to build the report in Power BI Desktop.

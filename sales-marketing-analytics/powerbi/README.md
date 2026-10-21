# Power BI report setup

Run the Python scripts first. In Power BI Desktop, choose Get data → Text/CSV and import the files from powerbi/exports/:

- sales_clean.csv — detailed transaction-level data
- monthly_performance.csv — monthly trend
- category_performance.csv — category performance
- regional_performance.csv — regional performance
- product_profitability.csv — category/sub-category profitability
- customer_summary.csv — customer sales, orders and average order value
- Optional HubSpot exports: hubspot_contacts.csv and hubspot_deals.csv



# Suggested report pages

1. **Executive Overview:** sales, profit, profit margin, orders and customers; monthly sales/profit; category and regional performance.
2. **Product & Profitability:** profit by sub-category, sales-vs-profit scatter plot, discount-vs-profit analysis and loss-making items.
3. **Customer & Marketing:** sales by segment, average order value and repeat-order patterns.


## Suggested DAX measures

    Total Sales = SUM(sales_clean[Sales])
    Total Profit = SUM(sales_clean[Profit])
    Total Orders = DISTINCTCOUNT(sales_clean[Order ID])
    Total Customers = DISTINCTCOUNT(sales_clean[Customer ID])
    Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)
    Average Order Value = DIVIDE([Total Sales], [Total Orders], 0)
    Loss-Making Rows = CALCULATE(COUNTROWS(sales_clean), sales_clean[Profit] < 0)

Column names may vary slightly by dataset version. Check the Fields pane after import, set Order Date to Date, and use a calendar table for production reporting.

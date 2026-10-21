"""Download, clean and analyze a public retail sales dataset for Power BI."""
from pathlib import Path
from urllib.request import urlopen
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "powerbi" / "exports"
DATA_URL = "https://raw.githubusercontent.com/atharvadhankarr/SampleSuperstore-Dataset/main/SampleSuperstore.csv"


def find_col(df, options):
    for col in options:
        if col in df.columns:
            return col
    raise ValueError(f"Expected one of these columns: {options}")


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    source = DATA_DIR / "sample_superstore.csv"
    if not source.exists():
        print("Downloading public Sample Superstore data...")
        try:
            with urlopen(DATA_URL, timeout=30) as response:
                source.write_bytes(response.read())
        except Exception as exc:
            raise RuntimeError(f"Download failed. Download {DATA_URL} and save it to {source}") from exc

    df = pd.read_csv(source, encoding="latin-1")
    df.columns = [c.strip().replace("\\ufeff", "") for c in df.columns]
    date = find_col(df, ["Order Date", "Order_Date"])
    ship_date = find_col(df, ["Ship Date", "Ship_Date"])
    sales = find_col(df, ["Sales", "sales"])
    profit = find_col(df, ["Profit", "profit"])
    qty = find_col(df, ["Quantity", "quantity"])
    category = find_col(df, ["Category", "category"])
    subcategory = find_col(df, ["Sub-Category", "Sub Category", "Sub_Category"])
    region = find_col(df, ["Region", "region"])
    segment = find_col(df, ["Segment", "segment"])
    order_id = find_col(df, ["Order ID", "Order_ID"])
    customer_id = find_col(df, ["Customer ID", "Customer_ID"])
    discount = find_col(df, ["Discount", "discount"])

    for col in [sales, profit, qty, discount]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df[date] = pd.to_datetime(df[date], errors="coerce")
    df[ship_date] = pd.to_datetime(df[ship_date], errors="coerce")
    df = df.dropna(subset=[date, sales, profit, order_id]).drop_duplicates()
    df["Order Month"] = df[date].dt.to_period("M").astype(str)
    df["Profit Margin %"] = df[profit].div(df[sales].where(df[sales] != 0)) * 100
    df["Delivery Days"] = (df[ship_date] - df[date]).dt.days
    df["Is Profitable"] = df[profit] > 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_DIR / "sales_clean.csv", index=False)
    df.groupby("Order Month", as_index=False).agg(
        Sales=(sales, "sum"), Profit=(profit, "sum"),
        Orders=(order_id, "nunique"), Quantity=(qty, "sum")
    ).to_csv(OUTPUT_DIR / "monthly_performance.csv", index=False)

    cat = df.groupby(category, as_index=False).agg(
        Sales=(sales, "sum"), Profit=(profit, "sum"),
        Orders=(order_id, "nunique"), Quantity=(qty, "sum"))
    cat["Profit Margin %"] = cat["Profit"] / cat["Sales"].replace(0, float("nan")) * 100
    cat.to_csv(OUTPUT_DIR / "category_performance.csv", index=False)

    df.groupby(region, as_index=False).agg(
        Sales=(sales, "sum"), Profit=(profit, "sum"),
        Orders=(order_id, "nunique")
    ).to_csv(OUTPUT_DIR / "regional_performance.csv", index=False)

    products = df.groupby([category, subcategory], as_index=False).agg(
        Sales=(sales, "sum"), Profit=(profit, "sum"), Quantity=(qty, "sum")
    ).sort_values("Profit")
    products.to_csv(OUTPUT_DIR / "product_profitability.csv", index=False)

    customer = df.groupby(customer_id, as_index=False).agg(
        Sales=(sales, "sum"), Profit=(profit, "sum"),
        Orders=(order_id, "nunique"), Last_Order=(date, "max"))
    customer["Average Order Value"] = customer["Sales"] / customer["Orders"].replace(0, float("nan"))
    customer.to_csv(OUTPUT_DIR / "customer_summary.csv", index=False)

    total_sales, total_profit = df[sales].sum(), df[profit].sum()
    summary = [
        "SALES ANALYSIS — RUN SUMMARY", f"Rows analyzed: {len(df):,}",
        f"Total sales: {total_sales:,.2f}", f"Total profit: {total_profit:,.2f}",
        f"Profit margin: {(total_profit / total_sales * 100) if total_sales else 0:.2f}%",
        f"Unique orders: {df[order_id].nunique():,}",
        f"Unique customers: {df[customer_id].nunique():,}",
        f"Highest-sales category: {cat.sort_values('Sales', ascending=False).iloc[0][category]}",
        f"Loss-making transaction rows: {(df[profit] < 0).sum():,}",
        "The source is a sample retail dataset, not live campaign-attribution data."
    ]
    (OUTPUT_DIR / "analysis_summary.txt").write_text("\n".join(summary), encoding="utf-8")
    print("\n".join(summary))
    print(f"\nPower BI exports created in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

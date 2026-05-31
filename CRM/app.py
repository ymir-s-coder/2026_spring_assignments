import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gradio as gr

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "clean_sales_data.csv")

# ------------------------------------------------------------
# Data loading
# ------------------------------------------------------------
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    if "OrderDateKey" in df.columns:
        df["OrderDateKey"] = df["OrderDateKey"].astype(str)
        df["OrderDate"] = pd.to_datetime(df["OrderDateKey"], format="%Y%m%d", errors="coerce")
        df["Year"] = df["OrderDate"].dt.year
        df["Month"] = df["OrderDate"].dt.month
        df["YearMonth"] = df["OrderDate"].dt.to_period("M").astype(str)

    if "Sales Amount" in df.columns and "Total Product Cost" in df.columns:
        df["Profit"] = df["Sales Amount"] - df["Total Product Cost"]
        df["Profit Margin"] = np.where(df["Sales Amount"] != 0, df["Profit"] / df["Sales Amount"], 0)

    return df


df = load_data()

FEATURE_COLS = [
    "CustomerKey",
    "ProductKey",
    "SalesTerritoryKey",
    "Order Quantity",
    "Unit Price",
    "Unit Price Discount Pct",
    "Year",
    "Month",
]
FEATURE_COLS = [col for col in FEATURE_COLS if col in df.columns]

# ------------------------------------------------------------
# Format helpers
# ------------------------------------------------------------
def money(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    value = float(value)
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:,.1f}K"
    return f"${value:,.2f}"


def number(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{float(value):,.0f}"


def percent(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{float(value) * 100:.1f}%"


# ------------------------------------------------------------
# Static HTML blocks
# ------------------------------------------------------------
def hero_html() -> str:
    return """
<section class="hero-shell">
  <div class="hero-left">
    <div class="eyebrow">CRM Sales Analytics</div>
    <h1>Customer Sales<br>Analysis</h1>
    <p>This application analyzes cleaned sales data, checks business performance, finds CRM insights, and tests prediction models for marketing decisions.</p>
  </div>

  <div class="flow-grid">
    <div class="flow-item">
      <div class="flow-icon">▦</div>
      <h3>Data Check</h3>
      <p>Verify rows, columns, missing values, duplicates, and date range.</p>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-item">
      <div class="flow-icon">⌕</div>
      <h3>EDA</h3>
      <p>Explore revenue, cost, quantity, customers, products, and trends.</p>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-item warm">
      <div class="flow-icon">◎</div>
      <h3>CRM Insight</h3>
      <p>Identify important products, customers, and sales territories.</p>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-item">
      <div class="flow-icon">↗</div>
      <h3>Prediction</h3>
      <p>Train classification and regression models on prepared features.</p>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-item warm">
      <div class="flow-icon">✈</div>
      <h3>Action</h3>
      <p>Convert analysis results into practical CRM recommendations.</p>
    </div>
  </div>
</section>
"""


def kpi_cards_html() -> str:
    total_revenue = df["Sales Amount"].sum() if "Sales Amount" in df.columns else np.nan
    total_profit = df["Profit"].sum() if "Profit" in df.columns else np.nan
    orders = df["SalesOrderLineKey"].nunique() if "SalesOrderLineKey" in df.columns else len(df)
    avg_sales = df["Sales Amount"].mean() if "Sales Amount" in df.columns else np.nan
    products = df["ProductKey"].nunique() if "ProductKey" in df.columns else np.nan
    customers = df["CustomerKey"].nunique() if "CustomerKey" in df.columns else np.nan

    cards = [
        ("□", "Total Revenue", money(total_revenue), "Overall sales scale"),
        ("🛒", "Orders", number(orders), "Sales line volume"),
        ("◇", "Avg Sales", money(avg_sales), "Average transaction value"),
        ("▣", "Products", number(products), "Active product base"),
        ("♙", "Customers", number(customers), "Unique customer base"),
        ("$", "Total Profit", money(total_profit), "Revenue after product cost"),
    ]

    html = '<section class="kpi-grid">'
    for icon, title, value, desc in cards:
        html += f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div>
                <p class="kpi-label">{title}</p>
                <h2>{value}</h2>
                <p class="kpi-desc">{desc}</p>
            </div>
        </div>
        """
    html += "</section>"
    return html


def intro_panel_html() -> str:
    rows = df.shape[0]
    cols = df.shape[1]
    missing = int(df.isna().sum().sum())
    duplicated = int(df.duplicated().sum())
    min_date = df["OrderDate"].min().date() if "OrderDate" in df.columns else "N/A"
    max_date = df["OrderDate"].max().date() if "OrderDate" in df.columns else "N/A"

    return f"""
<div class="section-head">
  <div>
    <span class="eyebrow">Data Verification</span>
    <h2>Dataset Check</h2>
    <p>This section verifies that the dashboard is using the cleaned project dataset. The values below are calculated directly from <b>clean_sales_data.csv</b>. Date keys are converted into Year, Month, and YearMonth. Profit is calculated as Sales Amount − Total Product Cost.</p>
  </div>
</div>
<div class="mini-stats">
  <div><span>Rows</span><strong>{number(rows)}</strong></div>
  <div><span>Columns</span><strong>{number(cols)}</strong></div>
  <div><span>Missing Values</span><strong>{number(missing)}</strong></div>
  <div><span>Duplicated Rows</span><strong>{number(duplicated)}</strong></div>
  <div><span>Date Range</span><strong>{min_date} → {max_date}</strong></div>
</div>
"""


def conclusion_html() -> str:
    return """
<div class="section-head">
  <div>
    <span class="eyebrow">Final Output</span>
    <h2>Conclusion & Marketing Action</h2>
    <p>The dashboard connects data verification, EDA, CRM insight, and prediction models. The final goal is to support concrete marketing decisions, not only to display charts.</p>
  </div>
</div>
<section class="action-grid">
  <div class="action-card">
    <div class="action-icon">◎</div>
    <h3>Target High-Value Segments</h3>
    <p>Use classification results to identify high-value purchases and prioritize CRM campaigns.</p>
  </div>
  <div class="action-card">
    <div class="action-icon">◇</div>
    <h3>Promote Top Products</h3>
    <p>Increase visibility for products and categories that generate high revenue and profit.</p>
  </div>
  <div class="action-card">
    <div class="action-icon">↗</div>
    <h3>Optimize Discounts</h3>
    <p>Use sales prediction to test how discount and quantity changes influence expected sales.</p>
  </div>
  <div class="action-card">
    <div class="action-icon">✉</div>
    <h3>Personalized Campaigns</h3>
    <p>Segment customers by purchase activity, revenue, and predicted purchase value.</p>
  </div>
</section>
"""


# ------------------------------------------------------------
# Tables
# ------------------------------------------------------------
def get_data_preview():
    return df.head(30)


def get_column_info():
    return pd.DataFrame({
        "Column": df.columns,
        "Data Type": [str(df[col].dtype) for col in df.columns],
        "Missing Values": [int(df[col].isna().sum()) for col in df.columns],
        "Unique Values": [int(df[col].nunique()) for col in df.columns],
    })


def get_kpis():
    return pd.DataFrame({
        "KPI": [
            "Total Revenue",
            "Total Profit",
            "Orders / Sales Lines",
            "Average Sales Amount",
            "Unique Products",
            "Unique Customers",
            "Sales Territories",
        ],
        "Value": [
            money(df["Sales Amount"].sum()),
            money(df["Profit"].sum()),
            number(df["SalesOrderLineKey"].nunique() if "SalesOrderLineKey" in df.columns else len(df)),
            money(df["Sales Amount"].mean()),
            number(df["ProductKey"].nunique() if "ProductKey" in df.columns else np.nan),
            number(df["CustomerKey"].nunique() if "CustomerKey" in df.columns else np.nan),
            number(df["SalesTerritoryKey"].nunique() if "SalesTerritoryKey" in df.columns else np.nan),
        ],
        "Business Meaning": [
            "Overall sales scale",
            "Revenue after product cost",
            "Transaction-level business volume",
            "Average value per sales line",
            "Product variety",
            "Customer base size",
            "Regional sales coverage",
        ],
    })


def top_products_table(top_n):
    return (
        df.groupby("ProductKey", as_index=False)
        .agg(
            Total_Revenue=("Sales Amount", "sum"),
            Total_Quantity=("Order Quantity", "sum"),
            Average_Sales=("Sales Amount", "mean"),
            Total_Profit=("Profit", "sum"),
        )
        .sort_values("Total_Revenue", ascending=False)
        .head(int(top_n))
    )


def top_customers_table(top_n):
    return (
        df.groupby("CustomerKey", as_index=False)
        .agg(
            Purchase_Count=("SalesOrderLineKey", "count"),
            Total_Revenue=("Sales Amount", "sum"),
            Average_Purchase=("Sales Amount", "mean"),
            Total_Profit=("Profit", "sum"),
        )
        .sort_values("Total_Revenue", ascending=False)
        .head(int(top_n))
    )


def territory_table():
    return (
        df.groupby("SalesTerritoryKey", as_index=False)
        .agg(
            Total_Revenue=("Sales Amount", "sum"),
            Total_Profit=("Profit", "sum"),
            Orders=("SalesOrderLineKey", "count"),
            Customers=("CustomerKey", "nunique"),
        )
        .sort_values("Total_Revenue", ascending=False)
    )


# ------------------------------------------------------------
# Plot helpers
# ------------------------------------------------------------
def beautify_ax(ax, title: str, xlabel: str, ylabel: str):
    ax.set_title(title, fontsize=14, fontweight="bold", color="#123b3d", pad=16)
    ax.set_xlabel(xlabel, color="#536466")
    ax.set_ylabel(ylabel, color="#536466")
    ax.tick_params(colors="#536466")
    ax.grid(axis="y", alpha=0.18)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#dfe8e7")
    ax.spines["bottom"].set_color("#dfe8e7")


def fig_bar(data, x_col, y_col, title, xlabel, ylabel, rotate=False):
    fig, ax = plt.subplots(figsize=(9, 5), facecolor="white")
    ax.bar(data[x_col].astype(str), data[y_col], color="#0f766e")
    beautify_ax(ax, title, xlabel, ylabel)
    if rotate:
        ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def plot_revenue_by_territory():
    data = (
        df.groupby("SalesTerritoryKey", as_index=False)["Sales Amount"]
        .sum()
        .sort_values("Sales Amount", ascending=False)
    )
    return fig_bar(data, "SalesTerritoryKey", "Sales Amount", "Revenue by Sales Territory", "Sales Territory Key", "Total Revenue")


def plot_top_products(top_n):
    data = (
        df.groupby("ProductKey", as_index=False)["Sales Amount"]
        .sum()
        .sort_values("Sales Amount", ascending=False)
        .head(int(top_n))
    )
    return fig_bar(data, "ProductKey", "Sales Amount", f"Top {int(top_n)} Products by Revenue", "Product Key", "Total Revenue", rotate=True)


def plot_cost_vs_sales():
    fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")
    ax.scatter(df["Total Product Cost"], df["Sales Amount"], alpha=0.35, color="#0f766e")
    beautify_ax(ax, "Cost vs Sales Amount", "Total Product Cost", "Sales Amount")
    fig.tight_layout()
    return fig


def plot_order_quantity_distribution():
    fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")
    ax.hist(df["Order Quantity"], bins=30, color="#0f766e", alpha=0.9)
    beautify_ax(ax, "Order Quantity Distribution", "Order Quantity", "Frequency")
    fig.tight_layout()
    return fig


def plot_customer_activity():
    customer_activity = df.groupby("CustomerKey", as_index=False).agg(Purchase_Count=("SalesOrderLineKey", "count"))
    fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")
    ax.hist(customer_activity["Purchase_Count"], bins=40, color="#0f766e", alpha=0.9)
    beautify_ax(ax, "Customer Purchase Activity", "Number of Purchases", "Number of Customers")
    fig.tight_layout()
    return fig


def plot_monthly_sales_trend():
    if "YearMonth" not in df.columns:
        return None
    monthly_sales = df.groupby("YearMonth", as_index=False)["Sales Amount"].sum().sort_values("YearMonth")
    fig, ax = plt.subplots(figsize=(12, 5), facecolor="white")
    ax.plot(monthly_sales["YearMonth"], monthly_sales["Sales Amount"], marker="o", color="#0f766e", linewidth=2.5)
    beautify_ax(ax, "Monthly Sales Trend", "Month", "Total Revenue")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


# ------------------------------------------------------------
# Prediction
# ------------------------------------------------------------
def prepare_model_data(max_rows=50000):
    model_df = df.dropna(subset=FEATURE_COLS + ["Sales Amount"]).copy()
    if len(model_df) > max_rows:
        model_df = model_df.sample(max_rows, random_state=42)
    X = model_df[FEATURE_COLS]
    return model_df, X


def run_classification():
    model_df, X = prepare_model_data()
    median_sales = model_df["Sales Amount"].median()
    y = (model_df["Sales Amount"] >= median_sales).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=80, max_depth=12, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, pred)
    cm = confusion_matrix(y_test, pred)
    report = classification_report(y_test, pred, target_names=["Low Value", "High Value"], output_dict=True)

    metrics = pd.DataFrame([
        {"Metric": "Median Sales Threshold", "Value": money(median_sales)},
        {"Metric": "Accuracy", "Value": f"{accuracy:.4f}"},
        {"Metric": "Low Value F1", "Value": f"{report['Low Value']['f1-score']:.4f}"},
        {"Metric": "High Value F1", "Value": f"{report['High Value']['f1-score']:.4f}"},
    ])

    importance = pd.DataFrame({"Feature": FEATURE_COLS, "Importance": model.feature_importances_}).sort_values("Importance", ascending=False)

    fig_cm, ax = plt.subplots(figsize=(6, 5), facecolor="white")
    im = ax.imshow(cm, cmap="Blues")
    ax.set_title("Confusion Matrix - High Value Purchase", fontsize=13, fontweight="bold", color="#123b3d")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("Actual Label")
    ax.set_xticks([0, 1], ["Low", "High"])
    ax.set_yticks([0, 1], ["Low", "High"])
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, cm[i, j], ha="center", va="center", color="#123b3d")
    fig_cm.colorbar(im, ax=ax)
    fig_cm.tight_layout()

    fig_imp, ax = plt.subplots(figsize=(9, 5), facecolor="white")
    ax.barh(importance["Feature"], importance["Importance"], color="#0f766e")
    beautify_ax(ax, "Feature Importance - Classification", "Importance", "Feature")
    ax.invert_yaxis()
    fig_imp.tight_layout()

    explanation = f"""
<div class="model-summary">
  <h3>High-Value Purchase Classification</h3>
  <p>The dataset contains completed sales transactions, so a real Buy / No Buy target is not available. The model predicts whether a purchase is <b>High Value</b> or <b>Low Value</b> based on the median sales amount.</p>
  <div class="metric-row">
    <div><span>Accuracy</span><strong>{accuracy:.3f}</strong></div>
    <div><span>Threshold</span><strong>{money(median_sales)}</strong></div>
    <div><span>Model</span><strong>Random Forest</strong></div>
  </div>
</div>
"""
    return explanation, metrics, importance, fig_cm, fig_imp


def run_regression():
    model_df, X = prepare_model_data()
    y = model_df["Sales Amount"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=80, max_depth=14, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)

    metrics = pd.DataFrame({
        "Metric": ["MAE", "RMSE", "R²"],
        "Value": [money(mae), money(rmse), f"{r2:.4f}"],
        "Meaning": ["Average prediction error", "Large-error-sensitive prediction error", "Explained variance of sales amount"],
    })

    importance = pd.DataFrame({"Feature": FEATURE_COLS, "Importance": model.feature_importances_}).sort_values("Importance", ascending=False)

    fig_pred, ax = plt.subplots(figsize=(7, 6), facecolor="white")
    ax.scatter(y_test, pred, alpha=0.35, color="#0f766e")
    min_value = min(y_test.min(), pred.min())
    max_value = max(y_test.max(), pred.max())
    ax.plot([min_value, max_value], [min_value, max_value], linestyle="--", color="#c49a6c")
    beautify_ax(ax, "Actual vs Predicted Sales Amount", "Actual Sales Amount", "Predicted Sales Amount")
    fig_pred.tight_layout()

    fig_imp, ax = plt.subplots(figsize=(9, 5), facecolor="white")
    ax.barh(importance["Feature"], importance["Importance"], color="#0f766e")
    beautify_ax(ax, "Feature Importance - Regression", "Importance", "Feature")
    ax.invert_yaxis()
    fig_imp.tight_layout()

    explanation = f"""
<div class="model-summary">
  <h3>Sales Amount Regression</h3>
  <p>The regression model predicts <b>Sales Amount</b> using customer, product, territory, quantity, price, discount, year, and month features.</p>
  <div class="metric-row">
    <div><span>R² Score</span><strong>{r2:.3f}</strong></div>
    <div><span>MAE</span><strong>{money(mae)}</strong></div>
    <div><span>Model</span><strong>Random Forest</strong></div>
  </div>
</div>
"""
    return explanation, metrics, importance, fig_pred, fig_imp


def predict_custom_input(customer_key, product_key, territory_key, order_quantity, unit_price, discount_pct, year, month):
    model_df, X = prepare_model_data()
    y = model_df["Sales Amount"]

    model = RandomForestRegressor(n_estimators=80, max_depth=14, random_state=42, n_jobs=-1)
    model.fit(X, y)

    input_df = pd.DataFrame([{
        "CustomerKey": int(customer_key),
        "ProductKey": int(product_key),
        "SalesTerritoryKey": int(territory_key),
        "Order Quantity": int(order_quantity),
        "Unit Price": float(unit_price),
        "Unit Price Discount Pct": float(discount_pct),
        "Year": int(year),
        "Month": int(month),
    }])

    input_df = input_df[FEATURE_COLS]
    predicted_sales = model.predict(input_df)[0]

    return f"Predicted Sales Amount: {money(predicted_sales)}"


# ------------------------------------------------------------
# Modern light design CSS
# ------------------------------------------------------------
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

:root {
  --bg: #fbfaf7;
  --panel: #ffffff;
  --ink: #123b3d;
  --muted: #5e6d6f;
  --teal: #0f766e;
  --teal-dark: #07575a;
  --teal-soft: #e5f3f0;
  --beige: #f4eee4;
  --line: #dfe8e7;
  --shadow: 0 18px 50px rgba(18, 59, 61, 0.08);
}

.gradio-container {
  max-width: 100% !important;
  width: 100% !important;
  margin: 0 !important;
  background: var(--bg) !important;
  color: var(--ink) !important;
  font-family: Inter, sans-serif !important;
}

body, .main, .wrap, .contain {
  background: var(--bg) !important;
}

#app-header {
  padding: 22px 32px 12px 32px;
  border-bottom: 1px solid var(--line);
  background: rgba(255,255,255,0.86);
  backdrop-filter: blur(14px);
}

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-mark {
  width: 42px;
  height: 42px;
  border: 2px solid var(--teal);
  border-radius: 12px;
  display: grid;
  place-items: center;
  color: var(--teal);
  font-weight: 800;
  background: #f7fffd;
}

.brand h1 {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  line-height: 1;
  margin: 0;
  letter-spacing: -0.03em;
  color: var(--ink);
}

.brand p {
  margin: 3px 0 0 0;
  font-size: 13px;
  color: var(--muted);
}

.nav-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 14px;
  color: var(--muted);
}

.nav-pills span {
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid transparent;
}

.nav-pills span:first-child {
  color: var(--teal-dark);
  background: var(--teal-soft);
  border-color: #cce5e0;
  font-weight: 700;
}

.hero-shell {
  position: relative;
  overflow: hidden;
  display: grid;
  grid-template-columns: 0.95fr 1.8fr;
  gap: 32px;
  padding: 58px 42px 50px 42px;
  background:
    radial-gradient(circle at 0% 90%, rgba(15,118,110,0.16), transparent 28%),
    linear-gradient(135deg, #ffffff 0%, #f4fbf9 55%, #fbf6ec 100%);
  border-bottom: 1px solid var(--line);
}

.hero-left h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(48px, 6vw, 76px);
  line-height: 0.95;
  margin: 12px 0 18px;
  letter-spacing: -0.05em;
  color: var(--ink);
}

.hero-left p {
  max-width: 380px;
  color: var(--muted);
  font-size: 17px;
  line-height: 1.65;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 12px;
  color: var(--teal);
  font-weight: 800;
}

.flow-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  align-items: start;
  gap: 10px;
}

.flow-arrow {
  display: none;
}

.flow-item {
  position: relative;
  text-align: center;
  padding: 10px 8px;
}

.flow-item::after {
  content: '';
  position: absolute;
  top: 44px;
  right: -18px;
  width: 36px;
  border-top: 1px dashed #9fcac5;
}

.flow-item:last-child::after { display: none; }

.flow-icon {
  width: 82px;
  height: 82px;
  margin: 0 auto 14px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--teal-soft);
  border: 1px solid #d9ebe8;
  color: var(--teal-dark);
  font-size: 34px;
  box-shadow: 0 10px 28px rgba(15,118,110,0.08);
}

.flow-item.warm .flow-icon {
  background: #f8efe2;
  border-color: #eadccb;
  color: #9a6b39;
}

.flow-item h3 {
  font-family: 'Playfair Display', serif;
  margin: 0 0 8px;
  font-size: 19px;
}

.flow-item p {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.55;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 14px;
  padding: 26px 32px 18px;
}

.kpi-card, .action-card, .model-summary, .mini-stats > div {
  background: rgba(255,255,255,0.92);
  border: 1px solid var(--line);
  border-radius: 20px;
  box-shadow: var(--shadow);
}

.kpi-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
}

.kpi-icon, .action-icon {
  flex: 0 0 auto;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--teal-soft);
  color: var(--teal-dark);
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 20px;
}

.kpi-label, .kpi-desc {
  margin: 0;
  color: var(--muted);
  font-size: 12px;
}

.kpi-card h2 {
  margin: 4px 0 3px;
  font-family: 'Playfair Display', serif;
  font-size: 27px;
  letter-spacing: -0.03em;
}

.section-head {
  padding: 22px 4px 8px;
}

.section-head h2 {
  font-family: 'Playfair Display', serif;
  font-size: 34px;
  margin: 6px 0 6px;
  color: var(--ink);
}

.section-head p {
  color: var(--muted);
  max-width: 820px;
  line-height: 1.65;
}

.mini-stats {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.mini-stats > div {
  padding: 18px;
}

.mini-stats span {
  display: block;
  color: var(--muted);
  font-size: 12px;
  margin-bottom: 8px;
}

.mini-stats strong {
  display: block;
  font-size: 20px;
  color: var(--ink);
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin-top: 14px;
}

.action-card {
  padding: 22px;
}

.action-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  margin: 16px 0 8px;
}

.action-card p {
  color: var(--muted);
  line-height: 1.6;
  margin: 0;
}

.model-summary {
  padding: 24px;
  margin: 8px 0 18px;
  background: linear-gradient(135deg, #ffffff, #f3fbf9);
}

.model-summary h3 {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  margin: 0 0 8px;
}

.model-summary p {
  color: var(--muted);
  line-height: 1.65;
}

.metric-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.metric-row div {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 14px;
}

.metric-row span {
  display: block;
  color: var(--muted);
  font-size: 12px;
}

.metric-row strong {
  display: block;
  margin-top: 5px;
  font-size: 22px;
  color: var(--teal-dark);
}

.gr-button, button {
  border-radius: 14px !important;
  border: 1px solid #bcded9 !important;
  background: linear-gradient(135deg, #0f766e, #07575a) !important;
  color: white !important;
  font-weight: 700 !important;
  box-shadow: 0 10px 24px rgba(15,118,110,0.18) !important;
}

.secondary-btn button, button.secondary-btn {
  background: #ffffff !important;
  color: var(--teal-dark) !important;
}

.block, .form, .panel, .gradio-accordion, .tabs, .tabitem, .dataframe, .plot-container {
  border-radius: 20px !important;
}

.tab-nav button {
  font-weight: 700 !important;
}

.table-wrap, .dataframe, .gr-dataframe {
  border-radius: 18px !important;
  overflow: hidden !important;
}

footer { display: none !important; }

/* Hide the custom top navigation because Gradio tabs are the real controls. */
#app-header { display: none !important; }

/* ============================================================
   FINAL FIX: wider page + stable visible full-width tabs
   ============================================================ */
html, body {
  width: 100% !important;
  min-width: 100% !important;
  overflow-x: hidden !important;
}

.gradio-container,
.gradio-container > .main,
.gradio-container > .wrap,
.gradio-container .contain {
  max-width: none !important;
  width: 100% !important;
  margin: 0 !important;
}

.hero-shell,
.kpi-grid,
#main_tabs {
  width: calc(100% - 56px) !important;
  max-width: none !important;
  margin-left: 28px !important;
  margin-right: 28px !important;
}

.hero-shell {
  border-radius: 0 0 26px 26px !important;
}

.kpi-grid {
  padding-left: 0 !important;
  padding-right: 0 !important;
}

#main_tabs {
  margin-top: 28px !important;
  margin-bottom: 0 !important;
  overflow: visible !important;
}

/* The real tab row in most Gradio versions */
#main_tabs [role="tablist"],
#main_tabs .tab-nav {
  width: 100% !important;
  max-width: none !important;
  min-height: 72px !important;
  height: auto !important;
  overflow: visible !important;

  display: grid !important;
  grid-template-columns: repeat(7, minmax(0, 1fr)) !important;
  gap: 12px !important;

  margin: 0 0 32px 0 !important;
  padding: 10px !important;

  background: rgba(255, 255, 255, 0.88) !important;
  border: 1px solid var(--line) !important;
  border-radius: 24px !important;
  box-shadow: 0 18px 45px rgba(18, 59, 61, 0.08) !important;
}

/* Every tab button */
#main_tabs [role="tablist"] button,
#main_tabs .tab-nav button,
#main_tabs button[role="tab"] {
  width: 100% !important;
  min-width: 0 !important;
  max-width: none !important;
  height: 48px !important;
  min-height: 48px !important;
  max-height: none !important;

  display: flex !important;
  justify-content: center !important;
  align-items: center !important;

  padding: 0 12px !important;
  margin: 0 !important;
  border-radius: 16px !important;

  background: #ffffff !important;
  border: 1px solid #cfe4e1 !important;
  color: var(--teal-dark) !important;

  font-size: 14px !important;
  font-weight: 800 !important;
  line-height: 1.1 !important;
  white-space: nowrap !important;

  opacity: 1 !important;
  visibility: visible !important;
  overflow: visible !important;
  box-shadow: none !important;
  transform: none !important;
}

#main_tabs [role="tablist"] button span,
#main_tabs .tab-nav button span,
#main_tabs button[role="tab"] span {
  display: inline-block !important;
  opacity: 1 !important;
  visibility: visible !important;
  color: inherit !important;
  line-height: 1.1 !important;
  transform: none !important;
}

/* Active tab */
#main_tabs [role="tablist"] button[aria-selected="true"],
#main_tabs button[role="tab"][aria-selected="true"],
#main_tabs .tab-nav button.selected {
  background: linear-gradient(135deg, #0f766e, #07575a) !important;
  color: #ffffff !important;
  border-color: #07575a !important;
  box-shadow: 0 10px 22px rgba(15, 118, 110, 0.22) !important;
}

/* Tab content width */
#main_tabs .tabitem,
#main_tabs > div:nth-child(2) {
  width: 100% !important;
  max-width: none !important;
  overflow: visible !important;
}

@media (max-width: 1100px) {
  #main_tabs [role="tablist"],
  #main_tabs .tab-nav {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  }
}

@media (max-width: 700px) {
  .hero-shell,
  .kpi-grid,
  #main_tabs {
    width: calc(100% - 24px) !important;
    margin-left: 12px !important;
    margin-right: 12px !important;
  }

  #main_tabs [role="tablist"],
  #main_tabs .tab-nav {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 8px !important;
  }

  #main_tabs [role="tablist"] button,
  #main_tabs .tab-nav button,
  #main_tabs button[role="tab"] {
    font-size: 12px !important;
  }
}

"""


# ------------------------------------------------------------
# Interface
# ------------------------------------------------------------
with gr.Blocks(
    title="CRM Insight Dashboard",
    css=custom_css,
    theme=gr.themes.Soft(
        primary_hue="teal",
        secondary_hue="stone",
        neutral_hue="slate",
        font=["Inter", "Arial", "sans-serif"],
    ),
) as demo:
    gr.HTML(
        """
<header id="app-header">
  <div class="header-row">
    <div class="brand">
      <div class="brand-mark">↗</div>
      <div>
        <h1>CRM Insight Dashboard</h1>
        <p>Customer Sales Analysis · Built with Gradio</p>
      </div>
    </div>
    <nav class="nav-pills">
      <span>Overview</span><span>EDA</span><span>Insights</span><span>Prediction</span><span>Marketing Action</span>
    </nav>
  </div>
</header>
"""
    )

    gr.HTML(hero_html())
    gr.HTML(kpi_cards_html())

    with gr.Tabs(elem_id="main_tabs"):
        with gr.Tab("Overview"):
            gr.HTML(intro_panel_html())
            with gr.Row():
                preview_btn = gr.Button("Show Data Preview")
                columns_btn = gr.Button("Show Column Information")
            preview_output = gr.Dataframe(label="Data Preview", interactive=False, wrap=True)
            columns_output = gr.Dataframe(label="Column Information", interactive=False, wrap=True)
            preview_btn.click(get_data_preview, outputs=preview_output)
            columns_btn.click(get_column_info, outputs=columns_output)

        with gr.Tab("KPI"):
            gr.HTML('<div class="section-head"><span class="eyebrow">Business Scale</span><h2>KPI Dashboard</h2><p>These indicators are calculated directly from the cleaned dataset and summarize revenue, orders, average sales, products, customers, and profit.</p></div>')
            kpi_btn = gr.Button("Calculate KPI")
            kpi_output = gr.Dataframe(label="KPI Table", interactive=False, wrap=True)
            kpi_btn.click(get_kpis, outputs=kpi_output)

        with gr.Tab("EDA"):
            gr.HTML('<div class="section-head"><span class="eyebrow">Visual Analysis</span><h2>Exploratory Data Analysis</h2><p>These charts show sales territory performance, product revenue, cost-sales relationship, customer activity, and monthly trend.</p></div>')
            top_n_slider = gr.Slider(5, 20, value=10, step=1, label="Top N Products")
            with gr.Row():
                territory_btn = gr.Button("Revenue by Territory")
                products_btn = gr.Button("Top Products")
                trend_btn = gr.Button("Monthly Trend")
            with gr.Row():
                cost_btn = gr.Button("Cost vs Sales")
                quantity_btn = gr.Button("Order Quantity Distribution")
                customer_btn = gr.Button("Customer Activity")
            plot_output = gr.Plot(label="EDA Chart")
            territory_btn.click(plot_revenue_by_territory, outputs=plot_output)
            products_btn.click(plot_top_products, inputs=top_n_slider, outputs=plot_output)
            trend_btn.click(plot_monthly_sales_trend, outputs=plot_output)
            cost_btn.click(plot_cost_vs_sales, outputs=plot_output)
            quantity_btn.click(plot_order_quantity_distribution, outputs=plot_output)
            customer_btn.click(plot_customer_activity, outputs=plot_output)

        with gr.Tab("Insights"):
            gr.HTML('<div class="section-head"><span class="eyebrow">CRM Insight</span><h2>Customer / Product Insight</h2><p>These tables identify high-value products, active customers, and strong sales territories for CRM decision-making.</p></div>')
            top_n = gr.Slider(5, 30, value=10, step=1, label="Top N")
            with gr.Row():
                top_products_btn = gr.Button("Show Top Products")
                top_customers_btn = gr.Button("Show Top Customers")
                territory_table_btn = gr.Button("Show Territory Summary")
            insight_output = gr.Dataframe(label="Insight Table", interactive=False, wrap=True)
            top_products_btn.click(top_products_table, inputs=top_n, outputs=insight_output)
            top_customers_btn.click(top_customers_table, inputs=top_n, outputs=insight_output)
            territory_table_btn.click(territory_table, outputs=insight_output)

        with gr.Tab("Prediction"):
            gr.HTML('<div class="section-head"><span class="eyebrow">Machine Learning</span><h2>Prediction Models</h2><p>Classification separates high-value and low-value purchases. Regression estimates expected sales amount from transaction features.</p></div>')
            with gr.Row():
                class_btn = gr.Button("Run Classification Model")
                reg_btn = gr.Button("Run Regression Model")

            with gr.Row():
                with gr.Column():
                    class_text = gr.HTML()
                    class_metrics = gr.Dataframe(label="Classification Metrics", interactive=False, wrap=True)
                    class_importance = gr.Dataframe(label="Classification Feature Importance", interactive=False, wrap=True)
                with gr.Column():
                    reg_text = gr.HTML()
                    reg_metrics = gr.Dataframe(label="Regression Metrics", interactive=False, wrap=True)
                    reg_importance = gr.Dataframe(label="Regression Feature Importance", interactive=False, wrap=True)

            with gr.Row():
                class_cm = gr.Plot(label="Confusion Matrix")
                class_imp_plot = gr.Plot(label="Classification Feature Importance Plot")
            with gr.Row():
                reg_pred_plot = gr.Plot(label="Actual vs Predicted")
                reg_imp_plot = gr.Plot(label="Regression Feature Importance Plot")

            class_btn.click(run_classification, outputs=[class_text, class_metrics, class_importance, class_cm, class_imp_plot])
            reg_btn.click(run_regression, outputs=[reg_text, reg_metrics, reg_importance, reg_pred_plot, reg_imp_plot])

        with gr.Tab("Custom Prediction"):
            gr.HTML('<div class="section-head"><span class="eyebrow">Scenario Testing</span><h2>Custom Sales Prediction</h2><p>Enter customer, product, territory, price, discount, and date conditions to estimate expected sales amount.</p></div>')
            with gr.Row():
                customer_key = gr.Number(value=int(df["CustomerKey"].median()), label="CustomerKey")
                product_key = gr.Number(value=int(df["ProductKey"].median()), label="ProductKey")
                territory_key = gr.Number(value=int(df["SalesTerritoryKey"].median()), label="SalesTerritoryKey")
                order_quantity = gr.Number(value=1, label="Order Quantity")
            with gr.Row():
                unit_price = gr.Number(value=float(df["Unit Price"].median()), label="Unit Price")
                discount_pct = gr.Number(value=0, label="Unit Price Discount Pct")
                year = gr.Number(value=int(df["Year"].max()), label="Year")
                month = gr.Number(value=12, label="Month")
            predict_btn = gr.Button("Predict Sales Amount")
            predict_output = gr.Textbox(label="Prediction Result")
            predict_btn.click(
                predict_custom_input,
                inputs=[customer_key, product_key, territory_key, order_quantity, unit_price, discount_pct, year, month],
                outputs=predict_output,
            )

        with gr.Tab("Marketing Action"):
            gr.HTML(conclusion_html())

    gr.HTML(
        """
<footer style="padding:28px 32px 44px; color:#5e6d6f; border-top:1px solid #dfe8e7; margin-top:24px;">
  <div style="display:flex; justify-content:space-between; gap:20px; flex-wrap:wrap;">
    <strong style="color:#123b3d;">CRM Insight Dashboard</strong>
    <span>Customer Data → EDA → CRM Insight → Prediction → Marketing Action</span>
  </div>
</footer>
"""
    )


if __name__ == "__main__":
    demo.launch()

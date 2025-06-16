import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page config ---
st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

# --- Load dataset ---
df = pd.read_csv("C:/Users/somas/Downloads/superstore.csv")  # Replace with correct path or file uploader

# --- Data Cleaning ---
# Rename columns for consistency
df.rename(columns={
    'Customer.ID': 'Customer ID',
    'Customer.Name': 'Customer Name',
    'Order.Date': 'Order Date',
    'Ship.Date': 'Ship Date',
    'Product.ID': 'Product ID',
    'Product.Name': 'Product Name',
    'Shipping.Cost': 'Shipping Cost',
    'Sub.Category': 'Sub-Category',
    'Row.ID': 'Row ID'
}, inplace=True)

# Convert dates
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Drop unnecessary columns if they exist
columns_to_drop = ['记录数', 'Row ID', 'Market2', 'weeknum']
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# --- Sidebar Filters ---
st.sidebar.header("Filter Data")
regions = df['Region'].unique()
selected_region = st.sidebar.multiselect("Select Region(s)", options=regions, default=regions)

categories = df['Category'].unique()
selected_category = st.sidebar.multiselect("Select Category(ies)", options=categories, default=categories)

filtered_df = df[
    (df['Region'].isin(selected_region)) &
    (df['Category'].isin(selected_category))
]

# --- KPI Metrics ---
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order.ID'].nunique() if 'Order.ID' in filtered_df.columns else 0
total_quantity = filtered_df['Quantity'].sum()
profit_margin = (total_profit / total_sales) if total_sales else 0

st.title("📊 Sales Performance Dashboard")
st.markdown("Use the filters on the left to explore sales performance across regions and categories.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("📦 Total Orders", total_orders)
col4.metric("📊 Profit Margin", f"{profit_margin:.2%}")

# --- Charts ---

# 1. Sales Trend Over Time
sales_trend = filtered_df.groupby('Order Date')['Sales'].sum().reset_index()
fig1 = px.line(sales_trend, x='Order Date', y='Sales', title="📅 Sales Over Time")
st.plotly_chart(fig1, use_container_width=True)

# 2. Sales by Region
fig2 = px.bar(filtered_df, x='Region', y='Sales', color='Region', title="🌍 Sales by Region")
st.plotly_chart(fig2, use_container_width=True)

# 3. Sales by Category
fig3 = px.pie(filtered_df, names='Category', values='Sales', title="🧩 Sales by Category")
st.plotly_chart(fig3, use_container_width=True)

# 4. Optional: Top 10 Products by Sales
top_products = (
    filtered_df.groupby('Product Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig4 = px.bar(top_products, x='Sales', y='Product Name', orientation='h',
              title="🏆 Top 10 Products by Sales", color='Sales')
st.plotly_chart(fig4, use_container_width=True)

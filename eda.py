import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

print("--- STEP 1: Data Loading and Cleaning ---")

# UPDATE THIS PATH! Use the absolute path to your extracted CSV file.
FILE_NAME = 'C:/Users/eswar/downloads/retail_sales_dataset.csv'
df = pd.read_csv(FILE_NAME)
print(f"Dataset '{FILE_NAME}' loaded successfully! (Initial Rows: {len(df)})")
print("\n--- Initial Data Information ---")
df.info()
df.columns = df.columns.str.replace(' ', '_')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
print("\n'Date' column converted to datetime format.")
initial_rows = len(df)
df.dropna(subset=['Date', 'Total_Amount'], inplace=True)
rows_dropped = initial_rows - len(df)
print(f"Dropped {rows_dropped} rows with missing critical values.")
print("\n--- Final Check for Missing Values (Post-Cleaning) ---")
print(df.isnull().sum())

print("\n\n--- STEP 2: Descriptive Statistics ---")

print("Descriptive Statistics for Sales, Quantity, and Price:")
numerical_cols = ['Quantity', 'Price_per_Unit', 'Total_Amount']
print(df[numerical_cols].describe().round(2))
print("\n--- Skewness and Kurtosis for Total_Amount ---")
print(f"Total_Amount Skewness: {df['Total_Amount'].skew():.2f}")
print(f"Total_Amount Kurtosis: {df['Total_Amount'].kurt():.2f}")


print("\n\n--- STEP 3: Time Series Analysis (Trends and Seasonality) ---")

df['Order_Year'] = df['Date'].dt.year
df['Order_Month'] = df['Date'].dt.month
print("\n--- Sales Trend by Month ---")
monthly_sales_agg = df.groupby('Order_Month')['Total_Amount'].sum().reset_index()
monthly_sales_agg = monthly_sales_agg.sort_values(by='Order_Month')
print(monthly_sales_agg)


print("\n\n--- STEP 4: Customer and Product Analysis (Segmentation) ---")

top_product_categories = df.groupby('Product_Category')['Total_Amount'].sum().sort_values(ascending=False).head(5)
print("\nTop 5 Product Categories by Revenue:")
print(top_product_categories)
top_products_quantity = df.groupby('Product_Category')['Quantity'].sum().sort_values(ascending=False).head(5)
print("\nTop 5 Product Categories by Quantity Sold:")
print(top_products_quantity)
if 'Customer_ID' in df.columns:
    apv = df.groupby('Customer_ID')['Total_Amount'].sum().mean()
    print(f"\nAverage Customer Spend (APV): ${apv:,.2f}")
else:
    apv = df['Total_Amount'].mean()
    print(f"\nMean Transaction Value: ${apv:,.2f}")
if 'Gender' in df.columns:
    sales_by_gender = df.groupby('Gender')['Total_Amount'].sum().sort_values(ascending=False)
    print("\nTotal Sales by Customer Gender:")
    print(sales_by_gender)
if 'Age' in df.columns:
    bins = [18, 25, 35, 45, 55, 65, 100]
    labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    sales_by_age = df.groupby('Age_Group', observed=True)['Total_Amount'].sum().sort_values(ascending=False)
    print("\nSales by Age Group:")
    print(sales_by_age)


print("\n\n--- STEP 5: Visualization ---")

plt.figure(figsize=(8, 5))
sns.histplot(df['Total_Amount'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of Transaction Amounts')
plt.xlabel('Total Amount ($)')
plt.ylabel('Frequency')
plt.xlim(0, df['Total_Amount'].quantile(0.99))
plt.show()
monthly_sales_plot = df.groupby(df['Date'].dt.to_period('M'))['Total_Amount'].sum().reset_index()
monthly_sales_plot['Date'] = monthly_sales_plot['Date'].astype(str)
plt.figure(figsize=(12, 6))
sns.lineplot(x='Date', y='Total_Amount', data=monthly_sales_plot, marker='o')
plt.title('Monthly Sales Trend Over Time')
plt.xlabel('Month-Year')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.figure(figsize=(10, 6))
sns.barplot(x=top_product_categories.index, y=top_product_categories.values, palette='viridis')
plt.title('Total Revenue by Top Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
if 'Age_Group' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.barplot(x=sales_by_age.index, y=sales_by_age.values, palette='magma')
    plt.title('Total Sales by Customer Age Group')
    plt.xlabel('Age Group')
    plt.ylabel('Total Sales ($)')
    plt.show()


print("\n\n--- STEP 6: Recommendations (Insights and Conclusion) ---")

peak_sales_month = monthly_sales_plot.sort_values(by='Total_Amount', ascending=False)['Date'].iloc[0]
top_category = top_product_categories.index[0]
top_age_group = sales_by_age.index[0] if 'Age_Group' in df.columns else "N/A"

print("\n**Key Findings from EDA:**")
print(f"1. **Average Purchase Value (APV):** The typical customer or transaction value is **${apv:,.2f}**.")
print(f"2. **Seasonality:** Sales show strong seasonality, peaking around **{peak_sales_month}**.")
print(f"3. **Product Performance:** The **'{top_category}'** category is the primary revenue driver.")
print(f"4. **Customer Demographics:** The **'{top_age_group}'** age segment contributes the highest total revenue.")

print("\n**Actionable Recommendations:**")
print("1. **Inventory and Staffing:** Prepare for the peak sales period by increasing stock for high-demand items and boosting sales staff to maximize revenue capture.")
print(f"2. **Targeted Marketing:** Direct most marketing and loyalty spend toward the high-value **'{top_age_group}'** segment.")
print(f"3. **Profitability Deep Dive:** Conduct a follow-up analysis to confirm if **'{top_category}'** leads in profit margin, not just revenue.")
print("4. **Upselling Strategy:** Optimize the store to encourage sales slightly above the APV of **${apv:,.2f}**.")

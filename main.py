import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_excel(r"C:\Users\jraja\OneDrive\Documents\Assignment\Online Retail.xlsx")
df

print("First 5 Rows:")
print(df.head())

print("\nLast 5 Rows:")
print(df.tail())

print("\nShape of Dataset:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nDataset Info:")
print(df.info())

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("\nUpdated Data Types:")
print(df.dtypes)
#Task 2 – Data Cleaning 
● Handle missing values (remove null CustomerID) 
● Remove duplicates 
● Fix invalid values (negative quantity, invalid price)
import pandas as pd

df = pd.read_excel(r"C:\Users\jraja\OneDrive\Documents\Assignment\Online Retail.xlsx")

print("Initial Shape:", df.shape)
print(df.info())

df = df.dropna(subset=['CustomerID'])

df = df.drop_duplicates()

df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

print("Final Shape:", df.shape)
print(df.isnull().sum())
print(df.head())

df = df.reset_index(drop=True)

print(df.describe())

#Task 3 – Feature Engineering 
● Create TotalPrice = Quantity × UnitPrice 
● Extract time features (Year, Month, Day, Hour) 
● Create categories (Customer Segment, Order Size, Day Type) 
import pandas as pd
df = pd.read_excel(r"C:\Users\jraja\OneDrive\Documents\Assignment\Online Retail.xlsx")

df = df.dropna(subset=['CustomerID'])
df = df.drop_duplicates()
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])


df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
df['Day'] = df['InvoiceDate'].dt.day
df['Hour'] = df['InvoiceDate'].dt.hour
df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()


customer_spend = df.groupby('CustomerID')['TotalPrice'].sum()

df['CustomerSegment'] = pd.qcut(
    df['CustomerID'].map(customer_spend),
    q=3,
    labels=['Low', 'Medium', 'High']
)


def order_size(q):
    if q <= 10:
        return 'Small'
    elif q <= 50:
        return 'Medium'
    else:
        return 'Large'

df['OrderSize'] = df['Quantity'].apply(order_size)

df['DayType'] = df['DayOfWeek'].apply(
    lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday'
)

print(df.head())
print(df.columns)
print(df[['TotalPrice', 'Year', 'Month', 'Hour',
          'CustomerSegment', 'OrderSize', 'DayType']].head())
#Task 4 – Data Exploration 
● Use describe() and dataset overview 
● Analyze categories (value_counts(), unique()) 
● Perform groupby() (country, month, product) 
import pandas as pd

df = pd.read_excel(r"C:\Users\jraja\OneDrive\Documents\Assignment\Online Retail.xlsx")
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Convert date
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Extract Month for grouping
df['Month'] = df['InvoiceDate'].dt.month


print("Dataset Shape:", df.shape)
print("\nColumn Info:")
print(df.info())

print("\nSummary Statistics:")
print(df.describe())

print("\nMissing Values:")
print(df.isnull().sum())

# Country distribution
print("\nTop Countries by Transactions:")
print(df['Country'].value_counts().head(10))

# Unique products
print("\nNumber of Unique Products:")
print(df['StockCode'].nunique())

# Most sold products
print("\nTop 10 StockCodes:")
print(df['StockCode'].value_counts().head(10))

# Unique customers
print("\nUnique Customers:")
print(df['CustomerID'].nunique())

# Invoice analysis
print("\nUnique Invoices:")
print(df['InvoiceNo'].nunique())

# Sales by Country
country_sales = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False)
print("\nSales by Country:")
print(country_sales.head(10))

# Sales by Month
monthly_sales = df.groupby('Month')['TotalPrice'].sum()
print("\nMonthly Sales:")
print(monthly_sales)

# Top Products by Revenue
product_sales = df.groupby('StockCode')['TotalPrice'].sum().sort_values(ascending=False)
print("\nTop Products by Revenue:")
print(product_sales.head(10))

# Average order value by country
avg_order_country = df.groupby('Country')['TotalPrice'].mean().sort_values(ascending=False)
print("\nAverage Order Value by Country:")
print(avg_order_country.head(10))
#Task 5 – Data Wrangling 
● Aggregate data using groupby() 
● Sort to find the top customers and countries 
● Restructure data if needed 
import pandas as pd

df = pd.read_excel(r"C:\Users\jraja\OneDrive\Documents\Assignment\Online Retail.xlsx")

# Basic cleaning (safe reuse from Task 2)
df = df.dropna(subset=['CustomerID'])
df = df.drop_duplicates()
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Create TotalPrice
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Convert date
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Extract Month for analysis
df['Month'] = df['InvoiceDate'].dt.month

# Total sales by customer
customer_sales = df.groupby('CustomerID')['TotalPrice'].sum()

# Total quantity purchased by customer
customer_quantity = df.groupby('CustomerID')['Quantity'].sum()

# Combine into a single dataframe
customer_summary = pd.DataFrame({
    'TotalSales': customer_sales,
    'TotalQuantity': customer_quantity
})

print("\nCustomer Summary (Top 5):")
print(customer_summary.head())

top_customers = customer_summary.sort_values(by='TotalSales', ascending=False)

print("\nTop 10 Customers by Revenue:")
print(top_customers.head(10))

country_sales = df.groupby('Country')['TotalPrice'].sum()
country_orders = df.groupby('Country')['InvoiceNo'].nunique()

country_summary = pd.DataFrame({
    'TotalSales': country_sales,
    'TotalOrders': country_orders
})

top_countries = country_summary.sort_values(by='TotalSales', ascending=False)

print("\nTop Countries by Revenue:")
print(top_countries.head(10))

product_sales = df.groupby('StockCode')['TotalPrice'].sum()

top_products = product_sales.sort_values(ascending=False)

print("\nTop 10 Products by Revenue:")
print(top_products.head(10))

# Monthly sales by country (pivot table)
pivot_country_month = pd.pivot_table(
    df,
    values='TotalPrice',
    index='Country',
    columns='Month',
    aggfunc='sum',
    fill_value=0
)

print("\nPivot Table: Country vs Month Sales")
print(pivot_country_month.head())

customer_monthly = pd.pivot_table(
    df,
    values='TotalPrice',
    index='CustomerID',
    columns='Month',
    aggfunc='sum',
    fill_value=0
)

print("\nCustomer Monthly Spending (Top 5):")
print(customer_monthly.head())
#Task 6 – Statistical Analysis 
● Analyze Quantity, UnitPrice, TotalPrice 
● Calculate mean, median, and mode 
● Find standard deviation, variance, and percentiles 
import pandas as pd
import numpy as np

df = pd.read_excel(r"C:\Users\jraja\OneDrive\Documents\Assignment\Online Retail.xlsx")

# Create TotalPrice
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

cols = ['Quantity', 'UnitPrice', 'TotalPrice']

print("\n CENTRAL TENDENCY")

for col in cols:
    print(f"\n--- {col} ---")
    print("Mean:", df[col].mean())
    print("Median:", df[col].median())
    print("Mode:", df[col].mode()[0])


print("\n SPREAD (VARIATION)")

for col in cols:
    print(f"\n--- {col} ---")
    print("Standard Deviation:", df[col].std())
    print("Variance:", df[col].var())


print("\n PERCENTILES")

percentiles = [0.25, 0.50, 0.75, 0.90, 0.95]

for col in cols:
    print(f"\n--- {col} ---")
    print(df[col].quantile(percentiles))

print("\n SUMMARY STATISTICS")
print(df[cols].describe())
Task 7 – Data Visualization (Min 8 Plots) 
Matplotlib: 
● Line chart 
● Bar chart 
● Histogram 
● Box plot 
Seaborn: 
● Count plot 
● Violin plot 
● Heatmap 
● Pair plot
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Cleaned Dataset
df = pd.read_excel(r"C:\Users\jraja\OneDrive\Documents\Assignment\Online Retail.xlsx")

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create additional useful columns
df['Month'] = df['InvoiceDate'].dt.to_period('M')
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# MATPLOTLIB PLOTS

# 1. Line Chart
monthly_sales = df.groupby('Month')['TotalPrice'].sum()

plt.figure(figsize=(10,5))
monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Bar Chart
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
top_products.plot(kind='bar', color='skyblue')
plt.title("Top 10 Selling Products")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.xticks(rotation=75)
plt.tight_layout()
plt.show()

# 3. Histogram
plt.figure(figsize=(8,5))
plt.hist(df['Quantity'], bins=50, color='purple')
plt.title("Quantity Distribution")
plt.xlabel("Quantity")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 4. Box Plot – Unit Price
plt.figure(figsize=(8,5))
plt.boxplot(df['UnitPrice'])
plt.title("Box Plot of Unit Price")
plt.ylabel("Price")
plt.tight_layout()
plt.show()

# SEABORN PLOTS

# 5. Count Plot
top_countries = df['Country'].value_counts().head(10).index
filtered_df = df[df['Country'].isin(top_countries)]
plt.figure(figsize=(10,5))
sns.countplot(data=filtered_df, x='Country', order=top_countries)
plt.title("Top 10 Countries by Transactions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 6. Violin Plot
plt.figure(figsize=(10,5))
sns.violinplot(data=filtered_df, x='Country', y='UnitPrice')
plt.title("Unit Price Distribution by Country")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 7. Heatmap – Correlation Matrix
corr = df[['Quantity', 'UnitPrice', 'TotalPrice']].corr()
plt.figure(figsize=(6,4))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# 8. Pair Plot
sns.pairplot(df[['Quantity', 'UnitPrice', 'TotalPrice']])
plt.suptitle("Pair Plot of Key Features", y=1.02)
plt.show()

Task 8 – Business Insights 
● Identify: 
○ Top country 
○ Best sales month 
○ Peak sales time 
● Analyze: 
○ Customer behavior 
○ High-value customers 
○ Top products 
import pandas as pd

df = pd.read_excel(r"C:\Users\jraja\OneDrive\Documents\Assignment\Online Retail.xlsx")

# Convert date column
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Feature Engineering
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df['Month'] = df['InvoiceDate'].dt.to_period('M')
df['Hour'] = df['InvoiceDate'].dt.hour

# 1. Top Country
top_country = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(1)

# 2. Best Sales Month
best_month = df.groupby('Month')['TotalPrice'].sum().sort_values(ascending=False).head(1)

# 3. Peak Sales Time (Hour)
peak_hour = df.groupby('Hour')['TotalPrice'].sum().sort_values(ascending=False).head(1)

print("===== KEY INSIGHTS =====")
print("\nTop Country by Sales:\n", top_country)
print("\nBest Sales Month:\n", best_month)
print("\nPeak Sales Hour:\n", peak_hour)

# 4. Customer Behavior
customer_orders = df.groupby('CustomerID')['InvoiceNo'].nunique()
customer_spending = df.groupby('CustomerID')['TotalPrice'].sum()

print("\n===== CUSTOMER BEHAVIOR =====")
print("\nAverage Orders per Customer:", round(customer_orders.mean(), 2))
print("Average Spending per Customer:", round(customer_spending.mean(), 2))

# 5. High-Value Customers (Top 10)
high_value_customers = customer_spending.sort_values(ascending=False).head(10)

print("\n===== HIGH-VALUE CUSTOMERS =====")
print(high_value_customers)

# 6. Top Products
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

print("\n===== TOP PRODUCTS =====")
print(top_products)
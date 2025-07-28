import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("sales_data.csv")

print("First 5 rows:")
print(df.head())

print("\nSummary:")
print(df.info())

df['date'] = pd.to_datetime(df['date'])

print("\nMissing values in each column:")
print(df.isnull().sum())

df = df.fillna(0)

df['day_of_week'] = df['date'].dt.dayofweek  
df['month'] = df['date'].dt.month  
df['day_of_year'] = df['date'].dt.dayofyear  

total_sales = df.groupby('product')['quantity'].sum()
print("\nTotal sales per product:")
print(total_sales)

sns.barplot(x=total_sales.index, y=total_sales.values)
plt.title("Total Sales by Product")
plt.ylabel("Units Sold")
plt.xlabel("Product")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

df_amg = df[df['product'] == 'Mercedes AMG']
df_amg_daily = df_amg.groupby('date')['quantity'].sum().reset_index()

plt.figure(figsize=(10, 4))
sns.lineplot(x='date', y='quantity', data=df_amg_daily)
plt.title("Daily Sales Trend - Mercedes AMG")
plt.xlabel("Date")
plt.ylabel("Units Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

sales_by_day = df.groupby('day_of_week')['quantity'].sum()

sns.barplot(x=sales_by_day.index, y=sales_by_day.values)
plt.title("Total Sales by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Units Sold")
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
plt.tight_layout()
plt.show()

df_daily = df.groupby(['date', 'product']).agg({'quantity': 'sum'}).reset_index()
df_daily.to_csv('sales_daily_processed.csv', index=False)

print("\nPreprocessing complete. Processed data saved to 'sales_daily_processed.csv'.")

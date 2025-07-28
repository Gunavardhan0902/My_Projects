import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os
df = pd.read_csv("sales_daily_processed.csv")  

df['date'] = pd.to_datetime(df['date'])

df['day_of_week'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['day_of_year'] = df['date'].dt.dayofyear

product_df = df[df['product'] == 'BMW']

X = product_df[['day_of_week', 'month', 'day_of_year']]
y = product_df['quantity']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

plt.figure(figsize=(10, 6))
plt.plot(y_test.values, label='Actual', marker='o')
plt.plot(y_pred, label='Predicted', marker='x')
plt.title('Overall Sales Prediction')
plt.xlabel('Sample Index')
plt.ylabel('Quantity Sold')
plt.legend()
plt.grid(True)

if not os.path.exists("static"):
    os.makedirs("static")

plt.savefig("predicted_graph.png")
print("Graph saved as predicted_graph.png")



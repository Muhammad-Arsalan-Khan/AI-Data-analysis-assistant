import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt

# File name set karna
file_path = sys.argv[1] if len(sys.argv) > 1 else "dataset.csv"

# Data load karna
df = pd.read_csv(file_path)

# Info print karna
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumn Names:")
print(df.columns)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nData Types:")
print(df.dtypes)

print("\nFirst 5 Rows:")
print(df.head())

print(f"\n Total Records (Rows): {len(df)}")

numerical_cols = df.select_dtypes(include=[np.number]).columns
categorical_cols = df.select_dtypes(include=['object', 'category']).columns

if len(numerical_cols) > 0:
    print("\n Numerical Columns Statistics:")
    for col in numerical_cols:
        print(f"\nColumn: {col} ")
        print(f"  Average (Mean)     : {df[col].mean():.2f}")
        print(f"  Maximum Value      : {df[col].max()}")
        print(f"  Minimum Value      : {df[col].min()}")
        print(f"  Count (Non-missing): {df[col].count()}")
else:
    print("\n No numerical columns found for averages/min/max.")

if len(categorical_cols) > 0:
    print("\n Categorical Columns Distribution & Frequency:")
    for col in categorical_cols:
        print(f"\n Column: {col}")
        
        distribution = df[col].value_counts()
        percentage = df[col].value_counts(normalize=True) * 100
        
        for category, count in distribution.items():
            pct = percentage[category]
            print(f"  {category}: {count} times ({pct:.1f}%)")
else:
    print("\n No categorical columns found for distribution.")


df.columns = df.columns.str.strip().str.lower()
product_sales = df.groupby('product')['sales'].sum()
top_product = product_sales.idxmax()
highest_sales_value = product_sales.max()
print(f"Product: {top_product}")
print(f"Total Sales: {round(highest_sales_value)}")


print(f"\nThe average age of customers: {df['customerage'].mean():.2f}")


city_orders = df['city'].value_counts()
top_city = city_orders.idxmax()          
maximum_orders_count = city_orders.max()  
print(f"City: {top_city}")
print(f"Total Orders: {maximum_orders_count}")

print("\nMost Frequent Category and its Frequency Count:")
category_counts = df['category'].value_counts()
top_category = category_counts.idxmax()
highest_frequency = category_counts.max()
print(f"Most Frequent Category: {top_category}")
print(f"Frequency Count: {highest_frequency} times")




category_counts = df["category"].value_counts()

category_counts.plot(
    kind="bar", color="#3498db", edgecolor="#2c3e50", width=0.6
)

plt.title("Total Orders Distribution by Category", fontsize=14, pad=15)
plt.xlabel("Product Category", fontsize=12)
plt.ylabel("Number of Orders", fontsize=12)

plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
# chart_filename = "category_distribution_chart.png"
# plt.savefig(chart_filename)
# plt.close()
# print(f"Chart successfully generated and saved as '{chart_filename}'\n")

top_category = category_counts.idxmax()
top_count = category_counts.max()
total_count = category_counts.sum()
percentage = (top_count / total_count) * 100

print("EXPLANATION OF THE RESULT")
explanation = (
    f"The '{top_category}' category contributes the highest number of orders, "
    f"with a count of {top_count} items, accounting for approximately {percentage:.1f}% "
    f"of the total transactions in this dataset."
)
print(explanation)




















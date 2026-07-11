import matplotlib.pyplot as plt
import pandas as pd

def generate_category_chart(df):
    # Category distribution
    category_counts = df["category"].value_counts()
    
    # Plotting
    category_counts.plot(kind="bar", color="#3498db", edgecolor="#2c3e50", width=0.6)
    plt.title("Total Orders Distribution by Category", fontsize=14, pad=15)
    plt.xlabel("Product Category", fontsize=12)
    plt.ylabel("Number of Orders", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    
    chart_filename = "category_distribution_chart.png"
    plt.savefig(chart_filename)
    plt.close()
    # plt.show()
   
    top_category = category_counts.idxmax()
    top_count = category_counts.max()
    percentage = (top_count / category_counts.sum()) * 100
    
    explanation = f"The '{top_category}' category contributes the highest number of orders ({top_count} items), accounting for {percentage:.1f}% of total transactions."
    
    return chart_filename, explanation
    # return explanation
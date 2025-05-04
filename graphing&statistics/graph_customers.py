import json
import matplotlib.pyplot as plt
import numpy as np
import statistics

def graph_and_stats():
    with open('data/customer_products.json', 'r', encoding='utf-8') as f:
        customer_data = json.load(f)

    product_counts = []
    total_reviews = 0
    total_customers = len(customer_data)

    for products in customer_data.values():
        count = len(products)
        if count > 0:  # Only consider customers who have reviewed at least 1 product
            product_counts.append(count)
            total_reviews += count

    average_reviews_per_customer = total_reviews / total_customers if total_customers else 0
    median_reviews_per_customer = statistics.median(product_counts) if product_counts else 0

    print("Summary:")
    print(f"Total reviews: {total_reviews}")
    print(f"Total customers: {total_customers}")
    print(f"Average products reviewed per customer: {average_reviews_per_customer:.2f}")
    print(f"Median products reviewed per customer: {median_reviews_per_customer}")

    # Define your new bin ranges based on the specified values
    bin_ranges = [1, 2, 5, 10, 20, 100, 200, float('inf')]

    # Digitize the data into bins based on the custom bin ranges
    digitized = np.digitize(product_counts, bin_ranges)
    counts = np.bincount(digitized)

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(np.arange(counts.size - 1), counts[1:], width=0.8)  # Skip the 0 bin (since there are no 0 values)

    # Set custom x-tick labels to represent the new bin ranges
    ax.set_xticks(np.arange(counts.size - 1))  # Skip the first bin
    ax.set_xticklabels(['1', '2-5', '5-10', '10-20', '20-100', '100-200', '200+'])


    plt.title("Histogram of Product Reviews per Customer")
    plt.xlabel("Number of Products Reviewed")
    plt.ylabel("Number of Customers")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    graph_and_stats()

import json
import matplotlib.pyplot as plt
import numpy as np
import statistics
from matplotlib.patches import Patch

def graph_and_stats(cusomter_data):

    product_counts = []
    total_reviews = 0
    total_customers = len(customer_data)

    for products in customer_data.values():
        count = len(products)
        if count > 0:
            product_counts.append(count)
            total_reviews += count

    average_reviews_per_customer = total_reviews / total_customers if total_customers else 0
    median_reviews_per_customer = statistics.median(product_counts) if product_counts else 0

    print("Summary:")
    print(f"Total reviews: {total_reviews}")
    print(f"Total customers: {total_customers}")
    print(f"Average products reviewed per customer: {average_reviews_per_customer:.2f}")
    print(f"Median products reviewed per customer: {median_reviews_per_customer}")

    bin_ranges = [1, 2, 5, 10, 20, 100, 200, float('inf')]
    bin_labels = ['1', '2-5', '5-10', '10-20', '20-100', '100-200', '200+']

    digitized = np.digitize(product_counts, bin_ranges)
    counts = np.bincount(digitized)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(np.arange(counts.size - 1), counts[1:], width=0.8) 
    ax.set_xticks(np.arange(counts.size - 1))
    ax.set_xticklabels(bin_labels)
    plt.title("Product Reviews per Customer")
    plt.xlabel("Number of Products Reviewed")
    plt.ylabel("Number of Customers")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    review_totals = [0] * len(bin_ranges)
    for count in product_counts:
        bin_index = np.digitize(count, bin_ranges)
        review_totals[bin_index] += count

    total_customers_with_reviews = sum(counts[1:])
    percentages = [(count / total_customers_with_reviews) * 100 for count in counts[1:]]

    legend_labels = [f"{label}: {pct:.4f}%" for label, pct in zip(bin_labels, percentages)]
    legend_patches = [Patch(color='white', label=label) for label in legend_labels]

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(np.arange(len(review_totals) - 1), review_totals[1:], width=0.8)
    ax2.set_xticks(np.arange(len(review_totals) - 1))
    ax2.set_xticklabels(bin_labels)
    ax2.legend(handles=legend_patches, title="% of customers", loc='upper left', frameon=False)

    plt.title("Total Reviews by Customer Group")
    plt.xlabel("Number of Products Reviewed (Customer Group)")
    plt.ylabel("Total Reviews")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def top_10_reviewers(customer_data):

    customer_review_counts = {customer: len(products) for customer, products in customer_data.items()}

    top_reviewers = sorted(customer_review_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    print("Top 10 Reviewers:")
    for i, (customer, count) in enumerate(top_reviewers, start=1):
        print(f"{i}. Customer ID: {customer}, Reviews: {count}")

if __name__ == '__main__':
    with open('data/customer_products.json', 'r', encoding='utf-8') as f:
        customer_data = json.load(f)
    graph_and_stats(customer_data)
    top_10_reviewers(customer_data)

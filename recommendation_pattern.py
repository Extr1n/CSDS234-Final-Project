import json
from collections import defaultdict, Counter

def load_products(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_customer_reviews(products):
    customer_reviews = defaultdict(set)  # customer_id -> set of ASINs
    product_data = {}  # asin -> product dict
    for product in products:
        asin = product.get("ASIN")
        product_data[asin] = product
        for review in product.get("reviews", []):
            customer = review.get("cutomer:")
            if customer:
                customer_reviews[customer].add(asin)
    return customer_reviews, product_data

def recommend_products(products, target_product, target_customer=None, rating_threshold=3.0, top_n=3):
    customer_reviews, product_data = build_customer_reviews(products)

    relevant_customers = set()
    for review in product_data.get(target_product, {}).get("reviews", []):
        customer = review.get("cutomer:")
        rating = float(review.get("rating:", 0))
        if customer and rating >= rating_threshold:
            relevant_customers.add(customer)

    product_counter = Counter()
    for customer in relevant_customers:
        for asin in customer_reviews[customer]:
            product_counter[asin] += 1

    if target_customer:
        already_reviewed = customer_reviews.get(target_customer, set())
        for asin in already_reviewed:
            product_counter.pop(asin, None)


    def sort_key(asin):
        salesrank = product_data.get(asin, {}).get("salesrank", -1)
        return (-product_counter[asin], salesrank if isinstance(salesrank, int) and salesrank > 0 else float('inf'))

    sorted_asins = sorted(product_counter, key=sort_key)

    recommendations = []
    for asin in sorted_asins[:top_n]:
        product = product_data.get(asin, {})
        title = product.get("title", "Unknown Title")
        salesrank = product.get("salesrank", -1)
        count = product_counter[asin]
        recommendations.append(f"{title} — recommended positively by {count} customers, salesrank: {salesrank}")
    
    return recommendations

if __name__ == "__main__":
    products = load_products("data/output.json")

    print("Enter the product ID (ASIN)")
    product_id = input("Product ID: ").strip()

    print("Enter the customer ID (press Enter to skip):")
    customer_id = input("Customer ID: ").strip()
    customer_id = customer_id if customer_id else None

    recommendations = recommend_products(products, product_id, customer_id)

    print("\nTop recommendations:")
    for rec in recommendations:
        print(rec)

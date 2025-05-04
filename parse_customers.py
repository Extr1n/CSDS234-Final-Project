import json


def parse_customers(data):
    customers = set()
    products_by_customer = {}

    for item in data:
        if 'reviews' in item and 'ASIN' in item:
            asin = item['ASIN']
            for review in item['reviews']:
                customer_id = review.get('cutomer:')
                if customer_id:
                    customers.add(customer_id)
                    if customer_id not in products_by_customer:
                        products_by_customer[customer_id] = []
                    products_by_customer[customer_id].append({
                        "product_id": asin,
                        "rating": int(review.get('rating:', 0))
                    })

    products_by_customer_json = {
        customer: products
        for customer, products in products_by_customer.items()
    }
    return products_by_customer_json
if __name__ == '__main__':
        with open('data/output.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        products_by_customer_json = parse_customers(data)
        with open('data/customer_products.json', 'w') as f:
            json.dump(products_by_customer_json, f, indent=2)

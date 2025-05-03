from product_distances import product_distances
import json
import multiprocessing
import random

class ProductDistances:
    def __init__(self):
        self.count = 0
    
    def process_asin(self, asin, n, products, asins):
        self.count += 1
        num = random.randint(1, 50)
        if num <= 4:
            print("...")
        total_products, total_distance, furthest = product_distances(products, asin, n, asins)
        if num >= 48:
            print("About %d/%d" % (self.count*num, len(asins)))
        return asin, {'total_products': total_products, 'total_distance': total_distance, 'furthest_distance': furthest}

if __name__ == '__main__':
    print("Loading products...")
    with open('output.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    print("Cleaning products...")
    for i in range(len(list(products))-1, -1, -1):
        if 'ASIN' not in products[i]:
            del products[i]

    similar_products_dict = {}

    for p in products:
        try:
            similar_products_dict[p['ASIN']] = p['similar']
        except KeyError:
            similar_products_dict[p['ASIN']] = []

    products = similar_products_dict

    asins = set(similar_products_dict.keys())

    n = len(asins)

    print("Initializing processes...")

    results = {}

    pd = ProductDistances()

    with multiprocessing.Manager() as manager:
        temp = manager.dict()
        with multiprocessing.Pool() as pool:
            temp = pool.starmap(pd.process_asin, [(asin, n, products, asins) for asin in asins])

            results = dict(temp)

    print("Writing %d results..." % len(results))

    with open('clean_output_with_distances.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

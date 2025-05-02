from product_distances import product_distances
import json
import multiprocessing

def process_asin(asin, n, products, results, asins):
    print("Processing %s" % asin)
    total_products, total_distance, furthest = product_distances(products, asin, n, asins)
    results[asin] = {'total_products': total_products, 'total_distance': total_distance, 'furthest_distance': furthest}
    print("Finished %s (%d/%d)" % asin, len(results), n)

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

    with multiprocessing.Manager() as manager:
        results = manager.dict()
        with multiprocessing.Pool() as pool:
            pool.starmap(process_asin, [(asin, n, products, results, asins) for asin in asins])

    results = dict(results)

    with open('clean_output_with_distances.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
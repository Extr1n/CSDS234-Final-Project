import json

def product_distances(products, product_id, max_distance=30):
    print("Cleaning products...")
    for i in range(len(list(products))-1, -1, -1):
        if 'ASIN' not in products[i]:
            del products[i]
    distances = {product_id: 0}
    queue = [(product_id, 0)]
    while queue:
        asin, distance = queue.pop(0)
        print("Processing %s (distance: %d)" % (asin, distance))
        if distance > max_distance:
            break
        try:
            for adjacent_asin in next(p['similar'] for p in products if p['ASIN'] == asin):
                if adjacent_asin not in distances:
                    distances[adjacent_asin] = distance + 1
                    queue.append((adjacent_asin, distance + 1))
        except StopIteration:
            print("No ASIN in DB for %s" % asin)
            continue
    return distances


print("Loading products...")

with open('output.json', 'r', encoding='utf-8') as f:
    products = json.load(f)


print("Product distances:")
print(product_distances(products, products[2]['ASIN']))

import json

def product_distances(products, product_id, max_distance):
    distances = {product_id: 0}
    queue = [(product_id, 0)]
    total_distance = 0
    total_products = 0
    while queue:
        asin, distance = queue.pop(0)
        total_distance += distance
        total_products += 1
        print("Processing %s (distance: %d)" % (asin, distance))
        if distance > max_distance:
            break
        try:
            for adjacent_asin in next(p['similar'] for p in products if p['ASIN'] == asin):
                if adjacent_asin not in distances:
                    distances[adjacent_asin] = distance + 1
                    queue.append((adjacent_asin, distance + 1))
        except (KeyError, StopIteration) as e:
            if isinstance(e, KeyError):
                print("No similar ASIN in DB for %s" % asin)
                distances[adjacent_asin] = distance + 1
                
            elif isinstance(e, StopIteration):
                print("No ASIN in DB for %s" % asin)
                distances[adjacent_asin] = distance + 1
            continue
    keys = list(distances.keys())
    return total_products, total_distance, distances[keys[-1]]
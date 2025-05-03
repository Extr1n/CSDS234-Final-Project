import json

def product_distances(products, product_id, max_distance, asins=[]):
    distances = {product_id: 0}
    queue = [(product_id, 0)]
    total_distance = 0
    total_products = 0
    while queue:
        asin, distance = queue.pop(0)
        total_distance += distance
        total_products += 1
        if distance > max_distance:
            break
        if asin not in asins:
            continue
        else:
            for adjacent_asin in (products[asin]):
                if adjacent_asin not in distances:
                    distances[adjacent_asin] = distance + 1
                    queue.append((adjacent_asin, distance + 1))
    keys = list(distances.keys())
    return total_products, total_distance, distances[keys[-1]]

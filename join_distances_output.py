import json

print("Loading data...")

with open('clean_output_with_distances.json', 'r', encoding='utf-8') as f:
    distances_data = json.load(f)

with open('output.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)

print("Joining data...")

joined_data = {}
for product in products_data:
    asin = product.get('ASIN')
    if asin:
        joined_data[asin] = product
        del joined_data[asin]["ASIN"]
        if asin in distances_data:
            joined_data[asin]['distances'] = distances_data[asin]

print("Writing joined data (%d records)..." % len(joined_data))

with open('joined.json', 'w', encoding='utf-8') as f:
    json.dump(joined_data, f, indent=2, ensure_ascii=False)


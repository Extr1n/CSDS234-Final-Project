import json

# Load data from clean_output_with_distances.json
with open('clean_output_with_distances.json', 'r', encoding='utf-8') as f:
    distances_data = json.load(f)

# Load data from output.json
with open('output.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)

# Create a dictionary indexed on ASIN
joined_data = {}
for product in products_data:
    asin = product.get('ASIN')
    if asin:
        joined_data[asin] = product
        del joined_data[asin]["ASIN"]
        # Merge distance data if available
        if asin in distances_data:
            joined_data[asin]['distances'] = distances_data[asin]

# Write the joined data to a new file
with open('joined.json', 'w', encoding='utf-8') as f:
    json.dump(joined_data, f, indent=2, ensure_ascii=False)


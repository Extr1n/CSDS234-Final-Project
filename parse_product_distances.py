from product_distances import product_distances
import json

def main():
    n = 548552        

    print("Loading products...")
    with open('output.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    print("Cleaning products...")
    for i in range(len(list(products))-1, -1, -1):
        if 'ASIN' not in products[i]:
            del products[i]

    for p in products:
    
        total_products, total_distance, furthest = product_distances(products, p['ASIN'], n)

        print("Updating ASIN: %s" % p['ASIN'])

        p['total_products'] = total_products
        p['total_distance'] = total_distance
        p['furthest_distance'] = furthest

        print("Total products: %d" % p['total_products'])
        print("Total distance: %d" % p['total_distance'])
        print("Furthest distance: %d" % p['furthest_distance'])

        print("Done with ASIN: %s" % p['ASIN'])

    with open('clean_output_with_distances.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
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

    distances, total_distance = product_distances(products, products[1]['ASIN'], n)

    print("Done. Total distance: %d" % total_distance)

    print("Avg distance: %d" % (total_distance / len(distances)))

    print("Total products: %d" % len(distances))

if __name__ == '__main__':
    main()
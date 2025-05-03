import json
from graph_data import get_distances

def get_statistics(data):
    avg_distances, furthest_distances, total_products_list, total_distances = get_distances(data)

    avg_furthest_distances = sum(furthest_distances) / len(furthest_distances)
    avg_total_products = sum(total_products_list) / len(total_products_list)
    avg_total_distances = sum(total_distances) / len(total_distances)

    return avg_furthest_distances, avg_total_products, avg_total_distances

if __name__ == '__main__':
    with open('data/joined.json', 'r', encoding = 'utf-8') as f:
        data = json.load(f)
    avg_furthest_distances, avg_total_products, avg_total_distances = get_statistics(data)
    print("Average Farthest Distance From Product: "+ str(avg_furthest_distances))
    print("Average Total Products Connected: " + str(avg_total_products))
    print("Average Total Distance From Product: " + str(avg_total_distances))


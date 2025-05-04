import json
from graph_data import get_distances


categories = ['Book', 'Music', 'DVD', 'Video', 'Toy', 'Video Games',
              'Software', 'Baby Product', 'CE', 'Sports']

def get_statistics(data):
    avg_distances, furthest_distances, total_products_list, total_distances = get_distances(data)

    avg_furthest_distances = sum(furthest_distances) / len(furthest_distances)
    avg_total_products = sum(total_products_list) / len(total_products_list)
    avg_total_distances = sum(total_distances) / len(total_distances)

    return avg_furthest_distances, avg_total_products, avg_total_distances

def get_categorical_statistics(data):
    category_values = {
    category: [0, 0, 0, 0] for category in categories
    }
    for item in data.values():
        cat = item.get('group')
        if cat not in categories:
            continue
        dist = item.get('distances',{})
        category_values[cat][0]+=dist.get('total_products',0)
        category_values[cat][1]+=dist.get('total_distance',0)
        category_values[cat][2]+=dist.get('furthest_distance',0)
        category_values[cat][3]+=1
    for cat in category_values:
        category_values[cat][0]/=category_values[cat][3]
        category_values[cat][1]/=category_values[cat][3]
        category_values[cat][2]/=category_values[cat][3]
    return category_values
        


if __name__ == '__main__':
    with open('data/joined.json', 'r', encoding = 'utf-8') as f:
        data = json.load(f)
    avg_furthest_distances, avg_total_products, avg_total_distances = get_statistics(data)
    category_values = get_categorical_statistics(data)
    print("Average Farthest Distance From Product: "+ str(avg_furthest_distances))
    print("Average Total Products Connected: " + str(avg_total_products))
    print("Average Total Distance From Product: " + str(avg_total_distances))
    for cat in category_values:
        print(f"\nTotal Items In {cat}:" + str(category_values[cat][3]))
        print(f"Average Farthest Distance From {cat}: "+ str(category_values[cat][2]))
        print(f"Average Total Products Connected To {cat}: " + str(category_values[cat][0]))
        print(f"Average Total Distance From {cat}: " + str(category_values[cat][1]))
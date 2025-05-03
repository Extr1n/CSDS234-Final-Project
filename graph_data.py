import json
import matplotlib.pyplot as plt


def get_distances(data):
    avg_distances = []
    furthest_distances = []
    total_products_list = []
    total_distances = []

    for product_id, info in data.items():
        dist = info.get('distances', {})
        total_products = dist.get('total_products', 0)
        total_distance = dist.get('total_distance', 0)
        furthest_distance = dist.get('furthest_distance', 0)

        avg_distance = total_distance / total_products if total_products > 0 else 0

        avg_distances.append(avg_distance)
        furthest_distances.append(furthest_distance)
        total_products_list.append(total_products)
        total_distances.append(total_distance)
    return avg_distances, furthest_distances, total_products_list, total_distances

# Function to plot histograms
def plot_histogram(data, title, xlabel):
    plt.figure()
    plt.hist(data, bins=10, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    with open('joined.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    avg_distances, furthest_distances, total_products, total_distances = get_distances(data)
    plot_histogram(avg_distances, 'Average Distance Histogram', 'Average Distance')
    plot_histogram(furthest_distances, 'Furthest Distance Histogram', 'Furthest Distance')
    plot_histogram(total_products, 'Total Products Histogram', 'Total Products')
    plot_histogram(total_distances, 'Total Distance Histogram', 'Total Distance')

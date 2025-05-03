import json
import matplotlib.pyplot as plt
from collections import defaultdict

categories = ['Book', 'Music', 'DVD', 'Video', 'Toy', 'Video Games',
              'Software', 'Baby Product', 'CE', 'Sports']
colors = ['blue', 'green', 'orange', 'red', 'purple', 'brown', 'cyan', 'pink', 'gray', 'olive']

def get_metrics_by_category(data):
    metrics = defaultdict(lambda: defaultdict(list))

    for item in data.values():
        cat = item.get('group')
        if cat not in categories:
            continue

        dist = item.get('distances', {})
        total_products = dist.get('total_products', 0)
        total_distance = dist.get('total_distance', 0)
        furthest_distance = dist.get('furthest_distance', 0)
        avg_distance = total_distance / total_products if total_products > 0 else 0

        metrics[cat]['avg_distance'].append(avg_distance)
        metrics[cat]['furthest_distance'].append(furthest_distance)
        metrics[cat]['total_distance'].append(total_distance)
        metrics[cat]['total_products'].append(total_products)
    
    return metrics

# Plot stacked histogram
def plot_stacked_histogram(metrics_by_cat, metric_name, title, xlabel):
    data = [metrics_by_cat[cat][metric_name] for cat in categories if metrics_by_cat[cat][metric_name]]
    labels = [cat for cat in categories if metrics_by_cat[cat][metric_name]]
    color_subset = [colors[categories.index(cat)] for cat in labels]

    plt.figure()
    plt.hist(data, bins=15, stacked=True, label=labels, color=color_subset, density=True, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Normalized Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    with open('data/joined.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    metrics_by_cat = get_metrics_by_category(data)
    plot_stacked_histogram(metrics_by_cat, 'avg_distance', 'Stacked Histogram: Average Distance', 'Average Distance')
    plot_stacked_histogram(metrics_by_cat, 'furthest_distance', 'Stacked Histogram: Furthest Distance', 'Furthest Distance')
    plot_stacked_histogram(metrics_by_cat, 'total_distance', 'Stacked Histogram: Total Distance', 'Total Distance')
    plot_stacked_histogram(metrics_by_cat, 'total_products', 'Stacked Histogram: Total Products', 'Total Products')

import json
import matplotlib.pyplot as plt


print("Loading data...")

with open('data/joined.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

categories = ['Book', 'Music', 'DVD', 'Video', 'Toy', 'Video Games', 'Software', 'Baby Product', 'CE', 'Sports']
colors = ['blue', 'green', 'orange', 'red', 'purple', 'brown', 'cyan', 'pink', 'gray', 'olive']

x = []
y = []
color = []

print("X and Y...")

for item in data.values():
    group = item.get('group')
    distances = item.get('distances', {})
    avg_distance = distances.get('total_distance', 0)  / distances.get('total_products', 1)
    furthest_distance = distances.get('furthest_distance', 0)
    if avg_distance > 0 and furthest_distance > 0:
        x.append(avg_distance)
        y.append(furthest_distance)
        color.append(colors[categories.index(group)])

print("Plotting...")

plt.scatter(x, y, c=color)
plt.xlabel('Average Distance')
plt.ylabel('Furthest Distance')
plt.title('Average Distance vs Furthest Distance')
plt.legend(categories,loc='upper left')
plt.show()

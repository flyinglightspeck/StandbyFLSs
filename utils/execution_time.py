import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import Counter

if not os.path.exists('.assets/figure'):
    os.makedirs('.assets/figure', exist_ok=True)

mpl.rcParams['font.family'] = 'Times New Roman'

fig = plt.figure(figsize=(5, 3), layout='constrained')
ax = fig.add_subplot()
CANF_line, = plt.plot([3, 5, 10, 20], [108.17, 118.11, 232.67, 1339.43], marker='o', label=f'CANF Execution Time')

kmeans_line, = plt.plot([3, 5, 10, 20], [5.15, 3.85, 3.15, 1.38], marker='x', label=f'k-means Execution Time')

plt.yscale('log')

plt.yticks([1, 10, 100, 1000], [1, 10, 100, 1000])

# plt.tight_layout()

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Set x-axis to only show values in group_sizes list
plt.xticks([3, 5, 10, 20])

y_locator = mpl.ticker.FixedLocator([1e-3, 1e-2, 1e-1, 1, 10, 100, 1000])
ax.yaxis.set_major_locator(y_locator)
y_formatter = mpl.ticker.FixedFormatter(["0.001", "0.01", "0.1", "1", "10", "100", "1000"])
ax.yaxis.set_major_formatter(y_formatter)

ax.set_title('Execution Time (Second)', loc='left')
# ax.set_ylabel('Execution Time (Second)', loc='top', rotation=0, labelpad=-124)
ax.set_xlabel('Group Size (G)', loc='right', labelpad=-1, fontsize='large')

plt.text(7.5, 88.5, 'CANF', color=CANF_line.get_color(), fontweight='bold')

plt.text(7.5, 4.5, 'k-means', color=kmeans_line.get_color(), fontweight='bold')

# Add legend
# plt.legend()

# plt.tight_layout()
# plt.show(dpi=500)
plt.savefig(f"./assets/figure/cmpRTkmeansCANF.png", dpi=500)
plt.close()


group_size = [6, 8, 8, 9, 10, 11, 11, 12, 13, 15, 15, 15, 15, 15, 16, 18, 18, 18, 18, 19, 19, 19, 20, 20, 21, 23, 25, 26, 26, 28, 28, 28, 29, 32, 33, 35, 38, 40]

group_counts = Counter(group_size)

fig = plt.figure(figsize=(5, 3), layout='constrained')
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Get the unique group sizes and their respective counts
sizes = list(group_counts.keys())
counts = list(group_counts.values())

# bin_edges = np.linspace(min(sizes) - 0.5, max(sizes) + 0.5, len(sizes) + 1)
# Create a bar graph
plt.bar(sizes, counts, align='center', edgecolor='black', linewidth=1, width=1)
plt.xlabel('Size of the Group', fontsize='large')

plt.xticks(sizes)
ax.set_title('Number of Groups', loc='left')
# ax.set_ylabel('Number of Groups', loc='top', rotation=0, labelpad=-91)

ax = plt.gca()
ax.get_xaxis().set_major_locator(plt.MaxNLocator(integer=True))
ax.get_yaxis().set_major_locator(plt.MaxNLocator(integer=True))


# plt.tight_layout()
plt.savefig(f"./assets/figure/group_size.png", dpi=500)
# plt.show(dpi=500)
plt.close()
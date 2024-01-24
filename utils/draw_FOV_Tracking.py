import ax
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib as mpl
import pandas as pd

meta_dir = "../assets"

mpl.rcParams['font.family'] = 'Times New Roman'

ratios = [1, 3, 5, 10]

value_list = [[324, 65, 38, 31], [41, 22, 23, 14]]

fig = plt.figure(figsize=(5, 3), layout='constrained')
ax = fig.add_subplot()
g3_line, = plt.plot(ratios, value_list[0], marker='o')

g20_line, = plt.plot(ratios, value_list[1], marker='x')


plt.text(3, 100, 'G=3', color=g3_line.get_color(), fontweight='bold')

plt.text(3, 35, 'G=20', color=g20_line.get_color(), fontweight='bold')

# ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for spine in ax.spines.values():
    spine.set_zorder(1)
# Set x-axis to only show values in group_sizes list
plt.xticks(ratios)

ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

ax.set_title('Number of Obstructing FLS', loc='left')

# ax.set_ylabel('Quality of Illumination (QoI)', loc='top', rotation=0, labelpad=-140)
ax.set_xlabel('Illumination Cell to Display Cell Ratio (Q)', loc='right', fontsize='large')
# plt.tight_layout()
# Add legend
# plt.show(dpi=500)
plt.savefig(f"{meta_dir}/figure/numobstructing.png", dpi=500)
plt.close()


value_list = [[31.59, 1.21, 1.31, 1.29], [25.61, 1.21, 1.29, 1.32]]

fig = plt.figure(figsize=(5, 3), layout='constrained')
ax = fig.add_subplot()
g3_line, = plt.plot(ratios, value_list[0], marker='o')

g20_line, = plt.plot(ratios, value_list[1], marker='x')


plt.text(1.5, 25, 'G=3', color=g3_line.get_color(), fontweight='bold')

plt.text(1.5, 8, 'G=20', color=g20_line.get_color(), fontweight='bold')

# ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for spine in ax.spines.values():
    spine.set_zorder(1)
# Set x-axis to only show values in group_sizes list
plt.xticks(ratios)

ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

ax.set_title('Display Cells Moved', loc='left')

# ax.set_ylabel('Quality of Illumination (QoI)', loc='top', rotation=0, labelpad=-140)
ax.set_xlabel('Illumination Cell to Display Cell Ratio (Q)', loc='right', fontsize='large')
# plt.tight_layout()
# Add legend
# plt.show(dpi=500)
plt.savefig(f"{meta_dir}/figure/illmove.png", dpi=500)
plt.close()


value_list = [[4.34, 5.07, 11.50, 26.19], [1.69, 4.37, 11.74, 14.09]]

fig = plt.figure(figsize=(5, 3), layout='constrained')
ax = fig.add_subplot()
g3_line, = plt.plot(ratios, value_list[0], marker='o')

g20_line, = plt.plot(ratios, value_list[1], marker='x')


plt.text(6, 17, 'G=3', color=g3_line.get_color(), fontweight='bold')

plt.text(6, 10, 'G=20', color=g20_line.get_color(), fontweight='bold')

# ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for spine in ax.spines.values():
    spine.set_zorder(1)
# Set x-axis to only show values in group_sizes list
plt.xticks(ratios)

ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

ax.set_title('Display Cells Moved', loc='left')

# ax.set_ylabel('Quality of Illumination (QoI)', loc='top', rotation=0, labelpad=-140)
ax.set_xlabel('Illumination Cell to Display Cell Ratio (Q)', loc='right', fontsize='large')
# plt.tight_layout()
# Add legend
# plt.show(dpi=500)
plt.savefig(f"{meta_dir}/figure/stbymove.png", dpi=500)
plt.close()



value_list = [[3.15298366, 0.05564516, 0.05133542, 0.05854882], [1.54317972, 0.02921781, 0.08598634, 0.01483916]]

fig = plt.figure(figsize=(5, 3), layout='constrained')
ax = fig.add_subplot()
g3_line, = plt.plot(ratios, value_list[0], marker='o')

g20_line, = plt.plot(ratios, value_list[1], marker='x')


plt.text(1.5, 2.6, 'G=3', color=g3_line.get_color(), fontweight='bold')

plt.text(1.5, 0.4, 'G=20', color=g20_line.get_color(), fontweight='bold')

ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for spine in ax.spines.values():
    spine.set_zorder(1)
# Set x-axis to only show values in group_sizes list
plt.xticks(ratios)

ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

ax.set_title('Percentage Change in MTID', loc='left')

ax.set_xlabel('Illumination Cell to Display Cell Ratio (Q)', loc='right', fontsize='large')
# plt.tight_layout()
# Add legend
# plt.show(dpi=500)
plt.savefig(f"{meta_dir}/figure/mtidchg.png", dpi=500)
plt.close()


value_list = [[57, 19, 8, 9], [5, 7, 5, 6]]

fig = plt.figure(figsize=(5, 3), layout='constrained')
ax = fig.add_subplot()
g3_line, = plt.plot(ratios, value_list[0], marker='o')

g20_line, = plt.plot(ratios, value_list[1], marker='x')


plt.text(4, 15, 'G=3', color=g3_line.get_color(), fontweight='bold')

plt.text(4, 1, 'G=20', color=g20_line.get_color(), fontweight='bold')

# ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for spine in ax.spines.values():
    spine.set_zorder(1)
# Set x-axis to only show values in group_sizes list
plt.xticks(ratios)

ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

ax.set_title('Number of Obstructing FLSs', loc='left')

ax.set_xlabel('Illumination Cell to Display Cell Ratio (Q)', loc='right', fontsize='large')
# plt.tight_layout()
# Add legend
# plt.show(dpi=500)
plt.savefig(f"{meta_dir}/figure/obstsec.png", dpi=500)
plt.close()
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

mpl.rcParams['font.family'] = 'Times New Roman'

ratios = [1, 3, 5, 10]
fig = plt.figure(figsize=(5, 3), layout='constrained')
ori_standby_line, = plt.plot(ratios, [0.82, 0.71, 0.79, 0.71], marker='o',  label=f'G=3')

dispatcher_line, = plt.plot(ratios, [0.88, 0.68, 0.78, 0.57], marker='x',  label=f'G=20')

ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_title('Percentage Changed', loc='left')
ax.set_xlabel('Illumination Cell To Display Cell Ratio (Q)', loc='right', fontsize='large')
# ax.set_xlim(left=0, right=100)
ax.set_ylim(0, 0.9)

ax.yaxis.set_major_formatter(PercentFormatter(1))
plt.xticks(ratios)

plt.text(7, 0.8, 'G=3', color=ori_standby_line.get_color(), fontweight='bold', zorder=3)

plt.text(7, 0.6, 'G=20', color=dispatcher_line.get_color(), fontweight='bold', zorder=3)

# Add legend
# ax.legend()
# plt.show(dpi=500)
plt.savefig(f"../assets/figures/obstruct_percentage_changed.png", dpi=500)
plt.close()




fig = plt.figure(figsize=(5, 3), layout='constrained')
ori_standby_line, = plt.plot(ratios, [-0.0116, 0.0116, -0.0042, -0.0243], marker='o',  label=f'G=3')

dispatcher_line, = plt.plot(ratios, [-0.1586, 0.0245, -0.0336, 0.0845], marker='x',  label=f'G=20')
zero_line, = plt.plot([0, 11], [0, 0], '--', color=(0.7, 0.7, 0.7), linewidth=1)

ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_title('Percentage Changed', loc='left')
ax.set_xlabel('Illumination Cell To Display Cell Ratio (Q)', loc='right', fontsize='large')
ax.set_xlim(left=0, right=10.2)
ax.set_ylim(-0.2, 0.1)

ax.yaxis.set_major_formatter(PercentFormatter(1))
plt.xticks(ratios)

plt.text(7, -0.04, 'G=3', color=ori_standby_line.get_color(), fontweight='bold', zorder=3)

plt.text(7, 0.04, 'G=20', color=dispatcher_line.get_color(), fontweight='bold', zorder=3)

# Add legend
# ax.legend()
# plt.show(dpi=500)
plt.savefig(f"../assets/figures/illum_move_percentage_changed.png", dpi=500)
plt.close()



fig = plt.figure(figsize=(5, 3), layout='constrained')
ori_standby_line, = plt.plot(ratios, [-4.8216, 0.5890, 0.1196, 0.2920], marker='o',  label=f'G=3')

dispatcher_line, = plt.plot(ratios, [-7.1344, 0.2494, 0.4737, 0.2501], marker='x',  label=f'G=20')

zero_line, = plt.plot([0, 11], [0, 0], '--', color=(0.7, 0.7, 0.7), linewidth=1)

ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_title('Percentage Changed', loc='left')
ax.set_xlabel('Illumination Cell To Display Cell Ratio (Q)', loc='right', fontsize='large')
ax.set_xlim(left=0, right=10.2)

ax.set_ylim(-7.2, 1)
yticks = plt.yticks()[0]
yticks = list(yticks)
yticks[0] = -7.2
yticks[-1] = 1
plt.yticks(sorted(yticks))

# Add the y_value to the y-ticks if it's not already there

ax.yaxis.set_major_formatter(PercentFormatter(1))
plt.xticks(ratios)

plt.text(7, -0.5, 'G=3', color=ori_standby_line.get_color(), fontweight='bold', zorder=3)

plt.text(7, 0.5, 'G=20', color=dispatcher_line.get_color(), fontweight='bold', zorder=3)

# Add legend
# ax.legend()
# plt.show(dpi=500)
plt.savefig(f"../assets/figures/standby_move_percentage_changed.png", dpi=500)
plt.close()



fig = plt.figure(figsize=(5, 3), layout='constrained')
ori_standby_line, = plt.plot(ratios, [-6.0107, 0.5813, -0.5874, 0.7143], marker='o',  label=f'G=3')

dispatcher_line, = plt.plot(ratios, [-8.5830, -2.0107, -0.7686, -0.1875], marker='x',  label=f'G=20')

zero_line, = plt.plot([0, 11], [0, 0], '--', color=(0.7, 0.7, 0.7), linewidth=1)

ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_title('Percentage Changed', loc='left')
ax.set_xlabel('Illumination Cell To Display Cell Ratio (Q)', loc='right', fontsize='large')
ax.set_xlim(left=0, right=10.2)

ax.set_ylim(-7.2, 1)
yticks = plt.yticks()[0]
yticks = list(yticks)
yticks.append(-8.6)
yticks[-1] = 1
plt.yticks(sorted(yticks))

# Add the y_value to the y-ticks if it's not already there

ax.yaxis.set_major_formatter(PercentFormatter(1))
plt.xticks(ratios)

plt.text(7, -0.5, 'G=3', color=ori_standby_line.get_color(), fontweight='bold', zorder=3)

plt.text(7, 0.5, 'G=20', color=dispatcher_line.get_color(), fontweight='bold', zorder=3)

# Add legend
# ax.legend()
# plt.show(dpi=500)
plt.savefig(f"../assets/figures/dragon_standby_move_percentage_changed.png", dpi=500)
plt.close()



fig = plt.figure(figsize=(5, 3), layout='constrained')
ori_standby_line, = plt.plot(ratios, [0.45, 0.52, 0.52, 0.54], marker='o',  label=f'G=3')

dispatcher_line, = plt.plot(ratios, [0.20, 0.21, 0.24, 0.28], marker='x',  label=f'G=20')

# zero_line, = plt.plot([0, 11], [0, 0], '--', color=(0.7, 0.7, 0.7), linewidth=1)

ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_title('MTID (Second)', loc='left')
ax.set_xlabel('Group Size (G)', loc='right', fontsize='large')
ax.set_xlim(left=0, right=10.2)
ax.set_ylim(0, 1)

# yticks = plt.yticks()[0]
# yticks = list(yticks)
# yticks.append(-8.6)
# yticks[-1] = 1
# plt.yticks(sorted(yticks))

# Add the y_value to the y-ticks if it's not already there

# ax.yaxis.set_major_formatter(PercentFormatter(1))
plt.xticks(ratios)

plt.text(7, 0.55, 'CANF', color=ori_standby_line.get_color(), fontweight='bold', zorder=3)

plt.text(7, 0.2, 'k-means', color=dispatcher_line.get_color(), fontweight='bold', zorder=3)

# Add legend
# ax.legend()
# plt.show(dpi=500)
plt.savefig(f"../assets/figures/skateboard_CANF_kmeans_MTID.png", dpi=500)
plt.close()
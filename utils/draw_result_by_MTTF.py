import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib as mpl
import pandas as pd


mpl.rcParams['font.family'] = 'Times New Roman'
# mttr_list = []
# QoI_list = []
# delay_list = []
mttf_list = [30, 60, 120, 300]
#
# QoI Plot
QoI_list = [[0.1621309, 0.3329473, 0.6595252, 0.9936306], [0.3057325, 0.6242038, 0.9779965, 0.9976838]]
fig = plt.figure(figsize=(5, 3), layout='constrained')
ax = fig.add_subplot()
rand_line, = plt.plot(mttf_list, QoI_list[0], marker='o', label=f'RandTTL', zorder=4)

exp_line, = plt.plot(mttf_list, QoI_list[1], marker='x', label=f'BetaTTL', zorder=4)


plt.text(60, 0.25, 'RandTTL', color=rand_line.get_color(), fontweight='bold')

plt.text(60, 0.90, 'BetaTTL', color=exp_line.get_color(), fontweight='bold')

ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for spine in ax.spines.values():
    spine.set_zorder(1)
# Set x-axis to only show values in group_sizes list
plt.xticks(mttf_list)

ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

ax.set_title('Quality of Illumination (QoI)', loc='left', zorder=4)

# ax.set_ylabel('Quality of Illumination (QoI)', loc='top', rotation=0, labelpad=-140)
ax.set_xlabel('Maximum Time To Live (λ)', loc='right', fontsize='large')
# plt.tight_layout()
# Add legend
# plt.show(dpi=500)
plt.savefig(f"../skateboard_G0_QoI_by_MTTF.png", dpi=500)
plt.close()


# MTTR Plot
#G=3
# mttr_list = [[72.9, 57.96, 0.91, 0.91], [60.19, 32.43, 0.58, 0.46]]

#G=0
mttr_list = [[72.67, 58.53, 29.44, 1.75], [59.65, 32.47, 1.49, 1.29]]

fig = plt.figure(figsize=(5, 3), layout='constrained')
ax = fig.add_subplot()

rand_line, = plt.plot(mttf_list, mttr_list[0], marker='o', label=f'RandTTL', zorder=4)

exp_line, = plt.plot(mttf_list, mttr_list[1], marker='x', label=f'BetaTTL', zorder=4)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


# Set x-axis to only show values in group_sizes list
plt.xticks(mttf_list)

ax.set_title('MTID (Second)', loc='left', zorder=1)

# ax.set_ylabel('Mean Time to Illuminate after a Failure(MTIF)', loc='top', rotation=0, labelpad=-225)
ax.set_xlabel('Maximum Time To Live (λ)', loc='right', fontsize='large')
ax.set_xlim(left=0)

yticks = plt.yticks()[0]
yticks = yticks[2:-2]
yticks = sorted(list(yticks) + [min(min(mttr_list)), max(max(mttr_list))])
# Set the updated y-ticks
plt.yticks(yticks)

ax.set_ylim(0, max(max(mttr_list))+2)

plt.text(55, 65, 'RandTTL', color=rand_line.get_color(), fontweight='bold', zorder=3)

plt.text(55, 13, 'BetaTTL', color=exp_line.get_color(), fontweight='bold', zorder=3)

# Add legend
# plt.tight_layout()
# plt.show(dpi=500)
plt.savefig(f"..assets/figures/skateboard_G0_MTIF_by_MTTF.png", dpi=500)
plt.close()


# Queuing delay Plot
#G=3
# delay_list = [[70.39, 56.12, 5.78, 5.78], [58.24, 31.81, 8.1, 8.52]]

# G=0
delay_list = [[58.4, 54.12, 30.09, 4.01], [51.56, 34.28, 6.82, 6.30]]

fig = plt.figure(figsize=(5, 3), layout='constrained')
ax = fig.add_subplot()

rand_line, = plt.plot(mttf_list, delay_list[0], marker='o', label=f'RandTTL', zorder=4)

exp_line, = plt.plot(mttf_list, delay_list[1], marker='x', label=f'BetaTTL', zorder=4)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


# Set x-axis to only show values in group_sizes list
plt.xticks(mttf_list)

ax.set_title('Queuing Delay (Second)', loc='left', zorder=4)
# ax.set_ylabel('Queuing Delay (Second)', loc='top', rotation=0, labelpad=-121)

ax.set_xlabel('Maximum Time To Live (λ)', loc='right', fontsize='large')
ax.set_xlim(left=0)

yticks = plt.yticks()[0]
# yticks = sorted(list(yticks) + [min(min(delay_list)), max(max(delay_list))])
# Set the updated y-ticks
# yticks = yticks[2:]
plt.yticks(yticks)

ax.set_ylim(0, max(max(delay_list))+2)

plt.text(65, 55, 'RandTTL', color=rand_line.get_color(), fontweight='bold', zorder=3)

plt.text(65, 13, 'BetaTTL', color=exp_line.get_color(), fontweight='bold', zorder=3)

# Add legend
# plt.tight_layout()
# plt.show(dpi=500)
plt.savefig(f"../skateboard_G0_QueDelay_by_MTTF.png", dpi=500)
plt.close()
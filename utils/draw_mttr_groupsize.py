import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import pandas as pd

mttr_list = [[],[]]
QoI_list = [[],[]]
for i, filename in enumerate(["True", "False"]):

    for folder in ["K0", "K3", "K5", "K10", "K15", "K20"]:

        folder_path = "/proj/nova-PG0/NAME/results/"# replace with the result folder of the final result

        input_path = f"{folder_path}/dragon/{folder}/dragon_D1_R10_T60_S6_P{filename}/dragon_D1_R10_T60_S6_P{filename}_final_report.xlsx"

        metrics_df = pd.read_excel(input_path, sheet_name='Metrics')

        print(folder)

        # Get the value from the "metrics" sheet
        mttr_list[i].append(metrics_df[metrics_df.iloc[:, 1] == "Avg MTTR"].iloc[0, 2])
        QoI_list[i].append(metrics_df[metrics_df.iloc[:, 1] == "QoI After Reset"].iloc[0, 2])


plt.figure()
pri_line, = plt.plot([0, 3, 5, 10, 15, 20], mttr_list[0], marker='o', label=f'With Priority Queue')

nopri_line, = plt.plot([0, 3, 5, 10, 15, 20], mttr_list[1], marker='x', label=f'No Priority Queue')

ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


# Set x-axis to only show values in group_sizes list
plt.xticks([0, 3, 5, 10, 15, 20])

ax.set_ylabel('Mean Time to Illuminate after a Failure(MTIF)', loc='top', rotation=0, labelpad=-260)
ax.set_xlabel('Group Size (G)', loc='right', fontsize='large')
ax.set_xlim(left=0)

yticks = plt.yticks()[0]
yticks = sorted(list(yticks) + [min(min(mttr_list)), max(max(mttr_list))])
# Set the updated y-ticks
plt.yticks(yticks)

ax.set_ylim(min(min(mttr_list)), max(max(mttr_list))+1)

plt.text(6, 48, 'With Priority Queue', color=pri_line.get_color(), fontweight='bold', zorder=3)

plt.text(6, 54, 'No Priority Queue', color=nopri_line.get_color(), fontweight='bold', zorder=3)

# Add legend
plt.show(dpi=500)
plt.tight_layout()
plt.savefig(f"../dragon_MTIF_groupsize_compare.png", dpi=500)
plt.close()

plt.figure()
pri_line, = plt.plot([0, 3, 5, 10, 15, 20], QoI_list[0], marker='o', label=f'With Priority Queue', zorder=3)

nopri_line, = plt.plot([0, 3, 5, 10, 15, 20], QoI_list[1], marker='x', label=f'No Priority Queue', zorder=3)

ax.yaxis.set_major_formatter(PercentFormatter(1))

plt.text(6, 0.385, 'With Priority Queue', color=pri_line.get_color(), fontweight='bold')

plt.text(6, 0.348, 'No Priority Queue', color=nopri_line.get_color(), fontweight='bold')
plt.tight_layout()

ax = plt.gca()

ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for spine in ax.spines.values():
    spine.set_zorder(1)
# Set x-axis to only show values in group_sizes list
plt.xticks([0, 3, 5, 10, 15, 20])

ax.set_xlim(left=0)
ax.set_ylim(0.3, 0.4)

ax.set_ylabel('Quality of Illumination (QoI)', loc='top', rotation=0, labelpad=-175)
ax.set_xlabel('Group Size (G)', loc='right', fontsize='large')
plt.tight_layout()
# Add legend
# plt.show(dpi=500)
plt.savefig(f"../dragon_QoI_groupsize_compare.png", dpi=500)
plt.close()
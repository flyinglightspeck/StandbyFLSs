import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# List of Excel file names
# shapes = ["dragon", "skateboard"]
shapes = ["skateboard"]
speed = "66"

mpl.rcParams['font.family'] = 'Times New Roman'

# data_names = ["50th percentile", "95th percentile", "99th percentile"]
data_names = ["95th percentile"]
for shape in shapes:

    for data_name in data_names:

        excel_files = [f'{shape}_G0_R3000_T900_S{speed}', f'{shape}_G3_R3000_T900_S{speed}', f'{shape}_G20_R3000_T900_S{speed}']
        path = "../assets/mtif_by_time/"
        labels = ["No Standby", "G=3", "G=20"]

        fig = plt.figure(figsize=(5, 3), layout='constrained')
        ax = fig.add_subplot()

        colors = ['#1f77b4', 'orange', '#9467bd']

        # Iterate over each Excel file and plot the data
        for i, file in enumerate(excel_files):
            # Read the Excel file
            df = pd.read_excel(path + file + ".xlsx", engine='openpyxl')
            df = df.drop([0, 1])
            df.drop(df.tail(2).index, inplace=True)

            time = df['Time(sec)']
            time = [t/60 for t in time]

            # Extract data from the '50th percentile' column
            mtif = df[data_name]

            # Plot the data
            plt.plot(time, mtif, label=labels[i], color=colors[i])

        # Customize the plot
        plt.xlabel('Time (Minute)', loc='right', fontsize="large")

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.set_title('MTID (Second)', loc='left', zorder=4)
        # plt.legend()
        plt.text(30, 0.43, 'No Standby', color=colors[0], fontweight='bold', zorder=3)
        plt.text(30, 0.1, 'G=3', color=colors[1], fontweight='bold', zorder=3)
        plt.text(30, 0.15, 'G=20', color=colors[2], fontweight='bold', zorder=3)

        # Show the plot
        # plt.show(dpi=500)

        if not os.path.exists(f"{path}figures/"):
            os.makedirs(f"{path}figures/", exist_ok=True)

        plt.savefig(f"{path}figures/{shape}_{data_name[0:2]}_S{speed}", dpi=500)
        plt.close()

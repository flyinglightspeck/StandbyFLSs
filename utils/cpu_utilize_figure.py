import os
import matplotlib.pyplot as plt
from collections import defaultdict


def plot_cpu_utilization(folder_path, output_png_file):
    try:
        primary_data = defaultdict(list)
        secondary_data = defaultdict(list)

        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as file:
                    for line in file:
                        time_stamp, cpu_util = map(float, line.strip().split(','))
                        time_stamp = round(time_stamp)
                        if filename == '0.txt':
                            primary_data[time_stamp].append(cpu_util)
                        else:
                            secondary_data[time_stamp].append(cpu_util)

        # Calculate the average CPU utilization for each second
        primary_avg = {k: sum(v) / len(v) for k, v in primary_data.items()}
        secondary_avg = {k: sum(v) / len(v) for k, v in secondary_data.items()}

        # Plot the data
        plt.figure()

        if secondary_avg:
            times, values = zip(*sorted(secondary_avg.items()))
            plt.plot(times, values, label='Secondary Nodes')

        if primary_avg:
            times, values = zip(*sorted(primary_avg.items()))
            plt.plot(times, values, label='Primary Node')

        # Configure plot
        plt.xlabel('Time (s)')
        plt.ylabel('CPU Utilization (%)')
        plt.title('CPU Utilization Over Time')
        plt.legend()
        plt.ylim(0, 100)

        # Save the plot as a PNG file
        plt.savefig(output_png_file)
        print(f"The plot has been saved to {output_png_file}")
    except FileNotFoundError:
        print(f"The folder at path {folder_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    folder_path = "../cpu_log"  # Replace with the path to your folder
    output_figure_path = '../cpu_log/cpu_utilization_plot.png'  # Replace with the path to save the output figure

    plot_cpu_utilization(folder_path, output_figure_path)

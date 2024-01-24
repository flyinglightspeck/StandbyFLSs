import json
import matplotlib.pyplot as plt


def plot_failed_growth(json_file_path, output_png_file):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            failed_data = data.get('failed', {})

        time_stamps = failed_data.get('t', [])
        failed_numbers = failed_data.get('y', [])

        if not time_stamps or not failed_numbers:
            print("The 't' or 'y' data is missing in the 'failed' dictionary.")
            return

        failed_per_time = [0]

        init_time = time_stamps[0]
        failed_num = 0

        x_value = [init_time]

        for i in range(len(failed_numbers)):
            if time_stamps[i] >= init_time + 1:
                init_time = init_time + 1
                x_value.append(init_time)
                failed_per_time.append(failed_num)
                failed_num = 0
            else:
                failed_num = failed_num + 1

        plt.figure(figsize=(60, 15))
        plt.plot(x_value, failed_per_time, linewidth=3)
        plt.title('Failed Per Sec', fontsize=30)

        plt.axhline(40, color='r', linestyle='--')

        plt.axhline(max(failed_per_time), color='g', linestyle='-')

        yticks = plt.yticks()[0]

        # Add the y_value to the y-ticks if it's not already there
        if max(failed_per_time) not in yticks:
            yticks = list(yticks) + [max(failed_per_time)]
            plt.yticks(sorted(yticks))
            
        # Configure plot
        plt.xlabel('Time', fontsize=30)
        plt.ylabel('Failed Number', fontsize=30)
        plt.title('Growth of Failed Number Over Time', fontsize=30)

        plt.legend(fontsize=30)

        # You can also change the font size of the tick labels
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)

        plt.ylim(bottom=0)
        plt.xlim(left=0)

        plt.legend()


        plt.savefig(output_png_file)
        print(f"The plot has been saved to {output_png_file}")
    except FileNotFoundError:
        print(f"The file at path {json_file_path} does not exist.")
    except json.JSONDecodeError:
        print("An error occurred while decoding the JSON data.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    # Example usage
    json_file_path = '../charts.json'  # Replace with the path to your JSON file
    output_png_file = '../failure_growth.png'  # Replace with the desired path for the output PNG file

    plot_failed_growth(json_file_path, output_png_file)

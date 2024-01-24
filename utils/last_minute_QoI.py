import json
import numpy as np

# Replace with the actual file path
directory = ""

shape = "skateboard"

folder = f"{shape}_BetaTTL/"
group_size = ["K0", "K3", "K5", "K10", "K15", "K20"]

file_name = f"{shape}_D1_R3000_T900_S6_PTrue"

for K in group_size:

    file_path = f"{directory}{folder}{K}/{file_name}/charts.json"

    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract the 'illuminating' data
    illuminating_data = data.get('illuminating', {})
    timestamps = illuminating_data.get('t', [])
    values = illuminating_data.get('y', [])

    # Calculate the average value per second
    # Assuming the timestamps are in seconds and are integers
    averages_per_second = []
    for second in range(2940, 3000):
        values_in_second = [value for timestamp, value in zip(timestamps, values) if (timestamp >= second and timestamp< second + 1)]
        if values_in_second:
            averages_per_second.append(np.mean(values_in_second))

    # Calculate the overall average of the averages per second
    overall_average = np.mean(averages_per_second) if averages_per_second else None

    print(overall_average/1727)

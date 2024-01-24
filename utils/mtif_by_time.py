import json
import pandas as pd

# Load the events from the JSON file

# shapes = ["dragon", "skateboard"]
shapes = ["hat"]
speed = "66"

group_size = [0, 3, 20]
point_nums = {
    "dragon": 760,
    "skateboard": 1727,
    "hat": 1562
}

for shape in shapes:
    for G in group_size:
        config = f"{shape}_G{G}_R3000_T900_S{speed}"
        with open(f'..assets/timelines/{config}.json', 'r') as file:
            events = json.load(file)

        file_name = f"..assets//mtif_by_time/{config}"
        # Dictionary to store the state of each point
        points = {}

        # Dictionary to store the dark times of each point
        dark_times = {}

        # List to store the dark-to-lightened time differences
        mtif = []

        report = [['Time(sec)', 'Samples', '50th percentile', '95th percentile', '99th percentile']]

        point_num = point_nums[shape]
        initial_num = 0
        start_time = 180000

        time_window = 60

        # Process each event
        for event in events:
            if event[0] > 3500:
                a=1
                pass

            if event[0] > start_time + time_window:

                mtif.sort()
                start_time += time_window

                # Calculate the average dark-to-lightened time
                if mtif:
                    print(f"Time: {round(start_time/60)}, {len(mtif)} Samples, The average MTIF: {mtif[round(0.5 * len(mtif))]:.2f}")
                    report.append(
                        [start_time, len(mtif), mtif[round(0.5 * (len(mtif) - 1))], mtif[round(0.95 * (len(mtif) - 1))],
                         mtif[round(0.99 * (len(mtif) - 1))]])
                else:
                    print(f"Time: {round(start_time/60)}, No points were lightened after going dark")
                    report.append([start_time, 0, 0, 0, 0])

                mtif = []

            if event[1] in [1, 6]:
                # The point is lightened by a drone
                coordinate = tuple(event[2])  # Convert the coordinate to a tuple to use it as a dictionary key

                if coordinate in dark_times:
                    # Calculate the time difference and add it to the list
                    time_difference = event[0] - dark_times[coordinate]
                    mtif.append(time_difference)

                    # Remove the dark time as the point is now lightened
                    del dark_times[coordinate]

                # Update the point's state
                points[coordinate] = event[-1]

            elif event[1] in [3, 5]:
                # The drone failed
                failed_drone_id = event[3]

                # Find the point that was lightened by the failed drone and set it to dark
                for coordinate, drone_id in points.items():
                    if drone_id == failed_drone_id:
                        dark_times[coordinate] = event[0]  # Record the time the point goes dark
                        del points[coordinate]  # Remove the point's state as it's now dark
                        break

            elif initial_num <= point_num and event[1] == 0:
                dark_times[tuple(event[2])] = 0
                initial_num += 1
                if initial_num == point_num:
                    start_time = event[0]
                    print("Rest")

        # Calculate the average dark-to-lightened time
        mtif.sort()
        start_time += time_window

        # Calculate the average dark-to-lightened time
        if mtif:
            print(f"Time: {round(start_time/60)}, {len(mtif)} Samples, The average MTIF: {mtif[round(0.5 * len(mtif))]:.2f}")
            report.append([start_time, len(mtif), mtif[round(0.5 * (len(mtif) - 1))], mtif[round(0.95 * (len(mtif) - 1))],
                 mtif[round(0.99 * (len(mtif) - 1))]])

        df = pd.DataFrame(report[1:], columns=report[0])

        # Write the DataFrame to an Excel file
        df.to_excel(f'{file_name}.xlsx', index=False, engine='openpyxl')

        print("Finished")
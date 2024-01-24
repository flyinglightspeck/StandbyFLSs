import csv
import statistics
import math
import numpy as np
import pandas as pd
from tqdm import tqdm
import multiprocessing as mp
import matplotlib.pyplot as plt
from find_obstructing_raybox import get_distance, read_cliques_xlsx, get_standby_coords, read_coordinates, is_disp_cell_overlap, get_points_from_file

def ray_cell_intersection(origin, direction, point, ratio, is_standby):
    """Check if a ray intersects with a cube."""
    # Cube dimensions
    if is_standby:
        half_size = 0.5
    else:
        half_size = 0.5 * ratio

    min_corner = point - half_size
    max_corner = point + half_size

    # Compute intersection of ray with all six bbox planes
    inv_direction = 1.0 / direction
    tmin = (min_corner - origin) * inv_direction
    tmax = (max_corner - origin) * inv_direction

    # Reorder intersections to find overall min/max
    tmin, tmax = np.minimum(tmin, tmax), np.maximum(tmin, tmax)

    tmin_max = np.max(tmin)
    tmax_min = np.min(tmax)

    # If tmax_min is less than tmin_max, then no intersection
    if tmax_min < tmin_max:
        return False

    # If both tmin_max and tmax_min are negative, then ray is in opposite direction
    if tmax_min < 0:
        return False

    return True


def check_visible_cell(user_eye, pix_list, points, ratio, resolution):
    visible, blocking, blocked, blocking_index = [], [], [], []
    vis_set = [False for _ in points]

    distances = [get_distance(user_eye, point[:3]) for point in points]
    sorted_indices = np.argsort(distances)
    rgb_matrix = np.ones((resolution[0], resolution[1], 3))

    for pix_index in tqdm(range(len(pix_list))):
        l_index = pix_index // resolution[1]
        w_index = pix_index % resolution[1]
        pix_coord = pix_list[pix_index]

        direction = (pix_coord - user_eye)
        direction /= np.linalg.norm(direction)
        direction[direction == 0] = 1e-10
        potential_index = []
        potential_obs = []

        for p_index in sorted_indices:

            point = points[p_index]

            if ray_cell_intersection(user_eye, direction, point[0:3], ratio, point[3]):
                if not vis_set[p_index] or point[3] == 1:
                    if point[3] == 1:
                        potential_index.append(p_index)
                        potential_obs.append(point[0:3])
                        vis_set[p_index] = True
                        visible.append(point)

                        rgb_matrix[l_index][w_index] = np.array([1, 0, 0])
                        continue

                    elif point[3] != 1 and len(potential_index) > 0:
                        blocking.extend(potential_obs)
                        for _ in potential_obs:
                            blocked.extend(point[0:3])

                        blocking_index.extend(potential_index)
                        break
                    else:
                        vis_set[p_index] = True
                        visible.append(point)
                        rgb_matrix[l_index][w_index] = np.array([0, 0, 1])
                        break

    # image = rgb_matrix
    # plt.imshow(image)
    # plt.show()
    return np.array(visible), np.array(blocking), np.array(blocked), np.unique(blocking_index)


def get_pixels(boundary, view_index, camera_shifting=100):
    origin = [
        [boundary[0][0], boundary[0][1], boundary[1][2]],
        [boundary[0][0], boundary[0][1], boundary[0][2]],
        [boundary[0][0], boundary[0][1], boundary[0][2]],
        [boundary[1][0], boundary[0][1], boundary[0][2]],
        [boundary[0][0], boundary[0][1], boundary[0][2]],
        [boundary[0][0], boundary[1][1], boundary[0][2]]
    ]

    axis_list = [
        [0, 1],
        [1, 2],
        [0, 2]
    ]

    axis = axis_list[view_index // 2]

    # pix_size = float('inf')
    pix_size = 0
    resolution = []

    # fixed_resolution = 360

    for ax in axis:
        pix_size = min(pix_size, 1 * camera_shifting / (boundary[1][ax] - boundary[0][ax] + camera_shifting))
        # pix_size = max(pix_size, (boundary[1][ax] - boundary[0][ax])/fixed_resolution)

    vec = [np.array([0., 0., 0.]) for _ in range(2)]
    for i, ax in enumerate(axis):
        resolution.append(math.ceil((boundary[1][ax] - boundary[0][ax]) / pix_size))
        vec[i][ax] += pix_size

    res_ori = origin[view_index]
    pix_list = []

    for l in range(resolution[0]):
        for w in range(resolution[1]):
            pix_list.append(res_ori + l * vec[0] + w * vec[1])

    resolution.reverse()
    print(f"Resolution: {resolution}")
    return pix_list, resolution


def get_points(shape, K, file_folder, ratio):
    input_file = f"{shape}_G{K}.xlsx"

    txt_file = f"{shape}.txt"

    groups = read_cliques_xlsx(f"{file_folder}/pointcloud/{input_file}", ratio)

    group_standby_coord = get_standby_coords(groups, K)

    points = read_coordinates(f"{file_folder}/pointcloud/{txt_file}")

    points = np.array(points)
    points = points * ratio

    point_boundary = [
        [min(points[:, 0]), min(points[:, 1]), min(points[:, 2])],
        [max(points[:, 0]), max(points[:, 1]), max(points[:, 2])]
    ]

    center = np.array([
        (min(points[:, 0]) + max(points[:, 0])) / 2,
        (min(points[:, 1]) + max(points[:, 1])) / 2,
        (min(points[:, 2]) + max(points[:, 2])) / 2
    ])

    check_times = []

    for coord in group_standby_coord:

        coords = points[:, :3]

        coords = coords.tolist()

        check = 0
        if not all([not is_disp_cell_overlap(coord, c) for c in coords]):

            overlap = True
            rims_check = 1

            while overlap:
                directions = []
                for x in range(-rims_check, rims_check + 1, 1):
                    for y in range(-rims_check, rims_check + 1, 1):
                        for z in range(-rims_check, rims_check + 1, 1):
                            if x == 0 and y == 0 and z == 0:
                                continue
                            directions.append([x, y, z])

                directions = sorted(directions, key=lambda d: get_distance(d, center))
                directions = np.array(directions)

                for dirc in directions:
                    new_coord = coord + dirc * 0.5
                    check += 1
                    if all([not is_disp_cell_overlap(new_coord, c) for c in coords]):
                        overlap = False
                        coord = new_coord.tolist()
                        break

                if overlap:
                    if rims_check % 10 == 0:
                        print(f"Rim: {rims_check}")
                    rims_check += 1
                # break
        check_times.append(check)

        coord.append(1)
        points = np.concatenate((points, [coord]), axis=0)

    return points, point_boundary, check_times


def calculate_obstructing(group_file, meta_direc, ratio, k, shape):
    result = [
        ["Shape", "K", "Ratio", "View", "Visible_Illum", "Obstructing FLS", "Min Times Checked",
         "Mean Times Checked",
         "Max Times Checked"]]
    report_path = f"{meta_direc}/obstructing/R{ratio}"

    output_path = f"{meta_direc}/obstructing/R{ratio}/K{k}"

    points, boundary, standbys = get_points_from_file(ratio, group_file, output_path)
    check_times = [0]

    camera_shifting = 100

    cam_positions = [
        # top
        [boundary[0][0] / 2 + boundary[1][0] / 2, boundary[0][1] / 2 + boundary[1][1] / 2,
         boundary[1][2] + camera_shifting],
        # down
        [boundary[0][0] / 2 + boundary[1][0] / 2, boundary[0][1] / 2 + boundary[1][1] / 2,
         boundary[0][2] - camera_shifting],
        # left
        [boundary[0][0] - camera_shifting, boundary[0][1] / 2 + boundary[1][1] / 2,
         boundary[0][0] / 2 + boundary[1][0] / 2],
        # right
        [boundary[1][0] + camera_shifting, boundary[0][1] / 2 + boundary[1][1] / 2,
         boundary[0][0] / 2 + boundary[1][0] / 2],
        # front
        [boundary[0][0] / 2 + boundary[1][0] / 2, boundary[0][1] - camera_shifting,
         boundary[0][0] / 2 + boundary[1][0] / 2],
        # back
        [boundary[0][0] / 2 + boundary[1][0] / 2, boundary[1][1] + camera_shifting,
         boundary[0][0] / 2 + boundary[1][0] / 2]
    ]

    views = ["top", "bottom", "left", "right", "front", "back"]

    illum = []
    standby = []
    for coord in points:
        if coord[3] == 0:
            illum.append(coord[:3])
        else:
            standby.append(coord[:3])

    illum = np.array(illum)
    standby = np.array(standby)

    np.savetxt(f'{output_path}/points/{shape}_illum.txt', illum, fmt='%f', delimiter=' ')
    np.savetxt(f'{output_path}/points/{shape}_standby.txt', standby, fmt='%f', delimiter=' ')

    for i in range(len(views)):

        print(f"START: {shape}, K: {k}, Ratio: {ratio} ,{views[i]}")

        camera = cam_positions[i]

        pix_list, resolution = get_pixels(boundary, i, camera_shifting)

        visible, blocking, blocked_by, blocking_index = check_visible_cell(camera, pix_list, points, ratio,
                                                                           resolution)

        visible_illum = []
        visible_standby = []
        for point in visible:
            if point[3] == 1:
                visible_standby.append(point[0:3])
            else:
                visible_illum.append(point[0:3])

        visible_illum = np.array(visible_illum)
        np.unique(visible_illum, axis=0)

        visible_standby = np.array(visible_standby)
        np.unique(visible_standby, axis=0)

        blocking = np.array(blocking)
        np.unique(blocking, axis=0)

        blocked_by = np.array(blocked_by)
        np.unique(blocked_by, axis=0)

        np.savetxt(f'{output_path}/points/{shape}_{views[i]}_visible_illum.txt', visible_illum, fmt='%f',
                   delimiter=' ')
        np.savetxt(f'{output_path}/points/{shape}_{views[i]}_visible_standby.txt', visible_standby,
                   fmt='%f',
                   delimiter=' ')
        np.savetxt(f'{output_path}/points/{shape}_{views[i]}_blocking.txt', blocking, fmt='%f',
                   delimiter=' ')
        np.savetxt(f'{output_path}/points/{shape}_{views[i]}_blocked.txt', blocked_by, fmt='%f',
                   delimiter=' ')

        print(
            f"{shape}, K: {k}, Ratio: {ratio} ,{views[i]} view: Number of Illuminating FLS: {len(visible_illum)}, Visible Standby FLS: {len(visible_standby)},  Obstructing Number: {len(blocking_index)}")

        result.append(
            [shape, k, ratio, views[i], len(visible_illum), len(blocking_index), min(check_times),
             statistics.mean(check_times), max(check_times)])

    with open(f'{report_path}/report_R{ratio}_K{k}_{shape}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the data from the list to the CSV file
        for row in result:
            writer.writerow(row)


if __name__ == "__main__":

    file_folder = "../assets"
    meta_dir = "../assets"

    p_list = []
    for illum_to_disp_ratio in [10]:

        for k in [3, 20]:

            for shape in ["skateboard"]:
                calculate_obstructing(file_folder, meta_dir, illum_to_disp_ratio, k, shape)
                # p_list.append(mp.Process(target=calculate_obstructing, args=(file_folder, meta_dir, illum_to_disp_ratio, k, shape)))

    # for p in p_list:
    #     print(p)
    #     p.start()

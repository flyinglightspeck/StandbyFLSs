import logging
import pickle

import matplotlib as mpl
from matplotlib.ticker import PercentFormatter

from move_back_obstructing import *
from distance_point_to_line import distance_point_to_line
from prevent_obstructing import rotate_vector, closest_points, read_obstruction_maps

mpl.rcParams['font.family'] = 'Times New Roman'

colors = ['#1f77b4', 'orange', '#9467bd', 'black']
markers = ['s', 'v', 'o', 'x']
Q_list = [1, 3, 5, 10]


def hide_in_closest_illuminating_fls(ptcld_folder, meta_direc, ratio, G, shape, granularity):
    output_path = f"{meta_direc}/obstructing/Q{ratio}/G{G}"

    txt_file = f"{shape}.txt"
    try:
        standby_file = f"{shape}_standby.txt"
        _, boundary, standbys = get_points_from_file(ratio, ptcld_folder, output_path, txt_file, standby_file)
    except Exception as e:
        print("File isn't generated yet, regenerating")
        _, boundary, standbys, _ = get_points(shape, G, ptcld_folder, ratio)

    points = read_coordinates(f"{ptcld_folder}/{txt_file}", ' ')
    points = np.array(points)
    points = points * ratio

    combined_obstruction_map = read_obstruction_maps(output_path, shape, granularity)

    print(sum(combined_obstruction_map))
    # return
    standbys = standbys[:, :3]
    # get the indices of the elements that are non-zero
    obs_idx = np.nonzero(combined_obstruction_map)
    obs_stb_coords = standbys[obs_idx]

    if ratio >= 3:
        closest_ill_coords = closest_points(standbys, points[:, :3])

        is_member = 0
        standby_match = get_illum_standby_matching(shape, G, ptcld_folder, ratio)
        for i in range(len(standbys)):
            if closest_ill_coords[i] in standby_match[i]:
                is_member += 1
        print(f"Is member percentage: {is_member / len(standbys)}")
        new_obs_stb_coords = closest_ill_coords + np.array([0, 0, -1])
        standbys = new_obs_stb_coords

        if not os.path.exists(f"{output_path}/points"):
            os.makedirs(f"{output_path}/points", exist_ok=True)
        np.savetxt(f'{output_path}/points/{shape}_{granularity}_hide_standby.txt', standbys, fmt='%d', delimiter=' ')


def hide_in_obstructed_fls(ptcld_folder, meta_direc, ratio, G, shape, granularity):
    output_path = f"{meta_direc}/obstructing/Q{ratio}/G{G}"

    txt_file = f"{shape}.txt"
    try:
        standby_file = f"{shape}_standby.txt"
        _, boundary, standbys = get_points_from_file(ratio, ptcld_folder, output_path, txt_file, standby_file)
    except Exception as e:
        print("File isn't generated yet, regenerating")
        _, boundary, standbys, _ = get_points(shape, G, ptcld_folder, ratio)

    points = read_coordinates(f"{ptcld_folder}/{txt_file}", ' ')
    points = np.array(points)
    points = points * ratio

    combined_obstruction_map = read_obstruction_maps(output_path, shape, granularity)

    print(sum(combined_obstruction_map))
    # return
    standbys = standbys[:, :3]
    # get the indices of the elements that are non-zero
    obs_idx = np.nonzero(combined_obstruction_map)
    obs_stb_coords = standbys[obs_idx]

    if ratio >= 3:
        closest_ill_coords = closest_points(standbys, points[:, :3])

        is_member = 0
        standby_match = get_illum_standby_matching(shape, G, ptcld_folder, ratio)
        for i in range(len(standbys)):
            if closest_ill_coords[i] in standby_match[i]:
                is_member += 1
        print(f"Is member percentage: {is_member / len(standbys)}")
        new_obs_stb_coords = closest_ill_coords + np.array([0, 0, -1])
        standbys = new_obs_stb_coords

        if not os.path.exists(f"{output_path}/points"):
            os.makedirs(f"{output_path}/points", exist_ok=True)
        np.savetxt(f'{output_path}/points/{shape}_{granularity}_standby_hidden_in_obstructed.txt', standbys, fmt='%d',
                   delimiter=' ')


def get_shape_info(file_path, ptcld_folder, shape, ratio):
    boundary = get_boundary(ptcld_folder, f"{shape}.txt", ratio)

    standby_file = f"{shape}_standby.txt"

    standbys = read_coordinates(f"{file_path}/points/{standby_file}", ' ', 1)
    standbys = standbys[:, 0:3]

    dispatcher = []
    dispatcher.append([boundary[0][0], boundary[0][1], 0])
    dispatcher.append([boundary[1][0], boundary[0][1], 0])

    return standbys, boundary, dispatcher


def get_boundary(ptcld_folder, ptcld_file, ratio):
    points = read_coordinates(f"{ptcld_folder}/{ptcld_file}", ' ')

    points = np.array(points)
    points = points * ratio

    point_boundary = [
        [min(points[:, 0]), min(points[:, 1]), min(points[:, 2])],
        [max(points[:, 0]), max(points[:, 1]), max(points[:, 2])]
    ]

    return point_boundary


def get_illum_standby_matching(shape, G, ptcld_folder, ratio):
    group_file = f"{shape}_G{G}.xlsx"

    groups = read_cliques_xlsx(f"{ptcld_folder}/{group_file}", ratio)

    standby_match = []

    for group in groups:
        standby_match.append(group)

    return standby_match


def get_recover_distance_transpose(shape, G, ptcld_folder, ratio, moved_standbys):
    group_file = f"{shape}_G{G}.xlsx"

    groups = read_cliques_xlsx(f"{ptcld_folder}/{group_file}", ratio)

    dists = []

    for i, group in enumerate(groups):
        distances = [get_distance(moved_standbys[i], coord) for coord in group]
        dists.extend(distances)

    return dists


def get_recover_distance_hide(standbys, obstructing_list, shape, G, ptcld_folder, ratio, moved_standbys):
    group_file = f"{shape}_G{G}.xlsx"

    groups = read_cliques_xlsx(f"{ptcld_folder}/{group_file}", ratio)

    dists = []

    for i, group in enumerate(groups):

        if obstructing_list[i]:
            distances = [get_distance(moved_standbys[i], coord) for coord in group]
            dists.extend(distances)
        else:
            distances = [get_distance(standbys[i], coord) for coord in group]
            dists.extend(distances)

    return dists


def get_recover_distance(standbys, shape, G, ptcld_folder, ratio, obstructing_list, dispatcher):
    group_file = f"{shape}_G{G}.xlsx"

    groups = read_cliques_xlsx(f"{ptcld_folder}/{group_file}", ratio)

    dists = []

    for i, group in enumerate(groups):

        if obstructing_list[i]:
            distances = [distance_point_to_line(coord, dispatcher) for coord in group]
            dists.extend(distances)

        else:
            distances = [get_distance(standbys[i], coord) for coord in group]
            dists.extend(distances)

    return dists


def read_bools_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read each line, strip whitespace, convert to int, and add to list
            bool_list = [int(line.strip()) for line in file]
            return bool_list

    except FileNotFoundError:
        logging.error(f"File {file_path} not found. Please run obstruction_prevention.py to generate it.")
        exit()


def draw_change_plot(path, type, title_name, all_info, figure_name):
    removed_lists, standby_nums, mtids_change_percentages, avg_dists_traveled, avg_dists_restored, avg_dists_combined = [], [], [], [], [], []

    for info in all_info:
        removed_lists.append(info[0])
        standby_nums.append(info[1])
        mtids_change_percentages.append(info[2])
        avg_dists_traveled.append(info[3])
        if len(info) >= 5:
            avg_dists_restored.append(info[4])
            avg_dists_combined.append([info[3][i] + info[4][i] for i in range(len(info[3]))])

    if not os.path.exists(f"{path}/{shape}"):
        os.makedirs(f"{path}/{shape}", exist_ok=True)

    if figure_name == "suspend_hide" or figure_name == "suspend_hide_obstructed":
        offset = 1
    else:
        offset = 0

    draw_dissolved_percentage(granularity, removed_lists, standby_nums, title_name,
                              f"{path}/{shape}/{shape}_K{G}_GR{granularity}_{figure_name}_percentage.png",
                              offset=offset)
    draw_MTID_change_percentage(granularity, mtids_change_percentages,
                                f"{path}/{shape}/{shape}_K{G}_GR{granularity}_MTID_percentage_{figure_name}.png",
                                offset=offset)
    draw_avg_dist_traveled(granularity, avg_dists_traveled,
                           f"{path}/{shape}/{shape}_K{G}_GR{granularity}_dist_traveled_{figure_name}.png",
                           offset=offset)
    if len(all_info[0]) >= 5:
        draw_avg_dist_traveled(granularity, avg_dists_restored,
                               f"{path}/{shape}/{shape}_K{G}_GR{granularity}_dist_traveled_restore_{figure_name}.png",
                               offset=offset)

        draw_avg_dist_traveled(granularity, avg_dists_combined,
                               f"{path}/{shape}/{shape}_K{G}_GR{granularity}_dist_traveled_combined_{figure_name}.png",
                               offset=offset)

    if not os.path.exists(f"{path}/{shape}/{shape}_K{G}_GR{granularity}_{figure_name}_info.pkl"):
        with open(f"{path}/{shape}/{shape}_K{G}_GR{granularity}_{figure_name}_info.pkl", "wb") as outfile:
            pickle.dump(all_info, outfile)


def draw_changed_standby(granularity, restored_list, removed_list, activating_list, save_path):
    degrees = [i * granularity for i in range(0, math.floor(360 / granularity) + 1)]

    fig = plt.figure(figsize=(5, 3), layout='constrained')
    plt.plot(degrees, restored_list, marker=markers[0], markersize=4, c=colors[0], label=f'Restored Standby FLSs')

    plt.plot(degrees, removed_list, marker=markers[1], markersize=4, c=colors[1], label=f'Removed Standby FLSs')

    plt.plot(degrees, activating_list, marker=markers[2], markersize=4, c=colors[2], label=f'Activated Standby FLSs')

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_title('Number of Standby FLSs', loc='left')
    ax.set_xlabel("User's View Angle ($^\circ$)", loc='right', fontsize="large")
    ax.set_xlim(left=0, right=365)
    plt.xticks(np.arange(0, 360 + granularity, step=max(granularity, 20)))
    # ax.set_ylim(0, 40)

    # plt.text(6, 48, 'With Priority Queue', color=pri_line.get_color(), fontweight='bold', zorder=3)
    #
    # plt.text(6, 54, 'No Priority Queue', color=nopri_line.get_color(), fontweight='bold', zorder=3)

    # Add legend
    ax.legend()
    # plt.show(dpi=500)
    plt.savefig(save_path, dpi=500)
    plt.close()


def draw_avg_dist_traveled(granularity, dists_lists, save_path, offset=0):
    degrees = [k * granularity for k in range(0, math.floor(360 / granularity) + 1)]

    fig = plt.figure(figsize=(5, 3), layout='constrained')

    for i in range(0, 4):
        if i >= len(dists_lists) or len(dists_lists[i]) <= 0:
            continue
        j = i + offset
        plt.plot(degrees, dists_lists[i], marker=markers[j], markersize=4, c=colors[j], label=f'Q={Q_list[j]}')

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_title('Avg Distance Traveled (Display Cell)', loc='left')
    ax.set_xlabel("Angle Relative to Start ($^\circ$)", loc='right', fontsize="large")
    ax.set_xlim(left=0, right=365)
    plt.xticks(np.arange(0, 360 + granularity, step=max(granularity, 20)))
    # ax.set_ylim(0, 710)
    ax.legend()

    # leg = ax.legend(loc=(0.8, 0.7), columnspacing=0.5, frameon=False)
    # plt.show(dpi=500)
    plt.savefig(save_path, dpi=500)
    plt.close()


def draw_MTID_change_percentage(granularity, change_lists, save_path, offset=0):
    degrees = [i * granularity for i in range(0, math.floor(360 / granularity) + 1)]

    fig = plt.figure(figsize=(5, 3), layout='constrained')
    cols = 0
    for i in range(0, 4):
        if i >= len(change_lists) or len(change_lists[i]) <= 0:
            continue
        cols += 1
        j = i + offset
        plt.plot(degrees, change_lists[i], marker=markers[j], markersize=4, c=colors[j], label=f'Q={Q_list[j]}')

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_major_formatter(PercentFormatter(1))

    ax.set_title('Percentage Increase in MTID', loc='left')
    ax.set_xlabel("Angle Relative to Start ($^\circ$)", loc='right', fontsize="large")

    max_value = max([max(sub_list) if len(sub_list) > 0 else -float('inf') for sub_list in change_lists])
    min_value = min([min(sub_list) if len(sub_list) > 0 else float('inf') for sub_list in change_lists])

    if max_value < 0:
        ax.set_ylim(min_value * 1.05, 0)
    elif max_value > 0 > min_value:
        ax.set_ylim(min_value * 1.05, max_value * 1.05)
    else:
        ax.set_ylim(0, max_value * 1.05)
    ax.set_xlim(left=0, right=365)
    plt.xticks(np.arange(0, 360 + granularity, step=max(granularity, 20)))

    # Add legend
    leg = ax.legend()
    # leg = ax.legend(loc=(0.7, 0.1), columnspacing=0.5, frameon=False)
    leg.get_frame().set_edgecolor('b')
    leg.get_frame().set_linewidth(0.0)

    # plt.show(dpi=500)
    plt.savefig(save_path, dpi=500)
    plt.close()


def draw_dissolved_percentage(granularity, removed_lists, total_groups, type, save_path, offset=0):
    degrees = [i * granularity for i in range(0, math.floor(360 / granularity) + 1)]

    fig = plt.figure(figsize=(5, 3), layout='constrained')
    cols = 0
    for i in range(0, 4):
        if i >= len(total_groups) or total_groups[i] <= 0:
            continue
        cols += 1
        j = i + offset
        dissolved_list = [dissolved / total_groups[i] for dissolved in removed_lists[i]]
        plt.plot(degrees, dissolved_list, marker=markers[j], markersize=4, c=colors[j], label=f'Q={Q_list[j]}')

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_major_formatter(PercentFormatter(1))

    ax.set_title(f'Percentage of {type} Reliability Groups', loc='left')
    ax.set_xlabel("Angle Relative to Start ($^\circ$)", loc='right', fontsize="large")
    ax.set_ylim(0, 1.05)
    ax.set_xlim(left=0, right=365)
    plt.xticks(np.arange(0, 360 + granularity, step=max(granularity, 20)))
    # ax.set_ylim(0, 40)

    # Add legend
    leg = ax.legend()
    # leg = ax.legend(loc=(0.7, 0.2), columnspacing=0.5, frameon=False)
    leg.get_frame().set_edgecolor('b')
    leg.get_frame().set_linewidth(0.0)
    # plt.show(dpi=500)
    plt.savefig(save_path, dpi=500)
    plt.close()


def draw_MTID(granularity, original_mtid, transpose_mtid, suspend_hide_mtid, save_path):
    degrees = [i * granularity for i in range(0, math.floor(360 / granularity) + 1)]
    original_mtid = [original_mtid for i in range(0, math.floor(360 / granularity) + 1)]

    fig = plt.figure(figsize=(5, 3), layout='constrained')

    plt.plot(degrees, transpose_mtid, marker=markers[2], markersize=4, c=colors[2], label=f'Transpose')

    if len(suspend_hide_mtid) >= 1:
        plt.plot(degrees, suspend_hide_mtid, marker=markers[0], markersize=4, c=colors[0],
                 label=f'Move to Closest Illuminating FLS')
        plt.text(80, min(suspend_hide_mtid) - .8, 'Hide in the Closest Illuminating FLS', color=colors[0],
                 fontweight='bold',
                 fontsize=12, zorder=3)
    plt.plot(degrees, original_mtid, marker=markers[1], markersize=4, c=colors[1], label=f'Obstructing FLS Present')

    plt.text(110, min(original_mtid) - 0.4, 'Obstructing FLS Present', color=colors[1], fontweight='bold', fontsize=12,
             zorder=3)

    plt.text(150, max(transpose_mtid) + 0.2, 'Transpose', color=colors[2], fontweight='bold', fontsize=12, zorder=3)

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_title(f'Avg MTID(Second)', loc='left')
    ax.set_xlabel("Angle Relative to Start ($^\circ$)", loc='right', fontsize="large")
    ax.set_xlim(left=0, right=365)
    plt.xticks(np.arange(0, 360 + granularity, step=max(granularity, 20)))
    ax.set_ylim(0, 4)

    # Add legend
    # ax.legend(loc=3)
    # plt.show(dpi=500)
    plt.savefig(save_path, dpi=500)
    plt.close()


def draw_dist_to_center(granularity, origin_dist, transpose_dist, suspend_hide_dist, save_path):
    degrees = [i * granularity for i in range(0, math.floor(360 / granularity) + 1)]

    fig = plt.figure(figsize=(5, 3), layout='constrained')

    plt.plot(degrees, transpose_dist, marker=markers[2], markersize=4, c=colors[2],
             label=f'Transpose')
    plt.plot(degrees, suspend_hide_dist, marker=markers[0], markersize=4, c=colors[0],
             label=f'Hide in the Closest Illuminating FLS')
    plt.plot(degrees, origin_dist, marker=markers[1], markersize=4, c=colors[1], label=f'Obstructing FLS Present')

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_title(f'Avg Distance From Group Member to Standby (Display Cells)', loc='left')
    ax.set_xlabel("Angle Relative to Start ($^\circ$)", loc='right', fontsize="large")
    ax.set_xlim(left=0, right=365)
    plt.xticks(np.arange(0, 360 + granularity, step=max(granularity, 20)))
    ax.set_ylim(0, )

    # Add legend
    ax.legend()
    # plt.show(dpi=500)
    plt.savefig(save_path, dpi=500)
    plt.close()


def draw_changed_standby_permanent(granularity, removed_list, activating_list, save_path):
    degrees = [i * granularity for i in range(0, math.floor(360 / granularity) + 1)]

    fig = plt.figure(figsize=(5, 3), layout='constrained')

    removed_line, = plt.plot(degrees, removed_list, marker=markers[0], markersize=4, c=colors[0],
                             label=f'Removed Standby FLSs')
    activating_line, = plt.plot(degrees, activating_list, marker=markers[1], markersize=4, c=colors[1],
                                label=f'Activated Standby FLSs')

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_title('Number of Standby FLSs', loc='left')
    ax.set_xlabel("User's View Angle ($^\circ$)", loc='right', fontsize="large")
    ax.set_xlim(left=0, right=365)
    plt.xticks(np.arange(0, 360 + granularity, step=max(granularity, 20)))
    # ax.set_ylim(0, 40)

    # plt.text(6, 48, 'With Priority Queue', color=pri_line.get_color(), fontweight='bold', zorder=3)
    #
    # plt.text(6, 54, 'No Priority Queue', color=nopri_line.get_color(), fontweight='bold', zorder=3)

    # Add legend
    ax.legend()
    # plt.show(dpi=500)
    plt.savefig(save_path, dpi=500)
    plt.close()


def dissolve(figure_path, file_path, ptcld_folder, granularity, shape, speed, ratio, k):
    """
    Implements dissolve technique of Section 6.2
    """
    print(f"Dissolve: {shape}, K:{k}, Q:{ratio}")

    max_speed = max_acceleration = max_deceleration = speed

    standbys, boundary, dispatcher = get_shape_info(file_path, ptcld_folder, shape, ratio)

    obstructing_list = read_bools_from_file(
        f'{file_path}/points/{shape}_{granularity}_{0}.txt')

    standby_list = [False for _ in obstructing_list]

    removed_list = []
    activating_list = []
    cumulative_removed_list = []
    cumulative_removed = 0

    mtids_change_percentage = []

    dists = get_recover_distance(standbys, shape, k, ptcld_folder, ratio, standby_list, dispatcher)
    mtids = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in dists]
    ori_mtid = statistics.mean(mtids)

    avg_dist_traveled = []
    prev_obstruting = []

    avg_MTID = []

    for i in range(0, math.floor(360 / granularity) + 1):
        index = i % math.floor(360 / granularity)
        obstructing_list = read_bools_from_file(f'{file_path}/points/{shape}_{granularity}_{index}.txt')

        dist_traveled = []
        removed = activating = difference_counter = 0

        for j in range(0, len(obstructing_list)):
            if obstructing_list[j] and not standby_list[j]:
                removed += 1
                standby_list[j] = True
                cumulative_removed += 1
                dist_traveled.append(distance_point_to_line(standbys[j], dispatcher))
            elif not obstructing_list[j] and not standby_list[j]:
                activating += 1
            elif i > 0 and obstructing_list[j] and standby_list[j] and not prev_obstruting[j]:
                difference_counter += 1

        prev_obstruting = obstructing_list

        removed_list.append(removed)
        activating_list.append(activating)
        cumulative_removed_list.append(cumulative_removed)

        avg_dist_traveled.append(statistics.mean(dist_traveled) if len(dist_traveled) > 0 else 0)

        # if i < 5:
        #     print(f"Removed: {removed}, Difference: {difference_counter}")
        #     print(statistics.mean(dist_traveled) if len(dist_traveled) > 0 else 0)

        dists = get_recover_distance(standbys, shape, k, ptcld_folder, ratio, standby_list, dispatcher)

        mtids = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in dists]

        avg_MTID.append(statistics.mean(mtids))

        mtids_change_percentage.append((statistics.mean(mtids) - ori_mtid) / ori_mtid)

    if not os.path.exists(f"{figure_path}/Dissolve"):
        os.makedirs(f"{figure_path}/Dissolve", exist_ok=True)

    draw_changed_standby_permanent(granularity, removed_list, activating_list,
                                   f"{figure_path}/Dissolve/{shape}_Q{ratio}_G{k}_GQ{granularity}.png")
    print(
        f"Shape:{shape}, R:{ratio}, G:{file_path[-1]}, Dissolved Percentage:{sum(removed_list) / len(standby_list) * 100}")

    return cumulative_removed_list, len(standby_list), mtids_change_percentage, avg_dist_traveled, avg_MTID, ori_mtid


def suspend_hangar(figure_path, file_path, ptcld_folder, granularity, shape, speed, ratio, G):
    """
    Implements suspend (move to hangar) technique of Section 6.3
    """
    print(f"Suspend: {shape}, G:{G}, Q:{ratio}")
    max_speed = max_acceleration = max_deceleration = speed

    standbys, boundary, dispatcher = get_shape_info(file_path, ptcld_folder, shape, ratio)

    obstructing_list = read_bools_from_file(
        f'{file_path}/points/{shape}_{granularity}_{0}.txt')

    standby_list = [False for _ in obstructing_list]

    restored_list = []
    removed_list = []
    activating_list = []
    mtids_change_percentage = []

    avg_remove_dist = []
    avg_restore_dist = []

    dists = get_recover_distance(standbys, shape, G, ptcld_folder, ratio, standby_list, dispatcher)
    mtids = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in dists]
    ori_mtid = statistics.mean(mtids)

    avg_MTID = []

    for i in range(0, math.floor(360 / granularity) + 1):
        index = i % math.floor(360 / granularity)
        obstructing_list = read_bools_from_file(f'{file_path}/points/{shape}_{granularity}_{index}.txt')

        remove_dist, restore_dist = [], []

        restored = removed = activating = 0

        for j in range(0, len(obstructing_list)):
            if obstructing_list[j] and not standby_list[j]:
                removed += 1
                remove_dist.append(distance_point_to_line(standbys[j], dispatcher))
            elif not obstructing_list[j] and standby_list[j]:
                restored += 1
                activating += 1
                restore_dist.append(distance_point_to_line(standbys[j], dispatcher))
            elif not obstructing_list[j]:  # and not standby_list[j]:
                activating += 1

        restored_list.append(restored)
        removed_list.append(removed)
        activating_list.append(activating)
        standby_list = obstructing_list

        avg_remove_dist.append(statistics.mean(remove_dist) if len(remove_dist) > 0 else 0)
        avg_restore_dist.append(statistics.mean(restore_dist) if len(restore_dist) > 0 else 0)

        # if i < 5:
        #     print(f"Removed: {removed}, Restored: {restored}")
        #     print(statistics.mean(remove_dist) if len(remove_dist) > 0 else 0)

        dists = get_recover_distance(standbys, shape, G, ptcld_folder, ratio, standby_list, dispatcher)
        mtids = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in dists]

        mtids_change_percentage.append((statistics.mean(mtids) - ori_mtid) / ori_mtid)
        avg_MTID.append(statistics.mean(mtids))

    if not os.path.exists(f"{figure_path}/Suspend"):
        os.makedirs(f"{figure_path}/Suspend", exist_ok=True)

    draw_changed_standby(granularity, restored_list, removed_list, activating_list,
                         f"{figure_path}/Suspend/{shape}_Q{ratio}_G{G}_GQ{granularity}.png")

    return removed_list, len(
        standby_list), mtids_change_percentage, avg_remove_dist, avg_restore_dist, avg_MTID, ori_mtid


def transpose(file_path, ptcld_folder, granularity, shape, speed, ratio, G, solve_obstruction=True):
    """
    Implements transpose technique of Section 6.1
    """
    max_speed = max_acceleration = max_deceleration = speed

    standbys, boundary, dispatcher = get_shape_info(file_path, ptcld_folder, shape, ratio)

    obstructing_list = read_bools_from_file(
        f'{file_path}/points/{shape}_{granularity}_{0}.txt')

    standby_list = [False for _ in obstructing_list]

    restored_list = []
    removed_list = []
    activating_list = []
    mtids_change_percentage = []
    avg_mtids = []

    dists = get_recover_distance_transpose(shape, G, ptcld_folder, ratio, standbys)
    mtids = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in dists]
    ori_mtid = statistics.mean(mtids)

    avg_remove_dist = []
    avg_restore_dist = []
    avg_MTID = []

    user_shifting = 100
    user_pos = [boundary[0][0] / 2 + boundary[1][0] / 2, boundary[0][1] - user_shifting,
                boundary[0][2] / 2 + boundary[1][2] / 2]
    shape_center = [boundary[0][0] / 2 + boundary[1][0] / 2, boundary[0][1] / 2 + boundary[1][1] / 2,
                    boundary[0][2] / 2 + boundary[1][2] / 2]
    vector = np.array(user_pos) - np.array(shape_center)

    for i in range(0, math.floor(360 / granularity) + 1):
        index = i % math.floor(360 / granularity)
        obstructing_list = read_bools_from_file(f'{file_path}/points/{shape}_{granularity}_{index}.txt')

        if solve_obstruction:
            angle = i * granularity
            user_pos = shape_center + rotate_vector(vector, angle)
            solve_single_view(shape, G, ratio, f"{granularity}_{index}", "", user_pos, ptcld_folder, file_path,
                              test=False, file_surfix="moved_standby")

        remove_dist = []
        restore_dist = []
        avg_dists = []

        none_obstruct_standby = read_coordinates(f"{file_path}/points/{shape}_{granularity}_{index}_moved_standby.txt",
                                                 ' ', 1)
        none_obstruct_standby = none_obstruct_standby[:, 0:3]

        restored = removed = activating = 0

        for j in range(0, len(obstructing_list)):
            if obstructing_list[j] and not standby_list[j]:
                removed += 1
                remove_dist.append(get_distance(standbys[j], none_obstruct_standby[j]))
            elif not obstructing_list[j] and standby_list[j]:
                restored += 1
                activating += 1
                restore_dist.append(get_distance(standbys[j], none_obstruct_standby[j]))
            elif not obstructing_list[j]:
                activating += 1

        restored_list.append(restored)
        removed_list.append(removed)
        activating_list.append(activating)
        standby_list = obstructing_list

        avg_remove_dist.append(statistics.mean(remove_dist) if len(remove_dist) > 0 else 0)
        avg_restore_dist.append(statistics.mean(restore_dist) if len(restore_dist) > 0 else 0)

        dists = get_recover_distance_transpose(shape, G, ptcld_folder, ratio, none_obstruct_standby)

        mtids = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in dists]
        avg_MTID.append(statistics.mean(mtids))

        mtids_change_percentage.append((statistics.mean(mtids) - ori_mtid) / ori_mtid)
        avg_mtids.append(statistics.mean(mtids))
        avg_dists.append(statistics.mean(dists))

    return removed_list, len(
        standby_list), mtids_change_percentage, avg_remove_dist, avg_restore_dist, avg_mtids, avg_MTID, avg_dists


def suspend_hide_in_closest_illuminating_fls(file_path, ptcld_folder, granularity, shape, speed, ratio, G,
                                             solve_obstruction=True):
    """
    Implements suspend:hide (hide in the closest illuminating FLS) technique of Section 6.3
    """
    if ratio < 3:
        return [], 0, [], [], [], [], []

    max_speed = max_acceleration = max_deceleration = speed

    standbys, boundary, dispatcher = get_shape_info(file_path, ptcld_folder, shape, ratio)

    obstructing_list = read_bools_from_file(
        f'{file_path}/points/{shape}_{granularity}_{0}.txt')

    standby_list = [False for _ in obstructing_list]

    restored_list = []
    removed_list = []
    activating_list = []
    mtids_change_percentage = []
    avg_mtids = []
    avg_dists = []

    dists = get_recover_distance_transpose(shape, G, ptcld_folder, ratio, standbys)
    mtids = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in dists]
    ori_mtid = statistics.mean(mtids)

    avg_remove_dist = []
    avg_restore_dist = []

    if solve_obstruction:
        hide_in_closest_illuminating_fls(ptcld_folder, meta_dir, ratio, G, shape, granularity)

    none_obstruct_standby = read_coordinates(f"{file_path}/points/{shape}_{granularity}_hide_standby.txt", ' ', 1)
    none_obstruct_standby = none_obstruct_standby[:, 0:3]

    avg_MTID = []

    for i in range(0, math.floor(360 / granularity) + 1):
        index = i % math.floor(360 / granularity)
        obstructing_list = read_bools_from_file(f'{file_path}/points/{shape}_{granularity}_{index}.txt')

        remove_dist = []
        restore_dist = []

        restored = removed = activating = 0

        for j in range(0, len(obstructing_list)):
            if obstructing_list[j] and not standby_list[j]:
                removed += 1
                remove_dist.append(get_distance(standbys[j], none_obstruct_standby[j]))
            elif not obstructing_list[j] and standby_list[j]:
                restored += 1
                activating += 1
                restore_dist.append(get_distance(standbys[j], none_obstruct_standby[j]))
            elif not obstructing_list[j]:
                activating += 1

        restored_list.append(restored)
        removed_list.append(removed)
        activating_list.append(activating)
        standby_list = obstructing_list

        avg_remove_dist.append(statistics.mean(remove_dist) if len(remove_dist) > 0 else 0)
        avg_restore_dist.append(statistics.mean(restore_dist) if len(restore_dist) > 0 else 0)

        dists = get_recover_distance_hide(standbys, obstructing_list, shape, G, ptcld_folder, ratio,
                                          none_obstruct_standby)

        mtids = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in dists]

        avg_MTID.append(statistics.mean(mtids))

        mtids_change_percentage.append((statistics.mean(mtids) - ori_mtid) / ori_mtid)
        avg_mtids.append(statistics.mean(mtids))
        avg_dists.append(statistics.mean(dists))

    return removed_list, len(
        standby_list), mtids_change_percentage, avg_remove_dist, avg_restore_dist, avg_mtids, avg_dists


def suspend_hide_in_obstructed_illuminating_fls(file_path, ptcld_folder, granularity, shape, speed, ratio, G,
                                                solve_obstruction=True):
    """
    Implements suspend:hide (hide in the obstructed illuminating FLS)
    """
    if ratio < 3:
        return [], 0, [], [], [], [], []

    max_speed = max_acceleration = max_deceleration = speed

    standbys, boundary, dispatcher = get_shape_info(file_path, ptcld_folder, shape, ratio)

    obstructing_list = read_bools_from_file(
        f'{file_path}/points/{shape}_{granularity}_{0}.txt')

    standby_list = [False for _ in obstructing_list]

    restored_list = []
    removed_list = []
    activating_list = []
    mtids_change_percentage = []
    avg_mtids = []
    avg_dists = []

    dists = get_recover_distance_transpose(shape, G, ptcld_folder, ratio, standbys)
    mtids = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in dists]
    ori_mtid = statistics.mean(mtids)

    avg_remove_dist = []
    avg_restore_dist = []

    if solve_obstruction:
        hide_in_obstructed_fls(ptcld_folder, meta_dir, ratio, G, shape, granularity)

    # none_obstruct_standby = read_coordinates(f"{file_path}/points/{shape}_{granularity}_hide_standby.txt", ' ', 1)
    # none_obstruct_standby = none_obstruct_standby[:, 0:3]

    avg_MTID = []

    none_obstruct_standby = {}
    for i in range(0, math.floor(360 / granularity) + 1):
        index = i % math.floor(360 / granularity)
        obstructing_list = read_bools_from_file(f'{file_path}/points/{shape}_{granularity}_{index}.txt')
        obstructed_fls_coords = np.loadtxt(f'{file_path}/points/{shape}_{granularity}_{index}_blocked.txt', dtype=float,
                                           delimiter=' ')
        obstructing_fls_coords = np.loadtxt(f'{file_path}/points/{shape}_{granularity}_{index}_blocking.txt', dtype=float,
                                           delimiter=' ')
        remove_dist = []
        restore_dist = []

        restored = removed = activating = 0

        for j in range(0, len(obstructing_list)):
            if obstructing_list[j] and not standby_list[j]:
                removed += 1
                standby_index = np.where(np.all(np.isclose(obstructing_fls_coords, standbys[j]), axis=1))[0]
                none_obstruct_standby[j] = obstructed_fls_coords[standby_index]
                remove_dist.append(get_distance(standbys[j], none_obstruct_standby[j]))
            elif not obstructing_list[j] and standby_list[j]:
                restored += 1
                activating += 1
                restore_dist.append(get_distance(standbys[j], none_obstruct_standby[j]))
            elif not obstructing_list[j]:
                activating += 1

        restored_list.append(restored)
        removed_list.append(removed)
        activating_list.append(activating)
        standby_list = obstructing_list

        avg_remove_dist.append(statistics.mean(remove_dist) if len(remove_dist) > 0 else 0)
        avg_restore_dist.append(statistics.mean(restore_dist) if len(restore_dist) > 0 else 0)

        dists = get_recover_distance_hide(standbys, obstructing_list, shape, G, ptcld_folder, ratio,
                                          none_obstruct_standby)

        mtids = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in dists]

        avg_MTID.append(statistics.mean(mtids))

        mtids_change_percentage.append((statistics.mean(mtids) - ori_mtid) / ori_mtid)
        avg_mtids.append(statistics.mean(mtids))
        avg_dists.append(statistics.mean(dists))

    return removed_list, len(
        standby_list), mtids_change_percentage, avg_remove_dist, avg_restore_dist, avg_mtids, avg_dists


if __name__ == "__main__":

    figure_path = "../assets/obstructing"
    if not os.path.exists(figure_path):
        os.makedirs(figure_path, exist_ok=True)

    ptcld_folder = "../assets/pointcloud"
    meta_dir = "../assets"

    # We assume that an FLS has a max velocity, acceleration and deceleration of {velocity_model}, and will react based on
    # the velocity model. (see './velocity.py')
    velocity_model = 6.11

    # We assume the user walk as a circle, centering the center of the shape.
    # Each time, the user will walk and the vector pointing from the center of the shape toward the user's eye will form
    # a {granularity} degree angle with the previous one.
    granularity_list = [10]  # the granularity of degree changes.

    Q_list = [1, 3, 5, 10]  # This is the list of Illumination cell to display cell ratio you would like to test.

    # Select these base on the group formation you have, see '../assets/pointclouds'
    # This is the size of group constructed by the group formation technique that you would like to test.
    G_list = [3]
    shape_list = ["skateboard", "dragon", "hat"]  # This is the list of shape to run this on

    for granularity in granularity_list:
        p_list = []

        for shape in shape_list:

            for G in G_list:

                suspend_info, dissolve_info, transpose_info, suspend_hide_info, suspend_hide_obstructed_info = [], [], [], [], []

                preloaded = False
                if os.path.exists(f"{figure_path}/{shape}/{shape}_K{G}_GR{granularity}_suspend_info.pkl"):
                    with open(f"{figure_path}/{shape}/{shape}_K{G}_GR{granularity}_suspend_info.pkl", 'rb') as file:
                        suspend_info = pickle.load(file)
                    with open(f"{figure_path}/{shape}/{shape}_K{G}_GR{granularity}_dissolve_info.pkl", 'rb') as file:
                        dissolve_info = pickle.load(file)
                    with open(f"{figure_path}/{shape}/{shape}_K{G}_GR{granularity}_transpose_info.pkl", 'rb') as file:
                        transpose_info = pickle.load(file)
                    with open(f"{figure_path}/{shape}/{shape}_K{G}_GR{granularity}_suspend_hide_info.pkl",
                              'rb') as file:
                        suspend_hide_info = pickle.load(file)
                    with open(f"{figure_path}/{shape}/{shape}_K{G}_GR{granularity}_suspend_hide_obstructed_info.pkl",
                              'rb') as file:
                        suspend_hide_obstructed_info = pickle.load(file)
                    preloaded = True
                for i, Q in enumerate(Q_list):
                    if not preloaded:
                        file_path = f"{meta_dir}/obstructing/Q{Q}/G{G}"

                        suspend_info.append(
                            suspend_hangar(figure_path, file_path, ptcld_folder, granularity, shape, velocity_model, Q, G))
                        dissolve_info.append(
                            dissolve(figure_path, file_path, ptcld_folder, granularity, shape, velocity_model, Q, G))
                        transpose_info.append(
                            transpose(file_path, ptcld_folder, granularity, shape, velocity_model, Q, G, True))

                        if Q >= 3:
                            suspend_hide_info.append(
                                suspend_hide_in_closest_illuminating_fls(file_path, ptcld_folder, granularity, shape, velocity_model, Q, G, True))

                            suspend_hide_obstructed_info.append(
                                suspend_hide_in_obstructed_illuminating_fls(file_path, ptcld_folder, granularity, shape,
                                                                            velocity_model, Q, G, True))

                    if Q >= 3:
                        suspend_hide_mtid = suspend_hide_info[i-1][5]
                        suspend_hide_obstructed_mtid = suspend_hide_obstructed_info[i-1][5]
                    else:
                        suspend_hide_mtid = []
                        suspend_hide_obstructed_mtid = []
                    ori_mtid = suspend_info[i][6]
                    suspend_mtid = suspend_info[i][5]
                    dissolve_mtid = dissolve_info[i][5]
                    transpose_mtid = transpose_info[i][5]

                    if not os.path.exists(f"{figure_path}/{shape}"):
                        os.makedirs(f"{figure_path}/{shape}", exist_ok=True)
                    draw_MTID(granularity, ori_mtid, transpose_mtid, suspend_hide_mtid,
                              f"{figure_path}/{shape}/{shape}_K{G}_Q{Q}_GR{granularity}_MTID_CMP.png")
                draw_change_plot(figure_path, 'Suspend', 'Suspended', suspend_info, 'suspend')
                draw_change_plot(figure_path, 'Dissolve', 'Dissolved', dissolve_info, 'dissolve')
                draw_change_plot(figure_path, 'Transpose', 'Transposed', transpose_info, 'transpose')
                draw_change_plot(figure_path, 'Suspend-Hide', 'Suspend-Hide', suspend_hide_info, 'suspend_hide')
                draw_change_plot(figure_path, 'Suspend-Hide-Obstructed', 'Suspend-Hide-Obstructed',
                                 suspend_hide_obstructed_info, 'suspend_hide_obstructed')

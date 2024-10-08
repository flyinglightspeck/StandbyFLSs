from solve_obstruction import *
import matplotlib as mpl

from utils.distance_point_to_line import distance_point_to_line

mpl.rcParams['font.family'] = 'Times New Roman'


def get_dist_to_dispatcher(dispatcher, shape, k, file_folder, ratio):
    input_file = f"{shape}_G{k}.xlsx"

    groups = read_cliques_xlsx(f"{file_folder}/{input_file}", ratio)

    dists = []

    for i, group in enumerate(groups):
        distances = [distance_point_to_line(coord, dispatcher) for coord in group]
        dists.append(np.mean(distances))

    return dists


def draw_dispatcher_standby_MTID(MTID_info, output_info, left=0, right=100, bottom=0, top=100):
    # output_info: save_path, shape, ratio, group_size, speed, ratio

    fig = plt.figure(figsize=(5, 3), layout='constrained')
    ori_standby_line, = plt.plot(MTID_info[0], MTID_info[1], marker='o', markersize=4,
                                 label=f'MTID with Original Standby', linewidth=0.5)

    new_standby_line, = plt.plot(MTID_info[0], MTID_info[2], marker='s', markersize=4, label=f'MTID with Moved Standby', linewidth=0.5)

    dispatcher_line, = plt.plot(MTID_info[0], MTID_info[3], marker='x', markersize=4, label=f'MTID with Dispatcher')

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_title('MTID (Second)', loc='left')
    ax.set_xlabel('Distance From Group To Dispatcher (Display Cells)', loc='right', fontsize="large")
    ax.set_xlim(left=left, right=right)
    ax.set_ylim(bottom=bottom, top=top)

    # plt.text(6, 48, 'With Priority Queue', color=pri_line.get_color(), fontweight='bold', zorder=3)
    #
    # plt.text(6, 54, 'No Priority Queue', color=nopri_line.get_color(), fontweight='bold', zorder=3)

    # Add legend
    ax.legend()
    # plt.show(dpi=500)
    plt.savefig(f"{output_info[0]}/{output_info[1]}_Q{output_info[2]}_G{output_info[3]}_S{int(output_info[4])}.png",
                dpi=400)
    plt.close()


def zip_and_sort(dists_to_dispatcher, standby_MTID, new_standby_MTID, dispatcher_MTID):
    # Pair elements from both lists
    paired_list = list(zip(dists_to_dispatcher, standby_MTID, new_standby_MTID, dispatcher_MTID))

    # Sort the paired list based on the elements from the first list
    sorted_paired_list = sorted(paired_list, key=lambda x: x[0])

    return np.transpose(sorted_paired_list)


def cmp_standby_dispatcher(ratio, ptcld_folder, file_path, move_back_path, txt_file, standby_file, speed):
    max_speed = max_acceleration = max_deceleration = speed

    points, boundary, standbys = get_points_from_file(ratio, ptcld_folder, file_path, txt_file, standby_file)

    new_standby_file = f"{shape}_back_standby.txt"
    _, _, new_standbys = get_points_from_file(ratio, ptcld_folder, move_back_path, txt_file, new_standby_file)

    dispatcher = []
    dispatcher.append([boundary[0][0], boundary[0][1], 0])
    dispatcher.append([boundary[1][0], boundary[0][1], 0])

    ori_dists_center = get_dist_to_centroid(standbys[:, 0:3], shape, k, ptcld_folder, ratio)
    new_dists_center = get_dist_to_centroid(new_standbys[:, 0:3], shape, k, ptcld_folder, ratio)
    dists_to_dispatcher = get_dist_to_dispatcher(dispatcher, shape, k, ptcloud_folder, ratio)

    standby_MTID = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in ori_dists_center]

    new_standby_MTID = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in
                        new_dists_center]

    dispatcher_MTID = [calculate_travel_time(max_speed, max_acceleration, max_deceleration, d) for d in
                       dists_to_dispatcher]

    return zip_and_sort(dists_to_dispatcher, standby_MTID, new_standby_MTID, dispatcher_MTID)


if __name__ == "__main__":
    np.random.seed(10)

    ptcloud_folder = "../assets/pointcloud"
    meta_dir = "../assets"

    top_map = {1: 40, 3: 50, 10: 160}

    for ratio in [1, 3, 10]:

        for k in [3, 20]:

            for shape in ["skateboard", "dragon", "hat"]:
                file_path = f"{meta_dir}/obstructing/Q{ratio}/G{k}"
                move_back_path = f"{meta_dir}/obstructing/Q{ratio}/G{k}"
                txt_file = f"{shape}.txt"
                standby_file = f"{shape}_standby.txt"

                for speed in [6.11]:
                    MTID_info = cmp_standby_dispatcher(ratio, ptcloud_folder, file_path, move_back_path, txt_file,
                                                       standby_file, speed)

                    slops = []
                    for i, _ in enumerate(MTID_info[0]):
                        if i == 0:
                            continue
                        if (MTID_info[0][i] - MTID_info[0][i - 1]) > 0:
                            slops.append((MTID_info[3][i] - MTID_info[3][i - 1]) / (
                                    MTID_info[0][i] - MTID_info[0][i - 1]))
                    print(f"{shape}, slop: {statistics.mean(slops)}")

                    output_info = [meta_dir, shape, ratio, k, speed, ratio]
                    draw_dispatcher_standby_MTID(MTID_info, output_info, top=top_map[ratio], right=ratio * 100)


from collections import Counter
import matplotlib as mpl
from detect_obstruction import *


def prevent_obstructions(ptcld_folder, meta_dir, ratio, G, shape, granularity, obstructing_maps=None):
    output_path = f"{meta_dir}/obstructing/Q{ratio}/G{G}"

    txt_file = f"{shape}.txt"
    standby_file = f"{shape}_standby.txt"

    try:
        _, boundary, standbys = get_points_from_file(ratio, ptcld_folder, output_path, txt_file, standby_file)
    except Exception as e:
        _, boundary, standbys, _ = get_points(shape, G, ptcld_folder, ratio)

    points = read_coordinates(f"{ptcld_folder}/{txt_file}", ' ')
    points = np.array(points)
    points = points * ratio


    if obstructing_maps:
        combined_obstruction_map = np.sum(obstructing_maps.values())
    else:
        combined_obstruction_map = read_obstruction_maps(output_path, shape, granularity)

    print(sum(combined_obstruction_map))
    # return
    standbys = standbys[:, :3]
    # get the indices of the elements that are non-zero
    obs_idx = np.nonzero(combined_obstruction_map)
    obs_stb_coords = standbys[obs_idx]

    if ratio >= 3:
        closest_ill_coords = closest_points(standbys, points[:, :3])
        new_obs_stb_coords = closest_ill_coords + np.array([0, 0, -1])
        # print(new_obs_stb_coords)
        # return
        # print(standbys)
        # standbys[list(obs_idx)] = new_obs_stb_coords
        standbys = new_obs_stb_coords
        # print(standbys)

        move_back_path = f"{meta_dir}/obstructing/Q{ratio}/G{G}"

        if not os.path.exists(f"{move_back_path}/points"):
            os.makedirs(f"{move_back_path}/points", exist_ok=True)

        np.savetxt(f'{move_back_path}/points/{shape}_back_standby.txt', standbys, fmt='%d', delimiter=' ')


if __name__ == "__main__":
    mpl.use('macosx')

    ptcld_folder = "../assets/pointcloud"
    meta_dir = "../assets"

    # We assume the user walk as a circle, centering the center of the shape.
    # Each time, the user will walk and the vector pointing from the center of the shape toward the user's eye will form
    # a {granularity} degree angle with the previous one.
    granularity = 10  # the granularity of degree changes.

    Q_list = [1, 3, 5, 10]  # This is the list of Illumination cell to display cell ratio you would like to test.


    # Select these base on the group formation you have, see '../assets/pointclouds'
    G_list = [3, 20]  # This is the size of group constructed by the group formation technique that you would like to test.
    shape_list = ["skateboard", "dragon", "hat"]  # This is the list of shape to run this on


    for illum_to_disp_ratio in Q_list:
        for G in G_list:
            for shape in shape_list:
                prevent_obstructions(ptcld_folder, meta_dir, illum_to_disp_ratio, G, shape, granularity)
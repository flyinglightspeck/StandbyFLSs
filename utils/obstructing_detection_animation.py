from functools import partial

from find_obstructing_raybox import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import matplotlib as mpl

from obstructing_detecting import rotate_vector
from worker.metrics import TimelineEvents
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D


def generate_animation(ptcld_folder, meta_direc, ratio, k, shape, granularity):
    output_path = f"{meta_direc}/obstructing/R{ratio}/K{k}"

    txt_file = f"{shape}.txt"
    standby_file = f"{shape}_standby.txt"
    standby_points = read_coordinates(f"{output_path}/points/{standby_file}", ' ', 1)

    illum_points = read_coordinates(f"{ptcld_folder}/{txt_file}", ' ')
    illum_points = np.array(illum_points) * ratio

    boundary = [
        [min(illum_points[:, 0]), min(illum_points[:, 1]), min(illum_points[:, 2])],
        [max(illum_points[:, 0]), max(illum_points[:, 1]), max(illum_points[:, 2])]
    ]
    fig, ax, user, fov = creat_figure()

    draw_shape(fig, ax, illum_points, standby_points, ratio)

    fps = 30

    duration = 1

    generate_video(fig, ax, user, fov, fps, boundary, granularity, duration)


def creat_figure():

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    user, = ax.plot([], [], [], 'ro', alpha=0)

    line1, = ax.plot([], [], [], lw=3)
    line2, = ax.plot([], [], [], lw=3)

    fov = [line1, line2]

    return fig, ax, user, fov


def draw_shape(fig, ax, illum_points, standby_points, Q):

    x_data = [point[0] for point in standby_points]
    y_data = [point[1] for point in standby_points]
    z_data = [point[2] for point in standby_points]

    ax.scatter(x_data, y_data, z_data, c="#929591", s=1, alpha=1)

    x_data = [point[0] for point in illum_points]
    y_data = [point[1] for point in illum_points]
    z_data = [point[2] for point in illum_points]

    ax.scatter(x_data, y_data, z_data, c='blue', s=Q, alpha=1)

    # ax.view_init(elev=90, azim=-90)
    # ax.grid(False)
    #
    # ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    # ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    # ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    # ax.set_xticks([])
    # ax.set_yticks([])
    # ax.set_zticks([])
    # ax.xaxis.line.set_visible(False)
    # ax.yaxis.line.set_visible(False)
    # ax.zaxis.line.set_visible(False)
    # plt.show()


def init(ax):
    ax.view_init(elev=90, azim=-90)
    ax.grid(False)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.xaxis.line.set_visible(False)
    ax.yaxis.line.set_visible(False)
    ax.zaxis.line.set_visible(False)

def update(frame, ax, dot, fov, boundary, granularity):

    user_shifting = 100

    shape_center = [boundary[0][0] / 2 + boundary[1][0] / 2, boundary[0][1] / 2 + boundary[1][1] / 2,
                    boundary[0][2] / 2 + boundary[1][2] / 2]
    user_pos = [boundary[0][0] / 2 + boundary[1][0] / 2, boundary[0][1] - user_shifting,
                boundary[0][2] / 2 + boundary[1][2] / 2]
    vector = np.array(user_pos) - np.array(shape_center)

    angle = frame * granularity

    user_pos = shape_center + rotate_vector(vector, angle)

    dot.set_data(user_pos[0:2])
    dot.set_3d_properties(user_pos[2])
    # dot.set_color(new_color)
    plt.draw()
    plt.pause(0.1)
    pass


def generate_video(fig, ax, user, fov, fps, boundary, granularity, duration):
    ani = FuncAnimation(
        fig, partial(update, ax=ax, fot=user, fov=fov, boundary=boundary, granularity=granularity),
        frames=fps * duration,
        init_func=partial(init, ax))

    writer = FFMpegWriter(fps=fps)
    # ani.save(f"{exp_dir}/{exp_name}.mp4", writer=writer)
    ani.save(f"../assets/obstructing_video.mp4", writer=writer)


if __name__ == "__main__":
    ptcld_folder = "../assets/pointcloud"
    meta_dir = "../assets"

    for ratio in [5]:
        for k in [3]:
            for shape in ["dragon"]:
                generate_animation(ptcld_folder, meta_dir, ratio, k, shape, 10)

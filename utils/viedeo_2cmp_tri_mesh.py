import itertools
import json
import math
from functools import partial

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
import matplotlib as mpl
from worker.metrics import TimelineEvents
from PIL import Image

ticks_gap = 20

start_time = 1800
duration = 60
fps = 30
frame_rate = 1 / fps
total_points = 760

output_name = "testd"
input_path = f"/Users/hamed/Desktop/{output_name}/bucket_face_G0_R90_T60_S6_PTrue.json"

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def mapping_face_to_surface(file):
    verts, faces = read_off(file)
    map = {}

    for face in faces:
        x, y, z = zip(*(verts[i] for i in face))
        center = tuple([sum(x)* 100 / len(face), sum(y)* 100 / len(face), sum(z)* 100 / len(face)])

        face_coord = [np.array(verts[i]) * 100 for i in face]
        map[center] = face_coord
    return map


def read_off(file_path, face_id=None):
    with open(file_path, 'r') as file:
        if 'OFF' != file.readline().strip():
            raise ValueError('Not a valid OFF file')

        n_verts, n_faces, _ = map(int, file.readline().strip().split(' '))
        vertices = [tuple(map(float, file.readline().strip().split(' '))) for _ in range(n_verts)]
        faces = [list(map(int, file.readline().strip().split(' ')[1:])) for _ in range(n_faces)]

        if face_id is not None:
            selected_faces = [faces[id] for id in face_id]
            faces = selected_faces

    return vertices, faces


def plot_off(ax, faces, c='white', a=1):
    mesh = Poly3DCollection([np.array([vertex for vertex in face]) for face in faces], color=c, alpha=a)

    # mesh.set_edgecolor('k')
    ax.add_collection3d(mesh)


def set_axis(ax, length, width, height, title=""):
    ax.axes.set_xlim3d(left=min(gtl[:, 0]), right=max(gtl[:, 0]))
    ax.axes.set_ylim3d(bottom=min(gtl[:, 1]), top=max(gtl[:, 1]))
    ax.axes.set_zlim3d(bottom=min(gtl[:, 2]), top=max(gtl[:, 2]))
    ax.set_aspect('equal')
    ax.grid(False)
    # ax.set_xticks(range(0, length + 1, ticks_gap))
    # ax.set_yticks(range(0, width + 1, ticks_gap))
    # ax.set_zticks(range(0, height + 1, ticks_gap))
    # ax.set_title(title, y=.9)


def set_wheel(ax):
    x_range = [12, 30]
    y_range = [20, 40]
    z_range = [30, 40]
    # ax.axes.set_xlim3d(left=min(gtl[:, 0]), right=max(gtl[:, 0]))
    # ax.axes.set_ylim3d(bottom=min(gtl[:, 1]), top=max(gtl[:, 1]))
    # ax.axes.set_zlim3d(bottom=min(gtl[:, 2]), top=max(gtl[:, 2]))

    ax.axes.set_xlim3d(left=x_range[0], right=x_range[1])
    ax.axes.set_ylim3d(bottom=y_range[0], top=y_range[1])
    ax.axes.set_ylim3d(bottom=z_range[0], top=z_range[1])
    ax.set_aspect('equal')
    ax.grid(False)


def set_axis_2d(ax, title):
    ax.axes.set_xlim(min(gtl[:, 0]), max(gtl[:, 0]))
    ax.axes.set_ylim(min(gtl[:, 1]), max(gtl[:, 1]))
    ax.set_aspect('equal')
    ax.grid(False)
    ax.axis('off')
    ax.set_title(title, y=-1, fontsize=20, color='white')


def update_title(ax, title, missing_flss):
    ax.set_title(f"Number of missing FLSs: {missing_flss}", y=0.9, fontsize=20, color='white')


def set_text_time(tx, t):
    tx.set(text=f"Elapsed time: {int(t)} seconds", fontsize=20, color='white')


def set_label(tx, label):
    tx.set(text=f"{label}", fontsize=30, color='white')


def draw_figure():
    px = 1 / plt.rcParams['figure.dpi']
    fig_width = 1920 * px
    fig_height = 1080 * px
    fig = plt.figure(figsize=(fig_width, fig_height), facecolor='black', edgecolor='black')
    # spec = fig.add_gridspec(4, 4, left=0.04, right=0.96, top=0.92, bottom=0.08)
    spec = fig.add_gridspec(2, 2)
    ax = fig.add_subplot(spec[0, 0], projection='3d', proj_type='ortho', facecolor='black')
    ax2 = fig.add_subplot(spec[0, 1], projection='3d', proj_type='ortho', facecolor='black')

    tx_K0 = fig.text(0.15, 0.88, s="", fontsize=20, color='white')
    tx_K3 = fig.text(0.05, 0.88, s="", fontsize=20, color='white')

    tx_left = fig.text(0.2, 0.5, s="", fontsize=20, color='white')
    tx_right = fig.text(0.7, 0.5, s="", fontsize=20, color='white')

    tx_title = fig.text(0.235, 0.03, s=f"The {shape} with {total_points} points, $\lambda$=900, Speed=6.11 m/sec",
                        fontsize=28, color='white')
    return fig, ax, ax2, tx_K0, tx_K3, tx_left, tx_right, tx_title


def read_point_cloud(input_path):
    with open(input_path) as f:
        events = json.load(f)

    height = 0
    width = 0
    length = 0
    filtered_events = []
    for e in events:
        if e[1] == TimelineEvents.FAIL and e[2] is False:
            filtered_events.append(e)
        elif e[1] == TimelineEvents.ILLUMINATE or e[1] == TimelineEvents.ILLUMINATE_STANDBY:
            filtered_events.append(e)
            length = max(int(e[2][0]), length)
            width = max(int(e[2][1]), width)
            height = max(int(e[2][2]), height)
    length = math.ceil(length / ticks_gap) * ticks_gap
    width = math.ceil(width / ticks_gap) * ticks_gap
    height = math.ceil(height / ticks_gap) * ticks_gap

    return filtered_events, length, width, height


def init(ax, ax2):
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0), alpha=0)
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0), alpha=0)
    ax.zaxis.set_pane_color((0, 0, 0, 0.025), alpha=0)
    ax.view_init(elev=14, azim=-136, roll=0)

    ax2.xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0), alpha=0)
    ax2.yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0), alpha=0)
    ax2.zaxis.set_pane_color((0, 0, 0, 0.025), alpha=0)
    ax2.view_init(elev=14, azim=-136, roll=0)


def update(frame, center_map, titles):
    t_K0 = start_time + frame * frame_rate
    t_K3 = start_time + frame * frame_rate
    while len(filtered_events_K0):
        # print(t)
        event_time = filtered_events_K0[0][0]
        if event_time <= t_K0:
            event = filtered_events_K0.pop(0)
            event_type = event[1]
            fls_id = event[-1]
            if event_type == TimelineEvents.ILLUMINATE or event_type == TimelineEvents.ILLUMINATE_STANDBY:
                points_K0[fls_id] = event[2]
            else:
                if fls_id in points_K0:
                    points_K0.pop(fls_id)
        else:
            t_K0 += frame_rate
            break
    coords_K0 = list(points_K0.values())
    ax.clear()

    faces = [center_map[tuple(center)] for center in coords_K0]

    plot_off(ax, faces)

    set_axis(ax, length, width, height)

    update_title(ax, titles[0], total_points - len(coords_K0))

    while len(filtered_events_K3):
        # print(t)
        event_time = filtered_events_K3[0][0]
        if event_time <= t_K3:
            event = filtered_events_K3.pop(0)
            event_type = event[1]
            fls_id = event[-1]
            if event_type == TimelineEvents.ILLUMINATE or event_type == TimelineEvents.ILLUMINATE_STANDBY:
                points_K3[fls_id] = event[2]
            else:
                if fls_id in points_K3:
                    points_K3.pop(fls_id)
        else:
            t_K3 += frame_rate
            break
    coords_K3 = points_K3.values()

    faces_2 = [center_map[center] for center in coords_K0]

    plot_off(ax2, faces_2)

    set_axis(ax2, length, width, height)
    update_title(ax2, titles[1], total_points - len(coords_K3))

    # plt.xlim(min(xs), max(xs))
    # plt.ylim(min(ys), max(ys))
    # plt.zlim(min(zs), max(zs))

    set_label(tx_left, "No Reliability Group")

    set_label(tx_right, "G=3")

    # return [ln, ln2, ln3, ln4]


def show_last_frame(events, t=30):
    final_points = dict()
    for event in events:
        event_time = event[0]
        if event_time > t:
            break
        event_type = event[1]
        fls_id = event[-1]
        if event_type == TimelineEvents.ILLUMINATE or event_type == TimelineEvents.ILLUMINATE_STANDBY:
            final_points[fls_id] = event[2]
        else:
            try:
                final_points.pop(fls_id)
            except Exception as e:
                continue

    coords = final_points.values()
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    zs = [c[2] for c in coords]

    return xs, ys, zs


def draw_last_frame(result_path, fig_name, end_time):
    input_path = result_path + "/bucket_face_G0_R90_T60_S6_PTrue.json"
    filtered_events, length, width, height = read_point_cloud(input_path)
    fig, ax, _ = draw_figure()
    init(ax)
    xs, ys, zs = show_last_frame(filtered_events, t=end_time)
    ax.scatter(xs, ys, zs, c='blue', s=2, alpha=1)
    set_axis(ax, length, width, height)
    plt.savefig(f"{result_path}/{fig_name}.png")
    plt.close()


def trim_png(image_path, output_path, trim_values):
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Get the dimensions of the image
            width, height = img.size

            # Calculate the new dimensions
            left = trim_values[0]
            top = trim_values[1]
            right = width - trim_values[2]
            bottom = height - trim_values[3]

            # Check if the trim values are valid
            if left >= right or top >= bottom:
                raise ValueError("Invalid trim values, resulting in non-positive width or height.")

            # Crop the image
            img_cropped = img.crop((left, top, right, bottom))

            # Save the cropped image
            img_cropped.save(output_path)

            print(f"The image has been trimmed and saved to {output_path}")
    except FileNotFoundError:
        print(f"The file at path {image_path} does not exist.")
    except ValueError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def read_coordinates(file_path):
    coordinates = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split the line by spaces and convert each part to a float
                coord = [float(x) for x in line.strip().split(' ')]
                if len(coord) == 3:  # Ensure that there are exactly 3 coordinates
                    coordinates.append(coord)
                else:
                    print(f"Invalid coordinate data on line: {line.strip()}")
        return coordinates
    except FileNotFoundError:
        print(f"The file at path {file_path} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred 5: {e}")
        return None


if __name__ == '__main__':
    shape = "bucket_face"
    start_time = 540
    mesh_file = f"../assets/pointcloud/{shape}.off"

    file_name_list = [[f"bucket_face_G0_R90_T60_S6_PTrue", f"bucket_face_G3_R90_T60_S6_PTrue"]]
    titles_list = [["No Standby", "G=3"]]
    video_name_list = ["bucket_face"]

    for i, file_names in enumerate(file_name_list):
        txt_file_path = f"../assets/pointcloud/{shape}.txt"
        gtl = read_coordinates(txt_file_path)
        gtl = np.array(gtl)
        print(f"Number of Points: {len(gtl)}")

        total_points = len(gtl)

        input_path_K0 = f"../assets/timelines/{file_names[0]}.json"
        filtered_events_K0, length, width, height = read_point_cloud(input_path_K0)

        input_path_K3 = f"../assets/timelines/{file_names[1]}.json"
        filtered_events_K3, length, width, height = read_point_cloud(input_path_K3)
        fig, ax, ax2, tx_K0, tx_K3, tx_left, tx_right, tx_title = draw_figure()
        points_K0 = dict()
        points_K3 = dict()

        center_map = mapping_face_to_surface(mesh_file)
        ani = FuncAnimation(
            fig, partial(update, center_map=center_map, titles=titles_list[i]),
            frames=fps * duration,
            init_func=partial(init, ax, ax2))
        #
        # plt.show()
        writer = FFMpegWriter(fps=fps)
        # ani.save(f"{exp_dir}/{exp_name}.mp4", writer=writer)
        ani.save(f"../assets/{video_name_list[i]}.mp4", writer=writer)

import numpy as np


def distance_point_to_line(point, line_points):
    point = np.array(point)
    line_point1 = np.array(line_points[0])
    line_point2 = np.array(line_points[1])

    AP = point - line_point1
    AB = line_point2 - line_point1

    # Calculate the cross product and its norm
    cross_product = np.cross(AP, AB)
    norm_cross = np.linalg.norm(cross_product)

    # Calculate the norm of AB
    norm_AB = np.linalg.norm(AB)

    # Calculate the distance
    distance = norm_cross / norm_AB

    return distance

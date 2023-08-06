import numpy as np
import pytransform3d.transformations as pt
from ..geometry import (
    convert_segment_to_line, convert_rectangle_to_vertices,
    convert_box_to_face)
from ._line_to_box import _line_to_box
from ._rectangle import rectangle_to_rectangle


def point_to_box(point, box2origin, size, origin2box=None, check=False):
    """Compute the shortest distance between point and box.

    Parameters
    ----------
    point : array, shape (3,)
        3D point.

    box2origin : array, shape (4, 4)
        Pose of the box.

    size : array, shape (3,)
        Size of the box along its axes.

    origin2box : array, shape (4, 4), optional (default: None)
        Transform from origin to box coordinates.

    check : bool, optional (default: True)
        Check if transformation matrix is valid before inversion.

    Returns
    -------
    dist : float
        The shortest between point and box.

    contact_point_box : array, shape (3,)
        Closest point on box.
    """
    if origin2box is None:
        origin2box = pt.invert_transform(box2origin, check=check)
    point_in_box = origin2box[:3, 3] + origin2box[:3, :3].dot(point)
    half_size = 0.5 * size
    contact_point_in_box = np.clip(point_in_box, -half_size, half_size)
    contact_point = box2origin[:3, 3] + box2origin[:3, :3].dot(contact_point_in_box)
    return np.linalg.norm(point - contact_point), contact_point


def line_to_box(line_point, line_direction, box2origin, size):
    """Compute the shortest distance between line and box.

    Parameters
    ----------
    line_point : array, shape (3,)
        Point on line.

    line_direction : array, shape (3,)
        Direction of the line. This is assumed to be of unit length.

    box2origin : array, shape (4, 4)
        Pose of the box.

    size : array, shape (3,)
        Size of the box along its axes.

    Returns
    -------
    dist : float
        The shortest between line and box.

    contact_point_line : array, shape (3,)
        Closest point on line.

    contact_point_box : array, shape (3,)
        Closest point on box.
    """
    return _line_to_box(line_point, line_direction, box2origin, size)[:3]


def line_segment_to_box(segment_start, segment_end, box2origin, size, origin2box=None):
    """Compute the shortest distance from line segment to box.

    Parameters
    ----------
    segment_start : array, shape (3,)
        Start point of segment.

    segment_end : array, shape (3,)
        End point of segment.

    box2origin : array, shape (4, 4)
        Pose of the box.

    size : array, shape (3,)
        Size of the box along its axes.

    origin2box : array, shape (4, 4), optional (default: None)
        Transform from origin to box coordinates.

    Returns
    -------
    distance : float
        The shortest distance between line segment and box.

    contact_point_line_segment : array, shape (3,)
        Closest point on line segment.

    contact_point_box : array, shape (3,)
        Closest point on box.
    """
    segment_direction, segment_length = convert_segment_to_line(
        segment_start, segment_end)

    distance, contact_point_segment, contact_point_box, t_closest = _line_to_box(
        segment_start, segment_direction, box2origin, size, origin2box=origin2box)

    if t_closest < 0:
        distance, contact_point_box = point_to_box(
            segment_start, box2origin, size, origin2box=origin2box)
        contact_point_segment = segment_start
    elif t_closest > segment_length:
        distance, contact_point_box = point_to_box(
            segment_end, box2origin, size, origin2box=origin2box)
        contact_point_segment = segment_end

    return distance, contact_point_segment, contact_point_box


def rectangle_to_box(rectangle_center, rectangle_axes, rectangle_lengths,
                     box2origin, size, epsilon=1e-6, origin2box=None):
    """Compute the shortest distance from rectangle to box.

    Parameters
    ----------
    rectangle_center : array, shape (3,)
        Center point of the rectangle.

    rectangle_axes : array, shape (2, 3)
        Each row is a vector of unit length, indicating the direction of one
        axis of the rectangle. Both vectors are orthogonal.

    rectangle_lengths : array, shape (2,)
        Lengths of the two sides of the rectangle.

    box2origin : array, shape (4, 4)
        Pose of the box.

    size : array, shape (3,)
        Size of the box along its axes.

    epsilon : float, optional (default: 1e-6)
        Values smaller than epsilon are considered to be 0.

    origin2box : array, shape (4, 4), optional (default: None)
        Transform from origin to box coordinates.

    Returns
    -------
    dist : float
        The shortest distance between rectangle and box.

    closest_point_rectangle : array, shape (3,)
        Closest point on the rectangle.

    closest_point_box : array, shape (3,)
        Closest point on the box.
    """
    overlap, result = _rectangle_points_in_box(
        rectangle_center, rectangle_axes, rectangle_lengths,
        box2origin, size, epsilon=epsilon, origin2box=origin2box)
    if overlap:
        return result
    return _rectangle_to_box_faces(
        rectangle_center, rectangle_axes, rectangle_lengths, box2origin, size,
        epsilon)


def _rectangle_points_in_box(
        rectangle_center, rectangle_axes, rectangle_lengths, box2origin, size,
        epsilon=1e-6, origin2box=None):
    rectangle_points = convert_rectangle_to_vertices(
        rectangle_center, rectangle_axes, rectangle_lengths)
    for i in range(len(rectangle_points)):
        dist, contact_point_box = point_to_box(
            rectangle_points[i], box2origin, size, origin2box=origin2box)
        if dist <= epsilon:
            return True, (dist, rectangle_points[i], contact_point_box)
    return False, None


def _rectangle_to_box_faces(
        rectangle_center, rectangle_axes, rectangle_lengths, box2origin, size,
        epsilon):
    best_distance = np.finfo(float).max
    for sign in [-1, 1]:
        for i in range(3):
            face_center, face_axes, face_lengths = convert_box_to_face(
                box2origin, size, i, sign)
            dist, closest_point_rectangle, closest_point_face = rectangle_to_rectangle(
                rectangle_center, rectangle_axes, rectangle_lengths,
                face_center, face_axes, face_lengths, epsilon)
            if dist < best_distance:
                best_distance = dist
                best_closest_point_rectangle = closest_point_rectangle
                best_closest_point_box = closest_point_face

                if best_distance <= epsilon:
                    break
    return best_distance, best_closest_point_rectangle, best_closest_point_box

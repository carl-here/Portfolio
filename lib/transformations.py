import numpy as np


def translate(x, y, z):
    return np.array([
        [1.0, 0.0, 0.0, x],
        [0.0, 1.0, 0.0, y],
        [0.0, 0.0, 1.0, z],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype=np.float64)


def scale(sx, sy, sz):
    """Return a 4x4 scaling matrix."""
    # Task 2
    # This is a placement matrix. Adjust this according to the task.
    return np.array([
        [sx,  0.0, 0.0, 0.0], #whatever number sx, sy or sz is will multiply the size
        [0.0, sy,  0.0, 0.0],
        [0.0, 0.0, sz,  0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype=np.float64)

def rotate_z(angle_radians):
    c = np.cos(angle_radians)
    s = np.sin(angle_radians)
    return np.array([
        [c, -s, 0.0, 0.0],
        [s,  c, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype=np.float64)

def rotate_x(angle_radians):
    # Task 3
    # This is a placement matrix. Adjust this according to the task.  
    c = np.cos(angle_radians)
    s = np.sin(angle_radians)
    
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0,   c,  -s, 0.0],
        [0.0,   s,   c, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype=np.float64)

def rotate_y(angle_radians):
    # Task 3
    # This is a placement matrix. Adjust this according to the task. 
    c = np.cos(angle_radians)
    s = np.sin(angle_radians)
    
    return np.array([
        [c, 0.0, -s, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [s, 0.0,   c, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype=np.float64)



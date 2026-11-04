import numpy as np
from .transformations import *
from pyglet.math import Mat4, Vec3
import math


class Camera:
    def __init__(self, width, height, fov, near, far):
        self.distance = 10
        self.theta = 0
        self.phi = 0

        self.width = width
        self.height = height
        self.fov = math.radians(fov)
        self.near = near
        self.far = far
        self.perspective: np.array = object
        self.view: np.array = object

    def get_position(self) -> Vec3:
        x = self.distance * np.cos(self.phi) * np.sin(self.theta)
        y = self.distance * np.sin(self.phi)
        z = self.distance * np.cos(self.phi) * np.cos(self.theta)

        return Vec3(x, y, z)

    def get_projection(self) -> Mat4:
        """Get the camera's projection matrix. Returns a 4x4 matrix"""
        # Translated from GLU's source code:
        # https://gitlab.freedesktop.org/mesa/glu/-/blob/master/src/libutil/project.c#L66
        half_fov = self.fov/2
        aspect = self.width/self.height
        delta_z = self.far - self.near
        sine = math.sin(half_fov)

        if delta_z == 0.0 or sine == 0.0 or aspect == 0.0:
            raise ValueError("Invalid perspective parameters")

        cotangent = math.cos(half_fov) / sine

        return Mat4(
            cotangent / aspect, 0, 0, 0,
            0, cotangent, 0, 0,
            0, 0, -(self.far + self.near) / delta_z, -1,
            0, 0, -(2.0 * self.near * self.far) / delta_z, 1,
        )
        
    def get_look_at(self) -> Mat4:
        eye = self.get_position()
        center = Vec3(0, 0, 0)  # looking at origin
        up = Vec3(0, 1, 0)
    
        # Compute the forward vector (z axis)
        f = (center - eye).normalize()
        # Compute the right vector (x axis)
        s = f.cross(up).normalize()
        # Compute the true up vector (y axis)
        u = s.cross(f)

        # Construct the lookAt matrix
        # Note: Mat4 constructor takes 16 values in column-major order, so be careful
        return Mat4(
            s.x,  u.x, -f.x, 0.0,
            s.y,  u.y, -f.y, 0.0,
            s.z,  u.z, -f.z, 0.0,
            -s.dot(eye), -u.dot(eye), f.dot(eye), 1.0
        )
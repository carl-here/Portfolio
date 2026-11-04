# Demo from Friday workshop on the 10th of April 2026.

import pyglet
import lib
from pyglet.gl import glEnable, GL_DEPTH_TEST
import numpy as np

# Window
# ------
window = pyglet.window.Window()
window.height = 720
window.width = 1280

# Rendering - Batch
# -----------------
batch = pyglet.graphics.Batch()

# Rendering - Other
# -----------------
glEnable(GL_DEPTH_TEST)

# Camera
# ------
camera = lib.Camera(width=window.width, height=window.height,
                    fov=60,
                    near=0.01, far=100.0)

# Global State
# ------------
# The global state ensures that the correct parameters and values are uploaded
# to the shader/GPU. We update the state in the draw function.
global_state = lib.GlobalState()

# Objects
# -------
# sphere = lib.Sphere(x=0.0, y=0.0, z=0.0,
#                     radius=5,
#                     color=(255, 0, 0, 255),
#                     batch=batch)

spaceship = lib.shapes.CustomModel(x=0, y=0, z=0,
                                   scale=1,
                                   batch=batch)

# Try to position the camera and/or the light source so we can see the spaceship
# easier
light_source_position = np.array([0, camera.y, 0])
# light_source_position[1] += 20


camera.x = 20

# Drawing
# -------
@window.event
def on_draw():
    window.clear()

    # Update the global state
    global_state.update(camera.get_position(), light_source_position)

    window.projection = camera.get_projection()
    window.view = camera.get_look_at()

    batch.draw()

pyglet.app.run()
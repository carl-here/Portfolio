import math
import random
import numpy as np
import pyglet
from pyglet.window import key
from pyglet.gl import (
    GL_DEPTH_TEST, glEnable, glPolygonMode, GL_FRONT_AND_BACK, GL_FILL, GL_LINE
)
import lib

# Window
window = pyglet.window.Window(1280, 720)
glEnable(GL_DEPTH_TEST)

# Shader + batches
shader = lib.create3DShader()
batch = pyglet.graphics.Batch()
ui_batch = pyglet.graphics.Batch()

# World grid
world_grid = lib.shapes.WorldGrid(batch)

# Gravity
GRAVITY = -9.81

# Camera
camera = lib.Camera(width=window.width, height=window.height,
                    fov=80,  # Measured in degrees
                    near=0.01, far=1000.0)

# Objects
size = 5
prism = lib.shapes.Prism3D(x=0, y=-size/2, z=0,
                           width=size, height=size, depth=size,
                           color=(190, 30, 160, 255),
                           program=shader)

# Camera position with spherical coordinates
camera.distance = 10
camera.phi = np.clip(camera.phi, 0.1, np.pi/2 - 0.1)
camera.theta = np.pi / 4


# Input
# -----
key_handler = key.KeyStateHandler()
window.push_handlers(key_handler)

# UI elements
font_size = 18
font_type = 'Times New Roman'

label = pyglet.text.Label(
    "Slider value: 0.0",
    font_name=font_type,
    font_size=font_size,
    x=30.0,
    y=600.0,
    anchor_x='left',
    anchor_y='center',
    batch=batch
)

slider = lib.widgets.Slider(
    x=150, y=660, 
    width=300, height=20,
    knob_width=40,
    knob_height=30,
    color=(249, 166, 253, 255),
    knob_color=(90, 90, 90, 255),
    starting_value=1.0,
    batch=batch
)
      
# Particle system
balls = []
spawn_interval = 1.0
time_since_last_spawn = 0.0


def random_unit_vector_3d():
    phi = random.uniform(0, 2 * math.pi)
    costheta = random.uniform(-1, 1)
    theta = math.acos(costheta)
    return np.array([
        math.sin(theta) * math.cos(phi),
        math.sin(theta) * math.sin(phi),
        math.cos(theta)
    ])


class Ball:
    def __init__(self, shape, x, y, z, vx, vy, vz, lifetime):
        self.shape = shape
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.lifetime = lifetime

def spawn_ball():
    r = random.uniform(0.2, 0.5)
    x, y, z = 0, 5, 0

    class UniqueGroup(pyglet.graphics.Group):
        pass

    group = UniqueGroup()

    circle = lib.Circle3D(
        x, y, z, r,
        segments=64, color=(224, 136, 206, 255),
        batch=batch, group=group, program=shader
    )

    speed = random.uniform(3, 5)
    vx, vy, vz = random_unit_vector_3d() * speed

    balls.append(Ball(circle, x, y, z, vx, vy, vz, lifetime=3.0))

# Input    
@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global camera

    min_distance = 1

    if camera.distance <= min_distance and scroll_y == 1:
        camera.distance = min_distance
    else:
        scroll_speed = -scroll_y
        camera.distance += scroll_speed
        
@window.event
def on_draw():
    window.clear()

    shader["u_projection"] = camera.get_projection()
    shader["u_view"] = camera.get_look_at()

    world_grid.shader["u_projection"] = camera.get_projection()
    world_grid.shader["u_view"] = camera.get_look_at()
    
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    batch.draw()
    
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    prism.draw()
    
def update(dt):
    global time_since_last_spawn, camera

    # Spawn balls
    time_since_last_spawn += dt
    if time_since_last_spawn >= spawn_interval:
        for _ in range(random.randint(5, 10)):
            spawn_ball()
        time_since_last_spawn = 0

    # ---- CAMERA MOVEMENT ----
    movement_step = 1.0 * dt

    if key_handler[key.D]:
        camera.theta += movement_step
    if key_handler[key.A]:
        camera.theta -= movement_step

    # Clamp vertical camera angle (optional)
    camera.phi = np.clip(camera.phi, 0.1, np.pi/2 - 0.1)

    # ---- UPDATE ALL BALLS ----
    for ball in balls[:]:

        # Lifetime
        ball.lifetime -= dt
        if ball.lifetime <= 0:
            ball.shape.delete()
            balls.remove(ball)
            continue

        # Gravity
        ball.vy += GRAVITY * dt

        # Damping
        damping = 0.98
        ball.vx *= damping
        ball.vy *= damping
        ball.vz *= damping

        # Position update
        ball.x += ball.vx * dt
        ball.y += ball.vy * dt
        ball.z += ball.vz * dt

        # Apply to mesh
        ball.shape.x = ball.x
        ball.shape.y = ball.y
        ball.shape.z = ball.z


pyglet.app.run()
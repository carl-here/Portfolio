import pyglet
from pyglet.gl import glEnable, GL_DEPTH_TEST
import lib
from lib.linalg import trilinear_interpolation
import math
import numpy as np
from pyglet.window import key
import icosphere

window = pyglet.window.Window()
window.width = 1280
window.height = 720

key_handler = key.KeyStateHandler()
window.push_handlers(key_handler)
glEnable(GL_DEPTH_TEST)

shapes_batch = pyglet.graphics.Batch()
batch = pyglet.graphics.Batch()

global_state = lib.GlobalState()

# Shaders
lit_shader = lib.create3DShader(enable_lighting=True)
flat_shader = lib.create3DShader(enable_lighting=False)

lib.shapes.shader = lit_shader

subdivision_frequency = 20
vertices, indices = icosphere.icosphere(subdivision_frequency)
indices = indices.flatten().tolist()
vertices = vertices.flatten().tolist()
num_of_vertices = len(vertices) // 3  # 3 floats per vertex (x, y, z

noise = []

frequency = 2.0   # controls continent size
amplitude = 1.0   # controls contrast

_GRADIENTS = np.array([
    [ 1,  1,  0], [-1,  1,  0],
    [ 1, -1,  0], [-1, -1,  0],
    [ 1,  0,  1], [-1,  0,  1],
    [ 1,  0, -1], [-1,  0, -1],
    [ 0,  1,  1], [ 0, -1,  1],
    [ 0,  1, -1], [ 0, -1, -1],
], dtype=float)

def _fade(t: float) -> float:
    """Perlin fade (smoothing) function"""
    return t * t * t * (t * (t * 6 - 15) + 10)


def _hash(ix: int, iy: int, iz: int) -> int:
    """Deterministic hash for lattice coordinates"""
    return (ix * 73856093 ^ iy * 19349663 ^ iz * 83492791) & 0xFFFFFFFF


def _gradient(ix: int, iy: int, iz: int) -> np.ndarray:
    """Select a gradient vector based on lattice hash"""
    return _GRADIENTS[_hash(ix, iy, iz) % len(_GRADIENTS)]


def _grad_dot(ix: int, iy: int, iz: int,
              x: float, y: float, z: float) -> float:
    """Dot product between gradient and distance vector"""
    g = _gradient(ix, iy, iz)
    return g[0] * (x - ix) + g[1] * (y - iy) + g[2] * (z - iz)


def _perlin_noise3(x: float, y: float, z: float) -> float:
    x0 = int(np.floor(x))
    y0 = int(np.floor(y))
    z0 = int(np.floor(z))

    x1 = x0 + 1
    y1 = y0 + 1
    z1 = z0 + 1

    tx = x - x0
    ty = y - y0
    tz = z - z0

    u = _fade(tx)
    v = _fade(ty)
    w = _fade(tz)

    c000 = _grad_dot(x0, y0, z0, x, y, z)
    c100 = _grad_dot(x1, y0, z0, x, y, z)
    c010 = _grad_dot(x0, y1, z0, x, y, z)
    c110 = _grad_dot(x1, y1, z0, x, y, z)
    c001 = _grad_dot(x0, y0, z1, x, y, z)
    c101 = _grad_dot(x1, y0, z1, x, y, z)
    c011 = _grad_dot(x0, y1, z1, x, y, z)
    c111 = _grad_dot(x1, y1, z1, x, y, z)

    return trilinear_interpolation(
        c000, c100, c010, c110,
        c001, c101, c011, c111,
        u, v, w
    )

def perlin(x: float, y: float, z: float,
           octaves: int = 4,
           lacunarity: float = 2.0,
           persistence: float = 0.5) -> float:
    """
    Fractal Brownian Motion (fBm) using Perlin noise.

    Parameters:
        x, y, z      : 3D coordinates
        octaves      : number of noise layers
        lacunarity   : frequency multiplier per octave
        persistence  : amplitude multiplier per octave

    Returns:
        float: normalized noise value in approximately [-1, 1]
    """

    value = 0.0
    amplitude = 1.0
    frequency = 1.0
    max_amplitude = 0.0

    for _ in range(octaves):
        value += amplitude * _perlin_noise3(
            x * frequency,
            y * frequency,
            z * frequency
        )

        max_amplitude += amplitude
        amplitude *= persistence
        frequency *= lacunarity

    return value / max_amplitude

noise = []

for i in range(num_of_vertices):
    x = vertices[3 * i]
    y = vertices[3 * i + 1]
    z = vertices[3 * i + 2]

    # Fractal Perlin noise (fBm)
    n = perlin(
        x, y, z,
        octaves=5,
        persistence=0.5,
        lacunarity=2.0
    )
    noise.append(n)


# 2. Normalize noise to [0, 1]
min_n = min(noise)
max_n = max(noise)

if max_n > min_n:
    noise = [(n - min_n) / (max_n - min_n) for n in noise]
else:
    # Fallback 
    noise = [0.5 for _ in noise]


# 3. Displace vertices using the noise
base_radius = 1.0     # original unit sphere
height_scale = 0.3   # terrain strength (increase to exaggerate)

for i in range(num_of_vertices):
    x = vertices[3 * i]
    y = vertices[3 * i + 1]
    z = vertices[3 * i + 2]

    # Current radius (≈ 1 for unit sphere)
    r = math.sqrt(x * x + y * y + z * z)

    # Radial displacement based on noise
    new_radius = base_radius + height_scale * noise[i]

    # Normalize direction and scale
    vertices[3 * i]     = x / r * new_radius
    vertices[3 * i + 1] = y / r * new_radius
    vertices[3 * i + 2] = z / r * new_radius


# Objects
the_sun = lib.Sphere(x=18, y=10, z=0,
                         radius=0.5,
                         color=(255, 50, 100, 255),
                         batch=shapes_batch)

world_grid = lib.WorldGrid(pyglet.graphics.Batch())

spaceship_model = lib.shapes.CustomModel(x=20.0, y=-23.0, z=0.0, 
                                         scale=3,
                                         filepath="data/spaceship.obj",
                                         batch=batch)

# Force flat (unlit) shader only for planet creation
lib.shapes.shader = flat_shader

planet = lib.shapes.Planet(
    x=-20, y=9, z=0,
    vertices=vertices,
    indices=indices,
    count=num_of_vertices,
    noise=noise,
    batch=shapes_batch
)

lib.shapes.shader = lit_shader
# Camera
camera = lib.Camera(width=window.width, height=window.height,
                    fov=80,
                    near=0.01, far=1000.0)

# Camera position with spherical coordinates
camera.distance = 27
camera.phi = np.pi / 2.4
camera.theta = 0

def random_unit_vector_3d():
    phi = np.random.uniform(0, 2 * math.pi)
    costheta = np.random.uniform(-1, 1)
    theta = math.acos(costheta)
    return np.array([
        math.sin(theta) * math.cos(phi),
        math.sin(theta) * math.sin(phi),
        math.cos(theta)
    ])

    
def on_update(dt: float):
    global camera, time_since_last_spawn

    movement_step = np.pi / 1.5 * dt
    if key_handler[key.W]:
        camera.phi += movement_step
    if key_handler[key.S]:
        camera.phi -= movement_step
    if key_handler[key.D]:
        camera.theta += movement_step
    if key_handler[key.A]:
        camera.theta -= movement_step
        
    spaceship_step = np.pi / 1.5 * dt
    if key_handler[key.UP]:
        spaceship_model.x += spaceship_step
    if key_handler[key.S]:
        spaceship_model.x -= spaceship_step
    if key_handler[key.D]:
        spaceship_model.y += spaceship_step
    if key_handler[key.A]:
        spaceship_model.y -= spaceship_step

    eps = 0.001
    camera.phi = max(eps, min(np.pi - eps, camera.phi))

    camera.x = camera.distance * np.sin(camera.phi) * np.cos(camera.theta)
    camera.y = camera.distance * np.cos(camera.phi)
    camera.z = camera.distance * np.sin(camera.phi) * np.sin(camera.theta)


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
    light_position = np.array([the_sun.x, the_sun.y, the_sun.z])
    #light_position = np.array([the_sun_big.x, the_sun_big.y, the_sun_big.z])
    
    # The global state needs the camera and the light position
    global_state.update(camera.get_position(), light_position)
    
    window.projection = camera.get_projection()
    window.view = camera.get_look_at()
    
    # Draw objects
    batch.draw()
    shapes_batch.draw()
    world_grid.draw()
    

pyglet.clock.schedule_interval(on_update, 1/60)
pyglet.app.run()
import pyglet
from pyglet.gl import glEnable, GL_DEPTH_TEST
import lib
import math
import numpy as np
from pyglet.window import key

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

# Gravity
G = 0.8
G_on = True

# Electromagnetism
EM_on = True

# Constant fields (must NOT be parallel)
E_field = np.array([0.0, 50.0, 0.0])   # Electric field (a storm)
B_field = np.array([0.0, 0.0, 5.0])   # Magnetic field makes it go weee around the z axis

# Objects
the_sun = lib.Sphere(x=18, y=10, z=0,
                         radius=0.5,
                         color=(255, 50, 100, 255),
                         batch=shapes_batch)

world_grid = lib.WorldGrid(pyglet.graphics.Batch())

spaceship_model = lib.shapes.CustomModel(x=20.0, y=-23.0, z=0.0, #I had a hard time placing the camera inside the bridge so the spaceship is a little wierdly placed.
                                         scale=3,
                                         filepath="data/spaceship.obj",
                                         batch=batch)


# Camera
camera = lib.Camera(width=window.width, height=window.height,
                    fov=80,
                    near=0.01, far=1000.0)

# Camera position with spherical coordinates
camera.distance = 27
camera.phi = np.pi / 2.4
camera.theta = 0

# Particle system
orbiting_balls = []
spawn_interval = 1.0
time_since_last_spawn = 0.0

def gravity_force(p1, p2):
    r = p1.x - p2.x
    softening = 0.3
    dist = np.linalg.norm(r) + softening
    return -G * p1.mass * p2.mass * r / dist**3

def lorentz_force(p):
    # F = q ( E + v × B )
    return p.charge * (E_field + np.cross(p.v, B_field))

#collision handler, normalizes (n) vectors,  geometric constrains, Newtons law of restitution, 
def resolve_collision(p1, p2, e=0.8):
    #r is the relative postion vector it comes from radius vector (Latin + geometry tradition), 
    #origin is from circles, but later we found that a position vector doesn't have to relate to a circle.
    r = p2.x - p1.x  
    dist = np.linalg.norm(r)

    min_dist = p1.radius + p2.radius #collision
    if dist == 0 or dist >= min_dist:
        return

    n = r / dist

    # positional separation
    overlap = min_dist - dist
    correction = 0.5 * overlap * n
    p1.x -= correction
    p2.x += correction

    # velocity correction
    v_rel = np.dot(p1.v - p2.v, n) 
    if v_rel > 0:
        return
    
    #impulse scalar
    j = -(1 + e) * v_rel
    j /= (1/p1.mass + 1/p2.mass)

    #algebra 
    impulse = j * n
    p1.v += impulse / p1.mass
    p2.v -= impulse / p2.mass

def random_unit_vector_3d():
    phi = np.random.uniform(0, 2 * math.pi)
    costheta = np.random.uniform(-1, 1)
    theta = math.acos(costheta)
    return np.array([
        math.sin(theta) * math.cos(phi),
        math.sin(theta) * math.sin(phi),
        math.cos(theta)
    ])

class Ball:
    def __init__(self, sphere, pos, vel, radius, mass, charge, lifetime):
        self.sphere = sphere
        self.x = np.array(pos, dtype=float)
        self.v = np.array(vel, dtype=float)
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.life = lifetime

def spawn_ball():
    pos = np.array([the_sun.x, the_sun.y, the_sun.z])

    radius = np.random.uniform(0.05, 0.15)
    mass = np.random.uniform(0.5, 2.0)
    charge = np.random.choice([-1, 1])

    speed = np.random.uniform(0.2, 0.4)
    vel = random_unit_vector_3d() * speed

    color = (224, 136, 206, 255)

    
    # Temporarily switch to flat shader
    lib.shapes.shader = flat_shader
    
    sphere = lib.Sphere(
        x=pos[0], y=pos[1], z=pos[2],
        radius=radius,
        color=color,
        batch=shapes_batch
    )
    
    # Restore lit shader for everything else
    lib.shapes.shader = lit_shader

    orbiting_balls.append(Ball(
        sphere=sphere,
        pos=pos,
        vel=vel,
        radius=radius,
        mass=mass,
        charge=charge,
        lifetime=3.0
    ))

    
def on_update(dt: float):
    global camera, time_since_last_spawn, G_on, EM_on

    movement_step = np.pi / 1.5 * dt
    if key_handler[key.W]:
        camera.phi += movement_step
    if key_handler[key.S]:
        camera.phi -= movement_step
    if key_handler[key.D]:
        camera.theta += movement_step
    if key_handler[key.A]:
        camera.theta -= movement_step
    
    if key_handler[key.Q]:
        G_on = not G_on
    if key_handler[key.E]:
        EM_on = not EM_on


    eps = 0.001
    camera.phi = max(eps, min(np.pi - eps, camera.phi))

    camera.x = camera.distance * np.sin(camera.phi) * np.cos(camera.theta)
    camera.y = camera.distance * np.cos(camera.phi)
    camera.z = camera.distance * np.sin(camera.phi) * np.sin(camera.theta)

    time_since_last_spawn += dt
    if time_since_last_spawn >= spawn_interval:
        for _ in range(np.random.randint(5, 10)):
            spawn_ball()
        time_since_last_spawn = 0.0

    forces = [np.zeros(3) for _ in orbiting_balls]
        
    if G_on:
        for i in range(len(orbiting_balls)):
            for j in range(i + 1, len(orbiting_balls)):
                f = gravity_force(orbiting_balls[i], orbiting_balls[j])
                forces[i] += f
                forces[j] -= f
            
    # Collision resolution
    for i in range(len(orbiting_balls)):
        for j in range(i + 1, len(orbiting_balls)):
            resolve_collision(orbiting_balls[i], orbiting_balls[j])

    for i, p in enumerate(orbiting_balls[:]):
        # Start with gravity acceleration
        a = np.zeros(3)
        if G_on:
            a += forces[i] / p.mass
    
        #Lorentz acceleration
        if EM_on:
            F_em = lorentz_force(p)
            a += F_em / p.mass
    
        # Integrate
        p.v += a * dt
        p.x += p.v * dt
        p.life -= dt
    
        p.sphere.x, p.sphere.y, p.sphere.z = p.x
    
        if p.life <= 0:
            p.sphere.delete()
            orbiting_balls.remove(p)


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
    
    # The global state needs the camera and the light position
    global_state.update(camera.get_position(), light_position)
    
    # Update the camera matrices
    window.projection = camera.get_projection()
    window.view = camera.get_look_at()
    
    # Draw objects
    shapes_batch.draw()
    batch.draw()
    world_grid.draw()

pyglet.clock.schedule_interval(on_update, 1/60)
pyglet.app.run()
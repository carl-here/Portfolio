import os
import pyglet


def createWorldGridShader():
    """Create a shader to draw a world grid
    """
    with open(os.path.join(os.path.dirname(__file__), "shaders/world_grid.vert"), "r") as file:
        vertex_source = file.read()
    with open(os.path.join(os.path.dirname(__file__), "shaders/world_grid.frag"), "r") as file:
        fragment_source = file.read()

    # The shaders are in a designated subdirectory at "lib/shaders/"
    return pyglet.gl.current_context.create_program((vertex_source, 'vertex'),
                                                    (fragment_source, 'fragment'))

def create3DShader():
    """Create a shader for regular 3D graphics
    """
    with open(os.path.join(os.path.dirname(__file__), "shaders/vertex.vert"), "r") as file:
        vertex_source = file.read()
    with open(os.path.join(os.path.dirname(__file__), "shaders/vertex.frag"), "r") as file:
        fragment_source = file.read()

    # The shaders are in a designated subdirectory at "lib/shaders/"
    return pyglet.gl.current_context.create_program((vertex_source, 'vertex'),
                                                    (fragment_source, 'fragment'))


# Task 5
def lerp(a: float,
         b: float,
         t: float):
    """
    Linearly interpolates between value a and b based on the fraction t. t
    should be a value between 0.0 and 1.0.

    Parameters
    ---------
    a : the minimum value
    b : the maximum value
    t : a fraction between 0.0 and 1.0 that determines the value between a and b

    Returns
    -------
    The value between point a and b determined by t
    """

    # TODO complete the implementation here
    return a + t * (b - a)

def trilinear_interpolation(
    c000, c100, c010, c110,
    c001, c101, c011, c111,
    tx: float, ty: float, tz: float
):
    """
    Perform trilinear interpolation inside a cube.

    Corner naming:
    cxyz where x, y, z ∈ {0, 1}
    """

    # Interpolate along x (bottom face)
    c00 = lerp(c000, c100, tx)
    c10 = lerp(c010, c110, tx)

    # Interpolate along x (top face)
    c01 = lerp(c001, c101, tx)
    c11 = lerp(c011, c111, tx)

    # Interpolate along y
    c0 = lerp(c00, c10, ty)
    c1 = lerp(c01, c11, ty)

    # Interpolate along z
    return lerp(c0, c1, tz)

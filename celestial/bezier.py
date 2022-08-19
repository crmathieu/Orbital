import numpy as np
import math
from functools import lru_cache

@lru_cache(maxsize=10)
def choose(n, k):
    return math.comb(n, k)

def bezier(points):
    """
    Classic implementation of a bezier curve.
    Parameters
    ----------
    points : np.ndarray
        points defining the desired bezier curve.
    Returns
    -------
    typing.Callable[[float], typing.Union[int, typing.Iterable]]
        function describing the bezier curve.
    """
    n = len(points) - 1

    # Cubic Bezier curve
    if n == 3:
        return (
            lambda t: (1 - t) ** 3 * points[0]
            + 3 * t * (1 - t) ** 2 * points[1]
            + 3 * (1 - t) * t**2 * points[2]
            + t**3 * points[3]
        )

    # Quadratic Bezier curve
    if n == 2:
        return (
            lambda t: (1 - t) ** 2 * points[0]
            + 2 * t * (1 - t) * points[1]
            + t**2 * points[2]
        )

    return lambda t: sum(
        ((1 - t) ** (n - k)) * (t**k) * choose(n, k) * point
        for k, point in enumerate(points)
    )

def partial_bezier_points(points, a, b):
    """
    Given an array of points which define bezier curve, and two numbers 0<=a<b<=1, return an array of the same size,
    which describes the portion of the original bezier curve on the interval [a, b].
    This algorithm is pretty nifty, and pretty dense.
    Parameters
    ----------
    points : np.ndarray
        set of points defining the bezier curve.
    a : float
        lower bound of the desired partial bezier curve.
    b : float
        upper bound of the desired partial bezier curve.
    Returns
    -------
    np.ndarray
        Set of points defining the partial bezier curve.
    """
    if a == 1:
        return [points[-1]] * len(points)

    a_to_1 = np.array([bezier(points[i:])(a) for i in range(len(points))])
    end_prop = (b - a) / (1.0 - a)
    return np.array([bezier(a_to_1[: i + 1])(end_prop) for i in range(len(points))])

# Shortened version of partial_bezier_points just for quadratics,
# since this is called a fair amount
def partial_quadratic_bezier_points(points, a, b):
    if a == 1:
        return 3 * [points[-1]]

    def curve(t):
        return (
            points[0] * (1 - t) * (1 - t)
            + 2 * points[1] * t * (1 - t)
            + points[2] * t * t
        )

    # bezier(points)
    h0 = curve(a) if a > 0 else points[0]
    h2 = curve(b) if b < 1 else points[2]
    h1_prime = (1 - a) * points[1] + a * points[2]
    end_prop = (b - a) / (1.0 - a)
    h1 = (1 - end_prop) * h0 + end_prop * h1_prime
    return [h0, h1, h2]

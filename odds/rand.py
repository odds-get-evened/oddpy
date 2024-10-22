import random
import secrets

import numpy as np


def quadratic_inverted(l, u):
    """
    results generally closer to zero
    Parameters
    ----------
    l
    u

    Returns
    -------

    """
    return float((random.uniform(l, u)) ** 3)  # cubing favors results nearer to 0


def quadratic(l, u):
    """
    results closer to the outer bounds (aka quadratic curve)
    Parameters
    ----------
    l
    u

    Returns
    -------

    """
    v = random.uniform(l, u)
    return float(v ** (1 / 3) if v >= 0 else -((-v) ** (1 / 3)))  # Cubic root emphasizes edges


def weighted(l, u, weight=None):
    """
    control the distribution with a weight value
    Parameters
    ----------
    l
    u
    weight

    Returns
    -------

    """
    v = np.random.uniform(l, u)
    # Higher weight near 0, tweak the multiplier to adjust
    weight = weight if weight else np.exp(-abs(v) * 5)
    return float(v * weight)


def gaussian(l, u):
    # Normal distribution centered at 0 with a small standard deviation
    v = np.random.normal(0, 0.3)
    return float(np.clip(v, l, u))  # clip off values not within bounds


def gaussian_curved(l, u):
    """
    Generate a value from a normal distribution centered at 0 with small std deviation
    """
    while True:
        v = np.random.normal(0, 0.4)
        # Restrict the value to be within the range [-1, 1]
        if l <= v <= u:
            return float(v)


def sigmoid(l, u):
    v = np.random.uniform(l, u)
    # Tanh transforms the range into a smooth S-curve
    return float(np.tanh(v * 2))


def random_secrets(l, u):
    len_bits = 64
    r_bits = secrets.randbits(len_bits)
    scaler = r_bits / (2 ** len_bits)

    # scale to the specified range
    return l + (scaler * (u - l))

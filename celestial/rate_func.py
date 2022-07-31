import numpy as np

# all func are a variation of:
# F(alpha, t) = (t^alpha)/(t^alpha + (1-t)^alpha)
# with t always belonging to the domain [0,1]
# F(1, t) = t (identity)
# F(2, t) = resembles the sigmoid: (t^2)/(t^2 + (1-t)^2)
# the higher the value of alpha, the steeper the curve
def F(alpha, t):
    return (t**alpha)/(t**alpha + (1-t)**alpha)

def ease_in_out(t):
    return F(4, t)

def sigmoid(t):
    return np.where(t < 0, np.exp(t)/(1 + np.exp(t)), 1/(1 + np.exp(-t)))

def linear(t):
    return t

def smooth(t):
    # Zero first and second derivatives at t=0 and t=1.
    # Equivalent to bezier([0, 0, 0, 1, 1, 1])
    s = 1 - t
    return (t**3) * (10 * s * s + 5 * s * t + t * t)


def rush_into(t):
    return 2 * smooth(0.5 * t)


def rush_from(t):
    return 2 * smooth(0.5 * (t + 1)) - 1


def slow_into(t):
    return np.sqrt(1 - (1 - t) * (1 - t))


def double_smooth(t):
    if t < 0.5:
        return 0.5 * smooth(2 * t)
    else:
        return 0.5 * (1 + smooth(2 * t - 1))


def there_and_back(t):
    new_t = 2 * t if t < 0.5 else 2 * (1 - t)
    return smooth(new_t)


def there_and_back_with_pause(t, pause_ratio = 1. / 3):
    a = 1. / pause_ratio
    if t < 0.5 - pause_ratio / 2:
        return smooth(a * t)
    elif t < 0.5 + pause_ratio / 2:
        return 1
    else:
        return smooth(a - a * t)

def wiggle(t, wiggles = 2.0):
    return there_and_back(t) * np.sin(wiggles * np.pi * t)


#
#  the following were defined from https://easings.net/
#

def exponential_decay(t, half_life = 0.1):
    # The half-life should be rather small to minimize
    # the cut-off error at the end
    return 1 - np.exp(-t / half_life)

# in-out sine
def ease_out_sine(t):
    return np.sin((t * np.PI) / 2)

def ease_in_sine(t):
  return 1 - np.cos((t * np.PI) / 2)

def ease_in_out_sine(t):
    return -(np.cos(np.PI * t) - 1) / 2


# in-out quad
def ease_in_quad(t):
    return t * t

def ease_out_quad(t):
    return 1 - (1 - t) * (1 - t)

def ease_in_cubic(t):
    return t * t * t

# shake it!
def wiggle(t, wiggles = 2):
    return there_and_back(t) * np.sin(wiggles * np.pi * t)


# in-out back (with a rebound)
def ease_in_back(t):
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * t * t * t - c1 * t * t

def ease_out_back(t):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

def ease_in_out_back(t):
    c1 = 1.70158
    c2 = c1 * 1.525
    return (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2 if t < 0.5  else (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2

# in-out circ
def ease_in_circ(t):
    return 1 - np.sqrt(1 - pow(t, 2))


def ease_out_circ(t):
    return np.sqrt(1 - pow(t - 1, 2))


def ease_in_out_circ(t: float) -> float:
    return (
        (1 - np.sqrt(1 - pow(2 * t, 2))) / 2
        if t < 0.5
        else (np.sqrt(1 - pow(-2 * t + 2, 2)) + 1) / 2
    )
# in-out elastic
def ease_in_elastic(t):
    c4 = (2 * np.PI) / 3

    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        -pow(2, 10 * t - 10) * np.sin((t * 10 - 10.75) * c4) 

def ease_out_elastic(t):
    c4 = (2 * np.PI) / 3

    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        return pow(2, -10 * t) * np.sin((t * 10 - 0.75) * c4) + 1


def ease_in_out_elastic(t):
    c5 = (2 * np.PI) / 4.5

    if t == 0:
        return 0
    elif t == 1:
        return 1
    elif t < 0.5:
        return -(pow(2, 20 * t - 10) * np.sin((20 * t - 11.125) * c5)) / 2
    else:
        return (pow(2, -20 * t + 10) * np.sin((20 * t - 11.125) * c5)) / 2 + 1


# in-out bounce
def ease_in_bounce(t: float) -> float:
    return 1 - ease_out_bounce(1 - t)

def ease_out_bounce(t):
    n1 = 7.5625
    d1 = 2.75

    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        return n1 * (t - 1.5 / d1) * (t - 1.5 / d1) + 0.75
    elif t < 2.5 / d1:
        return n1 * (t - 2.25 / d1) * (t - 2.25 / d1) + 0.9375
    else:
        return n1 * (t - 2.625 / d1) * (t - 2.625 / d1) + 0.984375

def ease_in_out_bounce(t):
    if t < 0.5:
        return (1 - ease_out_bounce(1 - 2 * t)) / 2
    else:
        return (1 + ease_out_bounce(2 * t - 1)) / 2


# This is a decorator that makes sure any function it's used on will
# return 0 if t<0 and 1 if t>1.
def unit_interval(function):
    def wrapper(t, *args, **kwargs):
        if 0 <= t <= 1:
            return function(t, *args, **kwargs)
        elif t < 0:
            return 0
        else:
            return 1

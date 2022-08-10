# Rate functions can be used "incrementally" or "absolutely"
#   Typically these functions require a domain between [0, 1] and will
#   return a value always comprise in the interval [0, 1]. 
#
#   So, as a consequence, always make sure to have the input parameter between [0, 1] 
# 2 types of rate functions:
# 1) When used absolutely, rate functions operate on a quantity to deduct a value at a 
# given step knowing the global quantity difference. 
#   
#   for instance: 
#
#       current_dist = original_distance + (original_distance - final_distance) * rate_func(step)
#
#    The current value is calculated using the original value as a reference, incremented by
#    the rate_function * the_total_difference
#   
# 2) When used incrementally, rate functions operate on a quantity to deduct a value at a 
# given step knowing the value at the previous step. 
# 
#   for instance:
#
#       current_angle = current_angle + (angle_variation) * rate_func(step)
#
#    The current value is calculated using the value at the previous step as a reference, incremented by
#    the rate_function * the_total_difference.
#
# Depending on the type of "rate of change" we want to use it for, we will need either type of rate functions.
#
# Note: the rate profile of rate functions will have a dratically different effect when used absolutely of incrementally.

import numpy as np

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

    return wrapper

# To improve runtime, this decorator is temporary and used for testing
# purpose, but should be removed upon good test results
def test_unit_interval(function):
    def wrapper(t, *args, **kwargs):
        if 0 <= t <= 1:
            return function(t, *args, **kwargs)
        elif t < 0:
            print (function, " returned a negative value: ", t)
            return 0
        else:
            print (function, " returned a value greater than 1: ", t)
            return 1

    return wrapper

# all func are a variation of:
# F(alpha, t) = (t^alpha)/(t^alpha + (1-t)^alpha)
# with t always belonging to the domain [0,1]
# F(1, t) = t (identity)
# F(2, t) = resembles the sigmoid: (t^2)/(t^2 + (1-t)^2)
# the higher the value of alpha, the steeper the curve
def F(alpha, t):
    return (t**alpha)/(t**alpha + (1-t)**alpha)

@unit_interval
def ease_in_out(t):
    return F(4, t)

def sigmoid(t):
    """
    - https://en.wikipedia.org/wiki/Sigmoid_function
    - https://en.wikipedia.org/wiki/Logistic_function
    """
    return np.exp(t)/(1 + np.exp(t)) if t < 0 else 1/(1 + np.exp(-t))
    #return np.where(t < 0, np.exp(t)/(1 + np.exp(t)), 1/(1 + np.exp(-t)))
    #return 1.0 / (1 + np.exp(-t))

def squish_rate_func(func, a = 0.4, b = 0.6):
    def result(t):
        if a == b:
            return a

        if t < a:
            return func(0)
        elif t > b:
            return func(1)
        else:
            return func((t - a) / (b - a))

    return result


@unit_interval
def lingering(t):
    return squish_rate_func(lambda t: t, 0, 0.8)(t)


@unit_interval
def linear(t):
    return t

@unit_interval
def smooth(t):
    # Zero first and second derivatives at t=0 and t=1.
    # Equivalent to bezier([0, 0, 0, 1, 1, 1])
    s = 1 - t
    return (t**3) * (10 * s * s + 5 * s * t + t * t)


@unit_interval
def smoothSig(t, inflection = 10.0):
    error = sigmoid(-inflection / 2)
    return min(
        max((sigmoid(inflection * (t - 0.5)) - error) / (1 - 2 * error), 0),
        1,
    )


@unit_interval
def rush_into(t):
    return 2 * smooth(0.5 * t)


@unit_interval
def rush_from(t):
    return 2 * smooth(0.5 * (t + 1)) - 1


@unit_interval
def slow_into(t):
    return np.sqrt(1 - (1 - t) * (1 - t))


@unit_interval
def double_smooth(t):
    if t < 0.5:
        return 0.5 * smooth(2 * t)
    else:
        return 0.5 * (1 + smooth(2 * t - 1))


@unit_interval
def there_and_back(t):
    new_t = 2 * t if t < 0.5 else 2 * (1 - t)
    return smooth(new_t)


@unit_interval
def there_and_back_with_pause(t, pause_ratio = 1. / 3):
    a = 1. / pause_ratio
    if t < 0.5 - pause_ratio / 2:
        return smooth(a * t)
    elif t < 0.5 + pause_ratio / 2:
        return 1
    else:
        return smooth(a - a * t)

@unit_interval
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
@unit_interval
def ease_out_sine(t):
    return np.sin((t * np.PI) / 2)

@unit_interval
def ease_in_sine(t):
  return 1 - np.cos((t * np.PI) / 2)

@unit_interval
def ease_in_out_sine(t):
    return -(np.cos(np.PI * t) - 1) / 2


# in-out quad
@unit_interval
def ease_in_quad(t):
    return t * t

@unit_interval
def ease_out_quad(t):
    return 1 - (1 - t) * (1 - t)

@unit_interval
def ease_in_cubic(t):
    return t * t * t

# shake it!
def wiggle(t, wiggles = 2):
    return there_and_back(t) * np.sin(wiggles * np.pi * t)


# in-out back (with a rebound)
@unit_interval
def ease_in_back(t):
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * t * t * t - c1 * t * t

@unit_interval
def ease_out_back(t):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

@unit_interval
def ease_in_out_back(t):
    c1 = 1.70158
    c2 = c1 * 1.525
    return (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2 if t < 0.5  else (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2

# in-out circ
@unit_interval
def ease_in_circ(t):
    return 1 - np.sqrt(1 - pow(t, 2))


@unit_interval
def ease_out_circ(t):
    return np.sqrt(1 - pow(t - 1, 2))


@unit_interval
def ease_in_out_circ(t):
    return (
        (1 - np.sqrt(1 - pow(2 * t, 2))) / 2
        if t < 0.5
        else (np.sqrt(1 - pow(-2 * t + 2, 2)) + 1) / 2
    )
# in-out elastic
@unit_interval
def ease_in_elastic(t):
    c4 = (2 * np.PI) / 3

    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        -pow(2, 10 * t - 10) * np.sin((t * 10 - 10.75) * c4) 

@unit_interval
def ease_out_elastic(t):
    c4 = (2 * np.PI) / 3

    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        return pow(2, -10 * t) * np.sin((t * 10 - 0.75) * c4) + 1


@unit_interval
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
@unit_interval
def ease_in_bounce(t):
    return 1 - ease_out_bounce(1 - t)

@unit_interval
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

@unit_interval
def ease_in_out_bounce(t):
    if t < 0.5:
        return (1 - ease_out_bounce(1 - 2 * t)) / 2
    else:
        return (1 + ease_out_bounce(2 * t - 1)) / 2



import colorsys

black = (0,0,0)
white = (1,1,1)
whiteish = (0.9, 0.9, 0.9)
grey = (0.5,0.5,0.5)
darkgrey = (0.32, 0.32, 0.32)
lightgrey = (0.75,0.75,0.75)

red = (1,0,0)
redish = (0.5, 0, 0)
green = (0,1,0)
greenish = (0, 0.5, 0)
blue = (0,0,1)
blueish = (0, 0, 0.5)
darkblue = (0, 0.5, 1)

yellow = (1,1,0)
yellowish = (0.5, 0.5, 0)
cyan = (0,1,1)
cyanish = (0, 0.5, 0.5)
magenta = (1,0,1)
magentish = (0.5, 0, 0.5)
dirtyYellow = (0.5,0.5,0)
orange = (1,0.6,0)
nightshade = (0.12, 0.12, 0.12)


def gray(luminance):
  return (luminance,luminance,luminance)

def rgb_to_hsv(T):
  if len(T) > 3:
    T = T[:3]
  return colorsys.rgb_to_hsv(*T)

def hsv_to_rgb(T):
  if len(T) > 3:
    T = T[:3]
  return colorsys.hsv_to_rgb(*T)

def rgb_to_grayscale(T):
  if len(T) > 3:
    T = T[:3]
  luminance = 0.21*T[0] + 0.71*T[1] + 0.07*T[2]
  return (luminance, luminance, luminance)

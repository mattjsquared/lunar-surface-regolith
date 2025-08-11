import numpy as np, matplotlib as mpl
def generate_limb_circle():
  rect = mpl.path.Path([[-90,-90],[90,-90],[90,90],[-90,90],[-90,-90]]).interpolated(100)
  return rect


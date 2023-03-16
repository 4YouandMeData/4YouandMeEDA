import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.patches as mpatches
import matplotlib.colors
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec

blue = '#2e91e8'
red = '#b81a2f'
orange = '#e88738'
turquoise = '#1ab5b8'
green = '#79c756'
purple = '#7839bd'

def pale(c):
    h = c.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4)) + (0.3,)

def cmap(c):
    norm = matplotlib.colors.Normalize(0, 1)
    colors = [
        [norm(0), pale(c)],
        [norm(1), c]
    ]

    cmap = matplotlib.colors.LinearSegmentedColormap.from_list('', colors)
    return cmap

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def palette_2(h1, h2, n):
    rgb1 = hex_to_rgb(h1)
    rgb2 = hex_to_rgb(h2)
    n-=1
    return [
        tuple([float(((n-i)*x[0] + i*x[1])/(255*n)) for x in list(zip(rgb1, rgb2))]) for i in range(n+1)
    ]

def palette_3(h1, h2, h3, n):
    return palette_2(h1, h2, int(n/2)) + palette_2(h2, h3, n-int(n/2))

def get_shade(c1, c2, c3, n):
    colors = palette_3(c1, c2, c3, n)
    colors = [tuple(int(255*c) for c in color) for color in colors]
    colors = ['#%02x%02x%02x' % color for color in colors]
    return colors
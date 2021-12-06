import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg


import matplotlib.pyplot as plt
import game_DB
import pygame
from pygame.locals import *

pygame.init()

n = len(game_DB.get_point("hi"))
nn_range = [0 for i in range(n)]
x = 0
for x in range(1, n):
    nn_range[x] = x

fig = plt.figure(figsize=[4, 4], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
ax = fig.gca()
ax.plot(nn_range, game_DB.get_point("hi"))

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()


window = pygame.display.set_mode((600, 400), DOUBLEBUF)
screen = pygame.display.get_surface()

size = canvas.get_width_height()

surf = pygame.image.fromstring(raw_data, size, "RGB")
screen.blit(surf, (0,0))
pygame.display.flip()

crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
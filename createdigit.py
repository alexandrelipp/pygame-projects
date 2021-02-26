import pygame
from arcade import*
import numpy as np
import matplotlib.pyplot as plt
hauteur=28
largeur=28

screen=pygame.display.set_mode((largeur,hauteur))
pygame.display.set_caption("CreateDigit")
pygame.init()
draw=False
done=False
screen.fill(color.WHITE)
grid=np.zeros((28,28))
while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
        if event.type==pygame.MOUSEBUTTONDOWN:
            draw=True
        if event.type==pygame.MOUSEBUTTONUP:
            draw=False


    if draw:
        pos=pygame.mouse.get_pos()
        pygame.draw.line(screen,color.BLACK,pos,pos)
        grid[pos[1]][pos[0]]=1

    pygame.display.flip()
plt.imshow(grid)
plt.show()

print(grid)
pygame.quit()
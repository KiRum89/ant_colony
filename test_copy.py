import pygame
import sys
import sys
import numpy as np

pygame.init()
N,M = 800,800
clock = pygame.time.Clock()
arr = np.random.random((N,M,3))
arr[:,:,:2]=[0,0]
arr = arr/arr.max()*255
arr=arr.astype('int')
gameDisplay = pygame.display.set_mode((N,M))
pygame.surfarray.blit_array(gameDisplay,arr)
pygame.display.flip()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 






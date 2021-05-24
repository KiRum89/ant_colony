import sys
import numpy as np
import pygame
pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((500,500))
arr = np.zeros((500,500))
def draw():
    x,y=pygame.mouse.get_pos()
    state = pygame.mouse.get_pressed(num_buttons=3) 
    
    if state[0]==True:
        print(x,y)
        arr[x,y]=1 
        x0,y0 = pygame.mouse.get_pos()
        rect = pygame.Rect(x,y,5,5)
        pygame.draw.rect(gameDisplay,(255,0,0),rect)


while 1:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
    pygame.display.update()


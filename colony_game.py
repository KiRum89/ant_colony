from ant import Ant
import sys
import world as w
import numpy as np
ants=[Ant(np.array([1,1]),50,np.pi/3,10,0) for _ in range(0,50)]

t = 1 
import pygame

pygame.init()
gameDisplay = pygame.display.set_mode((w.W,w.H))
col = (0,0,255)


clock = pygame.time.Clock()
trail_scout={}
trail_return = {}

def plot_rect(trail,col):
    for (i,j) in trail:
        for pherom in trail[(i,j)]:
            coor = pherom[0]
            rect = pygame.Rect(coor[0],coor[1],1,1)
            pygame.draw.rect(gameDisplay,col,rect)

count_home = 0
while 1:

    gameDisplay.fill((0,0,0))
    plot_rect(trail_scout,(0,0,255))
    plot_rect(trail_return,(255,0,0))

    pygame.draw.circle(gameDisplay,(255,0,0),tuple(w.r0),w.R)
    for ant in ants:   
        if w.isFood(ant.r) and ant.scout==True:
            ant.scout = False 
            ant.dr = -ant.dr
            ant.t = t
            col = (255,0,0)

        if w.isHome(ant.r) and ant.scout==False:
            count_home += 1
            print('count home {}'.format(count_home))
            ant.dr = -ant.dr
            ant.scout = True
            col = (0,0,255)
           

        ant.t = t
        if ant.scout == True:
            ant.mark_trail(trail_scout)
            ant.move()
            ant.decide(trail_return)            
        else:
            ant.mark_trail(trail_return)
            ant.move()
            ant.decide(trail_scout)            
    
    w.evap(trail_scout, 150,t)
    w.evap(trail_return, 150,t)
    print('scout:',len(trail_scout))
    print('return:',len(trail_return))

    t += 1
    pygame.display.update()

    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 


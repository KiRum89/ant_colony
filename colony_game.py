from ant import Ant
import sys
import world as w
import numpy as np
from area import CircArea
import pygame
import time
t1 = time.time()
t=0
ants=[Ant(np.array([1,1]),30,np.pi/3,5,t) for _ in range(0,10)]
pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((w.W,w.H))


col = (0,255,0)
green = (0,255,0)
red = (255,0,0)


Lmax = 3000
food = CircArea(red,np.array([w.W/2,w.H/2]),100)
home = CircArea(green,np.array([30,30]),30)


trail_scout={}
trail_return = {}
def plot_rect(trail,col):
    for (i,j) in trail:
        for pherom in trail[(i,j)]:
            coor = pherom[0]
            rect = pygame.Rect(coor[0],coor[1],1,1)
            pygame.draw.rect(gameDisplay,col,rect)

def plot_rect2(arr,Lmax):
    print(len(arr)) 
    if len(arr)>Lmax:
        els = arr.pop(0)
        for el in els: 
            r,m = el
            if m == True:
                c = green
            else:
                c = red
            rect = pygame.Rect(r[0],r[1],1,1)
            pygame.draw.rect(gameDisplay,(0,0,0),rect)

    if len(arr)>0:
        els = arr[-1]
        for el in els: 
            r,m = el
            if m == True:
                c = green
            else:
                c = red
            rect = pygame.Rect(r[0],r[1],1,1)
            pygame.draw.rect(gameDisplay,c,rect)

       
count_home = 0

pause = False
arr = []
while 1:

    #gameDisplay.fill((0,0,0))
    food.drag(pygame)
    home.drag(pygame)
    pygame.draw.circle(gameDisplay,red,tuple(food.r0),food.R)

    pygame.draw.circle(gameDisplay,green,tuple(home.r0),home.R)

     
    if pause==False:
        arr1=[]
        #plot_rect(trail_scout,green)
        #plot_rect(trail_return,red)
        plot_rect2(arr,Lmax)        
        for ant in ants:   
            if food.inside(ant.r) and ant.scout==True:
                ant.scout = False 
                ant.dr = -ant.dr
                ant.t = t
                col =  red 

            if home.inside(ant.r) and ant.scout==False:
                count_home += 1
                print('count home {}'.format(count_home))
                ant.dr = -ant.dr
                ant.scout = True
                col =green 
               

            ant.t = t
            if ant.scout == True:
                ant.mark_trail(trail_scout)
                arr1.append((ant.r,ant.scout))

                ant.move()
                ant.decide(trail_return)            
            else:
                ant.mark_trail(trail_return)
                arr1.append((ant.r,ant.scout))
                
                ant.move()
                ant.decide(trail_scout)            
        
        w.evap(trail_scout, Lmax,t)
        w.evap(trail_return, Lmax,t)
        arr.append(arr1)
        t += 1
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                trail_return={}
                trail_scout={}

                t = 0
                ants=[Ant(home.r0,30,np.pi/3,5,t) for _ in range(0,10)]
                pause = not(pause)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 


    #clock.tick(120)

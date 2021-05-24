from ant import Ant
import sys
import world as w
import numpy as np
from area import CircArea, CircAreaGranular
import pygame
import time
t1 = time.time()
t=0
ants=[Ant(np.array([w.W/2,w.H/2]),10,2*np.pi/100*i,1,t) for i in range(0,500)]
pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((w.W,w.H))


col = (0,255,0)
green = (0,255,0)
red = (255,0,0)


Lmax = 6000

home = CircArea(green,np.array([w.W/2,w.H/2]),10)
food_granular1 = CircAreaGranular(red,[20,20],20,w.N,w.M)
food_granular1.create()
food_granular2 = CircAreaGranular(red,[w.W-20,20],20,w.N,w.M)
food_granular2.create()
food_granular3 = CircAreaGranular(red,[w.W-20,w.H-20],20,w.N,w.M)
food_granular3.create()
food_granular4 = CircAreaGranular(red,[20,w.H-20],20,w.N,w.M)
food_granular4.create()

#obstacle=np.zeros()
def draw():
    x,y=pygame.mouse.get_pos()
    state = pygame.mouse.get_pressed(num_buttons=3) 
    
    if state[0]==True:
        print(x,y)
        arr[x,y]=1 
        x0,y0 = pygame.mouse.get_pos()
        rect = pygame.Rect(x,y,5,5)
        pygame.draw.rect(gameDisplay,(255,0,0),rect)




trail_scout=np.zeros((w.N,w.M))
trail_return =np.zeros((w.N,w.M))
def plot_rect_ant(ant):
    if ant.scout==True:
        c =(0,0,255) 
    else:
        c = red
    rect = pygame.Rect(ant.r[0],ant.r[1],1,1)
    pygame.draw.rect(gameDisplay,c,rect)

     

def plot_rect2(arr,Lmax):

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
    
def plot_trail(trail1,trail2):
    N,M = trail1.shape
    arr = np.zeros((N,M,3))
    if trail1.max()!=0:
        arr[:,:,0]=trail1/trail1.max()*2550
    else:
        arr[:,:,0] = trail1
    if trail2.max()!=0:
        arr[:,:,2]=trail2/trail2.max()*2550
    else:
        arr[:,:,2]=trail2
    

    
    arr=arr.astype('int')
    pygame.surfarray.blit_array(gameDisplay,arr)

    return arr
       
count_home = 0

pause = False
while 1:

    #gameDisplay.fill((0,0,0))
    #food.drag(pygame)
    #home.drag(pygame)
    #draw()     
    if pause==False:

        food_granular1.plot(pygame,gameDisplay)
        food_granular2.plot(pygame,gameDisplay)
        food_granular3.plot(pygame,gameDisplay)
        food_granular4.plot(pygame,gameDisplay)

        arr = plot_trail(trail_scout,trail_return)



        for ant in ants:   
            
            #plot_rect_ant(ant)
            if (food_granular1.inside(ant.r) or food_granular2.inside(ant.r) or food_granular3.inside(ant.r) or food_granular4.inside(ant.r))and ant.scout==True:

                ant.scout = False 
                ant.dr = -ant.dr
                ant.t = t
                col =  red 

            if home.inside(ant.r) and ant.scout==False:
                count_home += 1

                print('home {}'.format(count_home))
                ant.dr = -ant.dr
                ant.scout = True
                col =green 
               

            ant.t = t
            oldpos = ant.r
            if ant.scout == True:
                ant.mark_trail(trail_scout)
                ant.bite(food_granular1.arr)
                ant.bite(food_granular2.arr)
                ant.bite(food_granular3.arr)
                ant.bite(food_granular4.arr)


                ant.move()
                ant.decide(trail_return)            
            else:
                ant.mark_trail(trail_return)
                ant.bite(food_granular1.arr)
                ant.bite(food_granular2.arr)
                ant.bite(food_granular3.arr)
                ant.bite(food_granular4.arr)


                ant.move()
                ant.decide(trail_scout)            
    
        w.evap(trail_scout, Lmax,t)
        w.evap(trail_return, Lmax,t)
        trail_scout=w.diffuse(trail_scout)
        trail_return=w.diffuse(trail_return)
     
        t += 1
        if t%100==0:
            print(t)
    #pygame.draw.circle(gameDisplay,red,tuple(food.r0),food.R)

    pygame.draw.circle(gameDisplay,green,tuple(home.r0),home.R)


    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:

                t = 0
                ants=[Ant(np.array([w.W/2,w.H/2]),10,2*np.pi/100*i,1,t) for i in range(0,100)]

                pause = not(pause)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 


    #clock.tick(120)

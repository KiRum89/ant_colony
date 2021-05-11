from ant import Ant
import world as w
import numpy as np
ants=[Ant(np.array([1,1]),50,np.pi/2,10,0) for _ in range(0,1)]

t = 1 
import pygame

pygame.init()
gameDisplay = pygame.display.set_mode((w.W,w.H))
surf = pygame.Surface((w.W,w.H))
col = (0,0,255)


clock = pygame.time.Clock()
trail_scout={}
trail_return = {}
for ant in ants:   
        while 1:
            
            rect = pygame.Rect(ant.r[0],ant.r[1],1,1)

            pygame.draw.rect(gameDisplay,col,rect)
            if w.isFood(ant.r) and ant.scout==True:
                ant.scout = False 
                ant.dr = -ant.dr
                ant.t = t
                col = (255,0,0)

            if w.isHome(ant.r) and ant.scout==False:
                print('found home')
                ant.dr = -ant.dr
                ant.scout = True
                

            if ant.scout == True:
                ant.t = t
                ant.mark_trail(trail_scout)
                ant.move()
                ant.decide(trail_return)            
            else:
                ant.t = t
                ant.mark_trail(trail_return)
                ant.move()
                ant.decide(trail_scout)            

            t += 1

            pygame.display.update()
            clock.tick(60)

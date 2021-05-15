import world as w
import cProfile

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from ant import Ant
 
if __name__ == "__main__":
    
        T = 9000 # number of steps
        trail_scout = {} # no food
        trail_return = {} # 
        fig,ax = plt.subplots(1,1)

        def plot(ants):            
            for ant in ants:
                path = np.array(ant.path)
                t = ant.t
                if t!=0:
                    ax.plot(path[:t,0],path[:t,1],'+')
                    ax.plot(path[t:,0],path[t:,1],'+')
                else:
                    ax.plot(path[t:,0],path[t:,1],'+')

        def plot_trail(trail,c):
            arr = []
            for (i,j) in trail:
                for pherom in trail[(i,j)]:
                    if len(pherom)!=0:
                        coor = pherom[0]
                        arr.append(coor) 
            arr = np.asarray(arr)
            plt.plot(arr[:,0],arr[:,1],'x',c=c)
                    
        def myrun():                  
            #ant.get_pherom_counts(trail)                
            ants=[Ant(np.array([1,1]),50,np.pi/2,10,0) for _ in range(0,1)]
                
            for ant in ants:   
                for t in range(0,T):

                    if w.isFood(ant.r) and ant.scout==True:
                        ant.scout = False 
                        ant.dr = -ant.dr
                        ant.t = t

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

                    w.evap(trail_return,50,t)
                    w.evap(trail_scout,50,t)


      
        #cProfile.run('myrun()')        
        myrun()
        circle1 = plt.Circle(tuple(w.r0), w.R, color='r') 
        ax.add_patch(circle1)
        circle2 = plt.Circle((10,10), 5, color='r') 
        ax.add_patch(circle2)
        plot_trail(trail_scout,'r')
        plot_trail(trail_return,'g')

        import pygame
        pygame.init()
        gameDisplay = pygame.display.set_mode((w.W,w.H))
        surf = pygame.Surface((w.W,w.H))
        blue = (0,0,255)
        rect = pygame.Rect(1,1,10,10)

        pygame.draw.rect(gameDisplay,blue,rect)

        pygame.display.update()
        while True:
            pass

import world as w
import cProfile

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from ant import Ant
from area import CircArea
 
if __name__ == "__main__":
    
        T = 900 # number of steps
        trail_scout = {} # no food
        trail_return = {} # 
        fig,ax = plt.subplots(1,1)
        col = (0,255,0)
        green = (0,255,0)
        red = (255,0,0)

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

        def run_ant(ant,t,areas):
            home,food = areas
            if food.inside(ant.r) and ant.scout==True:
                ant.scout = False 
                ant.dr = -ant.dr
                ant.t = t
                col =  red 

            if home.inside(ant.r) and ant.scout==False:
                ant.dr = -ant.dr
                ant.scout = True
                col =green 
               

            if ant.scout == True:
                ant.mark_trail(trail_scout)
                ant.move()
                ant.decide(trail_return)            
            else:
                ant.mark_trail(trail_return)
                ant.move()
                ant.decide(trail_scout)            

                    
        def myrun():                  

            count_home = 0
            food = CircArea(red,[w.W/2,w.H/2],100)
            home = CircArea(green,[30,30],30)


            ants=[Ant(np.array([1,1]),30,np.pi/2,5,0) for _ in range(0,10)]

            areas = [home,food]
            for t in range(0,T):
                for ant in ants:   

                    ant.t = t
                    run_ant(ant,t,areas)
                                
                w.evap(trail_scout,300,t)
                w.evap(trail_return,300,t)

                t += 1
 
                


        cProfile.run('myrun()')        
        #myrun()
        #plot_trail(trail_scout,'r')
        #plot_trail(trail_return,'g')




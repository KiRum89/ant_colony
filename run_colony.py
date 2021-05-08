import world as w

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from ant import Ant
 
if __name__ == "__main__":
        T = 20000 # number of steps
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


                    
        #ant.get_pherom_counts(trail)                
        ants=[Ant(np.array([1,1]),5,np.pi/2,0.1,0)]
            
        for ant in ants:   
            for t in range(0,T):

                if w.isFood(ant.r) and ant.scout==True:
                    ant.scout = False 
                    ant.dr = -ant.dr
                    print(t)
                    ant.t = t

                if w.isHome(ant.r) and ant.scout==False:
                    print('found home')
                    ant.dr = -ant.dr
                    ant.scout = True
                    break

                if ant.scout == True:
                    ant.mark_trail(trail_scout)
                    ant.move()
                    ant.decide(trail_return)            
                else:
                    ant.mark_trail(trail_return)
                    ant.move()
                    ant.decide(trail_scout)            
   

        circle1 = plt.Circle(tuple(w.r0), w.R, color='r') 
        ax.add_patch(circle1)
        circle2 = plt.Circle((10,10), 5, color='r') 
        ax.add_patch(circle2)
        plot(ants)


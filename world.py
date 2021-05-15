import numpy as np
import world as w
H,W = 800,800

R = 100
r0 = np.array([W/2,H/2])

def isFood(r):
    # r ant coordinate
    # r0 food circle center
    # R food circle radius
    R = 100
    r0 = np.array([W/2,H/2])
 
    if np.sum((r-r0)**2)**0.5<R:
        return True
    else:
        return False
    
def isHome(r):
    # r ant coordinate
    # r0 nest circle center
    # R nest circle radius
    R = 5
    r0 = np.array([10,10])
    if np.sum((r-r0)**2)**0.5<R:
        return True
    else:
        return False
 
def evap(trail, timer,ctime):
    # ctime current time
    # if timer is exceeded, delet the pheromone 
    
    for (i,j) in trail:
        pherom2=[pherom for pherom in trail[(i,j)] if (ctime-pherom[1])<timer]
        trail[(i,j)] = pherom2


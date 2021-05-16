import numpy as np
import world as w
H,W = 800,800

def evap(trail, timer,ctime):
    # ctime current time
    # if timer is exceeded, delet the pheromone 
    key_list=list(trail.keys())

    for (i,j) in key_list:
        pherom2=[pherom for pherom in trail[(i,j)] if (ctime-pherom[1])<timer]
        trail[(i,j)] = pherom2
        if len(pherom2)==0:
            del trail[(i,j)]


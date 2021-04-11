import matplotlib.pyplot as plt
import numpy as np

# generate graph that corresponds to a NxM board. Ant can visit adjasent cells.
# and leaves a fremone on each edge. 
# food found come back using the same path
# equation to chose a particular state
#P_ij = tau_ij^alpha\sum(tau_ij^alpha), distance factor is omitted


ef get_new_pos(n):
    children = get_children(n,N,M)
    keys = []
    for child in children:
    
        key = [n,child]
        key.sort()
        key = tuple(key)
        keys.append(key)
    PP = []
    
    print('children',n,children)
    for key in keys:
        weight = edges[key]
        P = get_P(weight,alpha)
        PP.append(P)
    return PP
        
        

def get_event(PP):
    #retuns index of the event with the probability  
    arr = [0]
    for P in PP:
        arr.append(arr[-1]+P)
            

    return arr
        
       
        
    
        

   

T=1000
#when food found go back. Food for now is one node with infinite source.
# ant has a position

ant = []
N,M = 3,3
board = init_board(N,M)
edges = init_weights(N,M)
ant_counts=20
ants = [pos for pos in range(0,ant_counts)]
for t in range(0,T):
    for i in range(0,ant_counts):
        #new_pos = get_new_pos(ants[i])
        Ant(12)

        
        

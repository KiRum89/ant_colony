import world as w

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from ant import Ant
if __name__ == "__main__":
    N,M = w.N,w.M
    board = w.init_board(N,M) 
    edges = w.init_weights(board)
    assert(len(edges)==(N-1)*M + N*(M-1))
    a1=Ant(50,0)
    a2=Ant(50,0)
    i,j = w.get_row_col(50,M)
    ax = plt.subplot(111)
    ax.add_patch(Rectangle((i,j),10,10,facecolor="grey"))
    ax.set_ylim([0,100])
    ax.set_xlim([0,100])
    x = 0.001
    ants = []
    for i in range(0,10):
        ants.append(Ant(50,0))
    for t in range(0,400000):

        for a in ants:
            #print('time {}'.format(t))
            
            
            child=a.decide(edges)
            if w.region(a,80,80,5,5,M):
                if a.food==False:
                    #food source
                    a.food = True
            if w.region(a,50,50,5,5,M):
                    #home
                    a.food = False
            a.move(child)
            a.deposit(x,edges)
for a in ants:
    p = []
    for n in a.path:
        i,j = w.get_row_col(n,M)
        p.append([i,j])
    p = np.array(p)
    ax.plot(p[:,0],p[:,1])
MM=w.edges2mat(edges,N,M)
ax.add_patch(Rectangle((80,80),20,20,facecolor="grey"))

   
    
        
        


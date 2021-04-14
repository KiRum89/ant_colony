import world as w

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from ant import Ant
if __name__ == "__main__":
    N,M = w.N,w.M
    board = w.init_board(N,M) 
    pherom_arr = w.init_weights(N,M)
    ax = plt.subplot(111)
    x = 10
    ants = []
    count = 0
    for i in range(0,20):
        ants.append(Ant(0,0))
    for t in range(0,8000):

        for a in ants:
            #print('time {}'.format(t))
            
            
            if w.region(a,15,15,5,5,M):
                #print('food')
                a.going_back = True
            if a.going_back == True:
                #food source
                a.t+=1
                #print(a.t, len(a.path))
                if a.t == len(a.path):
                    count+=1 
                    print(count)
                    # time to get back
                    a.deposit(x,pherom_arr)
                    a.move(0)
                    a.oldpos=None
                       
                    child=a.decide(pherom_arr)
                    a.path = [0]
                     
                    a.t=0
                    a.going_back = False
            else:

                child=a.decide(pherom_arr)
                a.move(child)
            #evaporate 
        w.evaporate(pherom_arr,0.0001)
pherom_arr[0]=0
def get_path(a):
    p = []
    for n in a.path:
        i,j = w.get_row_col(n,M)
        p.append([i,j])
    p = np.array(p)
    return p

for a in ants:
    p = []
    for n in a.path:
        i,j = w.get_row_col(n,M)
        p.append([i,j])
    p = np.array(p)
    ax.plot(p[:,0],p[:,1])

mat = w.pherom2mat(pherom_arr,N,M)
plt.imshow(mat)
plt.show()

   
    
        
        


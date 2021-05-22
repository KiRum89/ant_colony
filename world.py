import numpy as np
from scipy.ndimage import convolve
import world as w
H,W = 200,200
M,N = 200,200
ones=np.ones((N,M))
def init(H,W,):
    pass
def evap(trail, timer,ctime):
    # ctime current time
    # if timer is exceeded, delet the pheromone 
    
    trail-=1e-3
    trail[np.where(trail<0)]=0

def diffuse(trail):
    M = 1/658*np.array([[1,1,1],[1,650,1],[1,1,1]])    
    return convolve(trail, M, mode='constant', cval=0.0)
    

                

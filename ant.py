import numpy as np

import matplotlib.pyplot as plt
import world as w

class Ant:
    def __init__(self,x,y,r,phi,speed,t):
        self.x = x
        self.dx = 0
        self.y = y
        self.dy=0
        self.scout = False
        self.t = 0
        self.phi = phi
        self.speed  = speed
        self.path = []

    def move(self):
        self.dx = self.speed*np.cos(self.phi) 
        self.dy=self.speed*np.sin(self.phi) 

        x = self.x + self.dx
        y = self.y + self.dy
        if 0<=x<=100 and 0<=y<=100:
            pass
        else:
            self.phi = self.phi + np.pi
            x = self.x + self.dx 
            y = self.y + self.dy
 
        self.x = x
        self.y = y 
        self.path.append([self.x,self.y])
    def decide(self,*pherom_arr):
         
        self.phi = np.random.uniform(self.phi-0.2,self.phi+0.2) 
        

    def get_cell(self):
        #TODO: improbe 
        X=np.linspace(0,100,100)
        Y = np.linspace(0,100,100)
        dx=np.diff(X)[0]
        idx_x = np.where(X<=self.x)[0][-1]*dx
        idx_y = np.where(Y<=self.y)[0][-1]*dx
        return [idx_x,idx_y]

     
def run2(ants,cells):

    for ant in ants: 
        for t in range(0,100):
            ant.decide()
            ant.move()
            cells.append(ant.get_cell())
    cells = np.array(cells)
    fig,ax = plt.subplots(1,1)
    def draw_grid(ax):
        ax.vlines(np.linspace(0,100,100),0,100)
        ax.hlines(np.linspace(0,100,100),0,100)
    def plot(ants):            
        for ant in ants:
            path = np.array(ant.path)
            ax.plot(path[:,0],path[:,1],'-x')
            ax.plot(cells[:,0],cells[:,1],'+') 
    plot(ants)       
    draw_grid(ax)
    ax.set_xlim([0,100])
    ax.set_ylim([0,100])
    plt.show()
   

if __name__ == "__main__":

    ants=[Ant(10,10,1,np.pi/3,1,0),Ant(10,10,1,np.pi/3,1,0),Ant(10,10,1,np.pi/3,1,0)]
    ant = ants[0] 

    cells = []


               
    run2(ants,cells)

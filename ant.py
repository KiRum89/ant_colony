import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
        self.phi_arr = []

    def move(self):
        self.dx = self.speed*np.cos(self.phi) 
        self.dy=self.speed*np.sin(self.phi) 

        x = self.x + self.dx
        y = self.y + self.dy
        if 5<=x<=w.W-5 and 5<=y<=w.H-5:
            pass
        else:
            self.phi = self.phi + np.pi
            x = self.x + self.dx 
            y = self.y + self.dy

        self.x = x
        self.y = y 
        self.path.append([self.x,self.y])
        self.phi_arr.append(self.phi)
    def decide(self,*pherom_arr):
         
        self.phi = np.random.uniform(self.phi-0.2,self.phi+0.2) 
        

    def get_cell(self):
        #TODO: improbe 
        X=np.linspace(0,w.W,100)
        Y = np.linspace(0,w.H,100)
        dx=np.diff(X)[0]
        idx_x = np.where(X<=self.x)[0][-1]
        idx_y = np.where(Y<=self.y)[0][-1]
        return [idx_x,idx_y]

    def mark_home(self,trail_home):
        i,j=self.get_cell()
        if (i,j) not in trail_home:
            trail_home[(i,j)]=[[self.x,self.y]]
        else:
            trail_home[(i,j)].append([self.x,self.y])
    
        
    def go_home(self,trail_home):
        pass

        

     
def run2(ants,cells):
    pherom_home = {}
    for ant in ants: 
        for t in range(0,500):

            ant.mark_home(pherom_home)
            ant.decide()
            ant.move()
            cells.append(ant.get_cell())
    cells = np.array(cells)
    fig,ax = plt.subplots(1,1)
    def draw_grid(ax):
        ax.vlines(np.linspace(0,w.W,100),0,100)
        ax.hlines(np.linspace(0,w.H,100),0,100)

    def plot(ants):            
        for ant in ants:
            path = np.array(ant.path)
            ax.plot(path[:,0],path[:,1],'-')
            #ax.plot(cells[:,0],cells[:,1],'+') 
    def draw_sight(ant):
        phis = np.array(ant.phi_arr)
        path = np.array(ant.path)
        for pos,phi in zip(path[::2],phis[::2]):    
            x,y = pos
            phi1,phi2 = np.rad2deg(phi+np.array([-0.2,0.2]))
            ax.add_patch(
            patches.Wedge(
                (x, y),         # (x,y)
                3,            # radius
                phi1,             # theta1 (in degrees)
                phi2,            # theta2
                color="g", alpha=0.2
                )
            )
                    
                
        

    plot(ants)    
    for ant in ants:   
        draw_sight(ant)
    #draw_grid(ax)
    ax.set_xlim([0,w.W])
    ax.set_ylim([0,w.H])
    plt.show()
    return pherom_home 

if __name__ == "__main__":

    ants=[Ant(10,10,1,np.pi/3,0.6,0),Ant(10,10,1,np.pi/3,0.6,0),Ant(10,10,1,np.pi/3,0.6,0)]
    ant = ants[0] 

    cells = []


               
    pherom_trail=run2(ants,cells)

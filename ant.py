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
        self.r = r
        self.scout = False
        self.t = 0
        self.phi = phi # direction of propagation 
        self.alpha = 0.3 # angular aperture of the ant (width of the vision
        self.speed  = speed
        self.path = []
        self.phi_arr = []

    def move(self):
        #TODO properly handle the case when the ant is outside the box
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
        self.phi = np.random.uniform(self.phi-self.alpha,self.phi+self.alpha) 
        

    def get_cell(self,x,y):
        
        #TODO: improve 
        X=np.linspace(0,w.W,100)
        Y = np.linspace(0,w.H,100)
        dx=np.diff(X)[0]
        idx_x = np.where(X<=x)[0][-1]
        idx_y = np.where(Y<=y)[0][-1]
        return [idx_x,idx_y]

    def mark_trail(self,trail):
        # trail can be scout trail - trail ant passed before food
        # trail_cargo - ant has food and goes follows the trail_scout
        i,j=self.get_cell(self.x, self.y)
        if (i,j) not in trail:
            trail[(i,j)]=[[self.x,self.y]]
        else:
            trail[(i,j)].append([self.x,self.y])
    
        

    def go_home(self,trail):
        # count of pheromes in the central part 
        # count pgeromes in the sides
        dphi = 2*self.alpha/3
        cells=self.get_sector_cell(self.x,self.y) #min to max
        #TODO: finish sectors 
        #central:
        idxs_min,idxs_max = cells
        for i in range(idxs_min[0],idxs_max[0]):  
            for j in range(idxs_min[1],idxs_max[1]):
               pass
        
    def get_sector_cells(self):
        # TODO: make more elegant return generator?

        #finidh finding the cells that a covered by the sector (it will be a rectangular. Find the min y, cover till y max, move until the x of the 3d vortex) 
        x = self.x
        y = self.y
        x1 = self.x+self.r*np.cos(self.phi-self.alpha)    
        x2 = self.x+self.r*np.cos(self.phi+self.alpha)    
        y1= self.y+self.r*np.sin(self.phi-self.alpha)    
        y2 = self.y+self.r*np.sin(self.phi+self.alpha)    
        
        [xi,yi]=self.get_cell(x,y)
        [x1i,y1i] = self.get_cell(x1,y1)
        [x2i,y2i]=self.get_cell(x2,y2)

        xi_min=min(xi,x1i,x2i)
        xi_max = max(xi,x1i,x2i)

        yi_min=min(yi,y1i,y2i)
        yi_max=max(yi,y1i,y2i)

        return [(xi_min,yi_min),(xi_max,yi_max)]
        
        




 
if __name__ == "__main__":
    def run2(ants,cells):
        trail = {}
        for ant in ants: 
            for t in range(0,1):
                print(ant.get_sector_cells())

                cells.append(ant.get_cell(ant.x,ant.y))
                ant.mark_trail(trail)
                ant.decide()
                ant.move()
        cells = np.array(cells)
        fig,ax = plt.subplots(1,1)
        def draw_grid(ax):
            ax.vlines(np.linspace(0,w.W,100),0,100)
            ax.hlines(np.linspace(0,w.H,100),0,100)

        def plot(ants):            
            for ant in ants:
                path = np.array(ant.path)
                ax.plot(path[:,0],path[:,1],'+')
                #ax.plot(cells[:,0],cells[:,1],'+') 
        def draw_sight(ant):
            phis = np.array(ant.phi_arr)
            path = np.array(ant.path)
            for pos,phi in zip(path[::5],phis[::5]):    
                x,y = pos
                phi1,phi2 = np.rad2deg(phi+np.array([-ant.alpha,ant.alpha]))
                ax.add_patch(
                patches.Wedge(
                    (x, y),         # (x,y)
                    5,            # radius
                    phi1,             # theta1 (in degrees)
                    phi2,            # theta2
                    color="g", alpha=0.2
                    )
                )
                ax.add_patch(
                patches.Wedge(
                    (x, y),         # (x,y)
                    5,            # radius
                    phi1+np.rad2deg(0.2),             # theta1 (in degrees)
                    phi2-np.rad2deg(0.2),            # theta2
                    color="r", alpha=0.2
                    )
               ) 
                        
                    
                

        plot(ants)    
        for ant in ants:   
            draw_sight(ant)
        draw_grid(ax)
        ax.set_xlim([0,w.W])
        ax.set_ylim([0,w.H])
        plt.show()
        return trail 


    ants=[Ant(10,10,5,np.pi/3,0.6,0),Ant(10,10,5,np.pi/3,0.6,0),Ant(10,10,5,np.pi/3,0.6,0)]
    ant = ants[0] 

    cells = []


               
    trail=run2(ants,cells)

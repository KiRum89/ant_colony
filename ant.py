import numpy as np
import matplotlib
import matplotlib.pyplot as plt

plt.ion()
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
        if 0<=x<=w.W and 0<=y<=w.H:
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
        self.phi = np.random.uniform(self.phi-self.alpha/2,self.phi+self.alpha/2) 
        

    def get_cell(self,x,y):
        
        #TODO: improve 
        X=np.linspace(0,w.W,w.W)
        Y = np.linspace(0,w.H,w.H)
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
        #trail is a dict. Keys are cell (i,j), values are pheromome coordinates
        # count of pheromes in the central part 
        # count pgeromes in the sides
        dphi = self.alpha/3

        pos = np.array([self.x, self.y])
        count1=0
        count2=0 #count of pheromones in the central part
        count3=0
        e = np.array([np.sin(self.phi),-np.cos(self.phi)])
        for (i,j) in self.get_sector_cells():
            pheroms = trail.get((i,j),None)         
            
            if pheroms!=None:
                for pher in pheroms:
                    print(pheroms)
                    vec=np.array(pher)-pos
                    vec_norm=np.sum(vec*vec)**0.5
                    theta=np.arccos(np.sum(vec*e)/vec_norm)
                    if np.pi/2+ant.alpha/2-ant.alpha/3<theta<np.pi/2+ant.alpha/2:

                        count1+=1
                    elif np.pi/2-ant.alpha/6<theta<np.pi/2+ant.alpha/6:
                        count2+=1
                    elif np.pi/2-ant.alpha/2<theta<np.pi/2-ant.alpha/2+ant.alpha/3:

                        count3+=1
                        
        print(count1,count2,count3)
             

        
    def get_sector_cells(self):
        # TODO: make more elegant 
        # return generator - yes

        #finidh finding the cells that a covered by the sector (it will be a rectangular. Find the min y, cover till y max, move until the x of the 3d vortex) 
        x = self.x
        y = self.y

        x1 = self.x+self.r*np.cos(self.phi-self.alpha/2)    
        y1= self.y+self.r*np.sin(self.phi-self.alpha/2)    

        x2 = self.x+self.r*np.cos(self.phi+self.alpha/2)    
        y2 = self.y+self.r*np.sin(self.phi+self.alpha/2)    
        
        [xi,yi]=self.get_cell(x,y)
        [x1i,y1i] = self.get_cell(x1,y1)
        [x2i,y2i]=self.get_cell(x2,y2)

        xi_min=min(xi,x1i,x2i)
        xi_max = max(xi,x1i,x2i)

        yi_min=min(yi,y1i,y2i)
        yi_max=max(yi,y1i,y2i)

        print(xi_min,xi_max,yi_min,yi_max) 
        for i in range(xi_min,xi_max+1):  
            for j in range(yi_min, yi_max+1):
                yield (i,j)
        




 
if __name__ == "__main__":
    def run2(ants,cells):
        trail = {}
        for ant in ants: 
            print('------')
            for t in range(0,1):
                ant.mark_trail(trail)
                ant.decide()
                ant.move()
                for cell in ant.get_sector_cells():
                    print('cell {}'.format(cell))


                cells.append(ant.get_cell(ant.x,ant.y))

        cells = np.array(cells)
        fig,ax = plt.subplots(1,1)
        def draw_grid(ax):
            ax.vlines(np.linspace(0,w.W,w.W),0,w.H)
            ax.hlines(np.linspace(0,w.H,w.H),0,w.W)

        def plot(ants):            
            for ant in ants:
                path = np.array(ant.path)
                ax.plot(path[:,0],path[:,1],'+')
                #ax.plot(cells[:,0],cells[:,1],'+') 

        def onclick(event):
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))
            print(ant.get_cell(event.xdata,event.ydata))
            cell = tuple(ant.get_cell(event.xdata,event.ydata))
            if cell not in trail:
                trail[cell]=[[event.xdata,event.ydata]]
            else:
                trail[cell].append([event.xdata,event.ydata])
   
            #print(trail)
            get_part(ant,[event.xdata, event.ydata])
            

        cid = fig.canvas.mpl_connect('button_press_event', onclick)

        def get_part(ant,pher):
            pos = np.array([ant.x,ant.y])
             
            vec=np.array(pher)-pos
            #print(vec)
            vec_norm=np.sum(vec*vec)**0.5
            e = np.array([np.sin(ant.phi),-np.cos(ant.phi)])
            theta=np.arccos(np.sum(vec*e)/vec_norm)
            #print(theta,ant.phi,e,vec) 
            print(np.pi/2+ant.alpha/2,theta,np.pi/2+ant.alpha/2-ant.alpha/3)
            if np.pi/2+ant.alpha/2-ant.alpha/3<theta<np.pi/2+ant.alpha/2:
                print('l') 
            elif np.pi/2-ant.alpha/6<theta<np.pi/2+ant.alpha/6:
                print('c')
    
            elif np.pi/2-ant.alpha/2<theta<np.pi/2-ant.alpha/2+ant.alpha/3:
                print('r')


        def draw_sight(ant):
            phis = np.array(ant.phi_arr)
            path = np.array(ant.path)
            for pos,phi in zip(path[::1],phis[::1]):    
                x,y = pos
                phi1,phi2 = np.rad2deg(phi+np.array([-ant.alpha/2,ant.alpha/2]))
                ax.add_patch(
                patches.Wedge(
                    (x, y),         # (x,y)
                    ant.r,            # radius
                    phi1,             # theta1 (in degrees)
                    phi2,            # theta2
                    color="g", alpha=0.2
                    )
                )
                ax.add_patch(
                patches.Wedge(
                    (x, y),         # (x,y)
                    ant.r,            # radius
                    phi1+np.rad2deg(ant.alpha/3),             # theta1 (in degrees)
                    phi2-np.rad2deg(ant.alpha/3),            # theta2
                    color="r", alpha=0.2
                    )
               ) 
                        
                    
        #ant.go_home(trail)                

        plot(ants)    
        for ant in ants:   
            draw_sight(ant)
        draw_grid(ax)
        ax.set_xlim([0,w.W])
        ax.set_ylim([0,w.H])
        plt.show()
        return trail 


    ants=[Ant(2,2,6,np.pi/3,0.6,0)]
    ant = ants[0] 

    cells = []


               
    trail=run2(ants,cells)
    

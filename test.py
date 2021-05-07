import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation
from ant import Ant
fig,ax = plt.subplots(1,1)

class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('click', event)
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
        cell = tuple(ant.get_cell(np.array([event.xdata,event.ydata])))
        if cell not in trail:
            trail[cell]=[np.array([event.xdata,event.ydata])]
        else:
            trail[cell].append(np.array([event.xdata,event.ydata]))
     
class Mover:
    def __init__(self,arrows):
        self.arrows = arrows
        self.xs = list([0])
        self.ys = list([0])
        
        self.cid = line.figure.canvas.mpl_connect('key_press_event', self)

    def __call__(self, event):
        
        print('click',event)
        self.xs.append(event.xdata)
        self.ys.append(event.ydata) 
        #self.arrow.set_xy([[ant.r[0],ant.r[1]],[ant.r[0]+ant.dr[0],ant.r[1]+ant.dr[1]]])  
        for arrow in self.arrows:
            arrow.figure.canvas.draw()
        ex = ant.dr/ant.norm(ant.dr) 
        ey = ant.rotate(ex,np.pi/2)
        angles = np.linspace(-ant.alpha/2,ant.alpha/2,4)
        for ang,arrow in zip(angles,self.arrows):
            d =ant.R*(np.cos(ang)*ex + np.sin(ang)*ey) 
            arrow.set_xy([[ant.r[0],ant.r[1]],[d[0]+ant.r[0],d[1]+ant.r[1]]])
        
        ant.decide(trail)
        ant.move() 
        #print(ant.get_pherom_counts(trail))

ant=Ant(np.array([1,1]),5,np.pi/3,0.1,0)
           
trail={}
ant.decide(trail)            
#ant.move()
line, = ax.plot([0],[0],'+')
linebuilder = LineBuilder(line)

arrows=[ax.arrow(0,0,5,5) for _ in range(0,4)]
mover=Mover(arrows)

#draw_sight(ant,ax)
ax.set_xlim([0,w.W])
ax.set_ylim([0,w.H])



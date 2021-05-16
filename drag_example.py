import sys
import pygame

pygame.init()
gameDisplay = pygame.display.set_mode((500,500))

clock = pygame.time.Clock()
x0,y0,R = 20,20,20
while 1:

    #gameDisplay.fill((0,0,0))
    print(x0,y0)
    pygame.draw.circle(gameDisplay,(0,255,0),(x0,y0),R)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
    x,y=pygame.mouse.get_pos()
    if ((x0-x)**2+(y0-y)**2)**0.5<R:
        
        state = pygame.mouse.get_pressed(num_buttons=3) 
        if state[0]==True:
            #     print('lala')
                                     
            x0,y0=pygame.mouse.get_pos()

        
    pygame.display.update()

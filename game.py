import pygame
import world as w
pygame.init()
gameDisplay = pygame.display.set_mode((w.W,w.H))
surf = pygame.Surface((w.W,w.H))
blue = (0,0,255)
rect = pygame.Rect(1,1,10,10)

pygame.draw.rect(gameDisplay,blue,rect)

pygame.display.update()
while True:
    pass

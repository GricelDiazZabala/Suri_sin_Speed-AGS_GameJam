import pygame
import sys
import os

WIDHT = 1100
HEIGHT = 700
BG = pygame.image.load("assets\Pixel Adventure 1\Free\Background\Pink.png")
BG = pygame.transform.scale(BG,(WIDHT,HEIGHT))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


pygame.init()
screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Suri sin Speed")

def draw():
    screen.blit(BG,(0,0))
    pygame.display.update()
    

def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw()
    
    pygame.quit()  

if __name__ == "__main__":
    main()

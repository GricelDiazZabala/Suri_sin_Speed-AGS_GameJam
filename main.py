import pygame
import sys
import os

WIDHT = 1100
HEIGHT = 700
BG = pygame.transform.scale(pygame.image.load("assets\Pixel Adventure 1\Free\Background\Pink.png"),(WIDHT,HEIGHT))

SURI_WIDTH = 40
SURI_HEIGHT = 60

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


pygame.init()
screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Suri sin Speed")

def draw(suri):
    screen.blit(BG,(0,0))

    pygame.draw.rect(screen, "red", suri)

    pygame.display.update()
    

def main():
    run = True

    suri = pygame.Rect(200, HEIGHT - SURI_HEIGHT, SURI_WIDTH, SURI_HEIGHT)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(suri)
    
    pygame.quit()  

if __name__ == "__main__":
    main()

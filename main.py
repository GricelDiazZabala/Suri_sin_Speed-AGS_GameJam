import pygame
pygame.init()
import sys
import os
import spritesheet
pygame.font.init()
pygame.display.init()

WIDHT = 1100
HEIGHT = 700

screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Suri sin Speed")

BLACK = (0,0,0)
BG = pygame.transform.scale(pygame.image.load("assets\Pixel Adventure 1\Free\Background\Pink.png"),(WIDHT,HEIGHT))
FONT = pygame.font.SysFont("arial", 30)

SURI_CHAR_DOUBLE_JUMP = pygame.image.load("assets\Pixel Adventure 1\Free\Main Characters\Pink Man\Double Jump (32x32).png").convert_alpha()
SURI_CHAR_FALL = pygame.image.load("assets\Pixel Adventure 1\Free\Main Characters\Pink Man\Fall (32x32).png").convert_alpha()
SURI_CHAR_HIT = pygame.image.load("assets\Pixel Adventure 1\Free\Main Characters\Pink Man\Hit (32x32).png").convert_alpha()
SURI_CHAR_IDLE = pygame.image.load("assets\Pixel Adventure 1\Free\Main Characters\Pink Man\Idle (32x32).png").convert_alpha()
SURI_CHAR_JUMP = pygame.image.load("assets\Pixel Adventure 1\Free\Main Characters\Pink Man\Jump (32x32).png").convert_alpha()
SURI_CHAR_RUN = pygame.image.load("assets\Pixel Adventure 1\Free\Main Characters\Pink Man\Run (32x32).png").convert_alpha()
SURI_CHAR_WALL_JUMP = pygame.image.load("assets\Pixel Adventure 1\Free\Main Characters\Pink Man\Wall Jump (32x32).png").convert_alpha()

SURI_WIDTH = 40
SURI_HEIGHT = 60

SURI_VEL = 5

sprite_sheet = spritesheet.SpriteSheet(SURI_CHAR_IDLE)

animation_list = []
animation_steps = 11
last_update = pygame.time.get_ticks()
animation_cooldown = 500
frame = 0

for x in range(animation_steps):
    animation_list.append(sprite_sheet.get_image(0, 32, 32, 3, BLACK))


def main():
    run = True

    suri = pygame.Rect(200, HEIGHT - SURI_HEIGHT, SURI_WIDTH, SURI_HEIGHT)
    
    reloj = pygame.time.Clock()

    while run:

        reloj.tick(60)

        screen.blit(animation_list[frame], (x * 72 , 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and suri.x - SURI_VEL >= 0:
            suri.x -= SURI_VEL
        if keys[pygame.K_d] and suri.x + SURI_VEL + suri.width <= WIDHT:
            suri.x += SURI_VEL
  
    
    pygame.quit()  

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    main()

import pygame
from sprites import *
from config import *
import sys
pygame.font.init()
custom_font = pygame.font.SysFont('impact', 20 )
class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True


        self.character_spritesheet = Spritesheet('assets\suri\suri_sprite_sheet.png')
        self.terrain_spritesheet = Spritesheet('assets\Pixel Art Top Down - Basic v1.2.2\Texture\TX Tileset Grass.png')
        self.props_spritesheet = Spritesheet('assets\Pixel Art Top Down - Basic v1.2.2\Texture\TX Props.png')
        self.speed_img = pygame.image.load('assets\otros\SPEED.png').convert_alpha()     
        self.intro_background = pygame.image.load('assets/otros/2.png').convert_alpha()
        self.go_background = pygame.image.load('assets/otros/2.png').convert_alpha()

        self.current_level = 0
        self.max_level = 4
        self.player = None

    def createTileMap(self, level_map):
        player_created = False
        for i, row in enumerate(level_map):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P" and not player_created:
                    self.player = Player(self, j, i)
                    player_created = True
                elif column == "P" and player_created:
                    Ground(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "C":
                    Item(self, j, i)
        
        if not player_created:
            self.player = Player(self, 1, 1)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.LayeredUpdates()

        self.createTileMap(level_maps[self.current_level])

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        if self.player:
            level_text = custom_font.render(f'Nivel: {self.current_level + 1}', True, WHITE)
            enemies_text = custom_font.render(f'Enemigos restantes: {len(self.enemies)}', True, WHITE)
            items_text = custom_font.render(f'Speeds restantes: {len(self.items)}', True, WHITE)
            health_text = custom_font.render(f'Vida: {self.player.health}', True, WHITE)
            
            self.screen.blit(level_text, (10, 10))
            self.screen.blit(enemies_text, (10, 50))
            self.screen.blit(items_text, (10, 90))
            self.screen.blit(health_text, (10, 130))
        
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
    
    def level_up(self):
        if self.current_level < self.max_level:
            self.current_level += 1

            for sprite in self.all_sprites:
                sprite.kill()
                
            self.player = None
                
            self.new()

            self.show_level_transition()
        else:

            self.game_completed()

    def show_level_transition(self):
        transition = True
        level_text = self.custom_font.render(f'Nivel {self.current_level + 1}', True, WHITE)
        continue_text = self.custom_font.render('PPresiona cualquier tecla para continuar', True, WHITE)
        
        while transition:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    transition = False
                    self.playing = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    transition = False
            
            self.screen.fill(BLACK)
            self.screen.blit(level_text, (SCREEN_WIDTH/2 - level_text.get_width()/2, SCREEN_HEIGHT/2 - 50))
            self.screen.blit(continue_text, (SCREEN_WIDTH/2 - continue_text.get_width()/2, SCREEN_HEIGHT/2 + 50))
            pygame.display.update()
            self.clock.tick(FPS)

    def game_completed(self):
        completed = True
        congrats_text = self.custom_font.render('¡Completaste todos los niveles', True, YELLOW)
        restart_text = self.custom_font.render('Apretá R para reiniciar o Q para salir', True, YELLOW)
        
        while completed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    completed = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        completed = False
                        self.current_level = 0
                        self.new()
                        self.main()
                    if event.key == pygame.K_q:
                        completed = False
                        self.running = False
            
            self.screen.fill(BLACK)
            self.screen.blit(congrats_text, (SCREEN_WIDTH/2 - congrats_text.get_width()/2, SCREEN_HEIGHT/2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH/2 - restart_text.get_width()/2, SCREEN_HEIGHT/2 + 50))
            pygame.display.update()
            self.clock.tick(FPS)

    def game_over(self):
        text = self.custom_font.render('Game Over', True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        restart_button = Button(10, SCREEN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Reiniciar')

        for sprite in self.all_sprites:
            sprite.kill()

        self.player = None

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.current_level = 0
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        title = custom_font.render('Suri sin speed', True, YELLOW)
        title_rect = title.get_rect(x=330, y=260)

        play_button = Button(380, 470, 100, 50, BLACK, YELLOW, 'Jugar')

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
            
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
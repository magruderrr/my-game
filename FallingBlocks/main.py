import pygame
from sys import exit
import random

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        player_1 = pygame.image.load('graphics/purple_character1.png').convert_alpha()
        player_1 = pygame.transform.scale2x(player_1)
        player_2 = pygame.image.load('graphics/purple_character2.png').convert_alpha()
        player_2 = pygame.transform.scale2x(player_2)
        self.player_walk = [player_1, player_2]
        self.player_index = 0
        self.facing_left = False
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 600))

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5
            self.facing_left = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5
            self.facing_left = False
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

    def animation_state(self):
        self.player_index += 0.1

        if self.player_index >= len(self.player_walk):
            self.player_index = 0

        self.image = self.player_walk[int(self.player_index)]

    def invert_image(self):

        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image

    def update(self):
        self.animation_state()
        self.movement()
        self.invert_image()

    def collisions(player, circles):
        if circles:
            for circle in circles:
                if player.rect.colliderect(circle.rect):
                    return True

class Circle(pygame.sprite.Sprite):

    def __init__(self, x, y, speed):

        super().__init__()
        self.image = pygame.image.load('graphics/Ball.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.fall_speed = speed
        self.y = float(y)
        
    def update(self):
        self.fall_speed += 0.01
        self.y += self.fall_speed
        self.rect.y = int(self.y)

        if self.rect.top > 650:
            self.y = 0
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, 800)

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("DODGE THE BLOCKS")
clock = pygame.time.Clock()
game_active = True
player_group = pygame.sprite.GroupSingle()
player_group.add(Player())
circle_group = pygame.sprite.Group()
score_value = 0

font = pygame.font.Font('font/Pixeltype.ttf', 50)
# initial score surface
score_surf = font.render(str(score_value), False, (64,64,64))
score_rect = score_surf.get_rect(center = (400,50))


ball_speed = 0

amount = 1
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer, 5000)

score_timer = pygame.USEREVENT + 2
pygame.time.set_timer(score_timer, 1000)

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                score_value = 0
                ball_speed = 0
                circle_group.empty()
                pygame.time.set_timer(timer, 5000)
        
        if event.type == score_timer and game_active:
            score_value += 1
            score_surf = font.render(str(score_value), False, (64,64,64))
        
        if event.type == timer and game_active:
            for _ in range(amount):
                x = random.randint(0, 800)
                y = random.randint(0, 300)
                circle = Circle(x, y, ball_speed)
                circle_group.add(circle)
        player = player_group.sprite
        if player.collisions(circle_group.sprites()):
            game_active = False

    screen.fill((50, 250, 230))
    screen.blit(score_surf, score_rect)

    if game_active:
        player_group.draw(screen)
        player_group.update()
        circle_group.draw(screen)
        circle_group.update()
        ball_speed += 0.01
    

    pygame.display.update()

    clock.tick(60)
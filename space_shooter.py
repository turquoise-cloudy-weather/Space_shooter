import pygame
import sys
from os.path import join
import random

# classes

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2, 3*WINDOW_HEIGHT/4))
        self.direction = pygame.Vector2()
        self.speed = 300
        
        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 2000

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time > self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, x, y, surf):
        super().__init__(groups)
        self.image = surf
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(x,y))

class Laser(pygame.sprite.Sprite):   
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_frect(midbottom = pos)
        

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.create_time = pygame.time.get_ticks()

    def meteor_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.create_time > 2000:
            self.kill()

    def update(self, dt):
        self.rect.centery += 200 *dt
        self.meteor_timer()
        if self.rect.top > WINDOW_HEIGHT:
           self.kill()
# setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True

#clock
clock = pygame.time.Clock()

# window options
player_img = pygame.image.load('images/player.png') 
pygame.display.set_caption("Space Shooter")
pygame.display.set_icon(player_img)



#laser setup


# creating background, taking care of cursor
pygame.mouse.set_visible(False)

# importing surfaces
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha() 
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()  
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()

# sprites
all_sprites = pygame.sprite.Group()
stars_num = 20
for i in range(stars_num):
    star = Star(all_sprites, random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT), star_surf)
    

# creating objects
player = Player(all_sprites)


# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)



while running:
    dt = clock.tick(60) /1000
    display_surface.fill("darkgray")
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            meteor = Meteor(meteor_surf, (random.randint(0, WINDOW_WIDTH), 0),all_sprites)
   
    player.update(dt)
    
    
    all_sprites.update(dt)
    all_sprites.draw(display_surface)
    pygame.display.update()
    
pygame.quit()
sys.exit()
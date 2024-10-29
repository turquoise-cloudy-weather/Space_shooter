import pygame
import sys
from os.path import join
import random

# setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True

player_img = pygame.image.load('images/player.png') 
pygame.display.set_caption("Space Shooter")
pygame.display.set_icon(player_img)

surf = pygame.Surface((50, 50))
surf.fill("Orange")

player_surf_path = join('images', 'player.png')
player_surf = pygame.image.load(player_surf_path).convert_alpha()
player_rect = player_surf.get_rect(center = (WINDOW_WIDTH/2, 3*WINDOW_HEIGHT/4))

star_surf_path = join('images', 'star.png')
star_surf = pygame.image.load(star_surf_path).convert_alpha() 

meteor_surf_path = join('images', 'meteor.png')
meteor_surf = pygame.image.load(meteor_surf_path).convert_alpha()
meteor_rect = meteor_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

laser_surf_path = join('images', 'laser.png')
laser_surf = pygame.image.load(laser_surf_path).convert_alpha()
laser_rect = laser_surf.get_rect(bottomleft = (20, WINDOW_HEIGHT - 20))

pygame.mouse.set_visible(False)
star_list = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]
speed = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    display_surface.fill("darkgray")

    for star in star_list:
        display_surface.blit(star_surf, star)

    player_rect.right += speed
    
    if player_rect.right >= WINDOW_WIDTH or player_rect.left <= 0:
        speed *=-1
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)
    display_surface.blit(player_surf, player_rect)

    pygame.display.update()
    
    


pygame.quit()
sys.exit()
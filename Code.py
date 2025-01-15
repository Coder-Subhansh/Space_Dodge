import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import pygame
import time
import random
from sys import exit
icon=pygame.image.load("rocket.png")
pygame.display.set_icon(icon)

def get_settings(): 
    return {
        "screen": {"width": 1000, "height": 700},
        "player": {"width": 40, "height": 60, "vel": 5},  
        "star": {"width": 10, "height": 20, "vel": 1},    
        "hit": False,"Life":3
    }

def initialize_game():
    pygame.init()
    pygame.font.init()
    settings = get_settings()  
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((settings["screen"]["width"], settings["screen"]["height"]))
    pygame.display.set_caption("Space Dodge")
    
    # Load and scale images
    space = pygame.transform.scale(
        pygame.image.load("space.jpg"),
        (settings["screen"]["width"], settings["screen"]["height"])
    )
    
    font = pygame.font.SysFont("comicsans", 30)  
    
    player_image = pygame.transform.scale(
        pygame.image.load("spaceship.jpg"),
        (settings["player"]["width"], settings["player"]["height"])
    )
    
    star_image = pygame.transform.scale(
        pygame.image.load("asteroid.jpg"),
        (settings["star"]["width"], settings["star"]["height"])
    )
    
    return settings, clock, screen, space, font, player_image, star_image

def draw(screen, space, player_image, star_image, player_rect, elapsed_time, stars, font,settings):
    screen.blit(space, (0, 0))
    time_text = font.render(f"Time: {round(elapsed_time)}s", 1, "white")
    life_text=font.render (f"Life:{round(settings["Life"])}",1,"red")
    screen.blit(time_text, (10, 10))
    screen.blit(life_text,(900,20))
    screen.blit(player_image, player_rect)
    for star_rect in stars:
        screen.blit(star_image, star_rect)
    pygame.display.update()

def main():
    settings, clock, screen, space, font, player_image, star_image = initialize_game()
    start_time = time.time()
    
    run = True
    star_add_increment = 2000
    star_count = 0
    stars = []
    
    player_rect = pygame.Rect(
        500,
        settings["screen"]["height"] - settings["player"]["height"],
        settings["player"]["width"],
        settings["player"]["height"]
    )
    
    while run:
        star_count += clock.tick(60)
        
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, settings["screen"]["width"] - settings["star"]["width"])
                star_rect = pygame.Rect(star_x, -settings["star"]["height"], settings["star"]["width"], settings["star"]["height"])
                stars.append(star_rect)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
        
        elapsed_time = time.time() - start_time
        keys = pygame.key.get_pressed()
        
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_rect.x - settings["player"]["vel"] >= 0:
            player_rect.x -= settings["player"]["vel"]
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_rect.x + settings["player"]["vel"] + settings["player"]["width"] <= settings["screen"]["width"]:
            player_rect.x += settings["player"]["vel"]
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.y - settings["player"]["vel"] > 0:
            player_rect.y -= settings["player"]["vel"]
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_rect.y + settings["player"]["vel"] + settings["player"]["height"] < settings["screen"]["height"]:
            player_rect.y += settings["player"]["vel"]
        
        for star_rect in stars[:]:
            star_rect.y += settings["star"]["vel"]
            if star_rect.y > settings["screen"]["height"]:
                stars.remove(star_rect)
            elif star_rect.colliderect(player_rect):
                stars.remove(star_rect)
                settings["hit"] = True
                settings["Life"]-=1
                break
        if settings["Life"] ==0:
            lost_text=font.render("YOU LOST!",2,"red")
            screen.blit(lost_text,(settings["screen"]["width"]/2-lost_text.get_width()/2,settings["screen"]["height"]/2-lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break
        
        draw(screen, space, player_image, star_image, player_rect, elapsed_time, stars, font,settings)

if __name__ == "__main__":
    main()

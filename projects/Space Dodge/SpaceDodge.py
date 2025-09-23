# Author : Killian O'Connor
# Date : 01/08/2025 - 02/08/2025
# Description : A very simple space invaders style game - goal to get a basic understanding of pygame - credit 'TechWithTim' youtube

import pygame
import time
import random

import os
os.chdir(os.path.dirname(__file__)) # had to add in to fix image not found error for background and sprite / player


pygame.font.init()

WIDTH , HEIGHT = 1000 , 800 #size of window
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Space Dodge") # name of window

BG = pygame.transform.scale(pygame.image.load("background.jpeg"), (WIDTH, HEIGHT))# setting up the background making it to scale of wimdow

Player_H = 60
Player_W = 40
PLAYER_VEL = 5

FONT = pygame.font.SysFont("comicsans" , 30) #set font and size
STAR_WIDTH = 5
STAR_HEIGHT = 20
STAR_VEL = 5

def draw(player , elapsed_time, stars):
    
    WIN.blit(BG, (0 , 0)) # select the image and coordinates
    
    time_text = FONT.render(f"Time:{round(elapsed_time)}s",1, "white")  # display the time rounded to seconds in white    
    WIN.blit(time_text,(10,10))
    PLAYER_IMAGE = pygame.image.load("sc1.png").convert_alpha()
    PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (Player_W, Player_H))
    WIN.blit(PLAYER_IMAGE, (player.x, player.y))

    
    for star in stars:
        pygame.draw.rect(WIN , "red" , star)
    
    pygame.display.update() # apply the drawings
def main():
    run = True
    
    player = pygame.Rect(200 , (HEIGHT - Player_H) , Player_W , Player_H )
    
    clock = pygame.time.Clock()#setting up a clock to ensure the game runs at a constant speed across computers  
    start_time = time.time()
    elapsed_time = 0
    # creating the projectiles
    star_add_increment = 2000
    star_count = 0
    
    stars = [] # keep track of falling
    hit = False
    
    
    while run:
        star_count += clock.tick(60) # max frames per second + how many ms before last clock tick
        elapsed_time = time.time() - start_time
        
        if star_count > star_add_increment:
            for i in range(3): # make 3 stars
                star_x = random.randint(0 , WIDTH - STAR_WIDTH) # choose a random x coordinate
                star = pygame.Rect(star_x , -STAR_HEIGHT , STAR_WIDTH , STAR_HEIGHT) # create the star off screen so it can drop down
                stars.append(star) # keep track of stars
            
            star_add_increment = max(200 , star_add_increment - 50) # make the stars appear faster with a max of 200
            star_count = 0   
        
        
        # if the user presses the x exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        keys = pygame.key.get_pressed()
        #move the player if arrow used and ensure they dont go out of screen
        if keys[pygame.K_LEFT ] and player.x - PLAYER_VEL >=0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + Player_W + PLAYER_VEL <=WIDTH:
            player.x += PLAYER_VEL
      
       #moving the stars 
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player): # check if the stars collide - 'star.y + star.height >= player.y' only check if stars collide if they're low enough to hit the player
                stars.remove(star)
                hit = True
                break
        if hit:
            lost_text = FONT.render("You Lost!" , 1 , "white")
            WIN.blit(lost_text , (WIDTH/2 - lost_text.get_width()/2 , HEIGHT/2 - lost_text.get_height()/2))
            
            button_text = FONT.render("Play Again" , 1 , "black")
            button_rect = pygame.Rect( WIDTH /2 - 100, HEIGHT /2 + 50, 200, 50)
            
            pygame.draw.rect(WIN, "white", button_rect)
            WIN.blit(button_text, (( button_rect.x + ( button_rect.width - button_text.get_width() ) // 2) , button_rect.y + 10)) #alligning with the centre of the box
            
            pygame.display.update()
            
            waiting = True # loop so button clicks can be seen
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect.collidepoint(event.pos):
                            main()
                            return

            
            
        draw(player , elapsed_time, stars)
    pygame.quit()
    
if __name__ == "__main__": # makes sure the function only runs if the files called directly and not imported
    main()
    

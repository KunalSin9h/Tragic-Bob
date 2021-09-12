# import the pygame module
import pygame

# Import random for random numbers
import random


#import pygame.locals to easier access to key coordinates.
from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# initialize pygame.
pygame.init()

# Defien constants for the screen width and height.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Define a player object by extending pygame.sprite.Sprite
# the surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("./images/rocket.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -3)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 3)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-3, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(3, 0)

        # keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# define the enemy object by extending pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("./images/bullet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
               random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
               random.randint(0, SCREEN_HEIGHT)
           )
        )
        self.speed = random.randint(5, 20)

    # move the sprite based on speed
    # Remove the sprite when it passed the left edge
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

          
# creat the screen object 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Creat a costom event for adding  a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

#Initialize player. Right now, this is just a rectangle.
player = Player()



# Creat groups to hold enemy sprites and all sprites
# $- enemies is used for collision detection and position updates
# $- all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# variable to keep the main loop running.
running = True

# THE GREAT GAME LOOP
while running:

    # EVENT HANDLER LOOP
    #look at every event in the queue
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # was it the escape key if so, stop the loop;
            if event.key == K_ESCAPE:
                running = False

        # did the user click the window close button? if so, stop the loop
        elif event.type == QUIT:
            running = False
        
        # add a new enemy?
        elif event.type == ADDENEMY:
            # create the new enemu and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # get the set of key pressed and check for user input
    pressed_keys = pygame.key.get_pressed()  # Dictionary.

    #update the player sprite based on user keypress
    player.update(pressed_keys)

    # update enemy position
    enemies.update()

    # fill the screen with white
    screen.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        #if so, then remove the player and stop the loop
        player.kill()
        running = False

    # Update the display.
    pygame.display.flip()

pygame.quit()


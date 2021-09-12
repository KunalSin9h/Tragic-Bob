# simple pygame program

#import and initialize the pygame library
import pygame
pygame.init()

#set up the drawing window
screen = pygame.display.set_mode([500, 500])

# run until the user asks to quit
running = True
while running: # the game loop.

	# did the user click the window close button?
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	# fill the background with white
	screen.fill((225, 225, 225))
	
	#drow a solid blue circle in the centre
	pygame.draw.circle(screen, (0, 0, 225), (250, 250), 75)

	# flip the display
	pygame.display.flip()

# done time to quit
pygame.quit()

import pygame, random
from pygame.locals import *

#Initialize pygame
pygame.init()

#Set display surface
WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600

OBJECT_WIDTH = 50
OBJECT_HEIGHT = 50
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("fly and shoot")

velocity = 5
angle = 0

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("space.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
BACKGROUND_IMAGE_RECT = BACKGROUND_IMAGE.get_rect()


FPS = 60
clock = pygame.time.Clock()

class Player1(pygame.sprite.Sprite):
    def __init__(self,x, y, velocity):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("spaceship_red.png"), (OBJECT_WIDTH, OBJECT_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = velocity
        self.angle = 0
    
    def update(self):
         self.move()
         self.rotate()
         self.shooting()

    def move(self):       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity
        
    def rotate(self):
        keys = pygame.key.get_pressed()

        if keys[K_w]:
            self.angle += 6            
            mx, my = 250,250
            img_copy = pygame.transform.rotate(self.image, self.angle)
            display_surface.blit(img_copy, (mx - int(img_copy.get_width() / 2), my - int(img_copy.get_height() / 2)))

    def shooting(self):
        pass


class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("planet.png"), (OBJECT_WIDTH, OBJECT_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = (random.randint(0, WINDOW_WIDTH-80),random.randint(0, WINDOW_HEIGHT-80))

    def update(self):
        pass



    
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"Assets/exp{num}.png")
			img = pygame.transform.scale(img, (100, 100))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
        
		explosion_speed = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

player_group = pygame.sprite.Group() 
red_player = Player1(0, 0, velocity)
player_group.add(red_player)


planet_group = pygame.sprite.Group()
planet1 = Planet()
planet_group.add(planet1)


running = True
while running:
    #Check to see if the user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   

    #Blit the background
    display_surface.blit(BACKGROUND_IMAGE, BACKGROUND_IMAGE_RECT)
    #Update display and tick clock
    player_group.update()
    player_group.draw(display_surface)
    planet_group.update()
    planet_group.draw(display_surface)
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()

import pygame, random, math
from pygame.locals import *

#Initialize pygame
pygame.init()

#Set display surface
WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600




OBJECT_WIDTH = 80
OBJECT_HEIGHT = 80
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("fly and shoot")

velocity = 10
angle = 0

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("space.png"),(WINDOW_WIDTH, WINDOW_HEIGHT))
BACKGROUND_IMAGE_RECT = BACKGROUND_IMAGE.get_rect()

green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0

PLANET_HIT = pygame.USEREVENT + 3


FPS = 60
clock = pygame.time.Clock()

class Player1(pygame.sprite.Sprite):
    def __init__(self,x, y, velocity):
        super().__init__()
        self.bullet = []
        self.image = pygame.transform.scale(pygame.image.load("spaceship_red.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = velocity
        self.angle = angle
    
    def update(self):
         self.move()
         self.rotate()



    def rad_to_offset(radians, offset): # insert better func name.
        pass
     #   x = cos(radians) * offset
      #  y = sin(radians) * offset
       # return [x, y]
    # from https://web.archive.org/web/20121126060528/http://eli.thegreenplace.net/2008/12/13/writing-a-game-in-python-with-pygame-part-i/


    def move(self):       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.velocity
            Player1.rad_to_offset(90,90)
        if keys[pygame.K_RIGHT] and self.rect.x <= WINDOW_WIDTH-50:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.y >= 0:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.y <= WINDOW_HEIGHT-50:
            self.rect.y += self.velocity
        
    
    def rotate(self):
        keys = pygame.key.get_pressed()
        
        if keys[K_q]:
                self.angle += 6            
                mx, my = self.rect.centerx, self.rect.centery
                img_copy = pygame.transform.rotate(self.image, self.angle)
                display_surface.blit(img_copy, (mx - int(img_copy.get_width() / 2), my - int(img_copy.get_height() / 2)))
                
        if keys[K_e]:
                self.angle -= 6            
                mx, my = self.rect.centerx, self.rect.centery
                img_copy = pygame.transform.rotate(self.image, self.angle)
                display_surface.blit(img_copy, (mx - int(img_copy.get_width() / 2), my - int(img_copy.get_height() / 2)))
                    
        
    def shooting(self):
        Bullet.handle_bullets()

  
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


class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("planet.png"),(OBJECT_WIDTH, OBJECT_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0,WINDOW_WIDTH-OBJECT_WIDTH), random.randint(0,WINDOW_HEIGHT-OBJECT_HEIGHT))

    def update(self):
        pass


class Bullet():
    def __init__(self):
        self.bullet = []

    def handle_bullets(self):
        for bullet in self.bullet:
            bullet.x += velocity
            if planet_group.colliderect(bullet):
                pygame.event.post(pygame.event.Event(PLANET_HIT))
                self.bullet.remove(bullet)		#po nárazu do planety smaže střelu
                
            elif bullet.x > WINDOW_WIDTH or bullet.y > WINDOW_HEIGHT:
                self.bullet.remove(bullet)


   
player_group = pygame.sprite.Group() 
red_player = Player1(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 , velocity)
player_group.add(red_player)


planet_group = pygame.sprite.Group()
planet1 = Planet()
planet2 = Planet()
planet_group.add(planet1, planet2)

running = True
while running:
    #Check to see if the user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LCTRL:
                Bullet.handle_bullets()
       
            keys = pygame.key.get_pressed()
            if keys[K_q]:
                angle +=6

            if keys[K_e]:
                angle -= 6

    

    display_surface.blit(BACKGROUND_IMAGE, BACKGROUND_IMAGE_RECT)

    player_group.update()
    player_group.draw(display_surface)

    planet_group.update()
    planet_group.draw(display_surface)

    
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()

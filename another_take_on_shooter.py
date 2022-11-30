import pygame, random, math
from pygame.locals import *

#Use 2D vectors
vector = pygame.math.Vector2

#Initialize pygame
pygame.init()

FPS = 60
clock = pygame.time.Clock()

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




class Player1(pygame.sprite.Sprite):
    def __init__(self,x, y, velocity, bullet_group):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("spaceship_red.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = velocity
        self.angle = angle

        self.bullet_group = bullet_group
        
    
        #Kinematics vectors (first value is the x, second value is the y)
        self.position = vector(x, y)
        self.velocity = vector(0, 0)        #0 aby ze začátku nikam nezrychloval
        self.acceleration = vector(0, 0)

        #Kinematic constants
        self.HORIZONTAL_ACCELERATION = 2       #toto je zrychlení při rozjezdu
        self.HORIZONTAL_FRICTION = 0.15     #takto rychle brzdí rozjetej
        

    def update(self):
        self.move()
        self.rotate()
        self.collisions()
       
         



    def rad_to_offset(radians, offset): # insert better func name.
        pass
     #   x = cos(radians) * offset
      #  y = sin(radians) * offset
       # return [x, y]
    # from https://web.archive.org/web/20121126060528/http://eli.thegreenplace.net/2008/12/13/writing-a-game-in-python-with-pygame-part-i/


    def move(self):  

        #Set the accleration vector to (0, 0) so there is initially no acceleration
        #If there is no force (no key presses) acting on the player then accerlation should be 0
        #Vertical accelration (gravity) is present always regardless of key-presses
        self.acceleration = vector(0, 0)     
        
        #If the user is presseing a key, set the x-component of the accleration vector to a non zero value.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x >= 50:
            self.acceleration.x = -1*self.HORIZONTAL_ACCELERATION
            self.image = pygame.transform.rotate(self.image, 90)
        if keys[pygame.K_RIGHT] and self.rect.x <= WINDOW_WIDTH-50:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
        if keys[pygame.K_UP] and self.rect.y >= 50:
            self.acceleration.y = -1*self.HORIZONTAL_ACCELERATION
        if keys[pygame.K_DOWN] and self.rect.y <= WINDOW_HEIGHT-50:
            self.acceleration.y = self.HORIZONTAL_ACCELERATION


         #Calculate new kinematics values (2, 5) + (1, 6) = (3, 11)
        self.acceleration.x -= self.velocity.x*self.HORIZONTAL_FRICTION
        self.acceleration.y -= self.velocity.y*self.HORIZONTAL_FRICTION

        self.velocity += self.acceleration
        self.position += self.velocity + 0.5*self.acceleration

        
         #Update new rect based on kinematic calculations
        self.rect.center = self.position

    
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
        
            #self.shoot_sound.play()      #zatím bez omezení počtu střel
            PlayerBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

        
                  
    def collisions(self):
        pass
        """ collide_planet = pygame.sprite.spritecollide(self, planet_group, False)
        if collide_planet:
            self.position.y = collide_planet[0].rect.top + 1
            self.velocity.y = 0 """

    """       #Check for collisions with the water tiles
        if pygame.sprite.spritecollide(self, planet_group, False):
            self.velocity.x = 0
            self.velocity.y = 0
             """

class PlayerBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired by the player"""

    def __init__(self, x, y, bullet_group):
        """Initialize the bullet"""
        super().__init__()
        self.image = pygame.image.load("green_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        """Update the bullet"""
        self.rect.y += self.velocity

        #If the bullet is off the screen, kill it
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.kill() 

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


my_player_bullet_group = pygame.sprite.Group()

   
player_group = pygame.sprite.Group() 
red_player = Player1(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 , velocity, my_player_bullet_group)
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

        keys = pygame.key.get_pressed()
        if keys[K_q]:
            angle +=6

        if keys[K_e]:
            angle -= 6

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                red_player.shooting()
    

    display_surface.blit(BACKGROUND_IMAGE, BACKGROUND_IMAGE_RECT)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    player_group.update()
    player_group.draw(display_surface)

    planet_group.update()
    planet_group.draw(display_surface)

    
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()

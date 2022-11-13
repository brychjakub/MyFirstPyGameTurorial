import pygame
import os

WIDTH, HEIGHT = 900, 500 #je to pro větší rozlišení, dá se jednoduše zmenšit
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #vytvářím okno velikosti width a height
pygame.display.set_caption("First Game!")   #název otevřeného okna

WHITE =  (255,255,255)     #rgb určení barvy - proměnnou máme jen ay později byl kód čitelnější
BLACK = (0, 0, 0)

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)    	# v závorce (x, y, width, height) - vytváříme hranici


FPS = 60  	#definuje, jak rychle se hra aktualizuje
VEL = 5     #velocity - rychlost lodí
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 44 	#proměnná velikosti lodí

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)		#rotace lodi + velikost žluté lodi
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)	

def draw_window(red, yellow):		#vykreslení herní obrazovky, pozor ZÁLEŽÍ NA POŘADÍ (vykreslím loď a pak vyplním bílou = nevidím loď)
	WIN.fill(WHITE)
	pygame.draw.rect(WIN, BLACK, BORDER)  		# vykreslení hranice - argumenty WIN (kde), BLACK (jakou barvou), BORDER (co vytváříme)
	WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))		#pozor, 0,0 je levý horní roh
	WIN.blit(RED_SPACESHIP, (red.x, red.y))			
	pygame.display.update()		#!!!musíme ručně updatovat změnu, jinak se neprojeví!!!!!


def yellow_handle_movement(keys_pressed, yellow): 	 
		if keys_pressed[pygame.K_a]:    #left key
			yellow.x -= VEL
		if keys_pressed[pygame.K_d]:    #right key
			yellow.x += VEL
		if keys_pressed[pygame.K_w]:    #up key
			yellow.y -= VEL
		if keys_pressed[pygame.K_s]:    #down key
			yellow.y += VEL



def red_handle_movement(keys_pressed, red): 	 
		if keys_pressed[pygame.K_LEFT]:    #left key
			red.x -= VEL
		if keys_pressed[pygame.K_RIGHT]:    #right key
			red.x += VEL
		if keys_pressed[pygame.K_UP]:    #up key
			red.y -= VEL
		if keys_pressed[pygame.K_DOWN]:    #down key
			red.y += VEL



def main(): 		#sem jdou smyčky (aktualizace hry - posun obrazovky, skóre...)
	red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)		#vytvářím čtverce, ve kterých jsou lodě, ty pak pohybuji po obrazovce
	yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) 		# v závorce(pozice x , pozice y , šířka, výška)

	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)		#máme určeno 60FPS, PC nebude zahlceno 
		for event in pygame.event.get():  	#zčekneme, co se děje a co je třeba
			if event.type == pygame.QUIT:
				run = False		#ukončuje hru - mění True na False

		keys_pressed = pygame.key.get_pressed()
		yellow_handle_movement(keys_pressed, yellow)
		red_handle_movement(keys_pressed, red)

		draw_window(red, yellow)	



	pygame.quit()

if __name__ == "__main__":
	main()			#ujišťujeme se že to jede jen z tohoto filu - z mainu

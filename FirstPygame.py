import pygame
import os
pygame.font.init()		#importujem font pro vypsání výherce
pygame.mixer.init()		#inicializace zvuku

WIDTH, HEIGHT = 900, 500 		#je to pro větší rozlišení, dá se jednoduše zmenšit
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 		#vytvářím okno velikosti width a height
pygame.display.set_caption("First Game!")   	#název otevřeného okna

WHITE =  (255,255,255)     #rgb určení barvy - proměnnou máme jen ay později byl kód čitelnější
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)    	# v závorce (x, y, width, height) - vytváříme hranici


BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))


HEALTH_FONT = pygame.font.SysFont('comicsans', 40)		#definujeme, který font chceme
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


FPS = 60  	#definuje, jak rychle se hra aktualizuje
VEL = 5     #velocity - rychlost lodí
MAX_BULLETS = 3
BULLET_VEL = 7
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 44 		#proměnná velikosti lodí

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)		#rotace lodi + velikost žluté lodi
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)	


SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))			#loading the background space


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):		#vykreslení herní obrazovky, pozor ZÁLEŽÍ NA POŘADÍ (vykreslím loď a pak vyplním bílou = nevidím loď)
	WIN.blit(SPACE, (0, 0))
	pygame.draw.rect(WIN, BLACK, BORDER)  		# vykreslení hranice - argumenty WIN (kde), BLACK (jakou barvou), BORDER (co vytváříme)

	red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)    #1 v závorce bude vždy - je pro antialiasing (nevysvětleno)
	yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
	WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
	WIN.blit(yellow_health_text, (10, 10))

	WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))		#pozor, 0,0 je levý horní roh
	WIN.blit(RED_SPACESHIP, (red.x, red.y))		



	for bullet in red_bullets:
		pygame.draw.rect(WIN, RED, bullet)

	for bullet in yellow_bullets:
		pygame.draw.rect(WIN, YELLOW, bullet)		#vykreslování střel


	pygame.display.update()		#!!!musíme ručně updatovat změnu, jinak se neprojeví!!!!!


def yellow_handle_movement(keys_pressed, yellow): 	 
		if keys_pressed[pygame.K_a] and yellow.x > 0:    #left key
			yellow.x -= VEL
		if keys_pressed[pygame.K_d] and yellow.x + yellow.width <= BORDER.x:    #right key
			yellow.x += VEL
		if keys_pressed[pygame.K_w] and yellow.y > 0:    #up key
			yellow.y -= VEL
		if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:    #down key
			yellow.y += VEL



def red_handle_movement(keys_pressed, red): 	 
		if keys_pressed[pygame.K_LEFT] and red.x >= BORDER.x + 16:    #left key
			red.x -= VEL
		if keys_pressed[pygame.K_RIGHT] and red.x + red.width <= WIDTH:    #right key
			red.x += VEL
		if keys_pressed[pygame.K_UP] and red.y > 0:    #up key
			red.y -= VEL
		if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:    #down key
			red.y += VEL



def handle_bullets(yellow_bullets, red_bullets, yellow, red):
	for bullet in yellow_bullets:
		bullet.x += BULLET_VEL
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)		#po nárazu do lodi smaže střelu
		elif bullet.x > WIDTH:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x -= BULLET_VEL
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)
		elif bullet.x < 0:
			red_bullets.remove(bullet)



def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))

	pygame.display.update()		#vítěze ukazujeme po 5 sekund a resetujeme hru
	pygame.time.delay(5000)


def main(): 		#sem jdou smyčky (aktualizace hry - posun obrazovky, skóre...)
	red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)		#vytvářím čtverce, ve kterých jsou lodě, ty pak pohybuji po obrazovce
	yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) 		# v závorce(pozice x , pozice y , šířka, výška)


	red_bullets = []
	yellow_bullets = []


	red_health = 10
	yellow_health = 10


	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)		#máme určeno 60FPS, PC nebude zahlceno 
		for event in pygame.event.get():  	#zčekneme, co se děje a co je třeba
			if event.type == pygame.QUIT:
				run = False		#ukončuje hru - mění True na False
				pygame.quit()

			if event.type == pygame.KEYDOWN:    #pokud zmáčknu (ne podržím) tlačítko
				if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
					bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)     #šířka, výška (+ polovina výšky lodě - 2 pixely, což je střela), pak šířka a výška střely
					yellow_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()

				if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
					bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)     #šířka, výška (+ polovina výšky lodě - 2 pixely, což je střela), pak šířka a výška střely
					red_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()



			if event.type == RED_HIT:		#ubírání životů
				red_health -= 1
				BULLET_HIT_SOUND.play()

			if event.type == YELLOW_HIT:		
				yellow_health -= 1
				BULLET_HIT_SOUND.play()
		winner_text = ""				#pokud nikdo nevyhraje, tiskne se prázdný string, pokud ano..
		if red_health <= 0:
			winner_text = "Yellow wins!"
		
		if yellow_health <= 0:	
			winner_text = "Red wins!"

		if winner_text != "":			#....tiskne se výherce
			draw_winner(winner_text)
			break
							
		keys_pressed = pygame.key.get_pressed()		#podržení tlačítka
		yellow_handle_movement(keys_pressed, yellow)
		red_handle_movement(keys_pressed, red)


		handle_bullets(yellow_bullets, red_bullets, yellow, red)	

		draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)	



	main()			#toto resetuje hru

if __name__ == "__main__":
	main()			#ujišťujeme se že to jede jen z tohoto filu - z mainu

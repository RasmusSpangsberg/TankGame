import pygame
from math import pi, sqrt

pygame.init()
display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

class Tank:
	def __init__(self, x, y, width, height, color, is_enemy=False):
		# TODO rename x and y to x_pos and y_pos of the tank
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.is_enemy = is_enemy

	def draw(self, mouse_x=None, mouse_y=None):
		rect_top_x = self.x + int(self.width/2)
		rect_top_y = self.y + 5

		pygame.draw.rect(game_display, self.color, [self.x, self.y, self.width, self.height])
		pygame.draw.circle(game_display, self.color, [rect_top_x, rect_top_y], 30)

		if self.is_enemy:
			pygame.draw.line(game_display, self.color, [rect_top_x, rect_top_y], [rect_top_x - 50, rect_top_y - 50], 5)
		else:
			x = mouse_x - rect_top_x
			y = 600 - mouse_y - rect_top_y + 400
			
			print(rect_top_y)

			len_vektor = sqrt(x**2 + y**2)
			enheds_vektor = [50*x/len_vektor, 50.0*y/len_vektor]

			start_pos = [rect_top_x, rect_top_y]
			end_pos = [enheds_vektor[0] + rect_top_x, 600 - enheds_vektor[1] - rect_top_y + 400]

			pygame.draw.line(game_display, RED, start_pos, end_pos, 5)


class Projectile:
	def __init__(self, x, y, radius, color, mouse_x, mouse_y):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		
		self.delta_time = 1/60
		self.mass = 50.0
		self.g = 9.82

		self.velocity_x = mouse_x
		self.velocity_y = 600 - mouse_y 

	def draw(self):
		pygame.draw.circle(game_display, self.color, [self.x, self.y], self.radius)

	def update(self):
		self.x += int(self.velocity_x * self.delta_time)
		self.y -= int(self.velocity_y * self.delta_time)

		# velocity_x only gets affected by wind/friction
		self.velocity_x -= 1
		self.velocity_y -= (self.mass * self.g) * self.delta_time

	def collided(self, obj):
		# parentheses for easier reading
		if (self.x + self.radius) >=  (obj.x) and (self.x - self.radius) <= (obj.x + obj.width):
			if (self.y + self.radius) >= (obj.y) and (self.y - self.radius) <= (obj.y + obj.height):
				return True
		return False
			

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

enemy_x = 650
enemy_y = 500
enemy_width = 100
enemy_height = 50
enemy = Tank(enemy_x, enemy_y, enemy_width, enemy_height, RED, is_enemy=True)

player_x = 50
player_y = 500
player_width = 100
player_height = 50
player = Tank(player_x, player_y, player_width, player_height, GREEN)

ball_x = 100
ball_y = 500
ball_radius = 20
balls = []

enemies_hit = 0
enemies_missed = 0
fire = False
game_exit = False
arc_enabled = False

cheat_code_str = ""

myfont = pygame.font.SysFont("Comic Sans MS", 30)

# variables used to calculate the arc
delta_time = 1/60
mass = 50.0
g = 9.82

while not game_exit:
	game_display.fill(BLACK)
	mouse_x, mouse_y = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_exit = True
		
		if event.type == pygame.KEYDOWN:
			cheat_code_str += pygame.key.name(event.key)
			
			if cheat_code_str == "hi":
				arc_enabled = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			
			balls.append(Projectile(ball_x, ball_y, ball_radius, BLUE, mouse_x, mouse_y))

	if arc_enabled:
		pos_x = ball_x
		pos_y = ball_y

		velocity_x = mouse_x
		velocity_y = 600 - mouse_y

		for i in range(100):
			pos_x += int(velocity_x * delta_time)
			pos_y -= int(velocity_y * delta_time)

			# velocity_x only gets affected by wind/friction
			velocity_x -= 1
			velocity_y -= (mass * g) * delta_time

			if i % 8 == 0:
				pygame.draw.circle(game_display, BLUE, [pos_x, pos_y], 5)

	for ball in balls:
		ball.update()
		ball.draw()

		if ball.y >= display_height + ball_radius:
			balls.remove(ball)
			enemies_missed += 1

		if ball.collided(enemy):
			balls.remove(ball)
			enemies_hit += 1

	enemies_hit_str = "Enemies hit: " + str(enemies_hit)
	enemies_missed_str = "Enemies missed: " + str(enemies_missed)

	enemies_hit_surface = myfont.render(enemies_hit_str, False, WHITE)
	enemies_missed_surface = myfont.render(enemies_missed_str, False, WHITE)
	game_display.blit(enemies_hit_surface, (0, 0))
	game_display.blit(enemies_missed_surface, (0, 30))

	enemy.draw()
	player.draw(mouse_x, mouse_y)
	
	pygame.display.update()
	clock.tick(60)

pygame.quit()

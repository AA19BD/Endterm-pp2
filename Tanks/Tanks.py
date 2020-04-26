import pygame
import random
import time
import sys
from enum import Enum

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
# pygame.mixer.music.load('mucistank.mp3')
sound1=pygame.mixer.Sound('expl6.wav')
sound2 =pygame.mixer.Sound('pew.wav')
# pygame.mixer.music.play()


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

def game_over():
    font = pygame.font.SysFont('Arial', 48)
    text = font.render('Game Over', True, (0, 0, 255))
    place = text.get_rect(center=(width // 2, height // 2 - 20))
    screen.blit(text, place)
    if tanks[0].life == 0 :
        font2 = pygame.font.SysFont("Arial", 24)
        text2 = font2.render('Blue tank wins!', True, (255 , 0 , 0))
        place2 = text2.get_rect(center=(width // 2, height // 2 + 10))
        screen.blit(text2, place2)

    if tanks[1].life == 0 :
        font3 = pygame.font.SysFont("Arial", 18)
        text3 = font3.render('Pink tank wins!', True, (255 , 0 , 0))
        place3 = text3.get_rect(center=(width // 2, height // 2 + 10))
        screen.blit(text3, place3)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

class Tank:
    def __init__(self, x, y, speed, color, shoot,
    d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
        self.x = x
        self.y = y
        self.size = 40
        self.life = 3
        self.speed = speed
        self.color = color
        self.direction = Direction.RIGHT
        self.KEYPULL = shoot
        
        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}

    def draw(self):
        tank_c = (self.x + int(self.size / 2), self.y + int(self.size / 2))
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.size, self.size), 2)
        pygame.draw.circle(screen, self.color, tank_c, int(self.size / 2))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.size + int(self.size / 2), self.y + int(self.size / 2)), 4)

        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (
            self.x - int(self.size / 2), self.y + int(self.size / 2)), 4)

        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.size / 2), self.y - int(self.size / 2)), 4)

        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.size / 2), self.y + self.size + int(self.size / 2)), 4)

    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed
        self.draw()
        self.x = (self.x + width) % width
        self.y = (self.y + height) % height
    
class Bullet:
    def __init__(self,x=0,y=0,color=(255,0,0),direction='LEFT',speed = 6):
        self.x=x
        self.y=y
        self.color=color
        self.speed=speed
        self.direction=direction
        self.status=True
        self.distance=0
        self.radius=5 

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed
        self.distance += 1
        self.draw()

    def draw(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)

def shotting(tank):
    if tank.direction == Direction.RIGHT:
        x = tank.x + tank.size + tank.size // 2
        y = tank.y + tank.size // 2

    if tank.direction == Direction.LEFT:
        x = tank.x - tank.size // 2
        y = tank.y + tank.size // 2

    if tank.direction == Direction.UP:
        x = tank.x + tank.size // 2
        y = tank.y - tank.size // 2

    if tank.direction == Direction.DOWN:
        x = tank.x + tank.size // 2
        y = tank.y + tank.size + tank.size // 2

    p = Bullet(x, y, (255,0,0), tank.direction)
    bullets.append(p)
    sound1.play()

def hits():

    for p in bullets:
        if p.x in range(tanks[0].x , tanks[0].x + 41) and p.y in range(tanks[0].y , tanks[0].y + 41) : 
            tanks[0].life -= 1
            bullets.remove(p)
            sound2.play()
        if p.x in range(tanks[1].x , tanks[1].x + 41) and p.y in range(tanks[1].y , tanks[1].y + 41) : 
            tanks[1].life -= 1
            bullets.remove(p)
            sound2.play()

        if tanks[0].life == 0 or tanks[1].life == 0 :
           game_over()


tank1 = Tank(100, 200, 2, (255, 0, 0), pygame.K_RETURN)
tank2 = Tank(300 , 100 , 2 , (0 , 255 , 0), pygame.K_SPACE, 
pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

bullet1 = Bullet()
bullet2 = Bullet()


tanks = [tank1, tank2]
bullets = [bullet1, bullet2]

clock = pygame.time.Clock()
colors = pygame.Color(0, 0, 0)

while True:
    clock.tick(30)
    screen.fill(colors)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over()
            pressed = pygame.key.get_pressed()
            for tank in tanks:
                if event.key in tank.KEY.keys():
                    tank.change_direction(tank.KEY[event.key])        
                
                if pressed[tank.KEYPULL]:
                    shotting(tank)

    for tank in tanks:                   
        tank.move()

    for p in bullets:
        p.move()
    
    for tank in tanks:
        tank.draw() 

    hits()
    
    pygame.display.flip()

pygame.quit()
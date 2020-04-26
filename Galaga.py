import pygame 
import random

pygame.init()
pygame.mixer.init()#для звука

width=480
height=600
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('Galaga')


class Player(pygame.sprite.Sprite):#встроенный класс Sprite 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#инициализатор встроенных классов Sprite
        self.image=pygame.transform.scale(player1,(50,30))#делаем новый размер игрока
        self.rect=self.image.get_rect()#get_rect -оценивает наш image и вычисляет прямоугольник способный его окружить 
        self.radius=20
        # pygame.draw.circle(self.image,((255,0,0)),self.rect.center,self.radius)
        self.rect.centerx=width/2
        self.rect.bottom=height-10
        self.speedx=0
        self.shield=120#здоровье игрока
    def update(self):#перемещение объекта 
        self.speedx=0
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx=-8
        if keys[pygame.K_RIGHT]:
            self.speedx=8
        self.rect.x+=self.speedx
        if self.rect.left>width:
            self.rect.right=0
        if self.rect.right<0:
            self.rect.left=width
    def shoot(self):
        bullet=Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        sound2.play()
    
def newenemy():
    m=Enemy()
    all_sprites.add(m)
    enemy.add(m)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=meteor
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width * .85/2)
        # pygame.draw.circle(self.image,((255,0,0)),self.rect.center,self.radius)
        self.rect.x=random.randrange(width-self.rect.width)
        self.rect.y=random.randrange(-100,-40)
        self.speedy=random.randrange(1,8)
        self.speedx=random.randrange(-3,3)
    def update(self):
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.y>height+10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x=random.randrange(width-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedy=random.randrange(1,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=laser
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-10
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()

font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name, size)
    text_surface=font.render(text,True,((255,255,255)))
    text_rect=text_surface.get_rect()
    text_rect_midtop=(x,y)
    surf.blit(text_surface,text_rect)
def draw_shield(surf,x,y,pct):
    if pct<0:
        pct=0
    bar_height=10
    bar_length=120
    fill=(pct)
    outline_rect=pygame.Rect(x,y,bar_length,bar_height)
    fill_rect=pygame.Rect(x,y,fill,bar_height)
    pygame.draw.rect(surf,((0,255,0)),fill_rect)
    pygame.draw.rect(surf,((255,255,255)),outline_rect,2)
def show_go_screen():
    screen.blit(background,background_rect)
    draw_text(screen,'GAME OVER',70 ,width/2,height/4)
    draw_text(screen,'Press a key to begin',10,width/2,height*3)
    pygame.display.flip()
    waiting=True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYUP:
                waiting=False





meteor=pygame.image.load('meteorBrown_med1.png')
background=pygame.image.load('starfield.png')
background_rect=background.get_rect()
player1=pygame.image.load('playerShip1_orange.png')
laser=pygame.image.load('laserRed16.png')
sound1=pygame.mixer.Sound('expl6.wav')
sound2=pygame.mixer.Sound('pew.wav')

all_sprites=pygame.sprite.Group()#группировка всех спрайтов для отображения их одновременно
enemy=pygame.sprite.Group()
bullets=pygame.sprite.Group()
player=Player() 
all_sprites.add(player)
for i in range(8):
    newenemy()
   
score=0
clock=pygame.time.Clock() #частота кадров (FPS)
FPS=60
runnig=True
game_over=False
while runnig:
    if game_over:
        show_go_screen()
        game_over=False
        all_sprites=pygame.sprite.Group()
        enemy=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        player=Player()
        all_sprites.add(player)
        for i in range(8):
            newenemy()
        score=0
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            runnig=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.shoot()

    all_sprites.update()#обновление наших спрайтов(действие в игре(т.е движение)

    hits = pygame.sprite.groupcollide(enemy,bullets,True,True)
    for hit in hits:#при столконовении создаются новые enemy
        score+=1#счет попадения в астероиды 
        sound1.play()
        newenemy()
    hits=pygame.sprite.spritecollide(player,enemy,True,pygame.sprite.collide_circle)
    for hit in hits:
        sound1.play()
        player.shield-=40
        newenemy()
        if player.shield<=0:
            game_over=True
    # hits = pygame.sprite.spritecollide(player, enemy, False)#проверка не ударил ли enemy playera (при значение True,enemy пропадут)
    # if hits:
    #     running = False
    
   
   


    screen.fill((0,0,0))#рендеринг
    screen.blit(background,background_rect)
    all_sprites.draw(screen)#прорисовка всех спрайтов одновременно 
    
    draw_shield(screen,5,5,player.shield)
    draw_text(screen,str(score),35,width,height/2)
    pygame.display.flip()#прорисовка

pygame.quit()



from pygame import *
from random import randint
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
font.init()

font1 = font.SysFont("Arial",80)

wins = font1.render("YOU WIN",True,(255,255,255))
lose = font1.render("YOU LOSE",True,(180,0,0))

font2 = font.SysFont("Arial",36)

win_height = 500
win_width = 700
fire_sound = mixer.Sound("fire.ogg")
lost = 0
score = 0
goal = 10
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self,char_image,char_x,char_y,size_x,size_y,char_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(char_image),(size_x,size_y))
        self.char_speed = char_speed
        self.rect = self.image.get_rect()
        self.rect.x = char_x
        self.rect.y = char_y
    def reset(self):
        win.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]and self.rect.x >5:
            self.rect.x -= self.char_speed

        if keys[K_RIGHT]and self.rect.x <600:
            self.rect.x += self.char_speed

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx ,self.rect.top ,15 ,20, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.char_speed
        if self.rect.y <0:
            self.kill()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.char_speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            lost = lost + 1
        
ship = Player("rocket.png",5,400,80,100,10)
monsters = sprite.Group()
bullets = sprite.Group() 
for i in range(1,6):
    monster = Enemy("ufo.png",randint(80,win_width - 80),-40,80,50,randint(1,5))
    monsters.add(monster)

win = display.set_mode((win_width,win_height))
display.set_caption("Shooter")
back = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))

run = True
finish = False

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type ==KEYDOWN: 
            if e.key ==K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        win.blit(back,(0,0))
        ship.update()
        monsters.update()
        bullets.update()
        monsters.draw(win)
        bullets.draw(win)
        ship.reset()

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png",randint(80,win_width - 80),-40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,False) or lost >= max_lost:
            finish = True
            win.blit(lose,(200,200))

        if score >= goal:
            finish = True
            win.blit(wins,(200,200))

        text_score = font2.render("score: " +str(score),1,(255,255,255))
        text_missed = font2.render("missed: " +str(lost),1,(255,255,255))

        win.blit(text_score,(10,20))
        win.blit(text_missed,(10,50))

        display.update()
    time.delay(50)
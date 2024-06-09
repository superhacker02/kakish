from pygame import *
from random import *
from time import time as timer

win_width = 700 
win_height = 500 
mw = display.set_mode((win_width, win_height)) 
back = transform.scale(image.load('galaxy.jpg'), (win_width, win_height)) 
clock = time.Clock() 

mixer.init() 
mixer.music.load('space.ogg') 
mixer.music.play() 

fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 36)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
score = 0
lost = 0
goal = 20
max_lost = 10
life = 3

class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
 
    def reset(self): 
        mw.blit(self.image, (self.rect.x, self.rect.y)) 
 
 
class Player(GameSprite): 
    def update(self): 
        keys = key.get_pressed() 
        if keys[K_LEFT] and self.rect.x > 5: 
            self.rect.x -= self.speed 
        if keys[K_RIGHT] and self.rect.x < win_width - 70: 
            self.rect.x += self.speed 



    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 1




class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

hero = Player('rocket.png', 300, win_height - 65, 50, 50, 5)
monsters = sprite.Group() 
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1,5))   
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)



num_fire = 0
rel_time = False 
finish = False
game = True 
while game: 
    for e in event.get(): 
        if e.type == QUIT: 
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    hero.fire()
                    fire_sound.play()
                    if num_fire >= 5 and rel_time == False:
                        last_time = timer()
                        rel_time = True

    if not finish:
        mw.blit(back, (0, 0))

        text = font1.render('Счет:'+ str(score), True, (255,255,255))
        mw.blit(text, (10,20))

        text_lose = font1.render('Пропущенно:' + str(lost), True, (255,255,255))
        mw.blit(text_lose, (10,50))

        hero.reset()
        hero.update()
        monsters.update()
        monsters.draw(mw)
        bullets.update()
        bullets.draw(mw)
        asteroids.update()
        asteroids.draw(mw)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('Wait! Reload. . .', True, (120, 0, 0))
                mw.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for j in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1,5))   
            monsters.add(monster)
        if sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero, asteroids, False):
            sprite.spritecollide(hero, monsters, True)
            sprite.spritecollide(hero, asteroids, True)
            life -= 1
        if life == 0 or lost >= max_lost:
            finish = True
            mw.blit(lose,(200, 200))

        if score >= goal:
            finish = True
            mw.blit(win,(10, 50))
        if life  == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), True, life_color)
        mw.blit(text_life, (650, 10))


        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000) 
        for i in range(1,6):
            monster = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1,5))   
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)


    clock.tick(60) 
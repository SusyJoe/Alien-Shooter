from pygame import *
from random import *
from time import time as timer
# Game Settings w/ const Variables
FPS = 50
WIDTH = 700
HEIGHT = 500

score = 0
miss = 0
coin = 0


num_fire = 0
screen = display.set_mode((WIDTH,HEIGHT))
display.set_caption("ALIEN SHOOTER")
clock = time.Clock()
background = transform.scale(image.load("galaxy.jpg"),(WIDTH,HEIGHT))

# Activate BG music
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
shoot = mixer.Sound("fire.ogg")
class Main(sprite.Sprite):
    def __init__(self, img, speed, x, y,w,h):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def abracadabra(self):
        screen.blit(self.image, (self.rect.x , self.rect.y))



class Player(Main):
    def controls(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 450:
            self.rect.y += self.speed
        if keys[K_d] and self.rect.x < 650:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def shoot(self):
        bullet = Bullet("bullet.png", 20, self.rect.centerx, self.rect.top, 25, 10)
        bull.add(bullet)
        
            
class Enemy(Main):
    def update(self):
        global miss
        self.rect.y += self.speed
        
        if self.rect.y >= HEIGHT:
            miss += 1
            self.rect.x = randint(0, WIDTH-50)
            self.rect.y = 0
class Enemy2(Main):
    def update(self):
        global miss
        self.rect.y += self.speed
        
        if self.rect.y >= HEIGHT:
            self.rect.x = randint(0, WIDTH-50)
            self.rect.y = 0
class Bullet(Main):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()
class Gold(sprite.Sprite):
    def __init__(self, coin_x, coin_y):
        super().__init__()
        self.rect = Rect(coin_x, coin_y, 25, 25)
        self.image = transform.scale(image.load("God.jpg"), (25, 25))
    
    def mint(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        
font.init()
font1 = font.Font(None, 36)



c1 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
c2 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
c3 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
c4 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
c5 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
c6 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
c7 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
c8 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
c9 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
c10 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
coins = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
coin_counter = 0
spaceship = Player("rocket.png",10, WIDTH//2-25, HEIGHT-75,50,50)

monsters = sprite.Group()

for i in range(1,5):
    monster = Enemy("ufo.png",1, randint(0,WIDTH-50),0,50,50)
    monsters.add(monster)

rocks = sprite.Group()

for r in range(1,3):
    rock = Enemy2("asteroid.png",randint(1,4), randint(0,WIDTH-50),0,50,50) 
    rocks.add(rock)

bull = sprite.Group()




# Game Loop
run = True
end = False
reload_time = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
            quit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 10 and reload_time == False:
                    num_fire += 1
                    spaceship.shoot()
                    shoot.play()
                if num_fire >= 10 and reload_time == False:
                    end_Time = timer()
                    reload_time = True                    
            
    if not end:
        screen.blit(background,(0,0)) 
        spaceship.abracadabra()
        spaceship.controls()
        monsters.update()
        rocks.update()
        bull.update()

        text_lose = font1.render("Missed: " + str(miss), 1, (255,255,255))
        screen.blit(text_lose, (10,20))
        text_score = font1.render("Score: " + str(score), 1, (255,255,255))
        screen.blit(text_score, (10,45))
        text_g = font1.render("Gold: " + str(coin_counter), 1, (255,255,255))
        screen.blit(text_g, (10,70))
        
        monsters.draw(screen)
        rocks.draw(screen)
        bull.draw(screen)
        if reload_time:
            current_Time = timer()   
            if current_Time - end_Time < 3:
                reload = font1.render("!RELOADING!", True, (156, 16, 16))
                screen.blit(reload, (WIDTH-175, 20))
            else:
                num_fire = 0
                reload_time = False
        collides = sprite.groupcollide(bull, monsters, True, True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png",randint(1,4), randint(0,WIDTH-50),0,50,50)
            monsters.add(monster)
        for coin in coins:
            coin.mint()
            if sprite.collide_rect(spaceship, coin):
                coin_counter += 1
                coins.remove(coin)
                coin.kill()
        if miss >= 10 or sprite.spritecollide(spaceship, monsters, True) or sprite.collide_rect(spaceship, rock):
            lose = font1.render("You Lose", True, (255, 255, 255))
            screen.blit(lose, (WIDTH/2, HEIGHT/2))
            end = True
        if score >= 10 and coin_counter >= 10:
            win = font1.render("You Win", True, (255, 255, 255))
            screen.blit(win, (WIDTH/2, HEIGHT/2))
            end = True

    else:
        end = False
        score = 0
        miss = 0
        for b in bull:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1,5):
            monster = Enemy("ufo.png",randint(1,4), randint(0,WIDTH-50),0,50,50)
            monsters.add(monster)
        spaceship = Player("rocket.png",10, WIDTH//2-25, HEIGHT-75,50,50)
        for r in rocks:
            r.kill()
        for r in range(1,3):
            rock = Enemy2("asteroid.png",randint(1,4), randint(0,WIDTH-50),0,50,50) 
            rocks.add(rock)
        for c in coins:
            c.kill()
        c1 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
        c2 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
        c3 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
        c4 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
        c5 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
        c6 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
        c7 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
        c8 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
        c9 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
        c10 = Gold(randint(0, WIDTH - 50), randint(0,HEIGHT-50)) 
        coins = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
          
    
    display.update()
    clock.tick(FPS)



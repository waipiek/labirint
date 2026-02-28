from pygame import *
import math

class GameSprite(sprite.Sprite):
    def __init__(self, img, speed, start):
        super().__init__()
        self.image = transform.scale(image.load(img), (65, 65))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def player_upd(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 430:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 630:
            self.rect.x += self.speed


class Enemy(GameSprite):
    def __init__(self, img, speed, start, end):
        super().__init__(img, speed, start)
        self.xstart, self.ystart = self.rect.x, self.rect.y
        self.xend, self.yend = end
        self.alpha = math.atan((self.yend - self.ystart) / (self.xend - self.xstart))
        self.xspeed = self.speed * math.cos(self.alpha)
        self.yspeed = self.speed * math.sin(self.alpha)
        self.kx = 1
        self.ky = 1

    def chaos(self):
        condition_1 = not min(self.xstart, self.xend) <= self.rect.x <= max(self.xstart, self.xend)
        condition_2 = not min(self.ystart, self.yend) <= self.rect.y <= max(self.ystart, self.yend)
        if condition_1:
            self.kx *= -1
        if condition_2:
            self.ky *= -1
        self.rect.x += self.kx * self.xspeed
        self.rect.y += self.ky * self.yspeed
    
    def normal(self):
        condition_1 = not min(self.xstart, self.xend) <= self.rect.x <= max(self.xstart, self.xend)
        condition_2 = not min(self.ystart, self.yend) <= self.rect.y <= max(self.ystart, self.yend)
        if condition_1 or condition_2:
            self.kx *= -1
            self.ky *= -1
        self.rect.x += self.kx * self.xspeed
        self.rect.y += self.ky * self.yspeed


class Wall(sprite.Sprite):
    def __init__(self, x, y, a, b, color):
        super().__init__()
        self.color = color
        self.surface = Surface((a, b))
        self.surface.fill(color)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.surface, (self.rect.x, self.rect.y))

window = display.set_mode((700, 500))
display.set_caption('Maze')
fps = 200
clock = time.Clock()

background = transform.scale(image.load('background.jpg'), (700, 500))
SPEED = 1
player = Player('hero.png', 1.5, (10, 10))
enemy_1 = Enemy('cyborg.png', SPEED, (0, 430), (630, 0))
enemy_2 = Enemy('cyborg.png', SPEED, (630, 430), (0, 0))
enemy_3 = Enemy('cyborg.png', SPEED, (630, 0), (0, 430))
treasure = GameSprite('treasure.png', 0, (625, 10))

font.init()
my_font = font.SysFont('Arial', 100)
lose = my_font.render('YOU LOSE!', True, (255, 0, 0))
win = my_font.render('YOU WIN!', True, (255, 255, 0))

GREEN = (154, 205, 50)
SIZE = 5
w1 = Wall(0, 0, SIZE, 500, GREEN)
w2 = Wall(0, 0, 700, SIZE, GREEN)
w3 = Wall(700 - SIZE, 0, SIZE, 500, GREEN)
w4 = Wall(0, 500 - SIZE, 700, SIZE, GREEN)
w5 = Wall(87, 0, SIZE, 420, GREEN)
w6 = Wall(174, 80, SIZE, 420, GREEN)
w7 = Wall(261, 0, SIZE, 420, GREEN)
w8 = Wall(348, 80, SIZE, 420, GREEN)
w9 = Wall(435, 0, SIZE, 420, GREEN)
w10 = Wall(522, 80, SIZE, 420, GREEN)
w11 = Wall(609, 0 , SIZE, 420, GREEN)
walls = [w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11]

finish = False
game = True
game_result = None
mixer.init()
mixer.music.load('limbo.ogg')
mixer.music.play()
mixer.music.set_volume(0.2)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_r:
                finish = False
                player.rect.x = 10
                player.rect.y = 10
                enemy_1.rect.x = 0
                enemy_1.rect.y = 430
                enemy_2.rect.x = 630
                enemy_2.rect.y = 430
                enemy_3.rect.x = 630
                enemy_3.rect.y = 0
                mixer.music.play()

    if not finish:
        for wall in walls:
            if sprite.collide_rect(player, wall):
                finish = True
                game_result = False
        if sprite.collide_rect(player, enemy_1) or sprite.collide_rect(player, enemy_3) or sprite.collide_rect(player, enemy_2):
            finish = True
            game_result = False
        if sprite.collide_rect(player, treasure):
            finish = True
            game_result = True
        
        window.blit(background, (0, 0))
        treasure.update()
        
        player.player_upd()
        enemy_1.chaos()
        enemy_2.chaos()
        enemy_3.chaos()
        
        for wall in walls:
            wall.draw()

        player.update()
        enemy_1.update()
        enemy_2.update()
        enemy_3.update()
    else:
        mixer.music.stop()
        if game_result:
            window.blit(win, (150, 180))
        else:
            window.blit(lose, (120, 180))

    display.update()
    clock.tick(fps)

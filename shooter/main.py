from pygame import *
from random import randint
from config import *
init()

# PARAMETROS INICIALES
puntos = 0
fallos = 0
vidas = 5

# TRABAJO CON TEXTO
font.init()
font_1 = font.Font(FONT_FILE, 24)

# TRABAJO CON MUSICA
mixer.pre_init(44100, -16, 2, 512) 
mixer.init()
mixer.music.load(BGM)
mixer.music.play()

# # efectos de sonido
gameover_sfx = mixer.Sound(SCREAM_SFX)

# MAIN WINDOWN
screen = display.set_mode((ANCHO, ALTO))
display.set_caption(TITULO)

# BACKGROUND
background = transform.scale(image.load(BG_IMG), (ANCHO, ALTO))


# CLASE PADRE 
class GameSprite(sprite.Sprite):
    def __init__(self, img, cor_x, cor_y, sprite_width, sprite_height, speed=0):
        super().__init__()
        self.width = sprite_width
        self.height = sprite_height
        self.image = transform.scale(image.load(img), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = cor_x
        self.rect.y = cor_y
        self.speed = speed

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x <= ANCHO - (self.rect.width + self.speed):
            self.rect.x += self.speed
        elif keys[K_a] and self.rect.x >= self.speed:
            self.rect.x -= self.speed

    def shoot(self):
        bala = Bullet(BULLET_IMG, self.rect.centerx - 5, self.rect.top, 10, 15, 5)
        balas.add(bala)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        global fallos
        self.rect.y += self.speed
        if self.rect.y >= ALTO:
            self.rect.y = -60
            self.rect.x = randint(0, ANCHO - 60)
            self.speed = randint(1, 6)
            fallos += 1
       

# OBJETOS
player = Player(PLAYER_IMG, (ANCHO - 60) // 2, ALTO - 100, 60, 80, 5)

# GRUPOS DE SPRITES
balas = sprite.Group()
mini_elvys = sprite.Group()

for i in range(6):
    enemy = Enemy(ENEMY_IMG, randint(0, ANCHO - 60), -60, 60, 60, randint(1, 6))
    mini_elvys.add(enemy)

# CICLO JUEGO
run = True
finish = False
clock = time.Clock()

while run:
    # MANEJO DE EVENTOS
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_r:
                finish = False
                puntos = 0
                fallos = 0
                vidas = 5
                gameover_sfx.stop()
            if e.key == K_SPACE:
                player.shoot()
                
    if not finish:
        screen.fill(COLOR_FONDO)
        screen.blit(background, (0, 0))
        player.reset()
        player.update()
   
        mini_elvys.update()
        mini_elvys.draw(screen)
        balas.update()
        balas.draw(screen)
        # renderizado de texto
        puntos_txt = font_1.render(f'PUNTOS: {puntos}', 1, WHITE)
        screen.blit(puntos_txt, (20, 20))
        fallos_txt = font_1.render(f'FALLOS: {fallos}', 1, WHITE)
        screen.blit(fallos_txt, (20, 60))
        vidas_txt = font_1.render(f'VIDAS: {vidas}', 1, WHITE)
        screen.blit(vidas_txt, (450, 20))

    # MECANICAS DE COLISION
    #  balas con enemigos
        if sprite.groupcollide(balas, mini_elvys, True, True):
            puntos += 1
            enemy = Enemy(ENEMY_IMG, randint(0, ANCHO - 60), -60, 60, 60, randint(1, 6))
            mini_elvys.add(enemy)

    #  player con enemigos
        if sprite.spritecollide(player, mini_elvys, True):
            vidas -= 1
            enemy = Enemy(ENEMY_IMG, randint(0, ANCHO - 60), -60, 60, 60, randint(1, 6))
            mini_elvys.add(enemy)


    # CONDICION DE DERROTA
        if fallos >= 20 or vidas <= 0:
            finish = True
            screen.fill(BLACK)
            gameover = transform.scale(image.load(GAMEOVER_IMG), (ANCHO, ALTO))
            screen.blit(gameover, (0,0))
            mixer.music.stop()
            gameover_sfx.play()

    # CONDICION VICTORIA
        if puntos == 67:
            finish = True
            screen.fill(BLACK)
            # RENDERIZAR LA PANTALLA VICTORIA
            

    # REFRESCAR A TASA SELECCIONADA
    display.update()
    clock.tick(FPS)
quit()

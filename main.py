import pygame as pg
from pygame.draw_py import draw_line
from Game.world import World
from Game.enemy import Enemy
import constants as c
from Game.tower import Tower


#inicializálom a pygamet
pg.init()

clock = pg.time.Clock()

#KEPEK BETOLTESE


# Térkép betöltése
map_image = pg.image.load('Assets/kepek/terkep.png')# a térképed útvonala
map_rect = map_image.get_rect()

#betöltöm az ablakot
screen = pg.display.set_mode((map_rect.width, map_rect.height))
map_image = map_image.convert_alpha()

#Az enemy betöltése
enemy_img1 = pg.image.load('Assets/kepek/piroshal.png').convert_alpha()  # Első kép
enemy_img2 = pg.image.load('Assets/kepek/kekhal.png').convert_alpha()  # Második kép


#Tower betoltese
tower_img=pg.image.load('Assets/kepek/ujLovo.png').convert_alpha()

def create_tower(mouse_pos):
    tower=Tower(tower_img,mouse_pos)
    tower_group.add(tower)


#terkep keszitese
world=World(map_image)

#csoport keszitese
enemy_group=pg.sprite.Group()
tower_group=pg.sprite.Group()

koordinatak=[
    (179,9),
    (113,60),
    (115,207),
    (227,331),
    (397,345),
    (455,403),
    (459,645),
    (559,715),
    (665,761),
    (869,785),
    (955,865)
]

#Uj enemyk keszitese
SPAWN_DELAY = 2000  # 2000 ms = 2 masodperc
last_spawn_time = 0


# Ellenség létrehozásakor mindkét képet átadjuk
enemy = Enemy(koordinatak, enemy_img1, enemy_img2)
enemy_group.add(enemy)

running = True
while running:

    clock.tick(c.Framerates)
    screen.fill("grey100")
    world.draw(screen)


     #Sebezhetoseg
    #for event in pg.event.get():
        #if event.type == pg.QUIT:
           # running = False

        # Teszt: nyomj meg egy gombot és sebzi az első enemy-t
       # if event.type == pg.KEYDOWN:
          #  if event.key == pg.K_SPACE:
             #   for enemy in enemy_group:
              #      enemy.take_damage(25)


    # Új enemy spawnolása idő alapján
    current_time = pg.time.get_ticks()
     # Új enemy spawnolásakor:
    if current_time - last_spawn_time > SPAWN_DELAY:
        enemy = Enemy(koordinatak, enemy_img1, enemy_img2)
        enemy_group.add(enemy)
        last_spawn_time = current_time


    #pg.draw.lines(screen,"grey100",False,koordinatak,2)
    #update groups
    enemy_group.update()

    #screen.fill((0, 0, 0)) háttér törlése
    enemy_group.draw(screen)
    tower_group.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        #mouse click event
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:#bal klikk
            mouse_pos=pg.mouse.get_pos()
            #a kurzornak a jatekban kell legyen
            if mouse_pos[0]<map_rect.width and mouse_pos[1]<map_rect.height:
                create_tower(mouse_pos )

    pg.display.update()
pg.quit()
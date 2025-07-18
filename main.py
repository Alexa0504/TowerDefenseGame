import pygame as pg
from pygame.draw_py import draw_line

from Game.enemy import Enemy
import constants as c

#inicializálom a pygamet
pg.init()

clock = pg.time.Clock()

# Térkép betöltése
map_image = pg.image.load('Assets/kepek/terkep.png')  # a térképed útvonala
map_rect = map_image.get_rect()

#betöltöm az ablakot
screen = pg.display.set_mode((c.Screen_width, c.Screen_height))
pg.display.set_caption("Játék")

#Az enemy betöltése
enemy_img=pg.image.load('Assets/kepek/Hal.png').convert_alpha()

enemy_group=pg.sprite.Group()
waypoints=[
    (179,9),
    (113,60),
    (115,207),
    (227,331),
    (397,345),
    (455,403),
    (459,645),
    (525,407),
    (599,713),
    (674,765),
    (855,779),
    (949,837),
    (947,941)
]

enemy=Enemy(waypoints,enemy_img,)
enemy_group.add(enemy)

running = True
while running:

    clock.tick(c.Framerates)
    screen.fill("grey100")

    pg.draw.lines(screen,"grey100",False,waypoints,2)
    #update groups
    enemy_group.update()


    #screen.fill((0, 0, 0)) háttér törlése
    enemy_group.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    pg.display.update()
pg.quit()
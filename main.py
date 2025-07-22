import pygame as pg
from pygame.draw_py import draw_line
from Game.world import World
from Game.enemy import Enemy
import constants as c
from Game.tower import Tower
from Game.button import Button


#inicializálom a pygamet
pg.init()

clock = pg.time.Clock()

pg.display.set_caption("Játék")
##################
#KEPEK BETOLTESE
##################


#Uj fegyverek letevése
placing_towers=False

# Térkép betöltése
map_image = pg.image.load('Assets/kepek/terkep.png')# a térképed útvonala
map_rect = map_image.get_rect()

#Ablak betöltése
screen = pg.display.set_mode((map_rect.width+c.Side_panel, map_rect.height))#hozzaadtam a side panelt is
map_image = map_image.convert_alpha()

#toolbar betoltese
toolbar_image = pg.image.load('Assets/kepek/JobbHatter.png')  # Kép betöltése
toolbar_image = pg.transform.scale(toolbar_image, (c.Side_panel, map_rect.height))  # Méretezés

#Ellenség betöltése
enemy_img1 = pg.image.load('Assets/kepek/piroshal.png').convert_alpha()  # Első kép
enemy_img2 = pg.image.load('Assets/kepek/kekhal.png').convert_alpha()  # Második kép

#Fegyver betöltése
tower_img=pg.image.load('Assets/kepek/ujLovo.png').convert_alpha()

#Térkép betöltése (Ahol fehér)
feherTerkep = pg.image.load('Assets/kepek/terkepfeher.png').convert_alpha()

# Toolbar kép betöltése
#toolbar= pg.image.load("Assets/kepek/toolbar2.png").convert_alpha()
# Átméretezzük, hogy pontosan kitöltse a jobb oldali sávot
#toolbar = pg.transform.scale(toolbar, (c.Side_panel, map_rect.height))

#Gombok betöltése és átméretezése
buy_button=pg.image.load('Assets/kepek/Gombok/BUYGOMB.png').convert_alpha()
buy_button=pg.transform.scale(buy_button, (200, 190))
cancel_button=pg.image.load('Assets/kepek/Gombok/CANCELGOMB.png').convert_alpha()
cancel_button=pg.transform.scale(cancel_button, (200, 190))
exit_button_img = pg.image.load('Assets/kepek/Gombok/EXITGOMB.png').convert_alpha()
exit_button_img = pg.transform.scale(exit_button_img, (200, 190))

#def create_tower(mouse_pos):
    #tower=Tower(tower_img,mouse_pos)
    #tower_group.add(tower)

#Hova lehet és hova nem lehet pakolni fegyvert
def create_tower(mouse_pos):
    # lehet e idepakolni
    color = feherTerkep.get_at(mouse_pos)
    if color == pg.Color(255, 255, 255):  # fehér → nem pakolható
        return
    # Torony kozepén lesz
    new_tower_rect = tower_img.get_rect(center=mouse_pos)

    # távolsag a középpontok között
    for tower in tower_group:
        #Megnézi hogy a torony túl közel van e egy már meglévőhöz
        dist = ((tower.rect.centerx - new_tower_rect.centerx) ** 2 +
                (tower.rect.centery - new_tower_rect.centery) ** 2) ** 0.5
        if dist < 40:  # Ha 40 pixelnel kozelebb van a masik torony
            return  # Nem hozok letre ujat

    # Ha nincs ütközés, hozzuk létre
    tower = Tower(tower_img, mouse_pos)
    tower_group.add(tower)


#Térkép elkészítése
world=World(map_image)

#Csoportok elkészítése
enemy_group=pg.sprite.Group()
tower_group=pg.sprite.Group()

#Új ellenségek létrehozása
SPAWN_DELAY = 2000  # 2000 ms = 2 masodperc
last_spawn_time = 0

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


# Ellenség létrehozásakor mindkét képet átadjuk
enemy = Enemy(koordinatak, enemy_img1, enemy_img2)
enemy_group.add(enemy)

#Gomb létrehozása(példányosítása) hova teszem le
buy_gomb=Button(map_rect.width+20,50,buy_button,True)
cancel_gomb=Button(map_rect.width+20,175,cancel_button,True)
exit_gomb = Button(map_rect.width + 20, 300, exit_button_img, True)

running = True
while running:

    clock.tick(c.Framerates)
    screen.fill("grey100")

        #############
        #Kirajzolás
        ##########
    # Térkép kirajzolása
    world.draw(screen)

    #Szin a toolbarnak
    #toolbar_rect = pg.Rect(map_rect.width, 0, c.Side_panel, map_rect.height)
    #pg.draw.rect(screen, (7,130,80), toolbar_rect)

    # Toolbar kirajzolása
    toolbar_rect = pg.Rect(map_rect.width, 0, c.Side_panel, map_rect.height)
    screen.blit(toolbar_image, toolbar_rect)

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

    #gomb kirajzolása
    if buy_gomb.draw(screen):
        placing_towers=True #Leteszi a fegyvert
    if placing_towers == True:
        #Ha megnyomom a buy gombot akkor megjelenik a cancel gomb
        if cancel_gomb.draw(screen):
            placing_towers=False

    # Exit gomb kezelése
    if exit_gomb.draw(screen):
        running = False

    #screen.fill((0, 0, 0)) háttér törlése
    enemy_group.draw(screen)
    tower_group.draw(screen)

    ################
    #UPDATEK
    ################
    #update groups
    enemy_group.update()


    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        #mouse click event
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:#bal klikk
            mouse_pos=pg.mouse.get_pos()
            #a kurzornak a jatekban kell legyen
            if placing_towers and mouse_pos[0]<map_rect.width and mouse_pos[1]<map_rect.height:
                create_tower(mouse_pos )

    pg.display.update()
pg.quit()
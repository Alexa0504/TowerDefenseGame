import pygame as pg
from Game.world import World
from Game.enemy import Enemy
import constants as c
from Game.tower import Tower
from Game.button import Button
from Game.explosion import Explosion


#inicializálom a pygamet
pg.init()

clock = pg.time.Clock()

pg.display.set_caption("Játék")

#változók
placing_towers=False
selected_towers=None
deleting_towers = False
dragging_tower = False
tower_preview_pos = None  # egér pozíció, ahova a tornyot mutatja
game_state = "menu"

##################
#KEPEK BETOLTESE
##################


# Térkép betöltése
map_image = pg.image.load('Assets/kepek/terkep.png')# a térképed útvonala
map_rect = map_image.get_rect()

#Ablak betöltése
screen = pg.display.set_mode((map_rect.width+c.Side_panel, map_rect.height))#hozzaadtam a side panelt is
map_image = map_image.convert_alpha()

#Kezdőképernyő betöltése
start_img=pg.image.load("assets/kepek/MenuKep.png")
start_img = pg.transform.scale(start_img, (screen.get_width(), screen.get_height()))

#toolbar betoltese
toolbar_image = pg.image.load('Assets/kepek/JobbHatter.png')  # Kép betöltése
toolbar_image = pg.transform.scale(toolbar_image, (c.Side_panel, map_rect.height))  # Méretezés

#Ellenség betöltése
enemy_img1 = pg.image.load('Assets/kepek/piroshal.png').convert_alpha()  # Első kép
enemy_img2 = pg.image.load('Assets/kepek/kekhal.png').convert_alpha()  # Második kép

#A fegyver animaciojanak betoltese
tower_frames = [
    pg.image.load('Assets/kepek/Lovo/ujLovo.png').convert_alpha(),
    pg.image.load('Assets/kepek/Lovo/ujLovo2.png').convert_alpha(),
    pg.image.load('Assets/kepek/Lovo/ujLovo3.png').convert_alpha(),
    pg.image.load('Assets/kepek/Lovo/ujLovo4.png').convert_alpha()
]
tower_frames = [pg.transform.scale(img, (100,100)) for img in tower_frames]

#Fegyver betöltése
tower_img=pg.image.load('Assets/kepek/Lovo/ujLovo.png').convert_alpha()
tower_img = pg.transform.scale(tower_img, (100, 100))

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
exit_button = pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha()
exit_button = pg.transform.scale(exit_button, (200, 190))
delete_button=pg.image.load('Assets/kepek/Gombok/DELETEGOMB.png').convert_alpha()
delete_button=pg.transform.scale(delete_button, (200, 190))
start_button=pg.image.load('Assets/kepek/Gombok/STARTGOMB.png').convert_alpha()
start_button=pg.transform.scale(start_button, (250, 250))
#exit_gomb2 = pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha()
#exit_gomb2 = pg.transform.scale(exit_button, (250, 250))
exit_button2 = pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha()
exit_button2 = pg.transform.scale(exit_button2, (250,250))


#Pénz és életerő ikonok
coin_img=pg.image.load('Assets/kepek/Coin.png').convert_alpha()
heart_img=pg.image.load('Assets/kepek/Heart.png').convert_alpha()

# x jel betöltése
x_img=pg.image.load('Assets/kepek/x.png').convert_alpha()
x_img=pg.transform.scale(x_img, (100, 100))

#Robbanás betöltése
bumm_img=pg.image.load('Assets/kepek/Robbanas/Robbanas.png').convert_alpha()
bumm_img=pg.transform.scale(bumm_img, (100, 100))

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
    tower = Tower(tower_frames, mouse_pos)
    tower_group.add(tower)

#Térkép elkészítése
world=World(map_image)

#Csoportok elkészítése
enemy_group=pg.sprite.Group()
tower_group=pg.sprite.Group()
#explosion_group=pg.sprite.Group()

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
buy_buttonn=Button(map_rect.width + 20, 50, buy_button, True)
cancel_buttonn=Button(map_rect.width + 20, 175, cancel_button, True)
exit_buttonn = Button(map_rect.width + 20, 300, exit_button, True)
delete_buttonn = Button(map_rect.width + 20, 450, delete_button, True)
start_button = Button(475, 150, start_button, True)
exit_button2 = Button(475,275, exit_button2, True)

#exit_gomb2=Button(475, 350, exit_gomb2, True)

#Szöveg megjelenítése
#Consolas
text_font=pg.font.SysFont('Comic Sans MS', 24,bold=True)
large_font=pg.font.SysFont('Comic Sans MS', 36)

#Számok(szöveg) kiírása a képernyőre
def draw_text(text,font,tex_color,x,y):
    img=font.render(text,True,tex_color)
    screen.blit(img,(x,y))



running = True
while running:

    clock.tick(c.Framerates)#hány képkockát engedélyez másodpercenként
    screen.fill("grey100")

    if game_state == "menu":
        screen.blit(start_img,(0,0))
       # screen.blit(toolbar_image, (map_rect.width, 0))
        if start_button.draw(screen):
            game_state = "playing"
        if exit_button2.draw(screen):
            running = False
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        continue  # Tovább a következő ciklusra


        #############
        #Kirajzolás
        ##########


    elif game_state == "playing":
        # Térkép kirajzolása
        world.draw(screen)
        # Toolbar kirajzolása
        toolbar_rect = pg.Rect(map_rect.width, 0, c.Side_panel, map_rect.height)
        screen.blit(toolbar_image, toolbar_rect)

    #Szin a toolbarnak
    #toolbar_rect = pg.Rect(map_rect.width, 0, c.Side_panel, map_rect.height)
    #pg.draw.rect(screen, (7,130,80), toolbar_rect)

    # Toolbar kirajzolása
   # if game_state == "game":
      #  toolbar_rect = pg.Rect(map_rect.width, 0, c.Side_panel, map_rect.height)
       # screen.blit(toolbar_image, toolbar_rect)


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


    #Itt tudom kurzorral húzni majd az ágyúkat
    if dragging_tower:
        tower_preview_pos = pg.mouse.get_pos()
        # Megnézem, hogy a preview kép a térképen van-e
        if tower_preview_pos[0] < map_rect.width:
            preview_rect = tower_img.get_rect(center=tower_preview_pos)
            screen.blit(tower_img, preview_rect)


    #gomb kirajzolása
    if buy_buttonn.draw(screen):
        dragging_tower = True
        placing_towers=True #Leteszi a fegyvert
        deleting_towers = False
        selected_towers = None
    if placing_towers == True:
        #Ha megnyomom a buy gombot akkor megjelenik a cancel gomb
        if cancel_buttonn.draw(screen):
            dragging_tower = False
            placing_towers=False
            deleting_towers = False
    # Exit gomb kezelése
    if exit_buttonn.draw(screen):
        running = False

    if delete_buttonn.draw(screen):
        deleting_towers = not deleting_towers  # Átvált True/False között

    #if delete_gomb.draw(screen):
    #    deleting_towers = True

    #screen.fill((0, 0, 0)) háttér törlése

#Csoportok kirajzolása
    enemy_group.draw(screen)
    #explosion_group.draw(screen)
    # tower_group.draw(screen)
    draw_text(str(world.health),text_font, "black", 5, 40)
    draw_text(str(world.money),text_font, "black", 5, 80)

#Pénz és életerő ikonok megjelenítése
    screen.blit(heart_img, (10, 40 + 20))
    screen.blit(coin_img, (10, 80 + 20))

    for tower in tower_group:
        tower.update()
        tower.draw(screen, selected=(tower == selected_towers))

    ################
    #UPDATEK
    ################
    #update groups
    enemy_group.update()
    tower_group.update()
    #explosion_group.update()

    # UPDATE-ek után: lőjenek a tornyok, ha enemy van a közelben
    for tower in tower_group:
        for enemy in enemy_group:
            distance = ((tower.rect.centerx - enemy.rect.centerx) ** 2 +
                        (tower.rect.centery - enemy.rect.centery) ** 2) ** 0.5
            if distance < tower.range:  # kisebb mint a range
                tower.fire()
                enemy.take_damage(5)
                break  # csak egy enemy-re lő egyszerre

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        #mouse click event
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:#bal klikk
            mouse_pos=pg.mouse.get_pos()
            if dragging_tower:
                # csak akkor rakjuk le, ha a térképre kattintunk
                if mouse_pos[0] < map_rect.width and mouse_pos[1] < map_rect.height:
                    if world.money > c.BUY_COST:
                        create_tower(mouse_pos)
                        world.money -= c.BUY_COST
                    else:
                        print("Nincs elég pénzed")
                    dragging_tower = False
                    tower_preview_pos = None


            #a kurzornak a jatekban kell legyen( nem a toolbar-ra kattintok hanem balra)
           # if placing_towers and mouse_pos[0]<map_rect.width and mouse_pos[1]<map_rect.height:
           #     create_tower(mouse_pos )

            # Ha nem vásárlás mód van, de toronyra kattintasz → TÖRLÉS
            elif placing_towers==False:
                for tower in tower_group:
                    if tower.rect.collidepoint(mouse_pos):#Az egeér benne van  ea torony téglalapjában
                        if deleting_towers:
                            tower.kill()
                            selected_towers=None
                        else:
                            selected_towers=tower
                        break  # csak egyet törlünk, amin a kurzor van
                else:
                    selected_towers=None #Ha nem a toronyra kattintottál

    if deleting_towers:
        screen.blit(x_img, (map_rect.width + 70, 550))
    pg.display.update()

pg.quit()
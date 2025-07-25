import pygame as pg
from Game.world import World
from Game.enemy import Enemy
import constants as c
from Game.tower import Tower
from Game.button import Button
from Game.explosion import Explosion

# inicializálom a pygamet
pg.init()

clock = pg.time.Clock()

pg.display.set_caption("Játék")

# változók
placing_towers = False
selected_towers = None
deleting_towers = False
dragging_tower = False
tower_preview_pos = None  # egér pozíció, ahova a tornyot mutatja
game_state = "menu"
# is_paused = False

##################
# KEPEK BETOLTESE
##################


# Térkép betöltése
map_image = pg.image.load('Assets/kepek/terkep.png')  # a térképed útvonala
map_rect = map_image.get_rect()

# Ablak betöltése
screen = pg.display.set_mode((map_rect.width + c.Side_panel, map_rect.height))  # hozzaadtam a side panelt is
map_image = map_image.convert_alpha()

# Kezdőképernyő betöltése
start_img = pg.image.load("assets/kepek/MenuKep.png")
start_img = pg.transform.scale(start_img, (screen.get_width(), screen.get_height()))

# toolbar betoltese
toolbar_image = pg.image.load('Assets/kepek/JobbHatter.png')  # Kép betöltése
toolbar_image = pg.transform.scale(toolbar_image, (c.Side_panel, map_rect.height))  # Méretezés

# Ellenség betöltése
enemy_img1 = pg.image.load('Assets/kepek/piroshal.png').convert_alpha()  # Első kép
enemy_img2 = pg.image.load('Assets/kepek/kekhal.png').convert_alpha()  # Második kép

# A fegyver animaciojanak betoltese
tower_frames = [
    pg.image.load('Assets/kepek/Lovo/ujLovo.png').convert_alpha(),
    pg.image.load('Assets/kepek/Lovo/ujLovo2.png').convert_alpha(),
    pg.image.load('Assets/kepek/Lovo/ujLovo3.png').convert_alpha(),
    pg.image.load('Assets/kepek/Lovo/ujLovo4.png').convert_alpha()
]
tower_frames = [pg.transform.scale(img, (100, 100)) for img in tower_frames]

# Fegyver betöltése
tower_img = pg.image.load('Assets/kepek/Lovo/ujLovo.png').convert_alpha()
tower_img = pg.transform.scale(tower_img, (100, 100))

# Térkép betöltése (Ahol fehér)
feherTerkep = pg.image.load('Assets/kepek/terkepfeher.png').convert_alpha()

# Toolbar kép betöltése
# toolbar= pg.image.load("Assets/kepek/toolbar2.png").convert_alpha()
# Átméretezzük, hogy pontosan kitöltse a jobb oldali sávot
# toolbar = pg.transform.scale(toolbar, (c.Side_panel, map_rect.height))

# Gombok betöltése és átméretezése
buy_button_img = pg.image.load('Assets/kepek/Gombok/BUYGOMB.png').convert_alpha()
buy_button_img = pg.transform.scale(buy_button_img, (200, 190))
cancel_button_img = pg.image.load('Assets/kepek/Gombok/CANCELGOMB.png').convert_alpha()
cancel_button_img = pg.transform.scale(cancel_button_img, (200, 190))
exit_button_img = pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha()
exit_button_img = pg.transform.scale(exit_button_img, (200, 190))
delete_button_img = pg.image.load('Assets/kepek/Gombok/DELETEGOMB.png').convert_alpha()
delete_button_img = pg.transform.scale(delete_button_img, (200, 190))
delete_button_red_img = pg.image.load('Assets/kepek/Gombok/DELETEGOMBPIROS.png').convert_alpha()
delete_button_red_img = pg.transform.scale(delete_button_red_img, (200, 190))
start_button_img = pg.image.load('Assets/kepek/Gombok/STARTGOMB.png').convert_alpha()
start_button_img = pg.transform.scale(start_button_img, (250, 250))
# exit_gomb2 = pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha()
# exit_gomb2 = pg.transform.scale(exit_button, (250, 250))
exit_button2_img = pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha()
exit_button2_img = pg.transform.scale(exit_button2_img, (250, 250))
pause_button_img = pg.image.load('Assets/kepek/Gombok/PAUSEGOMB.png').convert_alpha()
pause_button_img = pg.transform.scale(pause_button_img, (200, 190))
resume_button_img = pg.image.load('Assets/kepek/Gombok/RESUME.png').convert_alpha()
resume_button_img = pg.transform.scale(resume_button_img, (200, 190))

# Pénz és életerő ikonok
coin_img = pg.image.load('Assets/kepek/Coin.png').convert_alpha()
heart_img = pg.image.load('Assets/kepek/Heart.png').convert_alpha()

# x jel betöltése
# x_img=pg.image.load('Assets/kepek/x.png').convert_alpha()
# x_img=pg.transform.scale(x_img, (100, 100))


# Robbanás betöltése
bumm_img = pg.image.load('Assets/kepek/Robbanas/Robbanas.png').convert_alpha()
bumm_img = pg.transform.scale(bumm_img, (100, 100))


# def create_tower(mouse_pos):
# tower=Tower(tower_img,mouse_pos)
# tower_group.add(tower)

# Hova lehet és hova nem lehet pakolni fegyvert
def create_tower(mouse_pos):
    # lehet e idepakolni
    color = feherTerkep.get_at(mouse_pos)
    if color == pg.Color(255, 255, 255):  # fehér → nem pakolható
        return
    # Torony kozepén lesz
    new_tower_rect = tower_img.get_rect(center=mouse_pos)

    # távolsag a középpontok között
    for tower in tower_group:
        # Megnézi hogy a torony túl közel van e egy már meglévőhöz
        dist = ((tower.rect.centerx - new_tower_rect.centerx) ** 2 +
                (tower.rect.centery - new_tower_rect.centery) ** 2) ** 0.5
        if dist < 40:  # Ha 40 pixelnel kozelebb van a masik torony
            return  # Nem hozok letre ujat

    # Ha nincs ütközés, hozzuk létre
    tower = Tower(tower_frames, mouse_pos)
    tower_group.add(tower)


# Térkép elkészítése
world = World(map_image)

# Csoportok elkészítése
enemy_group = pg.sprite.Group()
tower_group = pg.sprite.Group()
# explosion_group=pg.sprite.Group()

# Új ellenségek létrehozása
SPAWN_DELAY = 2000  # 2000 ms = 2 masodperc
last_spawn_time = 0

koordinatak = [
    (179, 9),
    (113, 60),
    (115, 207),
    (227, 331),
    (397, 345),
    (455, 403),
    (459, 645),
    (559, 715),
    (665, 761),
    (869, 785),
    (955, 865)
]

# Ellenség létrehozásakor mindkét képet átadjuk
enemy = Enemy(koordinatak, enemy_img1, enemy_img2)
enemy_group.add(enemy)

# Gomb létrehozása(példányosítása) hova teszem le
buy_button = Button(map_rect.width + 20, c.start_y + 0 * (c.button_height + c.padding), buy_button_img, True)
cancel_button = Button(map_rect.width + 20, c.start_y + 1 * (c.button_height + c.padding), cancel_button_img, True)
delete_button = Button(map_rect.width + 20, c.start_y + 2 * (c.button_height + c.padding), delete_button_img, True)
pause_button = Button(map_rect.width + 20, c.start_y + 3 * (c.button_height + c.padding), pause_button_img, True)
resume_button = Button(map_rect.width + 20, c.start_y + 4 * (c.button_height + c.padding), resume_button_img, True)
exit_button = Button(map_rect.width + 20, c.start_y + 5 * (c.button_height + c.padding), exit_button_img, True)
start_button = Button(475, 150, start_button_img, True)  # Use the renamed variable
exit_button2 = Button(475, 275, exit_button2_img, True)  # Use the renamed variable

# exit_gomb2=Button(475, 350, exit_gomb2, True)

# Szöveg megjelenítése
# Consolas
text_font = pg.font.SysFont('Comic Sans MS', 24, bold=True)
large_font = pg.font.SysFont('Comic Sans MS', 36)


# Számok(szöveg) kiírása a képernyőre
def draw_text(text, font, tex_color, x, y):
    img = font.render(text, True, tex_color)
    screen.blit(img, (x, y))

def game_reset():
    global world, enemy_group, tower_group, last_spawn_time
    global placing_towers, selected_towers, deleting_towers, dragging_tower, tower_preview_pos

    world=World(map_image)
    enemy_group.empty()
    tower_group.empty()
    last_spawn_time = pg.time.get_ticks()
    enemy = Enemy(koordinatak, enemy_img1, enemy_img2)
    enemy_group.add(enemy)
    placing_towers = False
    selected_towers = None
    deleting_towers = False
    dragging_tower = False
    tower_preview_pos = None

running = True
while running:

    clock.tick(c.Framerates)  # hány képkockát engedélyez másodpercenként
    screen.fill("grey100")

    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Mouse click events
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Ez a bal klikkért felelős
            mouse_pos = pg.mouse.get_pos()

            if game_state == "menu":
                if start_button.draw(screen):
                    game_state = "playing"
                if exit_button2.draw(screen):
                    running = False
            elif game_state == "playing":
                if dragging_tower:
                    # Csak a térképre lehet tenni fegyvert
                    if mouse_pos[0] < map_rect.width and mouse_pos[1] < map_rect.height:
                        if world.money > c.BUY_COST:
                            create_tower(mouse_pos)
                            world.money -= c.BUY_COST
                        else:
                            print("Nincs elég pénzed")
                        dragging_tower = False
                        tower_preview_pos = None#Éppen nem húzok tornyot
                elif placing_towers == False:
                    for tower in tower_group:
                        if tower.rect.collidepoint(mouse_pos):#Az egér benne van a torony téglalapjában
                            if deleting_towers:
                                if delete_button_red_img.draw(screen):
                                    deleting_towers=False
                                else:
                                    if delete_button.draw(screen):
                                        deleting_towers = True
                                    else:
                                        selected_towers = tower
                                    break# csak egyet törlünk, amin a kurzor van
                            else:
                                selected_towers = None#Ha nem a toronyra kattintottál

                    if deleting_towers:
                        if delete_button_red_img.draw(screen):
                             deleting_towers = False  # Kikapcsolás, ha újra rákattintanak
                        else:
                            if delete_button.draw(screen):
                                 deleting_towers = True

    # A játék kirajzolása és frissítése
    if game_state == "menu":
        screen.blit(start_img, (0, 0))
        start_button.draw(screen)
        exit_button2.draw(screen)

    elif game_state == "playing":
        enemy_group.update()
        tower_group.update()

        # Térkép kirajzolása
        world.draw(screen)
        # Toolbar kirajzolása
        toolbar_rect = pg.Rect(map_rect.width, 0, c.Side_panel, map_rect.height)
        screen.blit(toolbar_image, toolbar_rect)

        # Új enemy spawnolása idő alapján
        current_time = pg.time.get_ticks()
        if current_time - last_spawn_time > SPAWN_DELAY:
            enemy = Enemy(koordinatak, enemy_img1, enemy_img2)
            enemy_group.add(enemy)
            last_spawn_time = current_time

        #Itt tudom kurzorral húzni majd az ágyúkat
        if dragging_tower:
            tower_preview_pos = pg.mouse.get_pos()
            # Megnézem, hogy a preview kép a térképen van-e
            if tower_preview_pos[0] < map_rect.width:
                preview_rect = tower_img.get_rect(center=tower_preview_pos)
                screen.blit(tower_img, preview_rect)

        # Gombok kirajolása és működése
        if buy_button.draw(screen):
            dragging_tower = True
            placing_towers = True
            deleting_towers = False
            selected_towers = None
        if placing_towers:
            if cancel_button.draw(screen):
                dragging_tower = False
                placing_towers = False
                deleting_towers = False

        # Átvált törlési és nem törlési mód között
        if deleting_towers:
            if delete_button_red_img.draw(screen):
                deleting_towers = False
        else:
            if delete_button.draw(screen):
                deleting_towers = True

        if exit_button.draw(screen):
            game_state="menu"
            game_reset()

           # running = False

        if pause_button.draw(screen):
            game_state = "paused"
            # enemy_group.empty()
            # tower_group.empty()

        ######################
        #Csoportok kirajzolása
        #######################

        enemy_group.draw(screen)
        draw_text(str(world.health), text_font, "black", 5, 40)
        draw_text(str(world.money), text_font, "black", 5, 80)

        # DPénz és szív okonok kirajzolása
        screen.blit(heart_img, (10, 40 + 20))
        screen.blit(coin_img, (10, 80 + 20))

        #távolsag a középpontok között
        for tower in tower_group:
            tower.update()
            tower.draw(screen, selected=(tower == selected_towers))
            for enemy in enemy_group:
                # Megnézi hogy a torony túl közel van e egy már meglévőhöz
                #A torony és az ellenség középpontja közötti távolság
                distance = ((tower.rect.centerx - enemy.rect.centerx) ** 2 +
                            (tower.rect.centery - enemy.rect.centery) ** 2) ** 0.5
                if distance < tower.range:
                    tower.fire()
                    enemy.take_damage(5)
                    break

    elif game_state == "paused":
        screen.fill("grey50")
        draw_text("PAUSED", large_font, "white", screen.get_width() / 2 - 80, screen.get_height() / 2 - 50)
        if resume_button.draw(screen):
            game_state = "playing"
        if exit_button.draw(screen):
            running = False

    pg.display.update()

pg.quit()
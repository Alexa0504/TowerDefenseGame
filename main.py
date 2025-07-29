import pygame as pg
from Game.world import World
from Game.enemy import Enemy
import constants as c
from Game.tower import Tower
from Game.button import Button

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
selected_button=None
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
enemy_img1 = pg.image.load('Assets/kepek/Enemy/piroshal.png').convert_alpha()  # Első kép
enemy_img2 = pg.image.load('Assets/kepek/Enemy/kekhal.png').convert_alpha()  # Második kép

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

# Gombok betöltése és átméretezése
buy_button_img = pg.image.load('Assets/kepek/Gombok/BUYGOMB.png').convert_alpha()
buy_button_img = pg.transform.scale(buy_button_img, (200, 190))
buy_button_img_2=pg.image.load('Assets/kepek/Gombok/BuyGombKlikk.png').convert_alpha()
buy_button_img_2=pg.transform.scale(buy_button_img_2, (200, 190))
cancel_button_img = pg.image.load('Assets/kepek/Gombok/CANCELGOMB.png').convert_alpha()
cancel_button_img = pg.transform.scale(cancel_button_img, (200, 190))
cancel_button_img_2=pg.image.load('Assets/kepek/Gombok/CancelGombKlikk.png').convert_alpha()
cancel_button_img_2=pg.transform.scale(cancel_button_img_2, (200, 190))
exit_button_img = pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha()
exit_button_img = pg.transform.scale(exit_button_img, (200, 190))
exit_button_img_2=pg.image.load('Assets/kepek/Gombok/EXITGOMB2Klikk.png').convert_alpha()
exit_button_img_2=pg.transform.scale(exit_button_img_2, (200, 190))
delete_button_img = pg.image.load('Assets/kepek/Gombok/DELETEGOMB.png').convert_alpha()
delete_button_img = pg.transform.scale(delete_button_img, (200, 190))
delete_button_red_img = pg.image.load('Assets/kepek/Gombok/DELETEGOMBPIROS.png').convert_alpha()
delete_button_red_img = pg.transform.scale(delete_button_red_img, (200, 190))
start_button_img = pg.image.load('Assets/kepek/Gombok/STARTGOMB.png').convert_alpha()
start_button_img = pg.transform.scale(start_button_img, (200, 190))
start_button_img_2=pg.image.load('Assets/kepek/Gombok/STARTGOMBKlikk.png').convert_alpha()
start_button_img_2=pg.transform.scale(start_button_img_2, (200, 190))
exit_button_menu_img = pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha()
exit_button_menu_img = pg.transform.scale(exit_button_menu_img, (200, 190))
exit_button_menu_img_2=pg.image.load('Assets/kepek/Gombok/EXITGOMB2Klikk.png').convert_alpha()
exit_button_menu_img_2=pg.transform.scale(exit_button_menu_img_2, (200, 190))
pause_button_img = pg.image.load('Assets/kepek/Gombok/PAUSEGOMB.png').convert_alpha()
pause_button_img = pg.transform.scale(pause_button_img, (200, 190))
pause_button_img_2=pg.image.load('Assets/kepek/Gombok/PAUSEGOMBKlikk.png').convert_alpha()
pause_button_img_2=pg.transform.scale(pause_button_img_2, (200, 190))
resume_button_img = pg.image.load('Assets/kepek/Gombok/RESUME.png').convert_alpha()
resume_button_img = pg.transform.scale(resume_button_img, (200, 190))
resume_button_img_2=pg.image.load('Assets/kepek/Gombok/RESUMEKlikk.png').convert_alpha()
resume_button_img_2=pg.transform.scale(resume_button_img_2, (200, 190))

# Pénz és életerő ikonok
coin_img = pg.image.load('Assets/kepek/Coin.png').convert_alpha()
heart_img = pg.image.load('Assets/kepek/Heart.png').convert_alpha()

# x jel betöltése
# x_img=pg.image.load('Assets/kepek/x.png').convert_alpha()
# x_img=pg.transform.scale(x_img, (100, 100))

# Robbanás betöltése

bumm_img = pg.image.load('Assets/kepek/Robbanas/Robbanas.png').convert_alpha()
bumm_img = pg.transform.scale(bumm_img, (100, 100))


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
# Mennyivel kell lejjebb helyezni a következő gombot
buy_button = Button(map_rect.width + 20, c.start_y + 0 * (c.button_height + c.padding), buy_button_img, buy_button_img_2)
cancel_button = Button(map_rect.width + 20, c.start_y + 1 * (c.button_height + c.padding), cancel_button_img, cancel_button_img_2)
delete_button = Button(map_rect.width + 20, c.start_y + 2 * (c.button_height + c.padding), delete_button_img, delete_button_red_img)
pause_button = Button(map_rect.width + 20, c.start_y + 3 * (c.button_height + c.padding), pause_button_img, pause_button_img_2)
resume_button = Button(map_rect.width + 20, c.start_y + 4 * (c.button_height + c.padding), resume_button_img, resume_button_img_2)
exit_button = Button(map_rect.width + 20, c.start_y + 5 * (c.button_height + c.padding), exit_button_img, exit_button_menu_img_2)
start_button = Button(475, 150, start_button_img, start_button_img_2)
exit_button_menu = Button(475, 275, exit_button_menu_img, exit_button_menu_img_2)

# exit_gomb_menu=Button(475, 350, exit_gomb_menu_img_2, True)

# Szöveg megjelenítése
text_font = pg.font.SysFont('Comic Sans MS', 24, bold=True)
large_font = pg.font.SysFont('Comic Sans MS', 36)


# Számok(szöveg) kiírása a képernyőre
def draw_text(text, font, tex_color, x, y):
    img = font.render(text, True, tex_color)
    screen.blit(img, (x, y))


def game_reset():
    global world, enemy_group, tower_group, last_spawn_time
    global placing_towers, selected_towers, deleting_towers, dragging_tower, tower_preview_pos

    world = World(map_image)
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
    # Reseteld a gomb képét is
    delete_button.image = delete_button_img


running = True
while running:

    clock.tick(c.Framerates)  # hány képkockát engedélyez másodpercenként
    screen.fill("grey100")

    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if game_state == "menu":
            # egérkattintás a menüben
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if start_button.rect.collidepoint(mouse_pos):
                    game_state = "playing"
                if exit_button_menu.rect.collidepoint(mouse_pos):
                    running = False

        elif game_state == "playing":
            # billentyűzet eseménykezelés
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:  # 'D' billentyű a törlésre
                    deleting_towers = not deleting_towers
                    placing_towers = False
                    dragging_tower = False
                    selected_towers = None
                    if deleting_towers:
                        delete_button.image = delete_button_red_img
                    else:
                        delete_button.image = delete_button_img
                elif event.key == pg.K_b:  # 'B' billentyű a vásárlásra
                    placing_towers = True
                    dragging_tower = True
                    deleting_towers = False
                    selected_towers = None
                    delete_button.image = delete_button_img

            # egérkattintás eseménykezelése
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # gombok kezelése
                if delete_button.rect.collidepoint(mouse_pos):
                    deleting_towers = not deleting_towers
                    placing_towers = False
                    dragging_tower = False
                    selected_towers = None
                    if deleting_towers:
                        delete_button.image = delete_button_red_img
                    else:
                        delete_button.image = delete_button_img
                elif buy_button.rect.collidepoint(mouse_pos):
                    dragging_tower = True
                    placing_towers = True
                    deleting_towers = False
                    selected_towers = None
                    delete_button.image = delete_button_img  # A buy gomb kikapcsolja a delete módot
                elif cancel_button.rect.collidepoint(mouse_pos):
                    dragging_tower = False
                    placing_towers = False
                    deleting_towers = False
                    selected_towers = None
                elif exit_button.rect.collidepoint(mouse_pos):
                    game_state = "menu"
                    game_reset()
                elif pause_button.rect.collidepoint(mouse_pos):
                    game_state = "paused"

                # torony elhelyezése
                elif dragging_tower and mouse_pos[0] < map_rect.width and mouse_pos[1] < map_rect.height:
                    if world.money >= c.BUY_COST:
                        create_tower(mouse_pos)
                        world.money -= c.BUY_COST
                    else:
                        print("Nincs elég pénzed")
                    dragging_tower = False
                    placing_towers = False
                    tower_preview_pos = None  # Éppen nem húzok tornyot

                # torony kijelölése vagy törlése
                elif mouse_pos[0] < map_rect.width and not dragging_tower:
                    clicked_on_tower = False
                    for tower in tower_group:
                        if tower.rect.collidepoint(mouse_pos):
                            clicked_on_tower = True
                            if deleting_towers:
                                tower.kill()
                                selected_towers = None
                                deleting_towers = False
                                delete_button.image = delete_button_img  # Törlés után visszaáll a gomb képe
                            else:
                                selected_towers = tower
                            break
                    if not clicked_on_tower:
                        selected_towers = None

        elif game_state == "paused":
            # egérkattintás a szünet képernyőn
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if resume_button.rect.collidepoint(mouse_pos):
                    game_state = "playing"
                if exit_button.rect.collidepoint(mouse_pos):
                    running = False

    # A játék kirajzolása és frissítése
    if game_state == "menu":
        screen.blit(start_img, (0, 0))
        start_button.draw(screen)
        exit_button_menu.draw(screen)

    elif game_state == "playing":
        enemy_group.update()
        tower_group.update()

        # térkép és toolbar kirajzolása
        world.draw(screen)
        toolbar_rect = pg.Rect(map_rect.width, 0, c.Side_panel, map_rect.height)
        screen.blit(toolbar_image, toolbar_rect)

        # Törlés mód szöveg kiírása
        if deleting_towers:
            draw_text("Törlés mód aktív!", text_font, (255, 0, 0), map_rect.width + 10, c.start_y - 40)

        # új ellenség spawnolása idő alapján
        current_time = pg.time.get_ticks()
        if current_time - last_spawn_time > SPAWN_DELAY:
            enemy = Enemy(koordinatak, enemy_img1, enemy_img2)
            enemy_group.add(enemy)
            last_spawn_time = current_time

        # torony húzása a kurzorral
        if dragging_tower:
            tower_preview_pos = pg.mouse.get_pos()
            # Megnézem, hogy a preview kép a térképen van-e
            if tower_preview_pos[0] < map_rect.width:
                preview_rect = tower_img.get_rect(center=tower_preview_pos)
                screen.blit(tower_img, preview_rect)

        # gombok kirajzolása
        buy_button.draw(screen)
        if placing_towers:  # csak akkor rajzolja ki a cancel gombot, ha tornyot helyezel el
            cancel_button.draw(screen)

        delete_button.draw(screen)
        pause_button.draw(screen)
        exit_button.draw(screen)

        # csoportok kirajzolása
        enemy_group.draw(screen)
        draw_text(str(world.health), text_font, "black", 5, 40)
        draw_text(str(world.money), text_font, "black", 5, 80)

        # Pénz és szív ikonok kirajzolása
        screen.blit(heart_img, (10, 40 + 20))
        screen.blit(coin_img, (10, 80 + 20))

        # távolsag a középpontok között, tornyok frissítése és lövése
        for tower in tower_group:
            tower.update()
            tower.draw(screen, selected=(tower == selected_towers))
            for enemy in enemy_group:
                # A torony és az ellenség középpontja közötti távolság
                distance = ((tower.rect.centerx - enemy.rect.centerx) ** 2 +
                            (tower.rect.centery - enemy.rect.centery) ** 2) ** 0.5
                if distance < tower.range:
                    tower.fire()
                    enemy.take_damage(5)
                    break

    elif game_state == "paused":
        screen.fill("grey50")
        draw_text("PAUSED", large_font, "white", screen.get_width() / 2 - 80, screen.get_height() / 2 - 50)
        resume_button.draw(screen)
        exit_button.draw(screen)

    pg.display.update()

pg.quit()
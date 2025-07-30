import pygame as pg
from Game.world import World
from Game.enemy import Enemy
import constants as c
from Game.tower import Tower
from Game.button import Button
from Game.enemy_boat import Enemy_boat

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
selected_button = None
game_state = "menu"

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

# Table betöltése
table_img = pg.image.load('Assets/kepek/Table.png').convert_alpha()
table_img = pg.transform.scale(table_img, (400, 100))

# Ellenség betöltése
enemy_fish_img1 = pg.image.load('Assets/kepek/Enemy/piroshal.png').convert_alpha()  # Első kép
enemy_fish_img2 = pg.image.load('Assets/kepek/Enemy/kekhal.png').convert_alpha()  # Második kép

enemy_boat_img = pg.image.load('Assets/kepek/Enemy/Hajo.png').convert_alpha()
enemy_boat_img = pg.transform.scale(enemy_boat_img, (100, 100))

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
buy_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/BUYGOMB.png').convert_alpha(), (200, 190))
cancel_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/CANCELGOMB.png').convert_alpha(), (200, 190))
exit_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha(), (200, 190))
delete_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/DELETEGOMB.png').convert_alpha(), (200, 190))
delete_button_red_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/DELETEGOMBPIROS.png').convert_alpha(),
                                           (200, 190))
start_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/STARTGOMB.png').convert_alpha(), (200, 190))
exit_button_menu_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha(),
                                          (200, 190))
pause_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/PAUSEGOMB.png').convert_alpha(), (200, 190))
resume_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/RESUME.png').convert_alpha(), (200, 190))

# Pénz és életerő ikonok
coin_img = pg.image.load('Assets/kepek/Coin.png').convert_alpha()
heart_img = pg.image.load('Assets/kepek/Heart.png').convert_alpha()


class Game:
    def __init__(self):

        # A játék aktuális állapotát jelző változók
        global placing_towers, selected_towers, deleting_towers, dragging_tower, tower_preview_pos, selected_button, game_state, last_spawn_time

        self.placing_towers = placing_towers
        self.selected_towers = selected_towers
        self.deleting_towers = deleting_towers
        self.dragging_tower = dragging_tower
        self.tower_preview_pos = tower_preview_pos
        self.selected_button = selected_button
        self.game_state = game_state
        self.running = True

        # Játék objektumok
        self.world = World(map_image)
        self.enemy_group = pg.sprite.Group()
        self.tower_group = pg.sprite.Group()

        # Új ellenségek létrehozásához időzítés
        self.SPAWN_DELAY = 2000  # 2000 ms = 2 masodperc
        self.last_spawn_time = 0  # Az előző spawn idejét tároljuk

        self.enemies_to_spawn_in_wave = 5  # Ennyi ellenség jön egy hullámban
        self.enemies_spawned_this_wave = 0  # Ennyi ellenség jött már a jelenlegi hullámban
        self.wave_completed = False  # Jelzi, ha egy hullám ellenségei elpusztultak

        # Koordináták az ellenség útvonalához
        self.koordinatak = [
            (179, 9), (113, 60), (115, 207), (227, 331), (397, 345),
            (455, 403), (459, 645), (559, 715), (665, 761), (869, 785), (955, 865)
        ]

        # Gomb létrehozása(példányosítása) hova teszem le
        # Mennyivel kell lejjebb helyezni a következő gombot
        self.buy_button = Button(map_rect.width + 20, c.start_y + 0 * (c.button_height + c.padding), buy_button_img,True)
        self.cancel_button = Button(map_rect.width + 20, c.start_y + 1 * (c.button_height + c.padding), cancel_button_img, True)
        self.delete_button = Button(map_rect.width + 20, c.start_y + 2 * (c.button_height + c.padding), delete_button_img, True)
        self.pause_button = Button(map_rect.width + 20, c.start_y + 3 * (c.button_height + c.padding), pause_button_img, True)
        self.resume_button = Button(map_rect.width + 20, c.start_y + 4 * (c.button_height + c.padding),resume_button_img, True)
        self.exit_button = Button(map_rect.width + 20, c.start_y + 5 * (c.button_height + c.padding), exit_button_img, True)
        self.start_button = Button(500, 150, start_button_img, True)
        self.exit_button_menu = Button(500, 275, exit_button_menu_img, True)

        # Szöveg megjelenítése
        self.text_font = pg.font.SysFont('Comic Sans MS', 24, bold=True)
        self.large_font = pg.font.SysFont('Comic Sans MS', 36, bold=True)

        # Kezdeti ellenségek spawnolása
        #self._spawn_initial_enemies()
        self._start_new_wave()

    def _start_new_wave(self):
        """Előkészíti és elindítja a következő ellenséghullámot."""
        # Növeljük a szintet
        if self.world.level<5:
            self.world.level += 1
        else:
            print("Finished")
            self.running = False

        # Beállítjuk a következő hullámhoz szükséges értékeket
        self.enemies_spawned_this_wave = 0
        self.wave_completed = False
        self.last_spawn_time = pg.time.get_ticks()  # Reseteljük a spawn időzítőt az új hullámhoz

        # Az ellenségek száma növekedhet a szinttel (például)
        self.enemies_to_spawn_in_wave = 5 + (self.world.level - 1) * 2 # Példa: minden szinten 4-el több ellenség(10-el kezd)

    def _spawn_enemy_in_wave(self):
        """Spawnol egy ellenséget, ha még nem érte el a hullám limitjét."""
        if self.enemies_spawned_this_wave < self.enemies_to_spawn_in_wave:
            # Ellenség létrehozása (globális képeket használ)
            enemy = Enemy(self.koordinatak, enemy_fish_img1, enemy_fish_img2)
            enemy_boat = Enemy_boat(self.koordinatak, enemy_boat_img)
            self.enemy_group.add(enemy, enemy_boat)
            self.enemies_spawned_this_wave += 1
            return True  # Jelzi, hogy spawnolt egy ellenséget
        return False  # Jelzi, hogy már nem kell több ellenséget spawnolni ebben a hullámban

    def draw_text(self, text, font, text_color, x, y):
        """Számok(szöveg) kiírása a képernyőre"""
        img = font.render(text, True, text_color)
        screen.blit(img, (x, y))  # A globális 'screen' felületre rajzolunk

    def create_tower(self, mouse_pos):
        """Hova lehet és hova nem lehet pakolni fegyvert"""
        # lehet e idepakolni
        color = feherTerkep.get_at(mouse_pos)  # feherTerkep globális
        if color == pg.Color(255, 255, 255):  # fehér → nem pakolható
            return
        # Torony kozepén lesz
        new_tower_rect = tower_img.get_rect(center=mouse_pos)  # tower_img globális

        # távolsag a középpontok között
        for tower in self.tower_group:
            # Megnézi hogy a torony túl közel van e egy már meglévőhöz
            dist = ((tower.rect.centerx - new_tower_rect.centerx) ** 2 +
                    (tower.rect.centery - new_tower_rect.centery) ** 2) ** 0.5
            if dist < 40:  # Ha 40 pixelnel kozelebb van a masik torony
                return  # Nem hozok letre ujat

        # Ha nincs ütközés, hozzuk létre
        tower = Tower(tower_frames, mouse_pos)  # tower_frames globális
        self.tower_group.add(tower)

    def game_reset(self):
        """Játék állapotának visszaállítása kezdeti értékre"""
        global placing_towers, selected_towers, deleting_towers, dragging_tower, tower_preview_pos, game_state, last_spawn_time

        self.world = World(map_image) # map_image globális
        self.enemy_group.empty()
        self.tower_group.empty()

        self.enemies_spawned_this_wave = 0
        self.wave_completed = False
        self.last_spawn_time = pg.time.get_ticks() #Időzítő

        # Uj első hullám
        self._start_new_wave() # Most már ezt hívjuk reseteléskor is
        self.world = World(map_image)  # map_image globális
        self.enemy_group.empty()
        self.tower_group.empty()
        self.last_spawn_time = pg.time.get_ticks()
        self.placing_towers = False
        self.selected_towers = None
        self.deleting_towers = False
        self.dragging_tower = False
        self.tower_preview_pos = None
        # Frissíteni a delete gombot is
        self.delete_button.image = delete_button_img  # delete_button_img globális

    # --- Eseménykezelő Metódusok Állapotokhoz ---

    def menu_events(self, event):
        """Eseménykezelés a 'menu' állapotban."""
        global running, game_state  # running globális ciklushoz

        # egérkattintás a menüben
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # bal klikk
            mouse_pos = event.pos
            if self.start_button.rect.collidepoint(mouse_pos):
                self.game_state = "playing"
            if self.exit_button_menu.rect.collidepoint(mouse_pos):
                self.running = False

    def playing_events(self, event):
        """Eseménykezelés a 'playing' állapotban."""
        # ezek a változók az osztályban is kezelve vannak, de a globálishoz is hozzáférés kellhet
        global placing_towers, selected_towers, deleting_towers, dragging_tower, tower_preview_pos, game_state

        # billentyűzet eseménykezelés
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:  # 'D' billentyű a törlésre
                self.deleting_towers = not self.deleting_towers
                self.placing_towers = False
                self.dragging_tower = False
                self.selected_towers = None
                if self.deleting_towers:
                    self.delete_button.image = delete_button_red_img  # globális kép
                else:
                    self.delete_button.image = delete_button_img  # globális kép
            elif event.key == pg.K_b:  # 'B' billentyű a vásárlásra
                self.placing_towers = True
                self.dragging_tower = True
                self.deleting_towers = False
                self.selected_towers = None
                self.delete_button.image = delete_button_img  # globális kép

        # egérkattintás eseménykezelése
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # gombok kezelése
            if self.delete_button.rect.collidepoint(mouse_pos):
                self.deleting_towers = not self.deleting_towers
                self.placing_towers = False
                self.dragging_tower = False
                self.selected_towers = None
                if self.deleting_towers:
                    self.delete_button.image = delete_button_red_img  # globális kép
                else:
                    self.delete_button.image = delete_button_img  # globális kép
            elif self.buy_button.rect.collidepoint(mouse_pos):
                self.dragging_tower = True
                self.placing_towers = True
                self.deleting_towers = False
                self.selected_towers = None
                self.delete_button.image = delete_button_img  # A buy gomb kikapcsolja a delete módot (globális kép)
            elif self.cancel_button.rect.collidepoint(mouse_pos):
                self.dragging_tower = False
                self.placing_towers = False
                self.deleting_towers = False
                self.selected_towers = None
            elif self.exit_button.rect.collidepoint(mouse_pos):
                self.game_state = "menu"
                self.game_reset()
            elif self.pause_button.rect.collidepoint(mouse_pos):
                self.game_state = "paused"

            # torony elhelyezése
            elif self.dragging_tower and mouse_pos[0] < map_rect.width and mouse_pos[1] < map_rect.height:  # map_rect globális
                if self.world.money >= c.BUY_COST:
                    current_tower_count = len(self.tower_group)
                    self.create_tower(mouse_pos)
                    # Csak akkor vonjuk le a pénzt, ha tényleg sikeresen létrehoztuk a tornyot
                    if len(self.tower_group) > current_tower_count:
                        self.world.money -= c.BUY_COST
                    else:
                        print("Nem lehet ide tornyot építeni, vagy túl közel van egy másikhoz!")
                else:
                    print("Nincs elég pénzed")
                self.dragging_tower = False
                self.placing_towers = False
                self.tower_preview_pos = None  # Éppen nem húzok tornyot

            # torony kijelölése vagy törlése
            elif mouse_pos[0] < map_rect.width and not self.dragging_tower:  # map_rect globális
                clicked_on_tower = False
                for tower in self.tower_group:
                    if tower.rect.collidepoint(mouse_pos):
                        clicked_on_tower = True
                        if self.deleting_towers:
                            tower.kill()
                            self.selected_towers = None
                            self.deleting_towers = False
                            self.delete_button.image = delete_button_img  # Törlés után visszaáll a gomb képe (globális kép)
                        else:
                            self.selected_towers = tower
                        break
                if not clicked_on_tower:
                    self.selected_towers = None

    def paused_events(self, event):
        """Eseménykezelés a 'paused' állapotban."""
        global game_state, running  # running globális ciklushoz

        # egérkattintás a szünet képernyőn
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.resume_button.rect.collidepoint(mouse_pos):
                self.game_state = "playing"
            if self.exit_button.rect.collidepoint(mouse_pos):
                self.running = False

    def _draw_menu_screen(self):
        """Kirajzolja a menü képernyő elemeit."""
        screen.blit(start_img, (0, 0))  # start_img globális
        self.start_button.draw(screen)
        self.exit_button_menu.draw(screen)

    def _draw_playing_screen(self):
        """Frissíti és kirajzolja a játék állapotának elemeit."""
        # Objektumok frissítése
        self.enemy_group.update()
        self.tower_group.update()

        # térkép és toolbar kirajzolása
        self.world.draw(screen)  # A globális 'screen' felületre rajzolunk
        toolbar_rect = pg.Rect(map_rect.width, 0, c.Side_panel, map_rect.height)  # Jobb szélén, 0 pixel magasságban
        screen.blit(toolbar_image, toolbar_rect)  # toolbar_image globális

        # Új ellenség spawnolása hullámok szerint
        current_time = pg.time.get_ticks()
        if not self.wave_completed:
            if current_time - self.last_spawn_time > self.SPAWN_DELAY:
                if self._spawn_enemy_in_wave():
                    self.last_spawn_time = current_time
                else:

                    if len(self.enemy_group) == 0:
                        self.wave_completed = True

        # Ha a hullám befejeződött és nincs több ellenség a pályán, lépjünk új hullámba
        if self.wave_completed and len(self.enemy_group) == 0:
            self._start_new_wave()  # Indítjuk a következő hullámot!

        # torony húzása a kurzorral
        if self.dragging_tower:
            self.tower_preview_pos = pg.mouse.get_pos()
            # Megnézem, hogy a preview kép a térképen van-e
            if self.tower_preview_pos[0] < map_rect.width:  # map_rect globális
                preview_rect = tower_img.get_rect(center=self.tower_preview_pos)  # tower_img globális
                screen.blit(tower_img, preview_rect)  # tower_img globális

        # gombok kirajzolása
        self.buy_button.draw(screen)
        if self.placing_towers:  # csak akkor rajzolja ki a cancel gombot, ha tornyot helyezel el
            self.cancel_button.draw(screen)

        self.delete_button.draw(screen)
        self.pause_button.draw(screen)
        self.exit_button.draw(screen)

        # csoportok kirajzolása
        self.enemy_group.draw(screen)
        self.draw_text(str(self.world.health), self.text_font, "black", 5, 40)
        self.draw_text(str(self.world.money), self.text_font, "black", 5, 80)
        screen.blit(table_img, (330, 35))  # table_img globális
        self.draw_text("Level: " + str(self.world.level), self.large_font, "black", 455, 45)

        # Pénz és szív ikonok kirajzolása
        screen.blit(heart_img, (10, 40 + 20))  # heart_img globális
        screen.blit(coin_img, (10, 80 + 20))  # coin_img globális

        # távolsag a középpontok között, tornyok frissítése és lövése
        for tower in self.tower_group:
            tower.update()
            tower.draw(screen, selected=(tower == self.selected_towers))
            for enemy in self.enemy_group:
                # A torony és az ellenség középpontja közötti távolság
                distance = ((tower.rect.centerx - enemy.rect.centerx) ** 2 +
                            (tower.rect.centery - enemy.rect.centery) ** 2) ** 0.5
                if distance < tower.range:
                    tower.fire()
                    enemy.take_damage(5)
                    break

    def _draw_paused_screen(self):
        """Kirajzolja a szünet képernyő elemeit."""
        screen.fill("grey50")
        self.draw_text("PAUSED", self.large_font, "white", screen.get_width() / 2 - 80, screen.get_height() / 2 - 50)
        self.resume_button.draw(screen)
        self.exit_button.draw(screen)

    def run(self):
        """A játék fő ciklusa."""
        global running, game_state, clock  # Globális változók elérése a fő ciklusban

        while self.running:  # Ez a ciklus az osztály running változóját figyeli
            clock.tick(c.Framerates)  # hány képkockát engedélyez másodpercenként
            screen.fill("grey100")

            # Eseménykezelés
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False  # Kilépés az osztály futásából, ami megállítja a while ciklust

                if self.game_state == "menu":
                    self.menu_events(event)
                elif self.game_state == "playing":
                    self.playing_events(event)
                elif self.game_state == "paused":
                    self.paused_events(event)

            # A játék kirajzolása és frissítése
            if self.game_state == "menu":
                self._draw_menu_screen()
            elif self.game_state == "playing":
                self._draw_playing_screen()
            elif self.game_state == "paused":
                self._draw_paused_screen()

            pg.display.update()

        pg.quit()


if __name__ == "__main__":
    game = Game()
    game.run()

import pygame as pg
from Game.world import World
from Game.enemy import Enemy
import constants as c
from Game.tower import Tower
from Game.button import Button
from Game.enemy_boat import Enemy_boat
from Game.enemy_pufferfish import Enemy_pufferfish
import random

"""Initialize Pygame"""
pg.init()

clock = pg.time.Clock()

pg.display.set_caption("Játék")

"""Loading images"""

"""Map"""
map_image = pg.image.load('Assets/kepek/terkep.png')
map_rect = map_image.get_rect()

"""Screen and side panel"""
screen = pg.display.set_mode((map_rect.width + c.Side_panel, map_rect.height))
map_image = map_image.convert_alpha()

"""Loading the start screen (menu)"""
start_img = pg.image.load("assets/kepek/MenuKep.png")
start_img = pg.transform.scale(start_img, (screen.get_width(), screen.get_height()))

"""Loading the toolbar"""
toolbar_image = pg.image.load('Assets/kepek/JobbHatter.png')
toolbar_image = pg.transform.scale(toolbar_image, (c.Side_panel, map_rect.height))

"""Loading the table"""
table_img = pg.image.load('Assets/kepek/Table.png').convert_alpha()
table_img = pg.transform.scale(table_img, (400, 100))

"""Loading enemy"""
enemy_fish_img1 = pg.image.load('Assets/kepek/Enemy/piroshal.png').convert_alpha()
enemy_fish_img2 = pg.image.load('Assets/kepek/Enemy/kekhal.png').convert_alpha()
enemy_boat_img = pg.image.load('Assets/kepek/Enemy/Hajo.png').convert_alpha()
enemy_boat_img = pg.transform.scale(enemy_boat_img, (100, 100))
pufferfish1_img=pg.image.load('Assets/kepek/Enemy/Pufferfish1.png').convert_alpha()
pufferfish1_img = pg.transform.scale(pufferfish1_img, (75, 75))
pufferfish2_img=pg.image.load('Assets/kepek/Enemy/Pufferfish2.png').convert_alpha()
pufferfish2_img = pg.transform.scale(pufferfish2_img, (75, 75))

"""Load turret animation frames"""
turret_frames = [
    pg.image.load('Assets/kepek/Lovo/ujLovo.png').convert_alpha(),
    pg.image.load('Assets/kepek/Lovo/ujLovo2.png').convert_alpha(),
    pg.image.load('Assets/kepek/Lovo/ujLovo3.png').convert_alpha(),
    pg.image.load('Assets/kepek/Lovo/ujLovo4.png').convert_alpha()]
turret_frames = [pg.transform.scale(img, (100, 100)) for img in turret_frames]

"""Loading the wturret for basic weapon handling"""
turret_img = pg.image.load('Assets/kepek/Lovo/ujLovo.png').convert_alpha()
turret_img = pg.transform.scale(turret_img, (100, 100))

"""Loading the white map"""
white_map = pg.image.load('Assets/kepek/terkepfeher.png').convert_alpha()

"""Loading buttons and scaling their size"""
buy_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/BUYGOMB.png').convert_alpha(), (200, 190))
cancel_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/CANCELGOMB.png').convert_alpha(), (200, 190))
exit_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha(), (200, 190))
delete_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/DELETEGOMB.png').convert_alpha(), (200, 190))
delete_button_red_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/DELETEGOMBPIROS.png').convert_alpha(), (200, 190))
start_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/STARTGOMB.png').convert_alpha(), (200, 190))
exit_button_menu_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/EXITGOMB2.png').convert_alpha(),   (200, 190))
pause_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/PAUSEGOMB.png').convert_alpha(), (200, 190))
resume_button_img = pg.transform.scale(pg.image.load('Assets/kepek/Gombok/RESUME.png').convert_alpha(), (200, 190))

"""Money and health icons"""
coin_img = pg.image.load('Assets/kepek/Coin.png').convert_alpha()
heart_img = pg.image.load('Assets/kepek/Heart.png').convert_alpha()


class Game:
    """Handles game initialization, main loop, event processing, updating game state, and rendering."""
    def __init__(self):
        """Sets up game variables, world, enemy and tower groups, UI buttons, fonts, and starts the first enemy wave."""

        self.placing_turrets = False
        self.selected_turrets = None
        self.deleting_turrets = False
        self.dragging_turret = False
        self.turret_preview_pos = None # Preview position for turret placement
        self.selected_button = None
        self.game_state = "menu"
        self.running = True
        self.is_game_over = False

        self.world = World(map_image)
        self.enemy_group = pg.sprite.Group()
        self.turret_group = pg.sprite.Group()

        self.SPAWN_DELAY = 1000  # 1000 ms = 1 second
        self.last_spawn_time = 0

        self.enemies_to_spawn_in_wave = 5
        self.enemies_spawned_this_wave = 0
        self.wave_completed = False

        self.enemy_list = []

        self.coordinates = [
            (179, 9), (113, 60), (115, 207), (227, 331), (397, 345),
            (455, 403), (459, 645), (559, 715), (665, 761), (869, 785), (955, 865)
        ]

        # Creating (instantiating) buttons-where to place them
        self.buy_button = Button(map_rect.width + 20, c.start_y + 0 * (c.button_height + c.padding), buy_button_img, True)
        self.cancel_button = Button(map_rect.width + 20, c.start_y + 1 * (c.button_height + c.padding), cancel_button_img, True)
        self.delete_button = Button(map_rect.width + 20, c.start_y + 2 * (c.button_height + c.padding), delete_button_img, True)
        self.pause_button = Button(map_rect.width + 20, c.start_y + 3 * (c.button_height + c.padding), pause_button_img,True)
        self.resume_button = Button(map_rect.width + 20, c.start_y + 4 * (c.button_height + c.padding),resume_button_img, True)
        self.exit_button = Button(map_rect.width + 20, c.start_y + 5 * (c.button_height + c.padding), exit_button_img,  True)
        self.start_button = Button(500, 150, start_button_img, True)
        self.exit_button_menu = Button(500, 275, exit_button_menu_img, True)

        # Displaying text
        self.text_font = pg.font.SysFont('Comic Sans MS', 24, bold=True)
        self.large_font = pg.font.SysFont('Comic Sans MS', 36, bold=True)

    def start_new_wave(self):
        """Prepares and starts the next enemy wave."""

        #Level up
        if self.world.level < 5:
            self.world.level += 1
        else:
            print("Finished")
            self.running = False

        #Set values needed for the next wave
        self.enemies_spawned_this_wave = 0
        self.wave_completed = False
        self.last_spawn_time = pg.time.get_ticks() #Reset the spawn timer for the new wave

        self.enemies_to_spawn_in_wave = 5 + (self.world.level - 1) * 2  #The number of enemies always increases by two with each level.

    def spawn_enemy_in_wave(self):
        """Spawns an enemy if the wave limit has not been reached yet"""

        if self.enemies_spawned_this_wave < self.enemies_to_spawn_in_wave:
            enemy_type = random.choice([
                Enemy_pufferfish(self.coordinates, pufferfish1_img, pufferfish2_img),
                Enemy_boat(self.coordinates, enemy_boat_img),
                Enemy(self.coordinates, enemy_fish_img1, enemy_fish_img2)
            ])
            self.enemy_group.add(enemy_type)
            self.enemies_spawned_this_wave += 1
            return True  #An enemy is successfully spawned
        return False  #It indicates that no more enemies need to be spawned in this wave once the limit is reached

    def draw_text(self, text, font, text_color, x, y, center=False):
        """Displays numbers (text) on the screen"""

        img = font.render(text, True, text_color)
        text_rect = img.get_rect()
        if center:
            text_rect.center = (x, y)  #If True, it will display the text centered on the screen
        else:
            text_rect.topleft = (x, y) #If False, the (x, y) point will be the top-left corner of the text.
        screen.blit(img, text_rect)

    def create_turret(self, mouse_pos):
        """Defines valid and invalid areas for tower placement"""

        # Checks if a turret can be placed here
        color = white_map.get_at(mouse_pos)
        if color == pg.Color(255, 255, 255):  #If it's white, placement is not allowed
            return
        # The tower will be centered at the mouse position.
        new_turret_rect = turret_img.get_rect(center=mouse_pos)

        for tower in self.turret_group:
            # It checks if the tower is too close to an existing one
            dist = ((tower.rect.centerx - new_turret_rect.centerx) ** 2 +
                    (tower.rect.centery - new_turret_rect.centery) ** 2) ** 0.5
            if dist < 40:  # If it is closer than 40 pixels to another tower
                return  # Do not create a new one

        # If there is no collision, create it
        tower = Tower(turret_frames, mouse_pos)
        self.turret_group.add(tower)

    def game_reset(self):
        """Resets the game state to the initial values, clearing the world, enemy, and tower groups."""

        self.world = World(map_image)
        self.enemy_group.empty()
        self.turret_group.empty()

        self.enemies_spawned_this_wave = 0
        self.wave_completed = False
        self.last_spawn_time = pg.time.get_ticks()

        self.is_game_over = False

        self.start_new_wave()

        self.placing_turrets = False
        self.selected_turrets = None
        self.deleting_turrets = False
        self.dragging_turret = False
        self.turret_preview_pos = None
        self.delete_button.image = delete_button_img

    def check_for_game_over(self):
        """Checks if the game is over, if any enemy has reached the end of the path."""
        # If any enemy's right edge is beyond the end of the path, the game is over.
        for enemy in self.enemy_group:
            if enemy.rect.right >= self.coordinates[10][0]:
                self.is_game_over = True
                self.game_state = "game_over"
                return True
        return False

    def game_over_events(self, event):
        """Handles events in the 'game_over' state."""
        # If the game is over, we can handle events like pressing 'M' for menu or 'Escape' to exit.
        if event.type == pg.QUIT:
            self.running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_m:
                self.game_state = "menu"
                self.game_reset()
                self.is_game_over = False
            elif event.key == pg.K_ESCAPE:
                self.game_state = "exit"
                self.running = False

    def menu_events(self, event):
        """Handles events in the 'menu' state."""
        # If the game is in the menu state, we can handle events like starting the game or exiting.
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # left mouse button
            # Check if the mouse position collides with the start or exit buttons
            mouse_pos = event.pos
            if self.start_button.rect.collidepoint(mouse_pos):
                self.game_state = "playing"
            if self.exit_button_menu.rect.collidepoint(mouse_pos):
                self.running = False

    def playing_events(self, event):
        """Handles events in the 'playing' state."""
        # If the game is in the playing state, we can handle events like placing towers,
        # deleting towers, or pausing the game.
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:  # 'D' key for deleting towers
                self.deleting_turrets = not self.deleting_turrets
                self.placing_turrets = False
                self.dragging_turret = False
                self.selected_turrets = None
                if self.deleting_turrets:
                    self.delete_button.image = delete_button_red_img
                else:
                    self.delete_button.image = delete_button_img
            elif event.key == pg.K_b:  # 'B' key for buying towers
                self.placing_turrets = True
                self.dragging_turret = True
                self.deleting_turrets = False
                self.selected_turrets = None
                self.delete_button.image = delete_button_img
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # left mouse button
            mouse_pos = event.pos # Get the mouse position

            # Check if the mouse position collides with the buttons
            if self.delete_button.rect.collidepoint(mouse_pos):
                self.deleting_turrets = not self.deleting_turrets
                self.placing_turrets = False
                self.dragging_turret = False
                self.selected_turrets = None
                if self.deleting_turrets:
                    self.delete_button.image = delete_button_red_img
                else:
                    self.delete_button.image = delete_button_img
            elif self.buy_button.rect.collidepoint(mouse_pos):
                self.dragging_turret = True
                self.placing_turrets = True
                self.deleting_turrets = False
                self.selected_turrets = None
                self.delete_button.image = delete_button_img # Reset the delete button image to the normal one
            # Cancel button to stop placing towers
            elif self.cancel_button.rect.collidepoint(mouse_pos):
                self.dragging_turret = False
                self.placing_turrets = False
                self.deleting_turrets = False
                self.selected_turrets = None
            elif self.exit_button.rect.collidepoint(mouse_pos):
                self.game_state = "menu" # Return to the menu state
                self.game_reset()
            elif self.pause_button.rect.collidepoint(mouse_pos):
                self.game_state = "paused" # Switch to the paused state

            # Turret placement
            # Mouse position is within the map area
            # If the mouse is within the map area and I am dragging a tower
            elif self.dragging_turret and mouse_pos[0] < map_rect.width and mouse_pos[1] < map_rect.height:
                if self.world.money >= c.BUY_COST: # Check if there is enough money to buy a turret
                    current_turret_count = len(self.turret_group) # Count the current number of turrets
                    self.create_turret(mouse_pos)
                    # If the turret was successfully created, deduct the cost
                    # If the number of turrets is less than the current count, it means a turret
                    if len(self.turret_group) > current_turret_count:
                        self.world.money -= c.BUY_COST
                    else:
                        print("Nem lehet ide tornyot építeni, vagy túl közel van egy másikhoz!")
                else:
                    print("Nincs elég pénzed")
                self.dragging_turret = False
                self.placing_turrets = False
                self.turret_preview_pos = None

            # If the mouse is within the map area and I am not dragging a turret
            elif mouse_pos[0] < map_rect.width and not self.dragging_turret:
                clicked_on_tower = False
                for tower in self.turret_group: #This checks if the mouse is on a turret
                    # If the mouse position collides with a turret's rectangle
                    if tower.rect.collidepoint(mouse_pos):
                        clicked_on_tower = True
                        if self.deleting_turrets:
                            tower.kill()
                            self.selected_turrets = None
                            self.deleting_turrets = False
                            self.delete_button.image = delete_button_img  # Törlés után visszaáll a gomb képe (globális kép)
                        else:
                            self.selected_turrets = tower
                        break
                if not clicked_on_tower:
                    self.selected_turrets = None

    def paused_events(self, event):
        """Handles events in the 'paused' state."""
        # If the game is paused, we can handle events like resuming the game or exiting

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.resume_button.rect.collidepoint(mouse_pos):
                self.game_state = "playing"
            if self.exit_button.rect.collidepoint(mouse_pos):
                self.running = False

    def draw_menu_screen(self):
        """The main menu screen is drawn here."""

        screen.blit(start_img, (0, 0)) # Draw the background image
        self.start_button.draw(screen)
        self.exit_button_menu.draw(screen)

    def draw_playing_screen(self):
        """The main game screen is drawn here."""

        self.enemy_group.update()
        self.turret_group.update()

        self.check_for_game_over()


        self.world.draw(screen)
        toolbar_rect = pg.Rect(map_rect.width, 0, c.Side_panel, map_rect.height)  # At the right edge, at 0 pixels height
        screen.blit(toolbar_image, toolbar_rect)

        # Spawning new enemies based on waves
        current_time = pg.time.get_ticks() # Get the current time in milliseconds
        if not self.wave_completed:
            if current_time - self.last_spawn_time > self.SPAWN_DELAY: # If enough time has passed since the last spawn
                # Spawn a new enemy if the wave limit has not been reached
                if self.spawn_enemy_in_wave():
                    self.last_spawn_time = current_time
                else:
                    if len(self.enemy_group) == 0: # If all enemies in the wave have been spawned
                        self.wave_completed = True # Set the wave as completed, so we can start a new one

        # If the wave is completed and there are no enemies left, start a new wave
        if self.wave_completed and len(self.enemy_group) == 0:
            self.start_new_wave()  # Start a new wave of enemies

        #Drawing the turret preview image if dragging a turret
        if self.dragging_turret:
            self.turret_preview_pos = pg.mouse.get_pos() # Get the current mouse position
            # If the turret preview position is within the map area
            if self.turret_preview_pos[0] < map_rect.width:
                preview_rect = turret_img.get_rect(center=self.turret_preview_pos) #The turret preview will be centered at the mouse position
                screen.blit(turret_img, preview_rect)

        #Buttons are drawn on the screen
        self.buy_button.draw(screen)
        if self.placing_turrets:  # If placing turrets, show the cancel button
            self.cancel_button.draw(screen)

        self.delete_button.draw(screen)
        self.pause_button.draw(screen)
        self.exit_button.draw(screen)

        # Drawing the enemy and turret groups
        self.enemy_group.draw(screen)
        self.draw_text(str(self.world.health), self.text_font, "black", 5, 40)
        self.draw_text(str(self.world.money), self.text_font, "black", 5, 80)
        screen.blit(table_img, (330, 35))
        self.draw_text("Level: " + str(self.world.level), self.large_font, "black", 455, 45)


        #Health and money icons are drawn
        screen.blit(heart_img, (10, 40 + 20))
        screen.blit(coin_img, (10, 80 + 20))

       #Calculate the distance between the centers of the towers and enemies to determine if a tower can fire at an enemy.
        # If the tower is selected, it will be highlighted with a range circle.
        for tower in self.turret_group:
            tower.update()
            tower.draw(screen, selected=(tower == self.selected_turrets)) #Draw the tower, highlighting it if it is selected
            for enemy in self.enemy_group:
                # Calculate the distance between the tower and the enemy
                distance = ((tower.rect.centerx - enemy.rect.centerx) ** 2 +
                            (tower.rect.centery - enemy.rect.centery) ** 2) ** 0.5
                if distance < tower.range:
                    tower.fire()
                    enemy.take_damage(5)
                    break

    def draw_paused_screen(self):
        """The paused screen is drawn here."""
        """Displays the paused screen with options to resume or exit."""

        screen.fill("#58a846")
        self.draw_text("PAUSED", self.large_font, "black", screen.get_width() / 2 - 80, screen.get_height() / 2 - 50) #The text is centered
        self.resume_button.draw(screen)
        self.exit_button.draw(screen)

    def draw_gameover_screen(self):
        """The game over screen is drawn here."""
        """Displays the game over screen with options to return to the menu or exit."""

        screen.fill("#58a846")
        screen_width, screen_height = pg.display.get_surface().get_size()
        self.draw_text("Press M for Menu, or Escape to Exit", self.large_font, "black", screen_width / 2, screen_height / 2,center=True)
        self.draw_text("Game over :/", self.large_font, "black", screen_width / 2,(screen_height / 2) - 50,center=True)

    def run(self):
        """The main game loop that runs the game."""
        """Handles the main game loop, including event processing, updating game state, and rendering."""
        self.running = True

        while self.running:  # Main game loop
            clock.tick(c.Framerates)  #How many frames per second are allowed
            screen.fill("grey100")

            # Event handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if self.game_state == "menu":
                    self.menu_events(event)
                elif self.game_state == "playing":
                    self.playing_events(event)
                elif self.game_state == "paused":
                    self.paused_events(event)
                elif self.game_state == "game_over":
                    self.game_over_events(event)

            # Update game state
            if self.game_state == "menu":
                self.draw_menu_screen()
            elif self.game_state == "playing":
                self.draw_playing_screen()
            elif self.game_state == "paused":
                self.draw_paused_screen()
            elif self.game_state == "game_over":
                self.draw_gameover_screen()

            if self.game_state == "exit":
                self.running = False

            pg.display.update()

        pg.quit()


if __name__ == "__main__":
    game = Game()
    game.run()

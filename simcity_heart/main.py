import arcade
import os
from pathlib import Path
import logic
import time

# window = arcade.Window(fullscreen= True, title="SimCity Heart")
window = arcade.Window(fullscreen=True, title='SimCity')
window.center_window()
assets_path = Path().absolute().resolve() / Path('assets')
arcade.resources.add_resource_handle('my-assets', assets_path)



class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # Загружаем карту
        tile_map = arcade.load_tilemap(':my-assets:maps/Starting_location.tmx', scaling=3)

        self.map_width = tile_map.width * tile_map.tile_width * tile_map.scaling
        self.map_height = tile_map.height * tile_map.tile_height * tile_map.scaling
        self.window_width = window.width
        self.window_height = window.height

        self.offset_x = self.window_width / 2 - self.map_width / 2
        self.offset_y = self.window_height / 2 - self.map_height / 2

        for layer in tile_map.sprite_lists.values():
            for sprite in layer:
                sprite.center_x += self.offset_x
                sprite.center_y += self.offset_y

        self.scene = arcade.Scene.from_tilemap(tile_map)

        #TIME
        self.last_update_time = time.time()

        #Picking a zone
        self.picked_zone = ''
        self.house = 'House'
        self.store = 'Store'
        self.factory = 'Factory'

        #Road, Grass, Water, Trees...
        self.road_cells = set()
        self.grass_cells = set()
        self.water_cells = set()
        self.tree_cells = set()


        def layer_position(layer_name, cells):
            tile_size = tile_map.tile_width * tile_map.scaling

            # Loop through the tiles in the "Road" and "Grass" layers
            for sprite in tile_map.sprite_lists.get(layer_name, []):
                grid_x = int((sprite.center_x - self.offset_x) // tile_size)
                grid_y = int((sprite.center_y - self.offset_y) // tile_size)
                cells.add((grid_x, grid_y))

        layer_position('Road', self.road_cells)
        layer_position('Grass', self.grass_cells)
        layer_position('Water', self.water_cells)
        layer_position('Tree', self.tree_cells)

    def on_draw(self) -> None:
        self.clear()
        self.scene.draw()
        arcade.draw_text(f"Money: {logic.city_money}", 20, 20, arcade.color.WHITE, 20)
        arcade.draw_text(f"Happiness: {int(logic.city_happiness)}", 20, 50, arcade.color.WHITE, 20)
        arcade.draw_text(f"Selected: {self.picked_zone if self.picked_zone else 'None'}",
                         20, 80, arcade.color.WHITE, 20)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            window.show_view(MainView())

        # Picking a zone through pressing on keyboard
        if symbol == arcade.key.H:
            self.picked_zone = self.house
        elif symbol == arcade.key.S:
            self.picked_zone = self.store
        elif symbol == arcade.key.F:
            self.picked_zone = self.factory



    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        tile_size = 16 * 3  # base tile size × scaling
        grid_x = int((x - self.offset_x) // tile_size)
        grid_y = int((y - self.offset_y) // tile_size)

        # Restriction for building on roads, water, etc

        if (grid_x, grid_y) in self.tree_cells:
            print("Cannot build on trees!")
            return


        # Check bounds before placing
        if not (0 <= grid_x < len(logic.grid[0]) and 0 <= grid_y < len(logic.grid)):
            return


        if self.picked_zone == self.house:
            zone_type = logic.House
            sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0027.png", scale=3)
        elif self.picked_zone == self.store:
            zone_type = logic.Store
            sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0046.png", scale=3)
        elif self.picked_zone == self.factory:
            zone_type = logic.Factory
            #sprite = arcade.Sprite(':my-assets:maps/Tiles/tile_0079.png', scale=3)
            sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0083.png", scale=3)
        # Try placing the building in logic
        if logic.try_placing_zone(grid_x, grid_y, zone_type):
            sprite.center_x = self.offset_x + grid_x * tile_size + tile_size / 2
            sprite.center_y = self.offset_y + grid_y * tile_size + tile_size / 2
            self.scene.add_sprite("Zone", sprite)

    def on_update(self, delta_time: float):
        # Money and Happiness update every second
        if time.time() - self.last_update_time > 1:
            logic.update_city()
            print('Money:', logic.city_money, 'Happiness:', round(logic.city_happiness, 2))
            self.last_update_time = time.time()


class MainView(arcade.View):
    def __init__(self):
        super().__init__()
        #adding bc
        img1 = 'assets/images/Loading.png'
        self.bc = arcade.Sprite(img1)


        #getting variables
        self.img_list = arcade.SpriteList()
        self.window_width, self.window_height = window.get_size()
        self.window_middle_x, self.window_middle_y = window.width /2, window.height /2


        #path
        self.menu_bar = arcade.Sprite('assets/images/menu_bars.png', scale=0.5)
        self.menu_bar.position = (self.window_middle_x, self.window_middle_y)


        #music loop
        self.music = arcade.Sound('assets/music/Menu_music.mp3')
        self.music.play(volume = 0.5, loop = True)

        #variables
        self.bc.width = self.window_width
        self.bc.height = self.window_height
        self.bc.center_x = self.window_middle_x
        self.bc.center_y = self.window_middle_y
        self.img_list.append(self.bc)
        self.img_list.append(self.menu_bar)
        self.menu_bar_left = self.window_middle_x - 155
        self.menu_bar_right = self.window_middle_x + 135
        self.button_width = 300
        self.button_height = 74

        #global volume
        global volume
        volume = 50


        #button position
        self.buttons = {
            'New Game': {"x" : self.window_middle_x-155, "y" : self.window_middle_y+100, "w": self.button_width, "h": self.button_height},
            'Load Game' : {'x': self.window_middle_x-155, "y": self.window_middle_y+5, "w": self.button_width, "h": self.button_height},
            'Settings': {'x': self.window_middle_x-155, 'y': self.window_middle_y-85, 'w': self.button_width, 'h': self.button_height},
            'Exit' : {'x': self.window_middle_x-155, 'y': self.window_middle_y-175, 'w': self.button_width, 'h': self.button_height}
        }


        #For exit button and settings
        self.show_confirm = False
        self.show_settings = False
        self.dragging = False
        self.left_handle_X = self.window_middle_x - 200
        self.label = arcade.Text("Are you sure?", self.window_middle_x, self.window_middle_y + 100, arcade.color.BLACK,
                                 20, anchor_x="center")
        self.yes = arcade.Text("[YES]", self.window_middle_x - 100, self.window_middle_y, arcade.color.RED, 20,
                               anchor_x="center", anchor_y="center")
        self.no = arcade.Text("[NO]", self.window_middle_x + 100, self.window_middle_y, arcade.color.DARK_GREEN, 20,
                              anchor_x="center", anchor_y="center")
        self.settings = arcade.Text("SETTINGS",self.window_middle_x, self.window_middle_y+250, arcade.color.WHITE,35, anchor_x="center")
        self.volume =arcade.Text(f"Volume: {volume}%", self.window_middle_x, self.window_middle_y+185,
                         arcade.color.WHITE, 20, anchor_x="center")
        self.back = arcade.Text('BACK', self.window_middle_x-150, self.window_middle_y-150,
                         arcade.color.WHITE, 20, anchor_x="center")


    def on_draw(self) -> None:
        self.clear()
        self.img_list.draw()


        #exit window creation
        if self.show_confirm:
            arcade.draw_lbwh_rectangle_filled(0, 0,self.window_width,self.window_height,(0, 0, 0, 200))
            arcade.draw_lbwh_rectangle_filled(self.window_middle_x-150, self.window_middle_y-50, 300, 200, arcade.color.DARK_GRAY)
            arcade.draw_lbwh_rectangle_outline(self.window_middle_x-150, self.window_middle_y-50, 300, 200, arcade.color.WHITE, 3)
            self.label.draw()
            self.yes.draw()
            self.no.draw()

        #setting window
        if self.show_settings:
            self.handle_X = self.left_handle_X + 350 * (volume / 100)
            arcade.draw_lbwh_rectangle_filled(0, 0, self.window_width, self.window_height, (0, 0, 0, 200))
            arcade.draw_lbwh_rectangle_filled(self.window_middle_x - 300, self.window_middle_y - 250, 600, 600,
                                              arcade.color.DARK_GRAY)
            arcade.draw_lbwh_rectangle_outline(self.window_middle_x - 300, self.window_middle_y - 250, 600, 600,
                                               arcade.color.WHITE, 3)
            arcade.draw_lbwh_rectangle_filled(self.window_middle_x - 200, self.window_middle_y + 125, 350, 5,
                                              arcade.color.LIGHT_GRAY)
            arcade.draw_circle_filled(self.handle_X, self.window_middle_y + 127, 10, arcade.color.GOLD)
            self.settings.draw()
            self.volume.draw()
            self.back.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        #defining what button is pressed
        if not self.show_confirm and not self.show_settings:
            for name, b in self.buttons.items():
                if x >=b['x'] and x <= b['x'] + b['w'] and y >= b['y'] and y<= b['y'] + b['h']:
                    if name == "New Game":
                        print("New Game")
                    elif name == "Load Game":
                        game = GameView()
                        self.window.show_view(game)
                    elif name == "Settings":
                        self.show_settings = True
                    elif name == "Exit":
                        self.show_confirm = True
                    break


        if self.show_confirm:
            if self.window_middle_x-138 <= x <= self.window_middle_x-35 and self.window_middle_y-25 <= y <= self.window_middle_y+24:
                    arcade.exit()
            elif self.window_middle_x+74 <= x <= self.window_middle_x+128 and self.window_middle_y-25 <= y <= self.window_middle_y+24:
                self.show_confirm = False
                self.clear()

        elif self.show_settings:
            # if abs(x - self.window_middle_x - 210) <= 10 * 2 and abs(y - self.window_middle_x - 210) <= 20:
            #     self.dragging = True
            if  self.window_middle_x-186 <= x <= self.window_middle_x-114 and self.window_middle_y-152 <= y <= self.window_middle_y-131:
                self.show_settings = False
                self.clear()


    # def on_mouse_release(self, x, y, button, modifiers):
    #     self.dragging = False
    #
    #
    # def on_mouse_motion(self, x, y, dx, dy):
    #     if self.dragging:
    #         left  = self.window_middle_x - 210 -450/2
    #         right = self.window_middle_x + 210 -450/2
    #         self.handle_X = max(min(x, right), left)
    #         self.volume = (self.handle_X - left) / (450)
    #         pass






class Loading_screen(arcade.View):
    def __init__(self):
        #intialization picture
        super().__init__()
        img1 = 'assets/images/Loading.png'
        self.bc = arcade.Sprite(
        img1,scale=1
        )
        screen_width, screen_height = window.get_size()


        #positioning
        self.bc.width = screen_width
        self.bc.height = screen_height
        self.bc.center_x = screen_width / 2
        self.bc.center_y = screen_height / 2
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.bc)


        #parameters for progress-bar
        self.progress = 0
        self.loading_speed = 20
        self.bar_width = 400
        self.bar_height = 25
        self.bar_y = screen_height / 2 -50


        #bc and progress bar
        self.image_folder = "assets/images"
        self.files = os.listdir(self.image_folder)
        self.total_files = len(self.files)
        self.loaded_files = 0
        self.progress = 0
        self.textures = []


    #drawing sprite(image) and bar
    def on_draw(self) -> None:
        # creating picture
        self.clear()
        self.sprite_list.draw()


        # creating loading bar
        bar_x = window.width / 2 - 100


        # bar outline
        arcade.draw_lbwh_rectangle_outline(
            bar_x, self.bar_y,
            self.bar_width, self.bar_height,
            arcade.color.WHITE
        )


        # width
        fill_width = (self.progress / 100) * (self.bar_width -0)


        # calculating bar edges
        left_edge_x = bar_x - fill_width /2
        fill_center_x = left_edge_x + fill_width / 2


        # filling code
        if fill_width > 0:
            arcade.draw_lbwh_rectangle_filled(
                fill_center_x,
                self.bar_y,
                fill_width,
                self.bar_height,
                arcade.color.WHITE
            )


        # loading txt
        percent_text = f"Loading... {int(self.progress)}%"
        arcade.draw_text(
            percent_text,
            bar_x+100, self.bar_y+33 ,
            arcade.color.WHITE, 28
        )


    def on_update(self, delta_time: float):
        if self.progress < 100:
            self.progress += self.loading_speed * delta_time
        else:
            self.progress = 100
            main = MainView()
            window.show_view(main)
    # def on_update(self, delta_time):
    #     #
    #     if self.loaded_files < self.total_files:
    #         file_name = self.files[self.loaded_files]
    #         file_path = os.path.join(self.image_folder, file_name)
    #         texture = arcade.load_texture(file_path)
    #         self.textures.append(texture)
    #         self.loaded_files += 1
    #         # calculating procent
    #         self.progress = (self.loaded_files / self.total_files) * 100
    #     else:
    #         main = MainView()
    #         window.show_view(main)
    #         print("All files are ready")

game = Loading_screen()
window.show_view(game)
arcade.run()
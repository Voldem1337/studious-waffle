import arcade
from pathlib import Path
import logic
import time

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
            window.close()

        # Picking a zone through pressing on keyboard
        if symbol == arcade.key.H:
            self.picked_zone = self.house
        elif symbol == arcade.key.S:
            self.picked_zone = self.store
        elif symbol == arcade.key.F:
            self.picked_zone = self.factory

    def on_update(self, delta_time: float):
        # Money and Happiness update every 15 seconds
        if time.time() - self.last_update_time > 1:
            logic.update_city()
            print('Money:', logic.city_money, 'Happiness:', logic.city_happiness)
            self.last_update_time = time.time()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        tile_size = 16 * 3  # base tile size × scaling
        grid_x = int((x - self.offset_x) // tile_size)
        grid_y = int((y - self.offset_y) // tile_size)

        # Restriction for building on roads, water, etc
        if (grid_x, grid_y) in self.road_cells:
            print("Cannot build on roads!")
            return
        if (grid_x, grid_y) in self.water_cells:
            print("Cannot build on water!")
            return
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




game = GameView()
window.show_view(game)
arcade.run()

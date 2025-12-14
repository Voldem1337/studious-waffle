import arcade
from pathlib import Path

import logic
import time

#novoje
import save_load

# window = arcade.Window(fullscreen=True, title='SimCity')
assets_path = Path().absolute().resolve() / Path('assets')
arcade.resources.add_resource_handle('my-assets', assets_path)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # Loading the map
        self.tile_map = arcade.load_tilemap(':my-assets:maps/Starting_location.tmx', scaling=2)

        self.map_width = self.tile_map.width * self.tile_map.tile_width * self.tile_map.scaling
        self.map_height = self.tile_map.height * self.tile_map.tile_height * self.tile_map.scaling
        self.window_width = self.window.width
        self.window_height = self.window.height

        self.offset_x = self.window_width / 2 - self.map_width / 2
        self.offset_y = self.window_height / 2 - self.map_height / 2


        for layer in self.tile_map.sprite_lists.values():
            for sprite in layer:
                sprite.center_x += self.offset_x
                sprite.center_y += self.offset_y

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        #TIME
        self.last_update_time = time.time()

        #Picking a placeable
        self.picked_placeable = ''
        self.house = 'House'
        self.store = 'Store'
        self.factory = 'Factory'
        self.road = 'Road'
        vertical_road = 'Road (vertical)'
        horizontal_road = 'Road (horizontal)'
        self.road_types = [vertical_road, horizontal_road]


        #Settings button
        # Список спрайтов для удобства
        self.ui_sprites = arcade.SpriteList()
        #warning sign
        self.warning_list = arcade.SpriteList()
        self.warning_sprite = arcade.Sprite("assets/images/warning_bulding.png", scale=0.25)
        self.warning_sprite.center_x = self.window.width / 2
        self.warning_sprite.center_y = self.window.height / 2
        self.warning_list.append(self.warning_sprite)


        self.show_warning = False

        # Загружаем шестерёнку
        self.window_middle_x, self.window_middle_y = self.window.width / 2, self.window.height / 2
        self.settings_gear = arcade.Sprite(
            "assets/images/setting_bt.png",
            scale=0.05
        )
        margin = 20
        self.settings_gear.center_x = self.window.width - self.settings_gear.width / 2 - margin
        self.settings_gear.center_y = self.window.height - self.settings_gear.height / 2 - margin

        self.ui_sprites.append(self.settings_gear)
        self.show_settings = False
        self.label = arcade.Text("Are you sure?", self.window_middle_x, self.window_middle_y + 100, arcade.color.BLACK,
                                 20, anchor_x="center")
        self.yes = arcade.Text("[YES]", self.window_middle_x - 100, self.window_middle_y, arcade.color.RED, 20,
                               anchor_x="center", anchor_y="center")
        self.no = arcade.Text("[NO]", self.window_middle_x + 100, self.window_middle_y, arcade.color.DARK_GREEN, 20,
                              anchor_x="center", anchor_y="center")
        self.settings = arcade.Text("SETTINGS",self.window_middle_x, self.window_middle_y+250, arcade.color.WHITE,35, anchor_x="center")


        self.building_sprites = {}
        self.construction_texture = arcade.load_texture("assets/maps/Tiles/tile_0012.png")

        self.final_textures = {
            logic.House: arcade.load_texture("assets/maps/Tiles/tile_0027.png"),
            logic.Store: arcade.load_texture("assets/maps/Tiles/tile_0046.png"),
            logic.Factory: arcade.load_texture("assets/maps/Tiles/tile_0083.png"),
        }

    def on_draw(self) -> None:
        self.clear()
        self.scene.draw()
        arcade.draw_text(f"Money: {logic.city_money}", 20, 20, arcade.color.WHITE, 20)
        arcade.draw_text(f"Happiness: {int(logic.city_happiness)}", 20, 50, arcade.color.WHITE, 20)
        arcade.draw_text(f"Selected: {self.picked_placeable if self.picked_placeable else 'None'}",
                         20, 80, arcade.color.WHITE, 20)
        arcade.draw_text(f"Population: {logic.city_population}", 20, 110, arcade.color.WHITE, 20)
        arcade.draw_text(f"City Profit: {logic.city_profit}", 20, 140, arcade.color.WHITE, 20)

        #Demand
        arcade.draw_text(f"Demand:", self.window_width - 200, 80, arcade.color.WHITE, 20)
        arcade.draw_text(f"{round(logic.residential_demand, 2)}", self.window_width - 80, 20, arcade.color.GREEN, 20)
        arcade.draw_text(f"{round(logic.commercial_demand, 2)}", self.window_width - 80, 50, arcade.color.BLUE, 20)
        arcade.draw_text(f"{round(logic.industrial_demand, 2)}", self.window_width - 80, 80, arcade.color.YELLOW, 20)


        self.ui_sprites.draw()
        if self.show_settings:
            arcade.draw_lbwh_rectangle_filled(0, 0,self.window_width,self.window_height,(0, 0, 0, 200))
            arcade.draw_lbwh_rectangle_filled(self.window_middle_x-150, self.window_middle_y-50, 300, 200, arcade.color.DARK_GRAY)
            arcade.draw_lbwh_rectangle_outline(self.window_middle_x-150, self.window_middle_y-50, 300, 200, arcade.color.WHITE, 3)
            self.label.draw()
            self.yes.draw()
            self.no.draw()
        if self.show_warning:
            self.warning_list.draw()





    def on_key_press(self, symbol: int, modifiers: int) -> None:
        road_picked = False

        if symbol == arcade.key.ESCAPE:
            self.window.close()


        # Picking a zone through pressing on keyboard
        if symbol == arcade.key.H:
            self.picked_placeable = self.house
        elif symbol == arcade.key.S:
            self.picked_placeable = self.store
        elif symbol == arcade.key.F:
            self.picked_placeable = self.factory
        elif symbol == arcade.key.R:
            self.picked_placeable = self.road_types[0]


    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:

        if self.picked_placeable == self.road_types[0]:
            if button == arcade.MOUSE_BUTTON_RIGHT:
                self.picked_placeable = self.road_types[1]
        else:
            if button == arcade.MOUSE_BUTTON_RIGHT:
                self.picked_placeable = self.road_types[0]



        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if self.show_settings:

            if self.window_middle_x-138 <= x <= self.window_middle_x-35 and self.window_middle_y-25 <= y <= self.window_middle_y+24:
                    save_load.save_game()
                    arcade.exit()
            elif self.window_middle_x+74 <= x <= self.window_middle_x+128 and self.window_middle_y-25 <= y <= self.window_middle_y+24:
                self.show_settings = False
                self.clear()
        else:
            if self.settings_gear.collides_with_point((x, y)):
                self.show_settings = True



            # Placing a zone

            tile_size = 16 * 2  # base tile size × scaling
            grid_x = int((x - self.offset_x) / tile_size)
            grid_y = int((y - self.offset_y) / tile_size)


            # Check bounds before placing
            if not (0 <= grid_x < len(logic.grid[0]) and 0 <= grid_y < len(logic.grid) + 1):
                return


            if self.picked_placeable == self.house:
                placeable = logic.Residential
                sprite = arcade.Sprite(":my-assets:images/green_zone.png", scale=0.055)
            elif self.picked_placeable == self.store:
                placeable = logic.Commercial
                sprite = arcade.Sprite(":my-assets:images/blue_zone.png", scale=0.055)
            elif self.picked_placeable == self.factory:
                placeable = logic.Industrial
                #sprite = arcade.Sprite(':my-assets:maps/Tiles/tile_0079.png', scale=3)
                sprite = arcade.Sprite(":my-assets:images/yellow_zone.jpg", scale=0.055)
            elif self.picked_placeable == self.road_types[0]:
                placeable = logic.VerticalRoad
                sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0144.png", scale=2)
            elif self.picked_placeable == self.road_types[1]:
                placeable = logic.HorizontalRoad
                sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0110.png", scale=2)

            # Try placing the placeable in logic
            if logic.try_placing_placeable(grid_x, grid_y, placeable) == 'placed':
                sprite.center_x = self.offset_x + grid_x * tile_size + tile_size / 2
                sprite.center_y = self.offset_y + grid_y * tile_size + tile_size / 2
                self.scene.add_sprite('Object', sprite)
            elif logic.try_placing_placeable(grid_x, grid_y, placeable) == 'occupied':
                self.show_warning = True
                self.warning_timer = time.time()
            elif logic.try_placing_placeable(grid_x, grid_y, placeable) == 'no_money':
                print('not enough money')


    #Novaje
    def rebuild_scene_from_logic(self):
        tile_size = 16*2
        tile_map = arcade.load_tilemap(':my-assets:maps/Starting_location.tmx', scaling=2)

        self.map_width = tile_map.width * tile_map.tile_width * tile_map.scaling
        self.map_height = tile_map.height * tile_map.tile_height * tile_map.scaling
        self.window_width = self.window.width
        self.window_height = self.window.height

        self.offset_x = self.window_width / 2 - self.map_width / 2
        self.offset_y = self.window_height / 2 - self.map_height / 2

        for layer in tile_map.sprite_lists.values():
            for sprite in layer:
                sprite.center_x += self.offset_x
                sprite.center_y += self.offset_y

        self.scene = arcade.Scene.from_tilemap(tile_map)
        for y, row in enumerate(logic.grid):
            for x, cell in enumerate(row):
                if cell is None:
                    continue
                if isinstance(cell, logic.House):
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0027.png", scale=2)
                elif isinstance(cell,logic.Store):
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0046.png", scale=2)
                elif isinstance(cell,logic.Factory) :
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0083.png", scale=2)
                elif isinstance(cell,logic.VerticalRoad):
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0144.png", scale=2)
                elif isinstance(cell,logic.HorizontalRoad):
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0110.png", scale=2)
                else: continue
                sprite.center_x = self.offset_x + x * tile_size + tile_size / 2
                sprite.center_y = self.offset_y + y * tile_size + tile_size / 2
                self.scene.add_sprite("Zone", sprite)


    def on_update(self, delta_time: float):

        if time.time() - self.last_update_time > 1:
            logic.update_city()
            self.last_update_time = time.time()

        # Money and Happiness update every second
        finished = logic.update_construction(delta_time)

        for building, x, y in finished:
            sprite = self.building_sprites[(x, y)]
            sprite.texture = self.final_textures[type(building)]

        for building, x, y in logic.buildings:
            if not building.built and (x, y) not in self.building_sprites:
                tile_size = 16 * 2

                sprite = arcade.Sprite(self.construction_texture, scale=2)
                sprite.center_x = self.offset_x + x * tile_size + tile_size / 2
                sprite.center_y = self.offset_y + y * tile_size + tile_size / 2

                self.scene.add_sprite("Object", sprite)
                self.building_sprites[(x, y)] = sprite


        if self.show_warning and time.time() - self.warning_timer > 2:
            self.show_warning = False



def main():
    # window = arcade.Window(fullscreen=True, title="SimCity")
    window = arcade.Window(width=1024, height=768, title="SimCity")

    window.center_window()
    game = GameView()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()

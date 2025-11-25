import arcade
from pathlib import Path
import logic
import time

# window = arcade.Window(fullscreen=True, title='SimCity')
assets_path = Path().absolute().resolve() / Path('assets')
arcade.resources.add_resource_handle('my-assets', assets_path)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # Loading the map
        tile_map = arcade.load_tilemap(':my-assets:maps/Starting_location.tmx', scaling=3)

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

        #TIME
        self.last_update_time = time.time()

        #Picking a zone
        self.picked_zone = ''
        self.house = 'House'
        self.store = 'Store'
        self.factory = 'Factory'

        #warning sign
        self.warning_list = arcade.SpriteList()
        self.warning_sprite = arcade.Sprite("assets/images/warning_bulding.png", scale=0.25)
        self.warning_sprite.center_x = self.window.width / 2
        self.warning_sprite.center_y = self.window.height / 2
        self.warning_list.append(self.warning_sprite)

        self.show_warning = False

        #Settings button

        self.ui_sprites = arcade.SpriteList()
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


    def on_draw(self) -> None:
        self.clear()
        self.scene.draw()
        arcade.draw_text(f"Money: {logic.city_money}", 20, 20, arcade.color.WHITE, 20)
        arcade.draw_text(f"Happiness: {int(logic.city_happiness)}", 20, 50, arcade.color.WHITE, 20)
        arcade.draw_text(f"Selected: {self.picked_zone if self.picked_zone else 'None'}",
                         20, 80, arcade.color.WHITE, 20)
        arcade.draw_text(f"Population: {logic.city_population}", 20, 110, arcade.color.WHITE, 20)

        # Demand
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
        if symbol == arcade.key.ESCAPE:
            self.window.close()

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
        if self.show_warning and time.time() - self.warning_timer > 2:
            self.show_warning = False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if self.show_settings:
            if self.window_middle_x-138 <= x <= self.window_middle_x-35 and self.window_middle_y-25 <= y <= self.window_middle_y+24:
                    arcade.exit()
            elif self.window_middle_x+74 <= x <= self.window_middle_x+128 and self.window_middle_y-25 <= y <= self.window_middle_y+24:
                self.show_settings = False
                self.clear()
        else:
            if self.settings_gear.collides_with_point((x, y)):
                self.show_settings = True

            tile_size = 16 * 3  # base tile size × scaling
            grid_x = int((x - self.offset_x) // tile_size)
            grid_y = int((y - self.offset_y) // tile_size)


            # Check bounds before placing
            if not (0 <= grid_x < len(logic.grid[0]) and 0 <= grid_y < len(logic.grid)):
                return


            if self.picked_zone == self.house:
                zone_type = logic.Residential
                sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0027.png", scale=3)
            elif self.picked_zone == self.store:
                zone_type = logic.Commercial
                sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0046.png", scale=3)
            elif self.picked_zone == self.factory:
                zone_type = logic.Industrial
                sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0083.png", scale=3)
            # Try placing the building in logic
            if logic.try_placing_zone(grid_x, grid_y, zone_type):
                sprite.center_x = self.offset_x + grid_x * tile_size + tile_size / 2
                sprite.center_y = self.offset_y + grid_y * tile_size + tile_size / 2
                self.scene.add_sprite("Zone", sprite)
            else:
                self.show_warning = True
                self.warning_timer = time.time()


def main():
    window = arcade.Window(1020, 720, "SimCity")
    window.center_window()
    game = GameView()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()

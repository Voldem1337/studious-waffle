import arcade
from pathlib import Path
import logic
import time
import save_load
import config

assets_path = Path().absolute().resolve() / Path('assets')
arcade.resources.add_resource_handle('my-assets', assets_path)


class GameView(arcade.View):
    def __init__(self):
        if config.music_player:
            config.music_player.pause()

        super().__init__()

        # GAME MUSIC
        config.load_config()
        self.birds = arcade.Sound("assets/sounds/Bird sounds- 5 minutes.mp3")
        self.game_music_player = self.birds.play(
            volume=config.effect_volume / 100,
            loop=True
        )

        # SOUND EFFECTS
        self.build_sound = arcade.Sound("assets/sounds/impact-wood-impact-on-wood-heavy-03.wav")
        self.remove_sound = arcade.Sound("assets/sounds/destruction-explosion-close-small-06.wav")

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

        # TIME
        self.last_update_time = time.time()

        # Picking a placeable
        self.picked_placeable = ''
        self.house = 'House'
        self.store = 'Store'
        self.factory = 'Factory'
        self.road = 'Road'
        vertical_road = 'Road (vertical)'
        horizontal_road = 'Road (horizontal)'
        self.townhall = 'TownHall'
        self.road_types = [vertical_road, horizontal_road]

        # UI elements
        self.ui_sprites = arcade.SpriteList()
        self.warning_list = arcade.SpriteList()
        self.warning_sprite = arcade.Sprite("assets/images/warning_bulding.png", scale=0.25)
        self.warning_sprite.center_x = self.window.width / 2
        self.warning_sprite.center_y = self.window.height / 2
        self.warning_list.append(self.warning_sprite)
        self.show_warning = False

        # Settings gear button
        self.window_middle_x, self.window_middle_y = self.window.width / 2, self.window.height / 2
        self.settings_gear = arcade.Sprite("assets/images/setting_bt.png", scale=0.05)
        margin = 20
        self.settings_gear.center_x = self.window.width - self.settings_gear.width / 2 - margin
        self.settings_gear.center_y = self.window.height - self.settings_gear.height / 2 - margin
        self.ui_sprites.append(self.settings_gear)

        # Settings window
        self.show_settings = False
        self.dragging = False
        config.load_config()

        # Volume slider
        self.left_handle_X = self.window_middle_x - 200
        self.handle_X = self.left_handle_X + 350 * (config.effect_volume / 100)

        # Settings UI texts

        self.settings_title = arcade.Text("SETTINGS", self.window_middle_x, self.window_middle_y + 250,
                                          arcade.color.WHITE, 35, anchor_x="center")
        self.volume_text = arcade.Text(f"Effect volume: {config.effect_volume}%", self.window_middle_x,
                                       self.window_middle_y + 185, arcade.color.WHITE, 20, anchor_x="center")
        self.back_text = arcade.Text('BACK', self.window_middle_x - 150, self.window_middle_y - 150,
                                     arcade.color.WHITE, 20, anchor_x="center")
        self.save_exit_text = arcade.Text('SAVE & EXIT', self.window_middle_x + 150, self.window_middle_y - 150,
                                          arcade.color.RED, 20, anchor_x="center")

        # Resolution dropdown
        self.resolutions = [
            ("Fullscreen", None),
            ("1920x1080", (1920, 1080)),
            ("1600x900", (1600, 900)),
            ("1280x720", (1280, 720))
        ]
        self.current_resolution_index = config.current_resolution_index
        self.dropdown_open = False
        self.dropdown_x = self.window_middle_x
        self.dropdown_y = self.window_middle_y + 50
        self.dropdown_width = 200
        self.dropdown_height = 40
        self.resolution_label = arcade.Text("Resolution:", self.dropdown_x - 200, self.dropdown_y + 10,
                                            arcade.color.WHITE, 20)

        # Building sprites
        self.building_sprites = {}
        self.construction_texture = arcade.load_texture("assets/maps/Tiles/tile_0012.png")
        self.final_textures = {
            logic.House: arcade.load_texture("assets/maps/Tiles/tile_0027.png"),
            logic.Store: arcade.load_texture("assets/maps/Tiles/tile_0046.png"),
            logic.Factory: arcade.load_texture("assets/maps/Tiles/tile_0083.png"),
            logic.TownHall: arcade.load_texture("assets/maps/Tiles/tile_0014.png"),
        }

    def on_draw(self) -> None:
        self.clear()
        self.scene.draw()

        # Game UI
        arcade.draw_text(f"Date: {logic.get_date_string()}", 10, self.window_height - 30, arcade.color.WHITE, 18)
        arcade.draw_text(f"Money: {logic.city_money}$", 20, 20, arcade.color.WHITE, 20)
        arcade.draw_text(f"Happiness: {int(logic.city_happiness)}%", 20, 50, arcade.color.WHITE, 20)
        arcade.draw_text(f"Selected: {self.picked_placeable if self.picked_placeable else 'None'}",
                         20, 80, arcade.color.WHITE, 20)
        arcade.draw_text(f"Population: {logic.city_population}", 20, 110, arcade.color.WHITE, 20)
        arcade.draw_text(f"City Profit: {logic.city_profit}$/h", 20, 140, arcade.color.WHITE, 20)

        # Demand
        arcade.draw_text(f"Demand:", self.window_width - 200, 80, arcade.color.WHITE, 20)
        arcade.draw_text(f"{round(logic.residential_demand, 2)}", self.window_width - 80, 20, arcade.color.ARMY_GREEN, 20)
        arcade.draw_text(f"{round(logic.commercial_demand, 2)}", self.window_width - 80, 50, arcade.color.BLUE, 20)
        arcade.draw_text(f"{round(logic.industrial_demand, 2)}", self.window_width - 80, 80, arcade.color.YELLOW, 20)

        self.ui_sprites.draw()

        # Settings window
        if self.show_settings:
            # Dark overlay
            arcade.draw_lbwh_rectangle_filled(0, 0, self.window_width, self.window_height, (0, 0, 0, 200))

            # Settings panel
            arcade.draw_lbwh_rectangle_filled(self.window_middle_x - 300, self.window_middle_y - 250,
                                              600, 600, arcade.color.DARK_GRAY)
            arcade.draw_lbwh_rectangle_outline(self.window_middle_x - 300, self.window_middle_y - 250,
                                               600, 600, arcade.color.WHITE, 3)

            # Volume slider bar
            arcade.draw_lbwh_rectangle_filled(self.window_middle_x - 200, self.window_middle_y + 125,
                                              350, 5, arcade.color.LIGHT_GRAY)
            # Volume slider handle
            arcade.draw_circle_filled(self.handle_X, self.window_middle_y + 127, 10, arcade.color.GOLD)

            # Draw texts
            self.settings_title.draw()
            self.volume_text.draw()
            self.back_text.draw()
            self.save_exit_text.draw()
            self.resolution_label.draw()

            # Resolution dropdown
            current_res_name = self.resolutions[self.current_resolution_index][0]

            # Dropdown button
            arcade.draw_lbwh_rectangle_filled(self.dropdown_x + 25, self.dropdown_y,
                                              self.dropdown_width, self.dropdown_height, arcade.color.DARK_GRAY)
            arcade.draw_lbwh_rectangle_outline(self.dropdown_x + 25, self.dropdown_y,
                                               self.dropdown_width, self.dropdown_height, arcade.color.WHITE, 2)
            arcade.draw_text(current_res_name, self.dropdown_x + 35, self.dropdown_y + 12,
                             arcade.color.WHITE, 16)

            # Arrow
            arrow = "▼" if not self.dropdown_open else "▲"
            arcade.draw_text(arrow, self.dropdown_x + self.dropdown_width - 15, self.dropdown_y + 10,
                             arcade.color.WHITE, 18)

            # Dropdown options
            if self.dropdown_open:
                for i, (res_name, res_value) in enumerate(self.resolutions):
                    option_y = self.dropdown_y - (i + 1) * self.dropdown_height
                    bg_color = arcade.color.GRAY if i == self.current_resolution_index else arcade.color.DARK_GRAY

                    arcade.draw_lbwh_rectangle_filled(self.dropdown_x + 25, option_y,
                                                      self.dropdown_width, self.dropdown_height, bg_color)
                    arcade.draw_lbwh_rectangle_outline(self.dropdown_x + 25, option_y,
                                                       self.dropdown_width, self.dropdown_height, arcade.color.WHITE, 2)
                    arcade.draw_text(res_name, self.dropdown_x + 35, option_y + 12, arcade.color.WHITE, 16)

        # Warning
        if self.show_warning:
            self.warning_list.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.show_settings = not self.show_settings

        # Picking zones
        if not self.show_settings:
            if symbol == arcade.key.H:
                self.picked_placeable = self.house
            elif symbol == arcade.key.S:
                self.picked_placeable = self.store
            elif symbol == arcade.key.F:
                self.picked_placeable = self.factory
            elif symbol == arcade.key.T:
                self.picked_placeable = self.townhall
            elif symbol == arcade.key.R:
                self.picked_placeable = self.road_types[0]

            # Road rotation
            if self.picked_placeable in self.road_types:
                if symbol in [arcade.key.UP, arcade.key.DOWN]:
                    current_index = self.road_types.index(self.picked_placeable)
                    self.picked_placeable = self.road_types[1 - current_index]

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT and button != arcade.MOUSE_BUTTON_RIGHT:
            return

        # Settings gear click
        if button == arcade.MOUSE_BUTTON_LEFT and self.settings_gear.collides_with_point((x, y)):
            self.show_settings = not self.show_settings
            return

        # Settings window interactions
        if self.show_settings and button == arcade.MOUSE_BUTTON_LEFT:
            # Volume slider
            if abs(x - self.handle_X) <= 15 and abs(y - (self.window_middle_y + 127)) <= 15:
                self.dragging = True
                return

            # Click on slider bar to jump
            if (self.window_middle_x - 200 <= x <= self.window_middle_x + 150 and
                    self.window_middle_y + 115 <= y <= self.window_middle_y + 140):
                self.handle_X = x
                config.load_config()
                config.set_effect_volume(int(((self.handle_X - self.left_handle_X) / 350) * 100))
                self.volume_text.text = f"Effect volume: {config.effect_volume}%"
                self.game_music_player.volume = config.effect_volume / 100
                config.save_config()

                return

            # BACK button
            if (self.window_middle_x - 186 <= x <= self.window_middle_x - 114 and
                    self.window_middle_y - 165 <= y <= self.window_middle_y - 135):
                self.show_settings = False
                return

            # SAVE & EXIT button
            if (self.window_middle_x + 74 <= x <= self.window_middle_x + 226 and
                    self.window_middle_y - 165 <= y <= self.window_middle_y - 135):
                config.load_config()
                self.game_music_player.pause()
                save_load.save_game(config.current_world_name)
                from main import MainView
                menu = MainView()
                self.window.show_view(menu)
                return

            # Dropdown toggle
            if (self.dropdown_x + 25 <= x <= self.dropdown_x + 25 + self.dropdown_width and
                    self.dropdown_y <= y <= self.dropdown_y + self.dropdown_height):
                self.dropdown_open = not self.dropdown_open
                return

            # Dropdown options
            if self.dropdown_open:
                for i, (res_name, res_value) in enumerate(self.resolutions):
                    option_y = self.dropdown_y - (i + 1) * self.dropdown_height

                    if (self.dropdown_x + 25 <= x <= self.dropdown_x + 25 + self.dropdown_width and
                            option_y <= y <= option_y + self.dropdown_height):

                        self.current_resolution_index = i
                        config.current_resolution_index = i
                        self.dropdown_open = False

                        if res_value is None:
                            self.window.set_fullscreen(True)
                        else:
                            self.window.set_fullscreen(False)
                            self.window.set_size(res_value[0], res_value[1])
                            self.window.center_window()

                        self._update_ui_positions()
                        return

            # If clicked inside settings but not on any control, don't place buildings
            if (self.window_middle_x - 300 <= x <= self.window_middle_x + 300 and
                    self.window_middle_y - 250 <= y <= self.window_middle_y + 350):
                return

        # Building placement
        if not self.show_settings:
            tile_size = 16 * 2
            grid_x = int((x - self.offset_x) / tile_size)
            grid_y = int((y - self.offset_y) / tile_size)

            # Check bounds
            if not (0 <= grid_x < len(logic.grid[0]) and 0 <= grid_y < len(logic.grid)):
                return

            # Left click - place
            if button == arcade.MOUSE_BUTTON_LEFT:
                sprite = None
                placeable = None

                if self.picked_placeable == self.house:
                    placeable = logic.Residential
                    sprite = arcade.Sprite(":my-assets:images/green_zone.png", scale=0.055)
                elif self.picked_placeable == self.store:
                    placeable = logic.Commercial
                    sprite = arcade.Sprite(":my-assets:images/blue_zone.png", scale=0.055)
                elif self.picked_placeable == self.factory:
                    placeable = logic.Industrial
                    sprite = arcade.Sprite(":my-assets:images/yellow_zone.jpg", scale=0.055)
                elif self.picked_placeable == self.road_types[0]:
                    placeable = logic.VerticalRoad
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0144.png", scale=2)
                elif self.picked_placeable == self.road_types[1]:
                    placeable = logic.HorizontalRoad
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0110.png", scale=2)
                elif self.picked_placeable == self.townhall:
                    placeable = logic.TownHall
                    sprite = arcade.Sprite(self.construction_texture, scale=2)

                if placeable and sprite:
                    result = logic.try_placing_placeable(grid_x, grid_y, placeable)
                    if result == 'placed':
                        self.build_sound.play(volume=config.effect_volume / 100)

                        sprite.center_x = self.offset_x + grid_x * tile_size + tile_size / 2
                        sprite.center_y = self.offset_y + grid_y * tile_size + tile_size / 2
                        if placeable != logic.TownHall:
                            self.scene.add_sprite('Object', sprite)
                    elif result == 'occupied':
                        self.show_warning = True
                        self.warning_timer = time.time()
                    elif result == 'no_money':
                        print('Not enough money!')

            # Right click - remove
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                result = logic.try_removing_object(grid_x, grid_y)

                if result == 'removed':
                    self.remove_sound = arcade.Sound("assets/sounds/remove.wav")
                    sprites = arcade.get_sprites_at_point((x, y), self.scene['Object'])
                elif result == 'tree_removed':
                    self.remove_sound = arcade.Sound("assets/sounds/remove.wav")
                    sprites = arcade.get_sprites_at_point((x, y), self.scene['Tree'])
                else:
                    sprites = []

                for sprite in sprites:
                    sprite.remove_from_sprite_lists()

    def on_mouse_release(self, x, y, button, modifiers):
        self.dragging = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.dragging:
            left = self.left_handle_X
            right = self.left_handle_X + 350
            self.handle_X = max(min(x, right), left)
            config.load_config()
            config.set_effect_volume(int(((self.handle_X - left) / 350) * 100))
            self.game_music_player.volume = config.effect_volume / 100
            self.volume_text.text = f"Effect volume: {config.effect_volume}%"
            config.save_config()

    def _update_ui_positions(self):
        """Update UI positions after resolution change"""
        config.load_config()
        self.tile_map.scaling = config.current_resolution_index - self.tile_map.scaling

        self.window_width, self.window_height = self.window.get_size()
        self.window_middle_x = self.window.width / 2
        self.window_middle_y = self.window.height / 2
        self.map_width = self.tile_map.width * self.tile_map.tile_width * self.tile_map.scaling
        self.map_height = self.tile_map.height * self.tile_map.tile_height * self.tile_map.scaling
        self.window_width = self.window.width
        self.window_height = self.window.height

        self.settings_title.x = self.window_middle_x
        self.settings_title.y = self.window_middle_y + 250

        self.volume_text.x = self.window_middle_x
        self.volume_text.y = self.window_middle_y + 185

        self.back_text.x = self.window_middle_x - 150
        self.back_text.y = self.window_middle_y - 150

        self.save_exit_text.x = self.window_middle_x + 150
        self.save_exit_text.y = self.window_middle_y - 150

        self.dropdown_x = self.window_middle_x
        self.dropdown_y = self.window_middle_y + 50

        self.resolution_label.x = self.dropdown_x - 200
        self.resolution_label.y = self.dropdown_y + 10

        self.left_handle_X = self.window_middle_x - 200
        self.handle_X = self.left_handle_X + 350 * (config.volume / 100)

    def rebuild_scene_from_logic(self):
        """Rebuild scene from saved logic data"""
        tile_size = 16 * 2
        tile_map = arcade.load_tilemap(':my-assets:maps/Starting_location.tmx', scaling=2)

        self.map_width = tile_map.width * tile_map.tile_width * tile_map.scaling
        self.map_height = tile_map.height * tile_map.tile_height * tile_map.scaling

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

                sprite = None
                if isinstance(cell, logic.House):
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0027.png", scale=2)
                elif isinstance(cell, logic.Store):
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0046.png", scale=2)
                elif isinstance(cell, logic.Factory):
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0083.png", scale=2)
                elif isinstance(cell, logic.VerticalRoad):
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0144.png", scale=2)
                elif isinstance(cell, logic.HorizontalRoad):
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0110.png", scale=2)
                elif isinstance(cell, logic.Residential):
                    sprite = arcade.Sprite(":my-assets:images/green_zone.png", scale=0.055)
                elif isinstance(cell, logic.Commercial):
                    sprite = arcade.Sprite(":my-assets:images/blue_zone.png", scale=0.055)
                elif isinstance(cell, logic.Industrial):
                    sprite = arcade.Sprite(":my-assets:images/yellow_zone.jpg", scale=0.055)
                elif isinstance(cell, logic.TownHall):
                    sprite = arcade.Sprite(":my-assets:maps/Tiles/tile_0014.png", scale=2)

                if sprite:
                    sprite.center_x = self.offset_x + x * tile_size + tile_size / 2
                    sprite.center_y = self.offset_y + y * tile_size + tile_size / 2
                    self.scene.add_sprite("Object", sprite)

    def on_update(self, delta_time: float):

        logic.update_time(delta_time)

        if time.time() - self.last_update_time > 1:
            logic.update_city()
            self.last_update_time = time.time()

        finished = logic.update_construction(delta_time)

        for building, x, y in finished:
            if (x, y) in self.building_sprites:
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
    window = arcade.Window(width=1024, height=768, title="SimCity")
    window.center_window()
    game = GameView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()


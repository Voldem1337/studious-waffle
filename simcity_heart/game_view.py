import arcade
from pathlib import Path

window = arcade.Window(fullscreen=True, title='SimCity')
window.center_window()

assets_path = Path().absolute().resolve() / Path('assets')
arcade.resources.add_resource_handle('my-assets', assets_path)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # Загружаем карту
        tile_map = arcade.load_tilemap(':my-assets:maps/Starting_location.tmx', scaling=3)

        map_width = tile_map.width * tile_map.tile_width * tile_map.scaling
        map_height = tile_map.height * tile_map.tile_height * tile_map.scaling
        window_width = window.width
        window_height = window.height

        offset_x = window_width / 2 - map_width / 2
        offset_y = window_height / 2 - map_height / 2

        for layer in tile_map.sprite_lists.values():
            for sprite in layer:
                sprite.center_x += offset_x
                sprite.center_y += offset_y

        self.scene = arcade.Scene.from_tilemap(tile_map)


    def on_draw(self) -> None:
        self.clear()
        self.scene.draw()


    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            window.close()

    def on_update(self, delta_time: float):
        pass




game = GameView()
window.show_view(game)
arcade.run()

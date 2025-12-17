import arcade
from pathlib import Path


class Worldname(arcade.View):

    def __init__(self):
        super().__init__()
        WORLDS_DIR = Path('data/worlds')

        world_files = list(WORLDS_DIR.glob("*.json"))

        self.world_names = [file.stem for file in world_files]

        self.window_middle_x = self.window.width / 2
        self.window_middle_y = self.window.height / 2

        self.world_name = ''
        self.max_length = 20

        self.cursor_visible = True
        self.cursor_timer = 0

        self.title = arcade.Text(
            'Worlds',
            self.window_middle_x,
            self.window_middle_y + 300,
            arcade.color.WHITE,
            30,
            anchor_x='center'
        )

        self.input_box_width = 400
        self.input_box_height = 50
        self.input_box_x = self.window_middle_x - (self.input_box_width / 2)
        self.input_box_y = self.window_middle_y +200

    def on_draw(self):
        self.clear(arcade.color.DARK_BLUE_GRAY)
        for i in range(len(self.world_names)):

            arcade.draw_lbwh_rectangle_filled(
                self.input_box_x ,
                self.input_box_y - i * 80,
                self.input_box_width,
                self.input_box_height,
                arcade.color.DARK_GRAY
            )

            arcade.draw_lbwh_rectangle_outline(
                self.input_box_x,
                self.input_box_y - i * 80,
                self.input_box_width,
                self.input_box_height,
                arcade.color.WHITE,
                3
            )
            arcade.draw_text(f'{self.world_names[i]}',
                self.input_box_x + self.input_box_width / 2,
                self.input_box_y + self.input_box_height / 2 - i * 80- 10,
                arcade.color.WHITE,20,
                anchor_x='center'
            )
        self.title.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        for i, world_name in enumerate(self.world_names):
            rect_x = self.input_box_x
            rect_y = self.input_box_y - i * 80
            rect_w = self.input_box_width
            rect_h = self.input_box_height

            if (
                    rect_x <= x <= rect_x + rect_w and
                    rect_y <= y <= rect_y + rect_h
            ):
                print(f"Clicked on world: {world_name}")

                from game_view import GameView
                import save_load

                if save_load.load_game(world_name):
                    game = GameView()
                    game.rebuild_scene_from_logic()
                    self.window.show_view(game)

                return

    def on_update(self, delta_time):
        self.cursor_timer += delta_time
        if self.cursor_timer >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            from main import MainView
            menu = MainView()
            self.window.show_view(menu)


def main():
    window = arcade.Window(width=1024, height=768, title="SimCity")
    window.center_window()
    game = Worldname()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
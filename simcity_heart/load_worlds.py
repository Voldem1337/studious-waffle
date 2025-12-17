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
                self.input_box_y - i * 150,
                self.input_box_width,
                self.input_box_height,
                arcade.color.DARK_GRAY
            )

            arcade.draw_lbwh_rectangle_outline(
                self.input_box_x,
                self.input_box_y + i * 150,
                self.input_box_width,
                self.input_box_height,
                arcade.color.WHITE,
                3
            )
        self.title.draw()

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
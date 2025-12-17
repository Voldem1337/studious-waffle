import arcade
from simcity_heart import config


class Worldname(arcade.View):
    def __init__(self):
        super().__init__()


        self.window_middle_x = self.window.width / 2
        self.window_middle_y = self.window.height / 2

        self.world_name = ''
        self.max_length = 20

        self.cursor_visible = True
        self.cursor_timer = 0

        self.title = arcade.Text(
            'Enter World Name:',
            self.window_middle_x,
            self.window_middle_y + 150,
            arcade.color.WHITE,
            30,
            anchor_x='center'
        )

        self.hint = arcade.Text(
            'Press ENTER to continue or ESC to go back',
            self.window_middle_x,
            self.window_middle_y - 150,
            arcade.color.WHITE,
            16,
            anchor_x='center'
        )

        self.input_box_width = 400
        self.input_box_height = 50
        self.input_box_x = self.window_middle_x - (self.input_box_width / 2)
        self.input_box_y = self.window_middle_y - 25

    def on_draw(self):
        self.clear(arcade.color.DARK_BLUE_GRAY)


        arcade.draw_lbwh_rectangle_filled(
            self.input_box_x,
            self.input_box_y,
            self.input_box_width,
            self.input_box_height,
            arcade.color.DARK_GRAY
        )


        arcade.draw_lbwh_rectangle_outline(
            self.input_box_x,
            self.input_box_y,
            self.input_box_width,
            self.input_box_height,
            arcade.color.WHITE,
            3
        )


        display_text = self.world_name if self.world_name else 'My World'
        if self.cursor_visible:
            display_text += '|'

        arcade.draw_text(
            display_text,
            self.window_middle_x,
            self.input_box_y + 15,
            arcade.color.WHITE,
            20,
            anchor_x='center'
        )

        self.title.draw()
        self.hint.draw()


        counter_text = f"{len(self.world_name)}/{self.max_length}"
        arcade.draw_text(
            counter_text,
            self.input_box_x + self.input_box_width - 10,
            self.input_box_y - 25,
            arcade.color.WHITE,
            14,
            anchor_x="right"
        )

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

        elif symbol == arcade.key.ENTER:
            if not self.world_name.strip():
                self.world_name = 'My World'

            config.current_world_name = self.world_name.strip()

            from game_view import GameView
            game = GameView()
            self.window.show_view(game)

        elif symbol == arcade.key.BACKSPACE:
            self.world_name = self.world_name[:-1]

    def on_text(self, text: str):
        if len(self.world_name) < self.max_length:
            if text.isalnum() or text in [' ', '-', '_']:
                self.world_name += text
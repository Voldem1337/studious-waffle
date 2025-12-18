import arcade
import os
from pathlib import Path
import save_load
from game_view import GameView
import config


class MainView(arcade.View):
    def on_show(self):

        self.window_width, self.window_height = self.window.get_size()

    def __init__(self):

        super().__init__()


        # self.music_player = config.music_player


        # adding bc
        img1 = 'assets/images/Loading.png'
        self.bc = arcade.Sprite(img1)

        # getting variables
        self.img_list = arcade.SpriteList()
        self.window_width, self.window_height = self.window.get_size()
        self.window_middle_x = self.window_width / 2
        self.window_middle_y = self.window_height / 2

        self.left_handle_X = self.window_middle_x - 200
        self.handle_X = self.left_handle_X + 350 * (config.volume / 100)

        # path
        self.menu_bar = arcade.Sprite('assets/images/menu_bars.png', scale=0.5)
        self.menu_bar.position = (self.window_middle_x, self.window_middle_y)

        # variables
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

        # button position
        self.buttons = {
            'New Game': {"x": self.window_middle_x - 155, "y": self.window_middle_y + 100, "w": self.button_width,
                         "h": self.button_height},
            'Load Game': {'x': self.window_middle_x - 155, "y": self.window_middle_y + 5, "w": self.button_width,
                          "h": self.button_height},
            'Settings': {'x': self.window_middle_x - 155, 'y': self.window_middle_y - 85, 'w': self.button_width,
                         'h': self.button_height},
            'Exit': {'x': self.window_middle_x - 155, 'y': self.window_middle_y - 175, 'w': self.button_width,
                     'h': self.button_height}
        }

        # For exit button and settings
        self.show_confirm = False
        self.show_settings = False
        self.dragging = False

        self.label = arcade.Text("Are you sure?", self.window_middle_x, self.window_middle_y + 100, arcade.color.BLACK,
                                 20, anchor_x="center")
        self.yes = arcade.Text("[YES]", self.window_middle_x - 100, self.window_middle_y, arcade.color.RED, 20,
                               anchor_x="center", anchor_y="center")
        self.no = arcade.Text("[NO]", self.window_middle_x + 100, self.window_middle_y, arcade.color.DARK_GREEN, 20,
                              anchor_x="center", anchor_y="center")

        self.settings = arcade.Text("SETTINGS", self.window_middle_x, self.window_middle_y + 250, arcade.color.WHITE,
                                    35, anchor_x="center")
        self.volume = arcade.Text(f"Volume: {config.volume}%", self.window_middle_x, self.window_middle_y + 185,
                                  arcade.color.WHITE, 20, anchor_x="center")
        self.back = arcade.Text('BACK', self.window_middle_x - 150, self.window_middle_y - 150,
                                arcade.color.WHITE, 20, anchor_x="center")

        # For windows modes bars
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
        self.resolution_label = arcade.Text(
            "Resolution:",
            self.dropdown_x - 200,
            self.dropdown_y + 10,
            arcade.color.WHITE,
            20
        )

    def on_draw(self) -> None:
        self.clear()
        self.img_list.draw()

        # exit window creation
        if self.show_confirm:
            arcade.draw_lbwh_rectangle_filled(0, 0, self.window_width, self.window_height, (0, 0, 0, 200))
            arcade.draw_lbwh_rectangle_filled(self.window_middle_x - 150, self.window_middle_y - 50, 300, 200,
                                              arcade.color.DARK_GRAY)
            arcade.draw_lbwh_rectangle_outline(self.window_middle_x - 150, self.window_middle_y - 50, 300, 200,
                                               arcade.color.WHITE, 3)
            self.label.draw()
            self.yes.draw()
            self.no.draw()

        # setting window
        if self.show_settings:
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
            self.resolution_label.draw()
            current_res_name = self.resolutions[self.current_resolution_index][0]
            arcade.draw_lbwh_rectangle_filled(
                self.dropdown_x + 25,
                self.dropdown_y,
                self.dropdown_width,
                self.dropdown_height,
                arcade.color.DARK_GRAY
            )
            arcade.draw_lbwh_rectangle_outline(
                self.dropdown_x + 25,
                self.dropdown_y,
                self.dropdown_width,
                self.dropdown_height,
                arcade.color.WHITE,
                2
            )
            arcade.draw_text(
                current_res_name,
                self.dropdown_x + 35,
                self.dropdown_y + 12,
                arcade.color.WHITE,
                16
            )
            arrow = "▼" if not self.dropdown_open else "▲"
            arcade.draw_text(
                arrow,
                self.dropdown_x + self.dropdown_width - 15,
                self.dropdown_y + 10,
                arcade.color.WHITE,
                18
            )
            if self.dropdown_open:
                for i, (res_name, res_value) in enumerate(self.resolutions):
                    option_y = self.dropdown_y - (i + 1) * self.dropdown_height

                    bg_color = arcade.color.GRAY if i == self.current_resolution_index else arcade.color.DARK_GRAY

                    arcade.draw_lbwh_rectangle_filled(
                        self.dropdown_x + 25,
                        option_y,
                        self.dropdown_width,
                        self.dropdown_height,
                        bg_color
                    )
                    arcade.draw_lbwh_rectangle_outline(
                        self.dropdown_x + 25,
                        option_y,
                        self.dropdown_width,
                        self.dropdown_height,
                        arcade.color.WHITE,
                        2
                    )

                    arcade.draw_text(
                        res_name,
                        self.dropdown_x + 35,
                        option_y + 12,
                        arcade.color.WHITE,
                        16
                    )

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        # defining what button is pressed
        if not self.show_confirm and not self.show_settings:
            for name, b in self.buttons.items():
                if x >= b['x'] and x <= b['x'] + b['w'] and y >= b['y'] and y <= b['y'] + b['h']:
                    if name == "New Game":
                        from worldname import Worldname
                        game = Worldname()
                        self.window.show_view(game)
                    elif name == "Load Game":

                        from load_worlds import Worldname
                        game = Worldname()
                        self.window.show_view(game)

                    elif name == "Settings":
                        self.show_settings = True
                    elif name == "Exit":
                        self.show_confirm = True
                    break

        if self.show_confirm:
            if self.window_middle_x - 138 <= x <= self.window_middle_x - 35 and self.window_middle_y - 25 <= y <= self.window_middle_y + 24:
                arcade.exit()
            elif self.window_middle_x + 74 <= x <= self.window_middle_x + 128 and self.window_middle_y - 25 <= y <= self.window_middle_y + 24:
                self.show_confirm = False
                self.clear()


        elif self.show_settings:
            if abs(x - self.handle_X) <= 15 and abs(y - (self.window_middle_y + 127)) <= 15:
                self.dragging = True

            # by selecting at the bar any point volume will change
            if self.window_middle_x - 200 <= x <= self.window_middle_x + 150 and self.window_middle_y + 115 <= y <= self.window_middle_y + 140:
                self.handle_X = x
                config.set_volume(int(((self.handle_X - self.left_handle_X) / 350) * 100))
                self.volume.text = f"Volume: {config.volume}%"

            if self.window_middle_x - 186 <= x <= self.window_middle_x - 114 and self.window_middle_y - 152 <= y <= self.window_middle_y - 131:
                self.show_settings = False
                self.clear()


            if (self.dropdown_x <= x <= self.dropdown_x + self.dropdown_width and
                    self.dropdown_y <= y <= self.dropdown_y + self.dropdown_height):
                self.dropdown_open = not self.dropdown_open
                return

            # dropdown if opened, showing all variants
            if self.dropdown_open:
                for i, (res_name, res_value) in enumerate(self.resolutions):
                    option_y = self.dropdown_y - (i + 1) * self.dropdown_height

                    if (self.dropdown_x <= x <= self.dropdown_x + self.dropdown_width and
                            option_y <= y <= option_y + self.dropdown_height):

                        # changing resolution
                        self.current_resolution_index = i
                        config.current_resolution_index = i
                        self.dropdown_open = False

                        if res_value is None:  # Fullscreen
                            self.window.set_fullscreen(True)
                        else:  # window mode
                            self.window.set_fullscreen(False)
                            self.window.set_size(res_value[0], res_value[1])
                            self.window.center_window()

                        # updating resolution
                        self.window_width, self.window_height = self.window.get_size()
                        self.window_middle_x = self.window.width / 2
                        self.window_middle_y = self.window.height / 2

                        # updating positioning of elements
                        self._update_ui_positions()
                        config.save_config()
                        return

            # Volume
            if abs(x - self.handle_X) <= 15 and abs(y - (self.window_middle_y + 127)) <= 15:
                self.dragging = True

            # Buttons Back
            if (self.window_middle_x - 186 <= x <= self.window_middle_x - 114 and
                    self.window_middle_y - 152 <= y <= self.window_middle_y - 131):
                self.show_settings = False
                self.dropdown_open = False
                self.clear()

    def _update_ui_positions(self):
        self.window_width, self.window_height = self.window.get_size()
        self.window_middle_x = self.window.width / 2
        self.window_middle_y = self.window.height / 2

        self.menu_bar.position = (self.window_middle_x, self.window_middle_y)

        self.buttons = {
            'New Game': {"x": self.window_middle_x - 155, "y": self.window_middle_y + 100, "w": 300, "h": 74},
            'Load Game': {'x': self.window_middle_x - 155, "y": self.window_middle_y + 5, "w": 300, "h": 74},
            'Settings': {'x': self.window_middle_x - 155, 'y': self.window_middle_y - 85, 'w': 300, 'h': 74},
            'Exit': {'x': self.window_middle_x - 155, 'y': self.window_middle_y - 175, 'w': 300, 'h': 74}
        }

        self.bc.width = self.window_width
        self.bc.height = self.window_height
        self.bc.center_x = self.window_middle_x
        self.bc.center_y = self.window_middle_y

        self.label.x = self.window_middle_x
        self.label.y = self.window_middle_y + 100
        self.yes.x = self.window_middle_x - 100
        self.yes.y = self.window_middle_y
        self.no.x = self.window_middle_x + 100
        self.no.y = self.window_middle_y

        self.settings.x = self.window_middle_x
        self.settings.y = self.window_middle_y + 250

        self.volume.x = self.window_middle_x
        self.volume.y = self.window_middle_y + 185

        self.back.x = self.window_middle_x - 50
        self.back.y = self.window_middle_y - 150

        self.dropdown_x = self.window_middle_x + 15
        self.dropdown_y = self.window_middle_y + 50

        self.resolution_label.x = self.dropdown_x - 215
        self.resolution_label.y = self.dropdown_y + 10

        self.left_handle_X = self.window_middle_x - 200
        self.handle_X = self.left_handle_X + 350 * (config.volume / 100)
        self.back = arcade.Text('BACK', self.window_middle_x - 150, self.window_middle_y - 150,
                                arcade.color.WHITE, 20, anchor_x="center")

    def on_mouse_release(self, x, y, button, modifiers):
        self.dragging = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.dragging:
            left = self.left_handle_X
            right = self.left_handle_X + 350

            self.handle_X = max(min(x, right), left)
            config.set_volume(int(((self.handle_X - left) / 350) * 100))
            self.volume.text = f"Volume: {config.volume}%"


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            if self.show_settings:
                self.show_settings = False
            elif self.show_confirm:
                self.show_confirm = False
            elif not self.show_confirm:
                self.show_confirm = True



class Loading_screen(arcade.View):
    def __init__(self):
        self.music = arcade.Sound('assets/music/Menu_music.mp3')
        config.music_player = self.music.play(
            volume=config.volume / 100,
            loop=True
        )

        # initialization picture
        self.window_middle_x, self.window_middle_y = window.width / 2, window.height / 2
        super().__init__()
        img1 = 'assets/images/Loading.png'
        self.bc = arcade.Sprite(img1, scale=1)

        screen_width, screen_height = window.get_size()

        # positioning
        self.bc.width = screen_width
        self.bc.height = screen_height
        self.bc.center_x = screen_width / 2
        self.bc.center_y = screen_height / 2
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.bc)

        # parameters for progress-bar
        self.progress = 0
        self.loading_speed = 20
        self.bar_width = 400
        self.bar_height = 25
        self.bar_y = screen_height / 2 - 50

        # bc and progress bar
        self.image_folder = "assets/images"
        self.files = os.listdir(self.image_folder)
        self.total_files = len(self.files)
        self.loaded_files = 0
        self.progress = 0
        self.textures = []

    def on_draw(self) -> None:
        self.clear()
        self.sprite_list.draw()

        bar_x = window.width / 2 - 200

        # bar outline
        arcade.draw_lbwh_rectangle_outline(
            bar_x, self.bar_y,
            self.bar_width, self.bar_height,
            arcade.color.WHITE
        )

        # width
        fill_width = (self.progress / 100) * (self.bar_width - 0)

        # calculating bar edges
        left_edge_x = bar_x - fill_width / 2
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
            bar_x + 100, self.bar_y + 33,
            arcade.color.WHITE, 28
        )

    def on_update(self, delta_time: float):
        if self.progress < 100:
            self.progress += self.loading_speed * delta_time
        else:
            self.progress = 100
            main = MainView()
            window.show_view(main)


if __name__ == '__main__':
    try:
        config.load_config()
        num = config.current_resolution_index
        if num == 0:
            window = arcade.Window(fullscreen=True, title='SimCity')
        elif num == 1:
            window = arcade.Window(width=1920, height=1080, title='SimCity')
        elif num == 2:
            window = arcade.Window(width=1600, height=900, title='SimCity')
        elif num == 3:
            window = arcade.Window(width=1280, height=720, title='SimCity')
    except Exception:
        window = arcade.Window(width=1920, height=1080, title='SimCity')
    window.center_window()
    assets_path = Path().absolute().resolve() / Path('assets')
    arcade.resources.add_resource_handle('my-assets', assets_path)

    game = Loading_screen()
    window.show_view(game)
    arcade.run()
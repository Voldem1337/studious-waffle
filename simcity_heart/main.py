import arcade
import os






class MainView(arcade.View):
    def __init__(self):
        super().__init__()
        #adding bc
        img1 = 'assets/images/Loading.png'
        self.bc = arcade.Sprite(img1)


        #getting variables
        self.img_list = arcade.SpriteList()
        self.window_width, self.window_height = self.window.get_size()
        self.window_middle_x, self.window_middle_y = self.window.width /2, self.window.height /2


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
                        from game_view import GameView  # game import
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
            if abs(x - self.window_middle_x - 210) <= 10 * 2 and abs(y - self.window_middle_x - 210) <= 20:
                self.dragging = True
            if  self.window_middle_x-186 <= x <= self.window_middle_x-114 and self.window_middle_y-152 <= y <= self.window_middle_y-131:
                self.show_settings = False
                self.clear()


    def on_mouse_release(self, x, y, button, modifiers):
        self.dragging = False

    def on_mouse_motion(self, x, y, dx, dy):
        """ Если тянем — обновляем позицию и громкость """
        if self.dragging:
            left = self.left_handle_X
            right = self.left_handle_X + self.slider_width
            self.handle_X = max(min(x, right), left)
            self.volume = ((self.handle_X - left) / self.slider_width) * 100


class Loading_screen(arcade.View):
    def __init__(self):
        #intialization picture
        super().__init__()
        img1 = 'assets/images/Loading.png'
        self.bc = arcade.Sprite(
        img1,scale=1
        )
        screen_width, screen_height = self.window.get_size()


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
        bar_x = self.window.width / 2 - 100


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
            self.window.show_view(main)
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

# window = arcade.Window(fullscreen= True, title="SimCity Heart")
def main():
    window = arcade.Window(1920, 1020, "SimCity")
    window.center_window()
    game = Loading_screen()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()

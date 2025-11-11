import arcade
import os

# window = arcade.Window(fullscreen= True, title="SimCity Heart")
window = arcade.Window( title="SimCity", width=1920, height=1080 )
window.center_window()

class MainView(arcade.View):
    def __init__(self):
        super().__init__()
        #getting variables
        self.img_list = arcade.SpriteList()
        self.window_width, self.window_height = window.get_size()
        self.window_middle_x, self.window_middle_y = window.width /2, window.height /2
        #path
        self.menu_bar = arcade.Sprite('assets/images/menu_bars.png', scale=0.5)
        self.menu_bar.position = (self.window_middle_x, self.window_middle_y)
        #music loop
        # self.music = arcade.Sound('assets/music/Menu_music.mp3')
        # self.music.play(loop=True)
        self.img_list.append(self.menu_bar)

        self.menu_bar_left = self.window_middle_x - 155
        self.menu_bar_right = self.window_middle_x + 135
        self.button_width = 300
        self.button_height = 74
        #button position
        self.buttons = {
            'New Game': {"x" : self.window_middle_x-155, "y" : self.window_middle_y+100, "w": self.button_width, "h": self.button_height},
            'Load Game' : {'x': self.window_middle_x-155, "y": self.window_middle_y+5, "w": self.button_width, "h": self.button_height},
            'Settings': {'x': self.window_middle_x-155, 'y': self.window_middle_y-85, 'w': self.button_width, 'h': self.button_height},
            'Exit' : {'x': self.window_middle_x-155, 'y': self.window_middle_y-175, 'w': self.button_width, 'h': self.button_height}
        }
        #For exit button
        self.show_confirm = False




    def on_draw(self) -> None:
        self.clear()
        self.img_list.draw()
        #exit window creation
        if self.show_confirm:
            arcade.draw_lbwh_rectangle_filled(0, 0,self.window_width,self.window_height,(0, 0, 0, 150))
            arcade.draw_lbwh_rectangle_filled(self.window_middle_x-150, self.window_middle_y-50, 300, 200, arcade.color.LIGHT_GRAY)  # само окно
            arcade.draw_lbwh_rectangle_outline(self.window_middle_x-150, self.window_middle_y-50, 300, 200, arcade.color.WHITE, 3)

            arcade.draw_text("Are you sure?",
                             self.window_middle_x, self.window_middle_y+100, arcade.color.BLACK, 20, anchor_x="center")
            arcade.draw_text("[YES]", self.window_middle_x-100, self.window_middle_y, arcade.color.RED, 20, anchor_x="center", anchor_y="center")
            arcade.draw_text("[NO]", self.window_middle_x+100, self.window_middle_y, arcade.color.DARK_GREEN, 20, anchor_x="center", anchor_y="center")
            arcade.draw_lbwh_rectangle_outline()
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        #defining what button is pressed
        if not self.show_confirm:
            for name, b in self.buttons.items():
                if x >=b['x'] and x <= b['x'] + b['w'] and y >= b['y'] and y<= b['y'] + b['h']:
                    if name == "New Game":
                        print("New Game")
                    elif name == "Load Game":
                        print("Load Game")
                    elif name == "Settings":
                        print("Settings")
                    elif name == "Exit":
                        self.show_confirm = True
                    break
        if self.show_confirm:



class Loading_screen(arcade.View):
    def __init__(self):
        #intialization picture
        super().__init__()
        img1 = 'assets/images/Loading.png'
        self.bc = arcade.Sprite(
        img1,scale=1
        )
        screen_width, screen_height = window.get_size()
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

        #da
        self.image_folder = "assets/images"
        self.files = os.listdir(self.image_folder)
        self.total_files = len(self.files)
        self.loaded_files = 0
        self.progress = 0
        self.textures = []

    #drawing sprite(image)
    def on_draw(self) -> None:
        # creating picture
        self.clear()
        self.sprite_list.draw()

        # creating loading bar
        bar_x = window.width / 2 - 100

        # рисуем рамку бара
        arcade.draw_lbwh_rectangle_outline(
            bar_x, self.bar_y,
            self.bar_width, self.bar_height,
            arcade.color.WHITE
        )

        # вычисляем ширину заливки
        fill_width = (self.progress / 100) * (self.bar_width -0)

        # вычисляем левый край и центр заливки, чтобы она росла слева направо

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
            window.show_view(main)
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
    #         print("Все ресурсы загружены!")


# game = Loading_screen()
game = MainView()
window.show_view(game)
arcade.run()

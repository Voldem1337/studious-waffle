import arcade
import os

# window = arcade.Window(fullscreen= True, title="SimCity Heart")
window = arcade.Window( title="SimCity", width=800, height=600 )
window.center_window()


class MainView(arcade.View):
    def __init__(self):
        super().__init__()
        #getting variables
        self.img_list = arcade.SpriteList()
        self.window_width, self.window_height = window.get_size()
        self.window_middle_x, self.window_middle_y = window.width /2, window.height /2
        #music loop
        # self.music = arcade.Sound('assets/music/Menu_music.mp3')
        # self.music.play(volume = 0.2, loop = True)
        #variables
        self.menu_bar_left = self.window_middle_x - 155
        self.menu_bar_right = self.window_middle_x + 135
        self.button_width = 300
        self.button_height = 74

        #For exit button and settings
        self.show_confirm = False
        self.show_settings = True
        self.dragging = False
        self.left_handle_X = self.window_middle_x-200
        self.volume = 50
        self.settings = arcade.Text("SETTINGS", self.window_middle_x, self.window_middle_y + 250, arcade.color.WHITE,
                                    35, anchor_x="center")
        self.volume = arcade.Text(f"Volume: {int(self.volume)}%", self.window_middle_x,
                                  self.window_middle_y + 185,
                                  arcade.color.WHITE, 20, anchor_x="center")



    def on_draw(self) -> None:
        self.clear()
        self.handle_X = self.left_handle_X + 200
        arcade.draw_lbwh_rectangle_filled(0, 0, self.window_width, self.window_height, (0, 0, 0, 200))
        arcade.draw_lbwh_rectangle_filled(self.window_middle_x-300,self.window_middle_y-250,600,600,arcade.color.DARK_GRAY)
        arcade.draw_lbwh_rectangle_outline(self.window_middle_x - 300, self.window_middle_y -250, 600, 600,arcade.color.WHITE, 3)
        arcade.draw_lbwh_rectangle_filled(self.window_middle_x-200, self.window_middle_y+125, 350, 5, arcade.color.LIGHT_GRAY)
        arcade.draw_circle_filled(self.handle_X,self.window_middle_y +127,10,arcade.color.GOLD)

        self.settings.draw()
        self.volume.draw()


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:


        if self.show_settings:
            print(y - self.window_middle_y)
            if self.window_middle_x-205 <=x <=self.window_middle_x+152 and self.window_middle_y+112<= y <=self.window_middle_y+139 :
                print('zahla')
                self.dragging = True


    def on_mouse_release(self, x, y, button, modifiers):
        self.dragging = False


    def on_mouse_motion(self, x, y, dx, dy):
        if self.dragging:
            left  = self.window_middle_x - 210 -450/2
            right = self.window_middle_x + 210 -450/2
            self.handle_X = max(min(x, right), left)
            self.volume = (self.handle_X - left) / (450)
            pass





game = MainView()
window.show_view(game)
arcade.run()
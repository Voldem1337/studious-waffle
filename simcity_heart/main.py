import arcade
import os

window = arcade.Window(fullscreen= True, title="SimCity Heart")
window.center_window()


class Loading_screen(arcade.View):
    def __init__(self):
        super().__init__()
        img1 = '../assets/images/Loading.png'
        self.bc = arcade.Sprite(
        img1,scale=1
        )
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.bc)


    def on_draw(self) -> None:
        self.clear()
        self.sprite_list.draw()

game = Loading_screen()
window.show_view(game)
arcade.run()

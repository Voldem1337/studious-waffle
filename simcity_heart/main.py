import arcade


# window = arcade.Window(fullscreen= True, title="SimCity Heart")
window = arcade.Window( title="SimCity Heart", width=1280, height=800 )
window.center_window()


class Loading_screen(arcade.View):
    def __init__(self):
        #intialization picture
        super().__init__()
        img1 = '../assets/images/Loading.png'
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
        self.progress =0
        self.loading_speed = 30
        self.bar_width = 400
        self.bar_height = 400
        self.bar_y = screen_height / 2


    #drawing sprite(image)
    def on_draw(self) -> None:
        #creating picture
        self.clear()
        self.sprite_list.draw()
        #creating loading bar
        bar_x = window.width / 2
        arcade.draw_lbwh_rectangle_outline(
            bar_x,self.bar_y,
            self.bar_width,self.bar_height,
            arcade.color.WHITE,3
        )
        fill_width = (self.progress / 100) * (self.bar_width - 6)
        #filling code
        if fill_width > 0:
            arcade.draw_lbwh_rectangle_filled(
                bar_x -(self.bar_width -6- fill_width)/2,
            self.bar_y,fill_width,
            self.bar_height -6,
            arcade.color.GREEN)
        #loading txt
        precent_text =f"{int(self.progress)}%"
        arcade.draw_text(
            precent_text,
            bar_x - 20, self.bar_y - 10,
            arcade.color.WHITE,14
        )
    def on_update(self,delta_time: float):
        if self.progress >= 100:
            self.progress += self.loading_speed * delta_time
        else:
            self.progress = 100



game = Loading_screen()
window.show_view(game)
arcade.run()

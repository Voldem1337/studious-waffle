import arcade
import os

# window = arcade.Window(fullscreen= True, title="SimCity Heart")
window = arcade.Window( title="SimCity Heart", width=1280, height=800 )
window.center_window()

class MainView(arcade.View):
    def __init__(self):
        super().__init__()
        self.bar_x = window.width / 2 - 100
        self.bar_y = window.height / 2


    def on_draw(self) -> None:
        self.clear()
        percent_text = f"Menuu"
        arcade.draw_text(
            percent_text,
            self.bar_x + 100, self.bar_y + 50,
            arcade.color.WHITE, 28
        )



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
        self.progress = 0
        self.loading_speed = 20
        self.bar_width = 400
        self.bar_height = 25
        self.bar_y = screen_height / 2 -50

        #da
        self.image_folder = "../assets/images"
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

        #Should be when project is ready #self.progress = (загружено_файлов / общее_количество_файлов) * 100

    def on_update(self, delta_time: float):
        if self.progress < 100:
            self.progress += self.loading_speed * delta_time
        else:
            self.progress = 100
            main = MainView()
            window.show_view(main)
    # def on_update(self, delta_time):
    #     # загружаем по одному файлу за кадр (для демонстрации)
    #     if self.loaded_files < self.total_files:
    #         file_name = self.files[self.loaded_files]
    #         file_path = os.path.join(self.image_folder, file_name)
    #         texture = arcade.load_texture(file_path)
    #         self.textures.append(texture)
    #         self.loaded_files += 1
    #         # вычисляем процент
    #         self.progress = (self.loaded_files / self.total_files) * 100
    #     else:
    #         main = MainView()
    #         window.show_view(main)
    #         print("Все ресурсы загружены!")




game = Loading_screen()
window.show_view(game)
arcade.run()

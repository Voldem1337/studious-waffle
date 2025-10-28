import arcade

# Размер окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "City Growth Simulator"

class CityApp(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.ASH_GREY)

    def setup(self):
        # Здесь можно будет инициализировать объекты карты, здания и т.д.
        pass

    def on_draw(self):
        # Очистка экрана и рендеринг
        arcade.start_render()
        arcade.draw_text(
            "City Simulator setup successful!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=24,
            anchor_x="center"
        )

def main():
    app = CityApp()
    app.setup()
    arcade.run()

if __name__ == "__main__":
    main()

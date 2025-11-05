import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Загрузочный экран"

class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.progress = 0  # процент загрузки
        self.loading_bar_width = 400
        self.city_offset = 0  # для движения фона

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.background = arcade.load_texture("city_background.png")

    def on_draw(self):
        arcade.start_render()

        # 1️⃣ — Рисуем анимацию города (прокрутка фона)
        arcade.draw_lrwh_rectangle_textured(
            -self.city_offset, 0,
            SCREEN_WIDTH, SCREEN_HEIGHT,
            self.background
        )
        # второй слой для бесконечной прокрутки
        arcade.draw_lrwh_rectangle_textured(
            SCREEN_WIDTH - self.city_offset, 0,
            SCREEN_WIDTH, SCREEN_HEIGHT,
            self.background
        )

        # 2️⃣ — Рисуем рамку и заполнение прогресс-бара
        bar_x = SCREEN_WIDTH // 2
        bar_y = 100
        progress_width = (self.progress / 100) * self.loading_bar_width
        arcade.draw_rectangle_outline(bar_x, bar_y, self.loading_bar_width, 30, arcade.color.WHITE, 3)
        arcade.draw_rectangle_filled(bar_x - (self.loading_bar_width - progress_width)/2, bar_y, progress_width, 30, arcade.color.GREEN)

        # 3️⃣ — Текст с процентом
        arcade.draw_text(f"{int(self.progress)}%", bar_x - 20, bar_y - 10, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        # 4️⃣ — Простая анимация
        self.city_offset += 100 * delta_time
        if self.city_offset > SCREEN_WIDTH:
            self.city_offset = 0

        # 5️⃣ — Увеличиваем прогресс
        if self.progress < 100:
            self.progress += 30 * delta_time
        else:
            # Когда 100% — переход на другую сцену
            game_view = MainMenuView()
            self.window.show_view(game_view)

class MainMenuView(arcade.View):
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Главное меню", 250, 300, arcade.color.WHITE, 24)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(LoadingView())
    arcade.run()

if __name__ == "__main__":
    main()

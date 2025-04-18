from random import randint
from config import CONFIG
from cord import Cord
from food import Food   
from snake import Snake
from window import Window

# Логика игры
class Game:
    # Базовая инициализация
    def __init__(self) -> None:
        self.frame_rate: int = CONFIG.get()["game"]["frame_rate"]
        self.config()
        self.window: Window = Window(self)
        self.snake: Snake = Snake(self.window)
        self.create_food(is_init = True)
        self.game_loop()
        self.window.root.mainloop()

    # Конфиг игры, используется при перезапуске
    def config(self) -> None:
        self.food_limit: int = CONFIG.get()["game"]["food_limit"]
        self.food_storage: list = []
        self.score: int = 0
        self.running: bool = True

    # Пауза
    def escape_or_proceed(self) -> None:
        self.running = not self.running
        if (self.running):
            self.game_loop()
        else:
            self.window.show_escape_message()

    # Вывод победы и остановка игры
    def win(self) -> None:
        self.running = False
        self.window.show_win_message()

    # Перезапуск игры
    def restart(self) -> None:
        self.config()
        self.snake = Snake(self.window)
        self.running = True
        self.create_food(is_init = True)
        self.game_loop()

    # По сути движок
    def game_loop(self) -> None:
        if self.running:
            if self.snake.move():
                self.window.render()
                self.window.root.after(self.frame_rate, self.game_loop)
            else:
                self.running = False
                self.window.render()

    # Ищем свободную ячейку
    def get_free_cell_coords(self):
        grid_w = self.window.width // self.window.grid_size
        grid_h = self.window.height // self.window.grid_size

        all_cells = {
            Cord(x * self.window.grid_size, y * self.window.grid_size)
            for x in range(grid_w)
            for y in range(grid_h)
        }

        occupied_cells = {food.cord for food in self.food_storage}.union(self.snake.tail)

        free_cells = list(all_cells - occupied_cells)

        if not free_cells:
            return None

        # Берем случайную из свободных ячеек
        return free_cells[randint(0, len(free_cells) - 1)]

    # Убираем съеденную еду
    def remove_food(self, food: Food) -> None:
        self.window.game.food_storage.remove(food)

    # Создаем новую еду
    def create_food(self, is_init: bool) -> None:
        while len(self.food_storage) < self.food_limit:
            cord = self.get_free_cell_coords()
            # Если свободное место не найдено - победа
            if (cord is None):
                self.win()
                return

            # Закидываем в хранилище
            self.food_storage.append(Food(cord))

            # При генерации еды, смотрим на добавление (решение такое себе, можно получше распределить)
            if not is_init:
                self.score += CONFIG.get()["food"]["score"]

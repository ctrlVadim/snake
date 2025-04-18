import tkinter as tk
from config import CONFIG
import directions

class Window:
    def __init__(self, game) -> None:
        self.config(game)
        self.create()

    def config(self, game) -> None:
        self.game = game
        self.background_color = CONFIG.get()["window"]["background_color"]
        self.width: int = CONFIG.get()["window"]["width"]
        self.height: int = CONFIG.get()["window"]["height"]
        self.grid_size: int = CONFIG.get()["window"]["grid_size"]

    def create(self) -> None:
        self.root = tk.Tk()
        self.root.title("Змейка")
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg=self.background_color)
        self.canvas.pack()
        self.config_binding()

    def config_binding(self) -> None:
        self.root.bind('<Left>', lambda e: self.game.snake.change_direction(directions.LEFT))
        self.root.bind('<Right>', lambda e: self.game.snake.change_direction(directions.RIGHT))
        self.root.bind('<Up>', lambda e: self.game.snake.change_direction(directions.UP))
        self.root.bind('<Down>', lambda e: self.game.snake.change_direction(directions.DOWN))
        self.root.bind('<space>', lambda e: self.game.restart())
        self.root.bind('<Escape>', lambda e: self.game.escape_or_proceed())

    def render(self) -> None:
        if (not self.game.running):
            pass
        self.canvas.delete('all')

        for i, cord in enumerate(self.game.snake.tail):
            color = self.game.snake.head_color if i == 0 else self.game.snake.color
            self.canvas.create_rectangle(
                cord.x, cord.y,
                cord.x + self.grid_size, cord.y + self.grid_size,
                fill=color, outline='black'
            )

        for food in self.game.food_storage:
            self.canvas.create_oval(
                food.cord.x, food.cord.y,
                food.cord.x + self.grid_size, food.cord.y + self.grid_size,
                fill=food.color, outline='black'
            )

        self.canvas.create_text(
            50, 20,
            text=f"Очки: {self.game.score}",
            fill="white", font=('Arial', 14)
            )

        if not self.game.running:
            self.canvas.create_text(
                self.width // 2, self.height // 2,
                text=f"Игра окончена! Очки: {self.game.score}",
                fill="white", font=('Arial', 20))

    def show_escape_message(self) -> None:
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=f"Игра остановлена",
            fill="white", font=('Arial', 20))

    def show_win_message(self) -> None:
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=f"Вы выиграли",
            fill="white", font=('Arial', 20))

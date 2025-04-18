from cord import Cord
from window import Window
import directions
from config import CONFIG

# Змейка
class Snake:
    # Конструктор объект
    def __init__(self, window: Window) -> None:
        # Привязываем объект к игровому окну
        self.window: Window = window
        self.config()

    # Базовые настройки, вынесены для удобства калибровки
    def config(self) -> None:
        # Текущее направление
        self.direction: str = directions.RIGHT
        # Для предотвращения бага с рендером нового направления
        self.next_direction: str = directions.RIGHT

        # Хвост змейки
        self.tail: list = [
            Cord(100, 100),
            Cord(80, 100),
            Cord(60, 100),
        ]

        # Цветовая гамма
        self.color: str = CONFIG.get()["snake"]["color"]
        self.head_color: str = CONFIG.get()["snake"]["head_color"]

    def rebuild(self) -> None:
        self.config()
    
    # Движение
    def move(self) -> bool:
        # Забираем последнее движение
        self.direction = self.next_direction

        # Мы всегда двигаем голову, и последнюю ячейку хвоста
        head: Cord = self.tail[0]

        if self.direction == directions.UP:
            new_head: Cord = Cord(head.x, head.y - self.window.grid_size)
        elif self.direction == directions.DOWN:
            new_head: Cord = Cord(head.x, head.y + self.window.grid_size)
        elif self.direction == directions.LEFT:
            new_head: Cord = Cord(head.x - self.window.grid_size, head.y)
        elif self.direction == directions.RIGHT:
            new_head: Cord = Cord(head.x + self.window.grid_size, head.y)


        # Проверям валидность движения, если False, то мы проиграли
        if (new_head.x < 0 or new_head.x >= self.window.width or
            new_head.y < 0 or new_head.y >= self.window.height or
            new_head in self.tail):
            return False

        # Добавляем голову
        self.tail.insert(0, new_head)

        # Проверяем, съели ли мы еду
        ate_food = False
        for food in self.window.game.food_storage:
            if food.is_eaten(new_head):
                ate_food = True
                self.window.game.remove_food(food)
                self.window.game.create_food(is_init = False)
                break


        # Если не съели еду, то убираем один хвост
        if not ate_food:
            self.tail.pop()

        return True

    # Смена направления
    def change_direction(self, direction: str) -> None:
        # Проверка валидности смены направления
        if (direction == directions.UP and self.direction != directions.DOWN or
            direction == directions.DOWN and self.direction != directions.UP or
            direction == directions.LEFT and self.direction != directions.RIGHT or
            direction == directions.RIGHT and self.direction != directions.LEFT):
            self.next_direction = direction

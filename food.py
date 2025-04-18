# Класс еды
from config import CONFIG
from cord import Cord

class Food:
    def __init__(self, cord) -> None:
        # Координата
        self.cord: Cord = cord
        # Цветовая гамма
        self.color: str = CONFIG.get()["food"]["color"]

    # Проверка съеденности
    def is_eaten(self, cord: Cord) -> bool:
        return cord == self.cord

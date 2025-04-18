# Координата, для предотвращения костылей и удоства
class Cord:
    # Конструктор объекта
    def __init__(self, x, y) -> None:
        self.x: int = x
        self.y: int = y

    # Определяем базовые методы
    def __eq__(self, cord) -> bool:
        return self.x == cord.x and self.y == cord.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Cord({self.x}, {self.y})"

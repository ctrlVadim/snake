# main.py
from config import CONFIG
from game import Game

# Запускаем код
if __name__ == "__main__":
    CONFIG.load()
    Game()

import yaml

# Загрузка настроек
class LazyConfig:
    _config = None

    # Загрузка
    @classmethod
    def load(cls, path="settings.yaml"):
        with open(path, "r") as f:
            cls._config = yaml.safe_load(f)

    # Геттер
    @classmethod
    def get(cls):
        if cls._config is None:
            raise Exception("Ошибка загрузки...")
        return cls._config

# Для удобства закидываем в константу
CONFIG = LazyConfig

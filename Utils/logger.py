import os
import logging
from datetime import datetime

class Logger:
    def __init__(self, test_name: str):
        # Создание директории logs/
        logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
        os.makedirs(logs_dir, exist_ok=True)

        # Уникальное имя лог-файла
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"{test_name}_{timestamp}.log"
        log_path = os.path.join(logs_dir, log_filename)

        # Создание уникального логгера с именем теста
        self.logger = logging.getLogger(test_name)
        self.logger.setLevel(logging.INFO)

        # Предотвращаем повторное добавление обработчиков
        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
            stream_handler = logging.StreamHandler()

            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

        # Отключаем всплытие логов к root-логгеру (иначе дублируются)
        self.logger.propagate = False

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

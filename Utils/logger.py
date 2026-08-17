import logging
import os
from datetime import datetime
from typing import Any


class Logger:
    """Per-test logger that writes both to the console and to ``logs/``."""

    def __init__(self, test_name: str) -> None:
        logs_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "logs")
        )
        os.makedirs(logs_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        log_filename = f"{test_name}_{timestamp}.log"
        log_path = os.path.join(logs_dir, log_filename)

        self.logger = logging.getLogger(f"brainygo.{test_name}.{timestamp}")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        stream_handler = logging.StreamHandler()

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def info(self, message: Any) -> None:
        self.logger.info(message)

    def warning(self, message: Any) -> None:
        self.logger.warning(message)

    def error(self, message: Any) -> None:
        self.logger.error(message)

    def debug(self, message: Any) -> None:
        self.logger.debug(message)

    def close(self) -> None:
        """Flush and close all handlers created for this test."""
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

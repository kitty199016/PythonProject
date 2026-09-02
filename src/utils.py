import json
import logging
import os
from typing import Any, Dict, List

# Определение корня проекта
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(CURRENT_DIR, "..", "logs")

# Автоматически создаем папку logs в корне, если её нет
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOGS_DIR, "transactions.log")

# Конфигурация логирования
logging.basicConfig(
    level=logging.DEBUG,
    # Формат: Время - Имя модуля - Уровень - Сообщение
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # Перезапись файла при каждом запуске приложения
    filemode="w",
    filename=LOG_FILE_PATH,
    encoding="utf-8",
)

logger = logging.getLogger(__name__)


def transaction(file_path: str = "../data/operations.json") -> List[Dict[str, Any]]:
    """Принимает путь к файлу и возвращает список словарей с транзакциями из JSON-файла.

    Если файл пустой, содержит некорректный JSON или не существует,
    функция возвращает пустой список.
    """
    # Проверяем, существует ли файл и не пустой ли он
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        logger.warning(
            f"Файл не найден или пуст: {file_path}"
        )  # Логируем причину возврата
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Проверяем, что корневой элемент JSON является списком
            if isinstance(data, list):
                logger.info(
                    f"Данные успешно прочитаны из {file_path}. Найдено транзакций: {len(data)}"
                )
                return data
            else:
                logger.error(
                    f"Неверный формат структуры JSON в {file_path}: ожидался список"
                )
    except (json.JSONDecodeError, PermissionError) as e:
        # Логируем конкретную ошибку (декодирования или прав доступа)
        logger.error(f"Ошибка при обработке файла {file_path}: {e}")
        return []

    return []


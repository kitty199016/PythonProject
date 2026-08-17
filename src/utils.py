import json
import os
from typing import Any, Dict, List

def transaction(file_path: str = "../data/operations.json") -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из JSON-файла.

    Возвращает список словарей. Если файл пустой, содержит не список
    или не найден, возвращает пустой список.
    """
    # Проверяем, существует ли файл и не пустой ли он на уровне системы
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Проверяем, что верхнеуровневый элемент является списком
            if isinstance(data, list):
                return data
    except (json.JSONDecodeError, PermissionError):
        # Возвращаем пустой список при ошибках чтения или парсинга JSON
        return []

    return []

data = transaction()
print(data)
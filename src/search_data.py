import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Фильтрует список банковских операций по строке поиска в описании."""
    if not search:
        return data

    filtered_data = []
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    for operation in data:
        description = operation.get("description")
        if isinstance(description, str):
            if pattern.search(description):
                filtered_data.append(operation)

    return filtered_data


def count_operations_by_counter(operations: list, categories: list) -> dict:
    """
    Подсчитывает количество банковских операций для заданных категорий.
    Использует Counter для оптимизации подсчета по полю description.
    """
    # Собираем все значения description из списка транзакций
    # Метод .get() защищает от ошибки, если поля description где-то не окажется
    descriptions = [op.get('description') for op in operations]

    # Подсчитываем количество упоминаний каждого описания одной операцией
    counts = Counter(descriptions)

    # Формируем итоговый словарь строго по списку запрашиваемых категорий
    return {category: counts[category] for category in categories}

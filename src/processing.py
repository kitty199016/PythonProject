from datetime import datetime


def filter_by_state(cards: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция принимает список словарей и опционально значение
    для ключа state (по умолчанию 'EXECUTED').
    :cards - входные данные(список словарей)
    :state - сортировка по статусу
    return - новый список словарей"""
    result = [i for i in cards if i.get("state") == state]
    return result


def sort_by_date(raw_data: list[dict], is_direction: bool = True) -> list[dict]:
    """Сортирует список транзакций по ISO-дате.

    Выбрасывает ValueError, если формат нарушен, или KeyError, если ключа нет.
    """
    validated_data = [(datetime.fromisoformat(item["date"].strip()), item) for item in raw_data]

    validated_data.sort(key=lambda pair: pair[0], reverse=is_direction)

    return [item for _, item in validated_data]

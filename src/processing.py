def filter_by_state(cards: list[dict], state: str = 'EXECUTED') -> list[dict]:
     """Функция принимает список словарей и опционально значение
     для ключа state (по умолчанию 'EXECUTED').
     :cards - входные данные(список словарей)
     :state - сортировка по статусу
     return - новый список словарей"""
     result = [i for i in cards if i['state'] == state]
     return result


def sort_by_date(data_input:list[dict], directions: bool = True) -> list[dict]:
     """Функция сортирует словари по дате
     :data_input -входные данные(список словарей)
     :directions - параметр сортировки
     :return - отсортированнфй список словарей
     """
     data_sort = sorted(data_input, key=lambda x: x["date"], reverse = directions)
     return data_sort

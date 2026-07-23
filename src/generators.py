from typing import Iterator, Generator, Any



def filter_by_currency(transactions:dict, currency_code:str) -> Iterator:
    """
    Возвращает итератор с транзакциями, фильтруя их по заданному коду валюты.
    """
    for transaction in transactions:
        amount_info = transaction.get("operationAmount", {})
        currency_info = amount_info.get("currency", {})

        if currency_info.get("code") == currency_code:
            yield transaction

def transaction_descriptions(transactions:dict) -> Generator[Any, Any, None]:
    """
    Генератор, который по очереди возвращает описание (description) каждой транзакции.
    """
    for transaction in transactions:
        yield transaction.get('description')
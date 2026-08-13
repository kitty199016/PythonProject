from typing import Any, Generator, Iterator


def filter_by_currency(transactions: dict, currency_code: str) -> Iterator:
    """
    Возвращает итератор с транзакциями, фильтруя их по заданному коду валюты.
    """
    for transaction in transactions:
        amount_info = transaction.get("operationAmount", {})
        currency_info = amount_info.get("currency", {})

        if currency_info.get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: dict) -> Generator[Any, Any, None]:
    """
    Генератор, который по очереди возвращает описание (description) каждой транзакции.
    """
    for transaction in transactions:
        yield transaction.get('description')


def card_number_generator(start, end):
    """
    Генератор, который выдает номера карт в формате XXXX XXXX XXXX XXXX
    в диапазоне от start до end включительно.
    """
    for number in range(start, end + 1):
        card_str = f"{number:016d}"

        formatted_card = f"{card_str[0:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"

        yield formatted_card

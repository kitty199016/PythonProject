import pytest
from generators import transaction_descriptions
from types import GeneratorType


def test_empty_transactions_list():
    """Проверка работы функции с пустым списком транзакций."""
    empty_list = []

    # Генератор должен сразу завершиться, не вернув значений
    result = list(transaction_descriptions(empty_list))

    assert result == []


def test_single_transaction():
    """Проверка работы функции с одной транзакцией."""
    single_transaction = [{'id': 1, 'description': 'Перевод организации'}]

    result = list(transaction_descriptions(single_transaction))

    assert result == ['Перевод организации']


def test_multiple_transactions():
    """Проверка работы функции с несколькими транзакциями."""
    transactions = [
        {'id': 1, 'description': 'Перевод организации'},
        {'id': 2, 'description': 'Оплата мобильной связи'},
        {'id': 3, 'description': 'Покупка в магазине'}
    ]
    expected_descriptions = [
        'Перевод организации',
        'Оплата мобильной связи',
        'Покупка в магазине'
    ]

    result = list(transaction_descriptions(transactions))

    assert result == expected_descriptions


@pytest.mark.parametrize(
    "transaction_input, expected_output",
    [
        # Случай, когда ключ 'description' отсутствует
        ([{'id': 1, 'amount': 100}], [None]),
        # Случай, когда значение 'description' пустое или имеет другой тип
        ([{'id': 2, 'description': ''}], ['']),
        # Комбинированный случай
        ([{'description': 'Успешно'}, {}], ['Успешно', None])
    ]
)
def test_missing_or_empty_description(transaction_input, expected_output):
    """Проверка устойчивости функции, если описания нет или оно пустое."""
    result = list(transaction_descriptions(transaction_input))
    assert result == expected_output








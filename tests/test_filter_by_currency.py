from collections.abc import Iterator

import pytest

from src.generators import filter_by_currency


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "operationAmount": {"currency": {"code": "USD", "name": "USD"}}
        },
        {
            "id": 2,
            "operationAmount": {"currency": {"code": "EUR", "name": "EUR"}}
        },
        {
            "id": 3,
            "operationAmount": {"currency": {"code": "USD", "name": "USD"}}
        },
        {
            "id": 4,
            "operationAmount": {}  # Отсутствует currency
        },
        {
            "id": 5,
            # Полностью отсутствует operationAmount
        }
    ]


def test_filter_returns_iterator(sample_transactions):
    """Проверка, что функция действительно возвращает генератор/итератор."""
    result = filter_by_currency(sample_transactions, "USD")
    assert isinstance(result, Iterator)


def test_filter_by_currency_success(sample_transactions):
    """Проверка корректной фильтрации по заданной валюте."""
    result = list(filter_by_currency(sample_transactions, "USD"))

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_currency_not_found(sample_transactions):
    """Проверка случая, когда транзакции в заданной валюте отсутствуют."""
    result = list(filter_by_currency(sample_transactions, "RUB"))

    assert result == []  # Возвращается пустой список


def test_filter_empty_list():
    """Проверка, что генератор не падает при обработке пустого списка."""
    result = list(filter_by_currency([], "USD"))

    assert result == []


def test_filter_missing_amount_keys(sample_transactions):
    """Проверка, что генератор игнорирует транзакции с битой структурой и не падает."""
    # Транзакции 4 и 5 имеют неполную структуру, но не должны вызывать AttributeError
    result = list(filter_by_currency(sample_transactions, "EUR"))

    assert len(result) == 1
    assert result[0]["id"] == 2

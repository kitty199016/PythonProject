import pytest
from search_data import process_bank_search


@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными банковских операций."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата услуг: Мобильная связь"},
        {"id": 3, "description": "Перевод частному лицу"},
        {"id": 4, "description": None},
        {"id": 5, "amount": 100},
    ]


def test_search_successful(sample_data):
    """Тест стандартного успешного поиска (регистронезависимого)."""
    result = process_bank_search(sample_data, "перевод")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_search_case_insensitivity(sample_data):
    """Тест независимости от регистра (верхний/смешанный регистр)."""
    result = process_bank_search(sample_data, "МОБИЛЬНАЯ")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_search_empty_string(sample_data):
    """Тест с пустой строкой поиска (должен вернуть все данные)."""
    result = process_bank_search(sample_data, "")
    assert result == sample_data


def test_search_no_matches(sample_data):
    """Тест, когда совпадений не найдено."""
    result = process_bank_search(sample_data, "Покупка продуктов")
    assert result == []


def test_search_special_characters(sample_data):
    """Тест корректной обработки спецсимволов регулярных выражений."""
    custom_data = [{"id": 6, "description": "Оплата услуг: Сбербанк (ПАО)"}]
    result = process_bank_search(custom_data, "(ПАО)")
    assert len(result) == 1
    assert result[0]["id"] == 6


def test_search_empty_data():
    """Тест передачи пустого списка операций."""
    result = process_bank_search([], "перевод")
    assert result == []

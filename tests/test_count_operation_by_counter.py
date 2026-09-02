from collections import Counter
import pytest

from search_data import count_operations_by_counter

@pytest.fixture
def base_operations():
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод organizations"},
        {"id": 4, "description": "Перевод организации"},
        {"id": 5, "description": "Пополнение счета"},
    ]


def test_standard_counting(base_operations):
    """Проверка правильности подсчета для стандартного случая."""
    categories = ["Перевод организации", "Открытие вклада", "Кредит"]
    expected = {
        "Перевод организации": 2,
        "Открытие вклада": 1,
        "Кредит": 0,  # Категории нет в данных — должен быть 0
    }
    assert count_operations_by_counter(base_operations, categories) == expected


def test_missing_description_field():
    """Проверка устойчивости функции к отсутствию ключа description в словаре."""
    corrupted_operations = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "amount": 1000},  # Ключ description отсутствует
        {"id": 3, "description": None},  # Ключ равен None
    ]
    categories = ["Перевод организации", "Пополнение счета"]
    expected = {"Перевод организации": 1, "Пополнение счета": 0}
    assert (
        count_operations_by_counter(corrupted_operations, categories)
        == expected
    )


# Параметризованный тест для граничных случаев с пустыми списками
@pytest.mark.parametrize(
    "operations, categories, expected",
    [
        # Пустые транзакции, но есть категории
        ([], ["Открытие вклада"], {"Открытие вклада": 0}),
        # Есть транзакции, но список искомых категорий пуст
        ([{"description": "Вклад"}], [], {}),
        # Оба списка пустые
        ([], [], {}),
    ],
)
def test_empty_inputs(operations, categories, expected):
    """Проверка поведения функции при пустых входных списках."""
    assert count_operations_by_counter(operations, categories) == expected

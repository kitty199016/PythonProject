import pytest

from src.generators import card_number_generator


def test_generator_values_in_range():
    """Проверяет, что сгенерированные числа точно соответствуют диапазону."""
    start, end = 1000, 1005
    result = list(card_number_generator(start, end))

    extracted_numbers = [int(card.replace(" ", "")) for card in result]
    expected_numbers = list(range(start, end + 1))

    assert extracted_numbers == expected_numbers


def test_card_number_format():
    """Проверяет маску XXXX XXXX XXXX XXXX (длина, блоки, пробелы)."""
    start, end = 1, 3
    for card in card_number_generator(start, end):
        # Строка должна быть ровно 19 символов (16 цифр + 3 пробела)
        assert len(card) == 19

        blocks = card.split(" ")
        assert len(blocks) == 4

        for block in blocks:
            assert len(block) == 4
            assert block.isdigit()


@pytest.mark.parametrize("start, end", [
    (0, 0),  # Диапазон из одного нулевого элемента
    (9999999999999995, 9999999999999999),  # Максимальная граница для 16 знаков
    (0, 3),  # Старт с абсолютного нуля
])
def test_generator_boundary_values(start, end):
    """Проверяет корректность работы на границах разрядности."""
    result = list(card_number_generator(start, end))

    # Проверка количества выданных карт
    assert len(result) == (end - start + 1)

    # Проверка первого и последнего значения в выборке
    assert int(result[0].replace(" ", "")) == start
    assert int(result[-1].replace(" ", "")) == end


def test_generator_termination_and_empty_range():
    """Проверяет, что генератор пуст, если start > end."""
    start, end = 50, 10
    result = list(card_number_generator(start, end))

    assert len(result) == 0


def test_generator_is_exhausted():
    """Проверяет выброс StopIteration после выдачи всех элементов."""
    gen = card_number_generator(1, 2)

    next(gen)  # Должен выдать "0000 0000 0000 0001"
    next(gen)  # Должен выдать "0000 0000 0000 0002"

    # Третий вызов обязан завершить генератор
    with pytest.raises(StopIteration):
        next(gen)

from unittest.mock import mock_open, patch

from table_utils import read_csv


def test_read_csv_success():
    """Тест успешного чтения корректного CSV-файла."""
    csv_data = "id,amount,currency\n1,100,RUB\n2,250,USD"

    with patch("builtins.open", mock_open(read_data=csv_data)):
        result = read_csv("dummy_path.csv")

    expected = [
        {"id": "1", "amount": "100", "currency": "RUB"},
        {"id": "2", "amount": "250", "currency": "USD"},
    ]
    assert result == expected


def test_read_csv_file_not_found(capsys):
    """Тест обработки ошибки, если CSV-файл не найден."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_csv("missing.csv")

    assert result == []
    # Проверяем, что в консоль вывелась ошибка
    captured = capsys.readouterr()
    assert "Ошибка: Файл по пути 'missing.csv' не найден." in captured.out


def test_read_csv_generic_exception(capsys):
    """Тест обработки непредвиденной ошибки при чтении CSV."""
    with patch("builtins.open", side_effect=RuntimeError("Какая-то ошибка")):
        result = read_csv("error.csv")

    assert result == []
    captured = capsys.readouterr()
    assert "Произошла ошибка при чтении файла" in captured.out

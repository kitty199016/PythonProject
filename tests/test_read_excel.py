import pytest
import pandas as pd
from table_utils import read_excel


@pytest.fixture
def valid_excel_file(tmp_path):
    """Фикстура, создающая корректный Excel-файл для тестов."""
    file_path = tmp_path / "transactions.xlsx"
    data = [
        {"date": "2026-08-23", "category": "Супермаркеты", "amount": -1500},
        {"date": "2026-08-24", "category": "Зарплата", "amount": 55000},
    ]
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    return str(file_path), data


@pytest.fixture
def empty_excel_file(tmp_path):
    """Фикстура, создающая пустой Excel-файл (только заголовки)."""
    file_path = tmp_path / "empty.xlsx"
    df = pd.DataFrame(columns=["date", "category", "amount"])
    df.to_excel(file_path, index=False)
    return str(file_path)


def test_read_excel_success(valid_excel_file):
    """Тест успешного чтения корректного файла."""
    file_path, expected_data = valid_excel_file

    result = read_excel(file_path)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["category"] == "Супермаркеты"
    assert result[1]["amount"] == 55000


def test_read_excel_file_not_found():
    """Тест поведения функции, если файл отсутствует."""
    non_existent_path = "this_file_does_not_exist.xlsx"

    result = read_excel(non_existent_path)

    assert isinstance(result, list)
    assert len(result) == 0


def test_read_excel_empty_file(empty_excel_file):
    """Тест чтения файла, в котором нет строк с данными (только шапка)."""
    result = read_excel(empty_excel_file)

    assert isinstance(result, list)
    assert len(result) == 0


def test_read_excel_corrupted_file(tmp_path):
    """Тест обработки ситуации, когда файл поврежден или имеет неверный формат."""
    corrupted_path = tmp_path / "corrupted.xlsx"

    # Создаем обычный текстовый файл, но с расширением .xlsx
    with open(corrupted_path, "w", encoding="utf-8") as f:
        f.write("Это не настоящий Excel файл")

    result = read_excel(str(corrupted_path))

    assert isinstance(result, list)
    assert len(result) == 0

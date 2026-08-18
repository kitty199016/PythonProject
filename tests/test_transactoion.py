import json
import pytest
from utils import transaction  # Замените your_module на имя вашего файла с функцией


def test_transaction_success(tmp_path):
    """Тест успешного чтения корректного JSON-файла."""
    data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    file = tmp_path / "operations.json"
    file.write_text(json.dumps(data), encoding="utf-8")

    assert transaction(str(file)) == data


def test_transaction_file_not_found():
    """Тест ситуации, когда файла не существует."""
    assert transaction("non_existent_file.json") == []


def test_transaction_empty_file(tmp_path):
    """Тест ситуации, когда файл существует, но он пустой (размер 0)."""
    file = tmp_path / "empty.json"
    file.write_text("")  # Создаем пустой файл

    assert transaction(str(file)) == []
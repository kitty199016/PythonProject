from unittest.mock import patch
import pytest
from src.main import main


@pytest.fixture
def mock_dependencies():
    """Фикстура для изоляции тестирования интерфейса от файлов и сети."""
    test_data = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-12-08T22:46:21.931776",
            "description": "Открытие вклада",
            "operationAmount": {"amount": "40542", "currency": {"name": "руб.", "code": "RUB"}},
            "to": "Счет 4321432143214321"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2019-11-12T11:54:10.514333",
            "description": "Перевод с карты на карту",
            "operationAmount": {"amount": "130", "currency": {"name": "USD", "code": "USD"}},
            "from": "MasterCard 7771272737273727",
            "to": "Visa Platinum 1293383892039203"
        },
        {
            "id": 3,
            "state": "CANCELED",
            "date": "2018-07-18T10:14:11.839012",
            "description": "Перевод организации",
            "operationAmount": {"amount": "8390", "currency": {"name": "руб.", "code": "RUB"}},
            "from": "Visa Platinum 7492656572027202",
            "to": "Счет 00000000000000000034"
        }
    ]

    with patch("src.main.read_json", return_value=test_data) as mock_json, \
            patch("src.main.read_csv", return_value=test_data) as mock_csv, \
            patch("src.main.read_excel", return_value=test_data) as mock_excel, \
            patch("src.main.get_transaction_amount_in_rub", return_value=9100.0) as mock_api:
        yield {
            "json": mock_json,
            "csv": mock_csv,
            "excel": mock_excel,
            "api": mock_api,
        }


def test_main_full_flow_success(monkeypatch, capsys, mock_dependencies):
    """
    Тестирует успешный сценарий:
    Выбор JSON -> Фильтр EXECUTED -> Сортировка по убыванию -> Конвертировать в рубли -> Поиск -> Вывод.
    """
    inputs = [
        "1",  # 1. Выбрать JSON-файл
        "EXECUTED",  # 2. Статус операции
        "да",  # 3. Сортировать по дате?
        "по убыванию",  # Сортировать по убыванию
        "да",  # 4. Выводить только рублевые? (активирует get_transaction_amount_in_rub)
        "да",  # 5. Отфильтровать по слову в описании?
        "Перевод"  # Слово для поиска в описании
    ]

    input_generator = (i for i in inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_generator))

    main()

    captured = capsys.readouterr().out

    mock_dependencies["json"].assert_called_once()
    mock_dependencies["api"].assert_called()

    assert "Для обработки выбран JSON-файл." in captured
    assert "Операции отфильтрованы по статусу \"EXECUTED\"" in captured
    assert "Всего банковских операций в выборке: 1" in captured
    assert "12.11.2019 Перевод с карты на карту" in captured
    assert "MasterCard 7771 27** **** 3727 -> Visa Platinum 1293 38** **** 9203" in captured
    assert "Сумма: 9100.0 руб." in captured


def test_main_invalid_status_retry(monkeypatch, capsys, mock_dependencies):
    """Тестирует обработку неверного статуса со второй попытки ввода."""
    inputs = [
        "2",  # 1. Выбрать CSV-файл
        "test",  # 2. Неверный статус (программа должна повторить запрос)
        "CANCELED",  # Корректный статус со второй попытки
        "нет",  # 3. Сортировать по дате? Нет
        "нет",  # 4. Выводить только рублевые? Нет
        "нет"  # 5. Фильтровать по описанию? Нет
    ]

    input_generator = (i for i in inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_generator))

    main()

    captured = capsys.readouterr().out

    mock_dependencies["csv"].assert_called_once()
    # Проверяем строку с верхним регистром TEST, как выводит программа в main.py
    assert 'Статус операции "TEST" недоступен.' in captured
    assert 'Операции отфильтрованы по статусу "CANCELED"' in captured
    assert "Всего банковских операций в выборке: 1" in captured
    assert "18.07.2018 Перевод организации" in captured


def test_main_empty_result(monkeypatch, capsys, mock_dependencies):
    """Тестирует вывод сообщения, если выборка по фильтрам оказалась пустой."""
    inputs = [
        "3",  # 1. Выбрать XLSX-файл
        "PENDING",  # 2. Статус PENDING (в моках такого статуса нет)
        "нет",  # 3. Сортировать по дате? Нет
        "нет",  # 4. Выводить только рублевые? Нет
        "нет"  # 5. Фильтровать по описанию? Нет
    ]

    input_generator = (i for i in inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_generator))

    main()

    captured = capsys.readouterr().out

    mock_dependencies["excel"].assert_called_once()
    assert "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации" in captured

from unittest.mock import Mock

import pytest
import requests

from external_api import get_transaction_amount_in_rub  # Замените на ваше имя модуля

# --- 1. Тесты для успешных сценариев (Happy Paths) ---


def test_get_transaction_amount_in_rub_success():
    """Проверка работы, если валюта уже RUB (API не должно вызываться)."""
    transaction = {
        "operationAmount": {
            "amount": "1500.50",
            "currency": {"code": "RUB"}
        }
    }
    result = get_transaction_amount_in_rub(transaction)
    assert result == 1500.50


def test_get_transaction_amount_usd_success(mocker):
    """Успешная конвертация USD в RUB через mock-ответ API."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }

    # Мокаем requests.request
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 7500.0}
    mock_request = mocker.patch("requests.request", return_value=mock_response)

    result = get_transaction_amount_in_rub(transaction)

    assert result == 7500.0

    # Проверяем, что запрос ушел на правильный URL.
    # Используем mocker.ANY для apikey, так как он берется из вашего .env
    mock_request.assert_called_once_with(
        "GET",
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100.0",
        headers={"apikey": mocker.ANY},
        data={}
    )


# --- 2. Тесты на обработку ошибок структуры данных ---

def test_missing_operation_amount():
    """Ошибка, если в транзакции нет operationAmount."""
    transaction = {}
    # Проверяем только тип ошибки, чтобы избежать проблем с кодировкой строк
    with pytest.raises(ValueError):
        get_transaction_amount_in_rub(transaction)


def test_unsupported_currency():
    """Ошибка, если валюта не входит в список RUB, USD, EUR (например, GBP)."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "GBP"}
        }
    }
    with pytest.raises(ValueError):
        get_transaction_amount_in_rub(transaction)


# --- 3. Тесты на обработку ошибок API и Сети ---

def test_api_returns_success_false(mocker):
    """Ошибка, если API ответил 200, но внутри success: False."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "EUR"}
        }
    }

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": False,
        "error": {"info": "Invalid API Key"}
    }
    mocker.patch("requests.request", return_value=mock_response)

    with pytest.raises(Exception):
        get_transaction_amount_in_rub(transaction)


def test_api_http_error(mocker):
    """Ошибка, если API вернул плохой HTTP статус (например, 401 Unauthorized)."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Client Error")
    mocker.patch("requests.request", return_value=mock_response)

    with pytest.raises(ConnectionError):
        get_transaction_amount_in_rub(transaction)


def test_network_connection_error(mocker):
    """Ошибка, если пропал интернет (разрыв соединения)."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }

    mocker.patch("requests.request", side_effect=requests.exceptions.ConnectionError("Timeout"))

    with pytest.raises(ConnectionError):
        get_transaction_amount_in_rub(transaction)

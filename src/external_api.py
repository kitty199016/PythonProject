import os
import requests
from typing import Dict, Any

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY", "7gvRsOeJkOYDhbYXibHoRUeLsRBQVAcS")


def get_transaction_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Принимает транзакцию, конвертирует сумму в рубли (float) с использованием Exchange Rates Data API,
    если валюта операции — USD или EUR. Если валюта RUB, возвращает сумму без запросов к API.
    """
    # 1. Извлекаем сумму и валюту из словаря транзакции
    to_currency = "RUB"
    operation_amount: Dict[str, Any] = transaction.get("operationAmount", None)
    if operation_amount:
        amount = float(operation_amount.get("amount", 0.0))
        currency_db = operation_amount.get("currency", {})
        currency = currency_db.get("code", "RUB")
    else:
        raise ValueError("Неправильная структура данных")
    # 2. Если транзакция уже в рублях, возвращаем сумму сразу
    if currency == "RUB":
        return amount

    # 3. Если транзакция в USD или EUR, делаем запрос к внешнему API
    if currency in ["USD", "EUR"]:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={currency}&amount={amount}"
        headers = {"apikey": API_KEY}
        payload = {}
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            response.raise_for_status()  # Вызовет ошибку, если HTTP-статус не 200

            data = response.json()

            if data.get("success"):
                return float(data["result"])
            else:
                error_msg = data.get("error", {}).get("info", "Неизвестная ошибка API")
                raise Exception(f"Ошибка API: {error_msg}")

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка сети при обращении к API курсов валют: {e}")

    # 4. Если передана любая другая валюта, кроме RUB, USD, EUR
    raise ValueError(f"Неподдерживаемая валюта транзакции: {currency}")

a =   {
    "id": 207126257,
    "state": "EXECUTED",
    "date": "2019-07-15T11:47:40.496961",
    "operationAmount": {
      "amount": "92688.46",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Открытие вклада",
    "to": "Счет 35737585785074382265"
  }

print(get_transaction_amount_in_rub(a))
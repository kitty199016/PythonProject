import os
import requests

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY", "7gvRsOeJkOYDhbYXibHoRUeLsRBQVAcS")
BASE_URL = "https://api.apilayer.com/exchangerates_data"


def convert_to_rub(amount: float, currency: str) -> float:
    """
    Конвертирует указанную сумму из USD или EUR в RUB с помощью Exchange Rates Data API.
    """
    currency = currency.upper()

    # Если валюта уже рубли, конвертация не требуется
    if currency == "RUB":
        return float(amount)

    if currency not in ["USD", "EUR"]:
        raise ValueError(f"Неподдерживаемая валюта для конвертации: {currency}")

    # Настройка заголовков для авторизации в API
    headers = {
        "apikey": API_KEY
    }

    # Параметры запроса для эндпоинта конвертации
    params = {
        "from": currency,
        "to": "RUB",
        "amount": amount
    }

    try:
        response = requests.get(f"{BASE_URL}/convert", headers=headers, params=params)
        response.raise_for_status()  # Генерирует исключение при HTTP-ошибках

        data = response.json()

        if data.get("success"):
            return float(data["result"])
        else:
            raise Exception(f"Ошибка API: {data.get('error', {}).get('info', 'Неизвестная ошибка')}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к Exchange Rates Data API: {e}")
        raise
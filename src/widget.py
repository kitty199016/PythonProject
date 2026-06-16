from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(text: str) -> str | None:  # функция обрабатывает информацию о картах и счетах
    if "Счет" in text:
        for index, char in enumerate(text):
            if char.isdigit():
                cipher = get_mask_account(int(text[index - 1 :]))
                return text[:index] + str(cipher)
        return None
    else:
        for index, char in enumerate(text):
            if char.isdigit():
                cipher = get_mask_card_number(int(text[index - 1 :]))
                return text[:index] + str(cipher)
        return None


def get_date(iso_string: str) -> str:  # функция перевода даты в формат дд.мм.гггг
    dt_obj = datetime.fromisoformat(iso_string)
    formatted_date_only = dt_obj.date().strftime("%d.%m.%Y")
    return formatted_date_only

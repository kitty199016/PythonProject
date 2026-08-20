import logging
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(CURRENT_DIR, "..", "logs")

# Автоматически создаем папку logs в корне проекта, если её нет
os.makedirs(LOGS_DIR, exist_ok=True)

# Инициализация конфигурации логирования
logging.basicConfig(
    level=logging.INFO,
    # Формат: Метка времени - Название модуля - Уровень серьезности - Сообщение
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # Перезапись файла при каждом запуске приложения
    filemode="w",
    filename=os.path.join(LOGS_DIR, "masks.log"),
    encoding="utf-8",
)

logger = logging.getLogger(__name__)


def get_mask_card_number(number_card_input: int) -> str:
    """Функция маскирования номера карты по маске.

    Visa Platinum 7000792289606361  # Входной аргумент
    Visa Platinum 7000 79** **** 6361  # Вывод функции
    """
    number_card = str(number_card_input)
    if number_card.isdigit() and len(number_card) >= 12:
        number_card_code = (
            number_card[0:6] + ("*" * (len(number_card) - 10)) + number_card[-4:]
        )
        result = " ".join(
            number_card_code[i : i + 4] for i in range(0, len(number_card_code), 4)
        )
        logger.info(f"Успешно замаскирован номер карты длины {len(number_card)}")
        return result
    else:
        logger.error(
            f"Ошибка маскирования карты: передан некорректный номер ({number_card_input})"
        )
        raise ValueError("Некорректный номер карты")


def get_mask_account(account_number_input: int) -> str:
    """Функция маскирования номера счета по маске."""
    account_number = str(account_number_input)
    if account_number.isdigit() and len(account_number) > 0:
        account_number_code = "**" + account_number[-4:]
        logger.info(f"Успешно замаскирован номер счета длины {len(account_number)}")
        return account_number_code
    else:
        logger.error(
            f"Ошибка маскирования счета: передан некорректный номер ({account_number_input})"
        )
        raise ValueError("Некорректный номер счета")
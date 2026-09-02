import os
from src.table_utils import read_csv, read_excel
from src.utils import transaction as read_json
from src.processing import filter_by_state, sort_by_date
from src.search_data import process_bank_search
from src.external_api import get_transaction_amount_in_rub
from src.widget import mask_account_card, get_date


def _normalize_transaction_structure(op: dict) -> dict:
    """
    Приводит плоские словари из CSV/Excel к единому формату вложенного JSON.
    Это необходимо, чтобы функции генераторов и API курсов валют не падали.
    """
    if not op or "operationAmount" in op:
        return op

    amount = op.get("amount", "0")
    currency_code = op.get("currency_code", "RUB")
    currency_name = op.get("currency_name", "руб.")

    normalized = {
        "id": op.get("id"),
        "state": op.get("state"),
        "date": op.get("date"),
        "operationAmount": {
            "amount": amount,
            "currency": {
                "name": currency_name,
                "code": currency_code
            }
        },
        "description": op.get("description"),
        "from": op.get("from"),
        "to": op.get("to")
    }
    return {k: v for k, v in normalized.items() if v is not None}


def main() -> None:
    """
    Основная функция, отвечающая за логику интерфейса пользователя
    и связывающая функциональности всех модулей проекта между собой.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла\n")

    raw_data = []

    # Пути к файлам внутри папки data
    json_path = os.path.join("data", "operations.json")
    csv_path = os.path.join("data", "transactions.csv")
    xlsx_path = os.path.join("data", "transactions_excel.xlsx")

    # 1. Шаг выбора и чтения файла с диска
    while True:
        choice = input("Пользователь: ").strip()
        if choice == "1":
            print("\nПрограмма: Для обработки выбран JSON-файл.")
            raw_data = read_json(json_path)
            break
        elif choice == "2":
            print("\nПрограмма: Для обработки выбран CSV-файл.")
            raw_data = read_csv(csv_path)
            break
        elif choice == "3":
            print("\nПрограмма: Для обработки выбран XLSX-файл.")
            raw_data = read_excel(xlsx_path)
            break
        else:
            print("Программа: Неверный пункт меню. Пожалуйста, введите 1, 2 или 3.")

    # Приводим все считанные данные к общему вложенному формату
    data = [_normalize_transaction_structure(item) for item in raw_data if item]

    # 2. Шаг фильтрации по статусу (с приведением к единому регистру)
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n")
        status_input = input("Пользователь: ").strip().upper()

        if status_input in valid_statuses:
            print(f'\nПрограмма: Операции отфильтрованы по статусу "{status_input}"')
            data = filter_by_state(data, state=status_input)
            break
        else:
            print(f'\nПрограмма: Статус операции "{status_input}" недоступен.')

    # 3. Шаг сортировки по дате операции
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет\n")
    sort_date_choice = input("Пользователь: ").strip().lower()

    if sort_date_choice == "да":
        print("\nПрограмма: Отсортировать по возрастанию или по убыванию?\n")
        sort_order = input("Пользователь: ").strip().lower()

        # Если во вводе пользователя содержится корень "убыва", ставим True (от новых к старым)
        is_reverse = True if "убыван" in sort_order else False
        data = sort_by_date(data, is_direction=is_reverse)

    # 4. Шаг обработки валют (используем get_transaction_amount_in_rub для конвертации)
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет\n")
    rub_choice = input("Пользователь: ").strip().lower()

    if rub_choice == "да":
        converted_data = []
        for op in data:
            try:
                # Получаем сумму в рублях через ваше внешнее API курсов валют
                rub_amount = get_transaction_amount_in_rub(op)

                # Обновляем поля транзакции, переводя её в рубли
                op["operationAmount"]["amount"] = str(round(rub_amount, 2))
                op["operationAmount"]["currency"]["name"] = "руб."
                op["operationAmount"]["currency"]["code"] = "RUB"
                converted_data.append(op)
            except Exception:
                # Если сбой сети или ключа API, оставляем оригинальную транзакцию в списке
                converted_data.append(op)
        data = converted_data

    # 5. Шаг текстового поиска по подстроке в поле 'description'
    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n")
    desc_choice = input("Пользователь: ").strip().lower()

    if desc_choice == "да":
        search_word = input("\nПользователь (введите слово): ").strip()
        data = process_bank_search(data, search_word)

    # 6. Шаг вывода отформатированных результатов на экран
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not data:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа:\nВсего банковских операций в выборке: {len(data)}\n")

    for op in data:
        # Форматируем дату (ДД.ММ.ГГГГ) через widget.py
        try:
            formatted_date = get_date(op.get("date", ""))
        except ValueError:
            formatted_date = "00.00.0000"

        # Безопасно маскируем отправителя ('from') через widget.py
        from_raw = op.get("from", "")
        from_info = ""
        if from_raw and str(from_raw).strip():
            try:
                from_info = f"{mask_account_card(str(from_raw))} -> "
            except ValueError:
                from_info = f"{from_raw} -> "

        # Безопасно маскируем получателя ('to') через widget.py
        to_raw = op.get("to", "")
        try:
            to_info = mask_account_card(str(to_raw)) if to_raw else "Не указан"
        except ValueError:
            to_info = str(to_raw)

        # Извлекаем сумму и валюту из вложенной структуры
        amount_block = op.get("operationAmount", {})
        amount = amount_block.get("amount", "0")
        currency_block = amount_block.get("currency", {})
        currency_name = currency_block.get("name", "руб.")

        # Печать итоговой карточки операции строго по шаблону ТЗ
        print(f"{formatted_date} {op.get('description', 'Без описания')}")
        print(f"{from_info}{to_info}")
        print(f"Сумма: {amount} {currency_name}\n")


if __name__ == "__main__":
    main()

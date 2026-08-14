def get_mask_card_number(number_card_input: int) -> str:
    '''функция редактирует номер карты по маске
    Visa Platinum 7000792289606361  # входной аргумент
    Visa Platinum 7000 79** **** 6361  # выход функции'''

    number_card = str(number_card_input)
    if number_card.isdigit() and len(number_card) >= 12:
        number_card_code = number_card[0:6] + ("*" * (len(number_card) - 10)) + number_card[-4:]
        result = ' '.join(number_card_code[i:i + 4] for i in range(0, len(number_card_code), 4))
        return result
    else:
        raise ValueError("Некорректный номер карты")


def get_mask_account(account_number_input: int) -> str:  # функция редактирует номер счета по маске
    account_number = str(account_number_input)
    if account_number.isdigit() and len(account_number) > 0:
        account_number_code = "**" + account_number[-4:]
        return account_number_code
    else:
        raise ValueError("Некорректный номер счета")

def get_mask_card_number(number_card_input: int) -> str:  # функция редактирует номер карты по маске
    number_card = str(number_card_input)
    if len(number_card) != 16:
        raise ValueError("Номер не верный")
    else:
        number_card_code = number_card[0:4] + " " + number_card[4:6] + "** **** " + number_card[12:]
        return number_card_code


def get_mask_account(account_number_input: int) -> str:  # функция редактирует номер счета по маске
    account_number = str(account_number_input)
    account_number_code = "**" + account_number[-4:]
    return account_number_code

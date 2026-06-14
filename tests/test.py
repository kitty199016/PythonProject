from sys import exec_prefix

from src.masks import get_mask_account, get_mask_card_number
number_correct = 1234567891223356
number_uncorrected = 1234567891223

assert get_mask_card_number(number_correct) == "1234 56** **** 3356"
assert get_mask_account(number_correct) == "**3356"


try:
    get_mask_card_number(number_uncorrected)
    raise AssertionError("Тест провален")
except ValueError:
    pass
except:
    raise AssertionError("Тест провален")
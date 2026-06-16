from masks import get_mask_account

from masks import get_mask_card_number

def mask_account_card(text:str) -> str | None:
    if "Счет" in text:
        for index, char in enumerate(text):
            if char.isdigit():
                cipher = get_mask_account(int(text[index-1:]))
                return text[:index] + str(cipher)
        return None
    else:
        for index, char in enumerate(text):
            if char.isdigit():
                cipher = get_mask_card_number(int(text[index-1:]))
                return text[:index] + str(cipher)
        return None



a = mask_account_card("Visa Platinum 7000792289606361")
print(a)
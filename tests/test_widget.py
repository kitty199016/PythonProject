
from src.widget import mask_account_card, get_date

import pytest

cases_mask_account_card = [("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
         ("Счет 73654108430135874305", "Счет **4305")]
cases_mask_account_card_negative = [("3333333"), (""), ("fff43432")]


@pytest.mark.parametrize("text, result", cases_mask_account_card)
def test_get_mask_account_card_positive(text: str, result: str) -> None:
    assert mask_account_card(text) == result


@pytest.mark.parametrize("text", cases_mask_account_card_negative)
def test_get_mask_account_card_negative(text: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(text)

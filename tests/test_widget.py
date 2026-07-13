
from src.widget import mask_account_card, get_date

import pytest

from datetime import datetime

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

cases_get_date = [("2024-03-11T02:26:18.671407", "11.03.2024")]
cases_get_date_negative =[("Дата: 01.01.2021"),("32/13/2021")]

@pytest.mark.parametrize("iso_string, result", cases_get_date)
def test_get_date_positive(iso_string:str, result:str) -> None:
    assert get_date(iso_string) == result

@pytest.mark.parametrize("iso_string", cases_get_date_negative)
def test_get_date_negative(iso_string:str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(iso_string)
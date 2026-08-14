import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def card_positive_cases() -> list[tuple[int, str]]:
    return [
        (1111111111111111, "1111 11** **** 1111"),
        (222222222222, "2222 22** 2222"),
    ]


@pytest.fixture
def card_negative_value_cases() -> list[tuple[str | int]]:
    return [
        (3333333,),
        ("fff43432",),
    ]


@pytest.fixture
def card_negative_type_cases() -> list[tuple[str]]:
    return [
        ("",),
    ]


def test_get_mask_card_number_positive(card_positive_cases: list[tuple[int, str]]) -> None:
    for number_card_input, result in card_positive_cases:
        assert get_mask_card_number(number_card_input) == result


def test_get_mask_card_number_negative_value(card_negative_value_cases: list[tuple[str | int]]) -> None:
    for (invalid_input,) in card_negative_value_cases:
        with pytest.raises(ValueError):
            get_mask_card_number(invalid_input)


cases_account = [(123456789, "**6789"), (73654108430135874305, "**4305")]
cases_account_negative = [(), ("fe4545432", )]


@pytest.mark.parametrize("account_number_input, result", cases_account)
def test_get_mask_account_positive(account_number_input: int, result: str) -> None:
    assert get_mask_account(account_number_input) == result


@pytest.mark.parametrize("account_number_input", cases_account_negative)
def test_gget_mask_account_negative(account_number_input: int) -> None:
    with pytest.raises(ValueError):
        get_mask_account(account_number_input)

import pytest
from src.processing import filter_by_state, sort_by_date

cases_filter_by_state = [
    (
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
        ],
        'CANCELED',
        [
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
        ]
    ),
    (
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
        ],
        'EXECUTED',
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
        ]
    ),
    (
        [
            {'id': 41428829, 'state': 'CANCELED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'CANCELED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
        ],
        'EXECUTED',
        []
    )
]

cases_filter_by_state_negative = [
    (
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED"},  # Ключа "date" нет
        ],
        KeyError,
    ),
    (
        [
            {"id": 41428829, "state": "EXECUTED", "date": "12.09.2018"},  # Ошибка формата
        ],
        ValueError,
    ),
    (
        [
            {"id": 41428829, "state": "EXECUTED", "date": 20190703},  # Число упадет на .strip()
        ],
        AttributeError,
    ),
    (
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-02-31T12:00:00"},  # 31 февраля нет
        ],
        ValueError,
    ),
]


@pytest.mark.parametrize("cards, state, result", cases_filter_by_state)
def test_filter_by_state_positive(cards: list[dict], state: str, result: list[dict]) -> None:
    assert filter_by_state(cards, state) == result


cases_sort_by_date = [
    (
        [
            {"id": 41428829, "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "date": "2018-10-14T08:21:33.419441"},
        ],
        True,
        [
            {"id": 41428829, "date": "2019-07-03T18:35:29.512364"},
            {"id": 615064591, "date": "2018-10-14T08:21:33.419441"},
            {"id": 594226727, "date": "2018-09-12T21:27:25.241689"},
            {"id": 939719570, "date": "2018-06-30T02:08:58.425572"},
        ],
    ),
    (
        [
            {"id": 41428829, "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "date": "2018-10-14T08:21:33.419441"},
        ],
        False,
        [
            {"id": 939719570, "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "date": "2018-10-14T08:21:33.419441"},
            {"id": 41428829, "date": "2019-07-03T18:35:29.512364"},
        ],
    ),
    ([], True, []),
]


@pytest.mark.parametrize("raw_data, is_direction, result", cases_sort_by_date)
def test_sort_by_date_positive(
    raw_data: list[dict], is_direction: bool, result: list[dict]
) -> None:
    assert sort_by_date(raw_data, is_direction) == result


@pytest.mark.parametrize("invalid_data, expected_exception", cases_filter_by_state_negative)
def test_sort_by_date_negative(invalid_data: list[dict], expected_exception) -> None:
    with pytest.raises(expected_exception):
        sort_by_date(invalid_data)

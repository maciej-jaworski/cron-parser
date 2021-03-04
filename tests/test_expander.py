from parser import InvalidCRON, expand_time_component

import pytest


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("*", list(range(0, 60))),
        ("*/15", [0, 15, 30, 45]),
        ("1-5", list(range(1, 6))),
        ("1,5", [1, 5]),
        ("1,6,10", [1, 6, 10]),
        ("1-10/2", list(range(1, 10, 2))),
    ],
)
def test_expand_expressions(input_str, expected):

    assert expand_time_component(input_str, 59, 0) == expected


@pytest.mark.parametrize(
    "input_str",
    (
        "ASD",
        "**",
        "0-70",
        "65-70",
        "1,15,40,70",
        "-",
        ",",
        "1-5/6",
        "0/5",
    ),
)
def test_invalid_expressions(input_str):
    with pytest.raises(InvalidCRON):
        expand_time_component(input_str, 59, 0)

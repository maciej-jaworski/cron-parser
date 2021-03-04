from parser import InvalidCRON, format_cron

import pytest


@pytest.mark.parametrize(
    "test_str",
    (
        "*/15 0 1,15",
        "70 0 1,15 * 1-5",
        "*/15 0 0/5 * 1-5",
        "*/15 0 -/5 * 1-5",
    ),
)
def test_invalid_crons(test_str):

    with pytest.raises(InvalidCRON):
        format_cron(test_str)


def test_valid_cron1():
    assert (
        format_cron("23 0-20/2 * * * cat /dev/null")
        == """minute        23
hour          0 2 4 6 8 10 12 14 16 18 20
day of month  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5 6 7
command       cat /dev/null"""
    )


def test_valid_cron2():
    assert (
        format_cron("*/15 0 1,15 * 1-5 /usr/bin/find")
        == """minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find"""
    )


def test_valid_cron3():
    assert (
        format_cron("0 0,12 1 */2 * python manage.py send_notifications")
        == """minute        0
hour          0 12
day of month  1
month         1 3 5 7 9 11
day of week   1 2 3 4 5 6 7
command       python manage.py send_notifications"""
    )

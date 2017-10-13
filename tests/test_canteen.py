import datetime
import re

import pytest

from canteens import canteen


@pytest.mark.freeze_time('2017-09-28')
def test_get_current_week():
    expected_range = [
        datetime.date(2017, 9, 25),
        datetime.date(2017, 9, 26),
        datetime.date(2017, 9, 27),
        datetime.date(2017, 9, 28),
        datetime.date(2017, 9, 29),
        datetime.date(2017, 9, 30),
        datetime.date(2017, 10, 1)
    ]
    current_week = canteen.get_current_week()
    assert current_week == expected_range


@pytest.mark.freeze_time('2017-09-28')
def test_next_week():
    expected_range = [
        datetime.date(2017, 10, 2),
        datetime.date(2017, 10, 3),
        datetime.date(2017, 10, 4),
        datetime.date(2017, 10, 5),
        datetime.date(2017, 10, 6),
        datetime.date(2017, 10, 7),
        datetime.date(2017, 10, 8)
    ]
    next_week = canteen.get_next_week()
    assert next_week == expected_range


@pytest.mark.freeze_time('2017-09-28')
def test_get_week_range():
    expected_range = [
        datetime.date(2017, 9, 25),
        datetime.date(2017, 9, 26),
        datetime.date(2017, 9, 27),
        datetime.date(2017, 9, 28),
        datetime.date(2017, 9, 29),
        datetime.date(2017, 9, 30),
        datetime.date(2017, 10, 1)
    ]
    week_range = canteen.get_week_range(datetime.date(2017, 10, 1))
    assert week_range == expected_range


@pytest.mark.parametrize('count', range(100))
def test_get_useragent__with_100_random_useragents(count):
    pattern = re.compile('.+/.+\(.+')
    agent = canteen.get_useragent()
    assert pattern.match(agent) is not None

import os.path
import pytest
from emoji import emojize
from flaky import flaky

import datetime

from canteens import studierendenwerk


@pytest.fixture
def studierendenwerk_sample() -> str:
    path = os.path.join(os.path.dirname(__file__), 'studierendenwerk_sample.html')
    with open(path) as file:
        return file.read()


@flaky
def test_download_menu__with_live_site():
    date = datetime.datetime.today().strftime(studierendenwerk.DATE_FORMAT_API)
    html = studierendenwerk.download_menu(538, date)
    assert 'Milch und Milchprodukte' in html


def test_parse_sample_menu(studierendenwerk_sample: str):
    parsed = studierendenwerk.parse_menu(studierendenwerk_sample)
    assert parsed == emojize('*Group 1*\n'
                             ':fish: Group 1 Item 1: *1,75€*\n'
                             '\n*Group 2*\n'
                             ':seedling: Group 2 Item 1: *1,75€*\n'
                             ':seedling: Group 2 Item 2: *0,65€*\n'
                             '\n*Group 3*\n'
                             ':seedling: Group 3 Item 1: *0,60€*\n'
                             '\n*Group 4*\n'
                             ':seedling: Group 4 Item 1: *1,90€*\n'
                             ':poultry_leg: Group 4 Item 2: *1,75€*\n'
                             ':poultry_leg: Group 4 Item 3: *1,35€*\n'
                             '\n*Group 5*\n'
                             ':seedling: Group 5 Item 1: *0,60€*\n'
                             ':seedling: Group 5 Item 2: *0,60€*\n'
                             ':seedling: Group 5 Item 3: *0,60€*\n'
                             '\n*Group 6*\n'
                             ':ear_of_corn: Group 6 Item 1: *0,65€*')

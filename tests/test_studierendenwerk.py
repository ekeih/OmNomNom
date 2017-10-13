import pytest
from flaky import flaky

import datetime

from canteens import studierendenwerk

@flaky
def test_download_menu__with_live_site():
    date = datetime.datetime.today().strftime(studierendenwerk.DATE_FORMAT_API)
    html = studierendenwerk.download_menu(538, date)
    assert 'Milch und Milchprodukte' in html

import pytest

from frontend import frontend


@pytest.mark.freeze_time('2017-09-28')
@pytest.mark.parametrize('test_input, canteen,date', [
    ('/tu_marchstr morgen', 'tu_marchstr', '2017-09-29'),
    ('/fu_2', 'fu_2', '2017-09-28'),
    ('/fu_veggie next monday', 'fu_veggie', '2017-10-02'),
    ('/tu_mensa today', 'tu_mensa', '2017-09-28'),
    ('/tu_ackerstr foobar', 'tu_ackerstr', False)
])
def test_get_canteen_and_date(test_input, canteen, date):
    canteen_result, date_result = frontend.get_canteen_and_date(test_input)
    assert canteen_result == canteen
    assert date_result == date

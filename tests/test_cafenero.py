import magic
import pytest
import requests
import requests_mock
from flaky import flaky

from canteens import cafenero


@flaky
def test_download_website_with_live_site():
    html = cafenero.download_website()
    if '<iframe src="https://www.dropbox.com' in html:
        assert True
    else:
        assert False


def test_download_website__with_connect_timeout():
    with requests_mock.Mocker() as m:
        with pytest.raises(requests.exceptions.ConnectTimeout):
            m.get(requests_mock.ANY, exc=requests.exceptions.ConnectTimeout)
            cafenero.download_website()


def test_extract_dropbox_link():
    html = '<html>\r\n\t<title>Café Nero Speisen</title>\r\n</html>\r\n<body>\r\n\t<iframe ' \
           'src="https://www.dropbox.com/s/swkhko9vwkwlgn0/speisekarte.pdf?raw=1" border="0" width="100%" ' \
           'height="2000px" />\r\n\t</body>\r\n</html>\r\n'
    expected_link = 'https://www.dropbox.com/s/swkhko9vwkwlgn0/speisekarte.pdf?raw=1'
    link = cafenero.extract_dropbox_link(html)
    assert link == expected_link


@flaky
def test_get_pdf():
    html = cafenero.download_website()
    link = cafenero.extract_dropbox_link(html)
    tmpdir_of_pdf = cafenero.get_pdf(link)
    filetype = magic.from_file('%s/cafenero.pdf' % tmpdir_of_pdf, mime=True)
    assert filetype == 'application/pdf'


def test_get_pdf__with_connect_timeout():
    with requests_mock.Mocker() as m:
        with pytest.raises(requests.exceptions.ConnectTimeout):
            m.get(requests_mock.ANY, exc=requests.exceptions.ConnectTimeout)
            html = cafenero.download_website()
            link = cafenero.extract_dropbox_link(html)
            cafenero.get_pdf(link)

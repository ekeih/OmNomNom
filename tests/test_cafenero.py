import magic
import pytest
import requests
import requests_mock
from flaky import flaky

from canteens import cafenero
from canteens.canteen import FISH, MEAT, VEGAN, VEGGIE


@pytest.fixture(scope='module')
def pdf_file():
    html = cafenero.download_website()
    link = cafenero.extract_dropbox_link(html)
    tmpdir_of_pdf = cafenero.get_pdf(link)
    return tmpdir_of_pdf


@flaky
def test_download_website__with_live_site():
    html = cafenero.download_website()
    assert 'Speisekarte als' in html


def test_download_website__with_connect_timeout():
    with requests_mock.Mocker() as m:
        with pytest.raises(requests.exceptions.ConnectTimeout):
            m.get(requests_mock.ANY, exc=requests.exceptions.ConnectTimeout)
            cafenero.download_website()


def test_extract_dropbox_link():
    html = cafenero.download_website()
    link = cafenero.extract_dropbox_link(html)
    assert 'dropbox' in link
    assert 'speisekarte.pdf' in link


@flaky
def test_get_pdf(pdf_file):
    filetype = magic.from_file('%s/cafenero.pdf' % pdf_file, mime=True)
    assert filetype == 'application/pdf'


def test_get_pdf__with_connect_timeout():
    with requests_mock.Mocker() as m:
        with pytest.raises(requests.exceptions.ConnectTimeout):
            m.get(requests_mock.ANY, exc=requests.exceptions.ConnectTimeout)
            html = cafenero.download_website()
            link = cafenero.extract_dropbox_link(html)
            cafenero.get_pdf(link)


@flaky
def test_pdf_to_text(pdf_file):
    menu = cafenero.pdf_to_text(pdf_file)
    assert menu != ''


def test_text_to_menu_list():
    text = 'cafeneroindervolkswagenuniversitätsbibliothekberlin\nmittagstisch – freitag den 06. oktober 2017 von ' \
           '12:00 bis 20:00 uhr\nkleine portion suppe 2,80 € --- kleine portion nudeln 3,60 €\n' \
           'pellkartoffeln mit hausgemachtem kräuterquark, leinoel und salat 4,40 €\n\n\nrussische ' \
           'gemüse-bortschtsch mit\ndill, schmand, lauchzwiebeln + biomehrkornbrot      3,80 €                  ' \
           '                          vegetarisch\n\n\n\nspaghetti bolognese\nmit frühlingszwiebeln + petersilie + ' \
           'parmesankäse     4,80 €                                                rindfleisch\n\n\n\nspaghetti mit ' \
           'tomaten,\nartischocken, lauchzwiebeln+ (parmesan)         4,80 €                          ' \
           'vegetarisch (vegan)\n\n\n\nspaghetti mit salbei-olivenoel und (parmesankäse)        4,80 €              ' \
           '                                vegetarisch (vegan)\n\n\n\nkartoffel-rosenkohl-quiche\nmit gorgonzola ' \
           'und gemischtem salat                               vegetarisch    6,00 €\nfilet vom schwarzen heilbutt ' \
           'mit chili-koriander-dip\nauf basmatireis mit zucchini-kirschtomaten-gemüse                              ' \
           '                                     fisch   6,50 €\n\x0c'

    expected_items = [
        'mittagstisch – freitag den 06. oktober 2017 von 12:00 bis 20:00 uhr',
        '\n',
        'kleine portion suppe 2,80€ vegetarisch',
        'kleine portion nudeln 3,60€ vegetarisch',
        'pellkartoffeln mit hausgemachtem kräuterquark, leinoel und salat 4,40€ vegetarisch',
        'russische gemüse-bortschtsch mit dill, schmand, lauchzwiebeln + biomehrkornbrot 3,80€ vegetarisch',
        'spaghetti bolognese mit frühlingszwiebeln + petersilie + parmesankäse 4,80€ rindfleisch',
        'spaghetti mit tomaten, artischocken, lauchzwiebeln+ (parmesan) 4,80€ vegetarisch (vegan)',
        'spaghetti mit salbei-olivenoel und (parmesankäse) 4,80€ vegetarisch (vegan)',
        'kartoffel-rosenkohl-quiche mit gorgonzola und gemischtem salat vegetarisch 6,00€',
        'filet vom schwarzen heilbutt mit chili-koriander-dip auf basmatireis mit zucchini-kirschtomaten-gemüse '
        'fisch 6,50€'
    ]

    menu = cafenero.text_to_menu_list(text)
    assert menu == expected_items


def test_annotate_menu():
    menu = [
        'mittagstisch – freitag den 06. oktober 2017 von 12:00 bis 20:00 uhr',
        '\n',
        'kleine portion suppe 2,80€ vegetarisch',
        'kleine portion nudeln 3,60€ vegetarisch',
        'pellkartoffeln mit hausgemachtem kräuterquark, leinoel und salat 4,40€ vegetarisch',
        'russische gemüse-bortschtsch mit dill, schmand, lauchzwiebeln + biomehrkornbrot 3,80€ vegetarisch',
        'spaghetti bolognese mit frühlingszwiebeln + petersilie + parmesankäse 4,80€ rindfleisch',
        'spaghetti mit tomaten, artischocken, lauchzwiebeln+ (parmesan) 4,80€ vegetarisch (vegan)',
        'spaghetti mit salbei-olivenoel und (parmesankäse) 4,80€ vegetarisch (vegan)',
        'kartoffel-rosenkohl-quiche mit gorgonzola und gemischtem salat vegetarisch 6,00€',
        'filet vom schwarzen heilbutt mit chili-koriander-dip auf basmatireis mit zucchini-kirschtomaten-gemüse '
        'fisch 6,50€'
    ]

    expected_annotations = 'mittagstisch – freitag den 06. oktober 2017 von 12:00 bis 20:00 uhr\n\n' \
                           '%s kleine portion suppe 2,80€\n' \
                           '%s kleine portion nudeln 3,60€\n' \
                           '%s pellkartoffeln mit hausgemachtem kräuterquark, leinoel und salat 4,40€\n' \
                           '%s russische gemüse-bortschtsch mit dill, schmand, lauchzwiebeln + biomehrkornbrot ' \
                           '3,80€\n' \
                           '%s spaghetti bolognese mit frühlingszwiebeln + petersilie + parmesankäse 4,80€\n' \
                           '%s spaghetti mit tomaten, artischocken, lauchzwiebeln+ (parmesan) 4,80€\n' \
                           '%s spaghetti mit salbei-olivenoel und (parmesankäse) 4,80€\n' \
                           '%s kartoffel-rosenkohl-quiche mit gorgonzola und gemischtem salat 6,00€\n' \
                           '%s filet vom schwarzen heilbutt mit chili-koriander-dip auf basmatireis mit ' \
                           'zucchini-kirschtomaten-gemüse 6,50€' % (VEGGIE, VEGGIE, VEGGIE, VEGGIE, MEAT, VEGAN, VEGAN, VEGGIE, FISH)

    annotated_menu = cafenero.annotate_menu(menu)
    assert annotated_menu == expected_annotations


@flaky
def test_main():
    menu = cafenero.main()
    assert 'mittagstisch' in menu

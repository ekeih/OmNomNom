"""
This parser tries to download the menu for the TU canteen Cafe Nero which is located in the Volkswagen Bibliothek in
Berlin. Apparently someone thought it would be a nice idea to upload the daily menu as a PDF document to Dropbox and
include it in the Wordpress website (http://cafenero.net) ... so we have to do some extra parsing to extract the
content of the PDF.
"""

import datetime
import subprocess
import tempfile

import bs4
import requests
from celery.utils.log import get_task_logger

from backend.backend import app, cache, cache_date_format, cache_ttl
from canteens.canteen import FISH, MEAT, VEGAN, VEGGIE

logger = get_task_logger(__name__)


def download_website():
    """
    Download the website of Cafe Nero and return the HTML source code.

    Returns:
        The full HTML source code as string.

    Raises:
        HTTPError: When the underlying requests library fails we also raise a HTTPError.
    """
    url = 'http://cafenero.net/speisen.html'
    request = requests.get(url)
    request.raise_for_status()
    return request.text


def extract_dropbox_link(html):
    """
    Parse the HTML code and return the Dropbox link to the menu.

    Args:
        html (str): The website as HTML that should contain the Dropbox link.

    Returns:
        The link as string.
    """
    soup = bs4.BeautifulSoup(html, 'html.parser')
    iframe = soup.find('iframe')
    return iframe.attrs['src']


def get_pdf(link):
    """
    Download the actual menu as PDF file and store it in $tmpdir/cafenero.pdf.

    Args:
        link (str): The link to the PDF file.

    Returns:
        The $tmpdir as string where the PDF is stored.

    Raises:
        HTTPError: When the underlying requests library fails we also raise a HTTPError.
    """
    request = requests.get(link)
    request.raise_for_status()
    tmpdir = tempfile.mkdtemp()
    pdfpath = '%s/cafenero.pdf' % tmpdir
    with open(pdfpath, 'wb') as f:
        f.write(request.content)
    return tmpdir


def pdf_to_text(tmpdir):
    """
    Use pdftotext to parse the PDF file to text.

    Args:
        tmpdir (str): Path to the $tmpdir that contains cafenero.pdf.

    Returns:
        The content of the PDF as string.
    """
    pdfpath = '%s/cafenero.pdf' % tmpdir
    txtpath = '%s/cafenero.txt' % tmpdir
    popen = subprocess.Popen(('pdftotext', '-layout', pdfpath), stdout=subprocess.PIPE)
    popen.wait()
    with open(txtpath, 'r') as f:
        menu = f.read()
    return menu


def clean_newlines(text):
    """
    Unfortunately it is not easy to detect reliable if a menu entry spans multiple lines. So this function does some
    parsing that should work in most cases. It tries to remove all unnecessary newlines and returns a list of strings
    with one item for every menu entry.

    Args:
        text (str): The text that has to be cleaned. Usually this is the output of pdftotext.

    Returns:
        A list of strings with one item for every menu entry.
    """
    cleaned_result = []
    for line in text.splitlines():
        if not line == '' and 'cafeneroinder' not in line:
            if 'mittagstisch' in line or '---' in line or 'schonkost' in line:
                line = '%s\n' % line
            else:
                if line.endswith(('€', 'vegetarisch', 'schweinefleisch', 'rindfleisch',
                                  'fisch', 'vegan', '(vegan)')):
                    line = '%s\n' % line
                else:
                    line = '%s ' % line
            cleaned_result.append(line)
    return cleaned_result


def annotate_menu(menu):
    """
    Detect if a menu entry is vegan, contains fish, etc. and adds an appropriate emoji to the menu.

    Args:
        menu (:obj:`list` of :obj:`str`): The complete menu as a list of strings. Each item should be one menu entry.

    Returns:
        One string containing the complete menu with all annotations.
    """
    result = ''
    for entry in menu:
        if 'mittagstisch' in entry or '---' in entry or 'schonkost' in entry:
            annotation = ''
        elif 'vegan' in entry:
            annotation = '%s ' % VEGAN
        elif 'vegetarisch' in entry:
            annotation = '%s ' % VEGGIE
        elif 'fisch' in entry:
            annotation = '%s ' % FISH
        else:
            annotation = '%s ' % MEAT
        entry = entry.replace('vegetarisch', '')
        entry = entry.replace('(vegan)', '')
        entry = entry.replace('fisch', '')
        entry = entry.replace('rindfleisch', '')
        entry = entry.replace('vegan', '')
        entry = entry.replace('schweinefleisch', '')
        entry = ' '.join(entry.split())
        result += '%s%s\n' % (annotation, entry)
    return result


def main():
    """
    Parse the menu.
    """
    html = download_website()
    link = extract_dropbox_link(html)
    tmpdir_of_pdf_file = get_pdf(link)
    text_of_pdf_menu = pdf_to_text(tmpdir_of_pdf_file)
    cleaned_text = clean_newlines(text_of_pdf_menu)
    return annotate_menu(cleaned_text)


@app.task(bind=True, default_retry_delay=30)
def update_cafenero(self):
    """
    Celery task to update cafenero.
    """
    try:
        logger.info('[Update] TU Cafenero')
        menu = main()
        if menu:
            cache.hset(datetime.date.today().strftime(cache_date_format), 'tu_cafenero', menu)
            cache.expire(datetime.date.today().strftime(cache_date_format), cache_ttl)
    except Exception as ex:
        raise self.retry(exc=ex)


if __name__ == '__main__':
    print(main())

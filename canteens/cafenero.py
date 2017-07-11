import bs4
import requests
import subprocess
import tempfile

from canteens.canteen import Canteen, VEGGIE, MEAT


def __parse_menu(url):

    def get_dropbox_link():
        request = requests.get('http://cafenero.net/speisen.html')
        if request.status_code == requests.codes.ok:
            soup = bs4.BeautifulSoup(request.text, 'html.parser')
            iframe = soup.find('iframe')
            return iframe.attrs['src']
        else:
            return False

    def get_pdf():
        dropbox_link = get_dropbox_link()
        if dropbox_link:
            request = requests.get(dropbox_link)
            if request.status_code == requests.codes.ok:
                tmpdir = tempfile.mkdtemp()
                pdfpath = '%s/cafenero.pdf' % tmpdir
                with open(pdfpath, 'wb') as f:
                    f.write(request.content)
                return tmpdir
            else:
                return False
        else:
            return False

    def pdf_to_text(tmpdir):
        pdfpath = '%s/cafenero.pdf' % tmpdir
        txtpath = '%s/cafenero.txt' % tmpdir
        popen = subprocess.Popen(('pdftotext', '-layout', pdfpath), stdout=subprocess.PIPE)
        popen.wait()
        with open(txtpath, 'r') as f:
            menu = f.read()
        return menu

    return pdf_to_text(get_pdf())

cafenero = Canteen(
    id_='tu_cafenero',
    name='Cafe Nero',
    url='',
    update=__parse_menu,
    website='http://cafenero.net'
)

CANTEENS = [cafenero]

if __name__ == '__main__':
    print(__parse_menu())

import ssl
import urllib.request
from bs4 import BeautifulSoup
import parsing.db.local_db_connect as db
from parsing.settings import TourModel

SITE_URL = 'http://volga-travel.ru/category/rechnye-kruizy/?product_orderby=price'


def get_html(url):
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    return response.read()


def _parse(url):
    soup = BeautifulSoup(url, 'html.parser')
    tours_block = soup.find('ul', class_='products row-fluid products-3')

    print(tours_block)


def parse_tour(tour_soup):
    tour = TourModel()
    tour.title = parse_title(tour_soup)
    tour.date = parse_date(tour_soup)
    tour.price = parse_price(tour_soup)
    #tour.time = parse_time(tour_soup)
    return tour


def parse_date(tour_soup, title, price):
    pass


def parse_title(tour_soup):
    pass


def parse_price(tour_soup):
    pass


def parse():
    return _parse(get_html(SITE_URL))


if __name__ == '__main__':
    db.migrate()
    parse()

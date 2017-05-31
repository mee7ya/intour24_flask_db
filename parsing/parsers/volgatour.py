import ssl
import urllib.request
from datetime import *
from bs4 import BeautifulSoup
import parsing.db.local_db_connect as db
from parsing.settings import TourModel

SITE_URL = 'http://www.volga-tour.ru/gruppovye-jekskursii.html'
HOME_URL = 'http://www.volga-tour.ru'


def get_html(url):
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    return response.read()


def _parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    tours = []
    for link in soup.findAll('a', {'class': 'clear'}):
        link_tour = HOME_URL + link['href']
        tours_soup = BeautifulSoup(get_html(link_tour), 'html.parser')
        tours.extend(parse_tours(tours_soup))
    return tours


def parse_tours(tours_soup):
    tours = []
    for tour_soup in tours_soup.find_all('table', {'border': '1', 'cellpadding': '1', 'cellspacing': '0',
                                                   'style': 'width: 90%;'}):
        tour = TourModel()
        tour.title = parse_title(tour_soup)
        tour.date = parse_date(tour_soup)
        tour.price = parse_price(tour_soup)
        tour.time = parse_time(tour_soup)
        tours.append(tour)
    return tours


def parse_title(tour_soup):
    # print(str(tour_soup.find('strong').text))
    return str(tour_soup.find('strong').text)


def parse_price(tour_soup):
    return ' '


def parse_date(tour):
    return ' '


def parse_time(tour):
    return ' '


def parse():
    return _parse(get_html(SITE_URL))


if __name__ == '__main__':
    db.migrate()
    parse()

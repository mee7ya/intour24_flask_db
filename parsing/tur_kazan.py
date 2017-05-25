import datetime
from bs4 import BeautifulSoup
import urllib.request
import ssl
import parsing.db_model as db
import re


# from postgre_connect import DBConnect as db

def make_url():
    start_date = datetime.datetime.today()
    end_date = start_date + datetime.timedelta(days=30)
    return 'https://tur-kazan.ru/excursions?daterange={}+to+{}' \
        .format(start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d'))


HOME_URL = make_url()


def get_html(url):
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    return response.read()


def _parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    for old_price in soup.find_all('span', class_="old_price"):
        old_price.extract()

    tours_soup = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['tr'])
    tours = []
    for tour_soup in tours_soup:
        tours.append(parse_tour(tour_soup))
    return tours


def parse_tour(tour_soup):
    tour = db.Tour()
    tour.title = parse_title(tour_soup)
    tour.date = parse_date(tour_soup)
    tour.price = parse_price(tour_soup)
    tour.time = parse_time(tour_soup)
    return tour


def parse_title(tour):
    return tour.find('div', class_='info-col td') \
        .find('div', class_='title clearfix') \
        .find('a') \
        .text


def parse_price(tour):
    return re.search('[\d]+', tour.find('div', class_='bold-col td') \
                     .find('span', class_='border-right') \
                     .text).group(0)


def parse_date(tour):
    return tour.find('div', class_='title clearfix') \
        .find('span', class_='date') \
        .text


def parse_time(tour):
    return tour.find_all('div', class_='bold-col td')[1] \
        .find('span', class_='border-right') \
        .text


def parse():
    return _parse(get_html(HOME_URL))


if __name__ == '__main__':
    db.migrate()
    # database = DBConnect('dbafp', 'user', 'pass')

    parse()

    # database.close()

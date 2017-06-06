import re
import ssl
import urllib.request
from bs4 import BeautifulSoup
import parsing.db.local_db_connect as db
from parsing.settings import TourModel
import codecs

SITE_URL = 'https://to-kazan.ru/%D0%B5%D0%B6%D0%B5%D0%B4%D0%BD%D0%B5%D0%B2%D0%BD%D1%8B%D0%B5-%D1%81%D0%B1%D0%BE%D1%80' \
           '%D0%BD%D1%8B%D0%B5-%D1%8D%D0%BA%D1%81%D0%BA%D1%83%D1%80%D1%81%D0%B8%D0%B8-%D0%BF%D0%BE-%D0%BA%D0%B0%D0%B7' \
           '%D0%B0/ '


def get_html(url):
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    return response.read()


def _parse(url):
    soup = BeautifulSoup(url, 'html.parser')
    tours_block = soup.find('div', class_='content')
    tours = []
    for item in tours_block.find_all('a', class_='cat_post'):
        tour_link = item.get('href')
        tours_soup = BeautifulSoup(get_html(tour_link), 'html.parser')
        tours.extend(parse_tour(tours_soup))
    return tours


def parse_tour(tours_soup):
    tours = []
    for tour_soup in tours_soup.find_all('div', class_='single_post'):
        tour = TourModel()
        tour.title = parse_title(tour_soup)
        tour.date = parse_dates(tour_soup)
        tour.price = parse_price(tour_soup)
        tour.time = parse_time(tour_soup)
        tour.description = parse_description(tour_soup)
        tours.append(tour)
    return tours


def parse_time(tour_soup):
    times_soup = tour_soup.find('div', class_='programm').find_all('p')
    if len(times_soup) < 2:
        return ''
    else:
        return times_soup[1].text


def parse_dates(tour_soup):
    dates = tour_soup.find('div', class_='programm').find('p')
    if dates is None:
        dates = ''
        dates_soup = tour_soup.find_all('td')
        for date in dates_soup:
            dates += date.text + ' '
    else:
        return dates.text

    if dates == '':
        dates = tour_soup.find('div', class_='text').find(['p', 'div']).text
    else:
        return dates
    return dates


def parse_title(tour_soup):
    title = tour_soup.find('div', class_='table').find('h1').text
    return title


def parse_price(tour_soup):
    prices_soup = tour_soup.find('div', class_='programm').find_all('p')
    if len(prices_soup) < 2:
        return ''
    elif prices_soup.text.find('Стоимость') == -1:
        return ''
    else:
        return prices_soup.text


def parse_description(tour_soup):
    return ''


def parse():
    return _parse(get_html(SITE_URL))


if __name__ == '__main__':
    db.migrate()
    parse()

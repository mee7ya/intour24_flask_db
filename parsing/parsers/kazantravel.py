import ssl
import urllib.request
from datetime import *
from re import split

from bs4 import BeautifulSoup

import parsing.db.local_db_connect as db
from parsing.settings import Models

SITE_URL = 'http://kazantravel.ru'
HOME_URL = 'http://kazantravel.ru/tours/'

DAY_THRESHOLD = 30


def get_html(url):
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    return response.read()


def _parse(url):
    soup = BeautifulSoup(url, 'html.parser')
    tours_block = soup.find('section', class_='tours-list')
    tours = []
    for item in tours_block.find_all('div', class_='tour-header'):
        link_tour = SITE_URL + item.a['href']
        tours.extend(parse_tour(get_html(link_tour)))
    return tours


def parse_tour(html):
    tour_soup = BeautifulSoup(html, 'html.parser')
    return parse_dates(tour_soup, parse_title(tour_soup), parse_price(tour_soup), parse_description(tour_soup))


def parse_title(tour_soup):
    return tour_soup.find('h3', class_="booking-tour-name").text


def parse_price(tour_soup):
    return tour_soup.find('span', class_='tour-price-value').text


def parse_dates(tour_soup, title, price, description):
    schedule_soup = tour_soup.find('dl', class_='dl dl-horizontal booking-tour-days')
    weekday_names = [weekday_num(day) for day in schedule_soup.find_all('dt')]
    weekday_params = schedule_soup.find_all('dd')
    tours = []
    if not len(weekday_names) == 0:
        for i in range(len(weekday_names)):
            times = weekday_params[i].find_all('b')
            periods = weekday_params[i].find_all('small')
            for j in range(len(periods)):
                day = datetime.today()
                last_day = datetime.today() + timedelta(days=DAY_THRESHOLD + 1)
                while day < last_day:
                    if day.weekday() == weekday_names[i] and day_in_period(day, periods[j].text):
                        tour = Models.Tour()
                        tour.title = title
                        tour.price = price
                        tour.description = description
                        tour.date = day.strftime('%d.%m')
                        tour.time = times[2 * j].text + '-' + times[2 * j + 1].text
                        tours.append(tour)
                    day += timedelta(days=1)
    return tours


def parse_description(tour_soup):
    descriptions = tour_soup.find('div', class_='col-xs-12 col-sm-7').find_all(['p', 'li'])
    if descriptions is None:
        return ''
    else:
        result = ''
        for description in descriptions:
            result += description.text + '\n'
        return result


def weekday_num(day):
    days = {
        'Понедельник': 0, "Вторник": 1, "Среда": 2, "Четверг": 3, "Пятница": 4, "Суббота": 5, "Воскресенье": 6
    }
    for day in days:
        return days[day]


def day_in_period(day, str_period):
    _, str_start_date, str_end_date, _ = split(r'[(]|[)]|[-]', str_period)
    start_date = datetime.strptime(str_start_date, '%d.%m.%Y')
    end_date = datetime.strptime(str_end_date, '%d.%m.%Y')
    if start_date <= day <= end_date:
        return True
    return False


def parse():
    return _parse(get_html(HOME_URL))


if __name__ == '__main__':
    # db.migrate()
    parse()

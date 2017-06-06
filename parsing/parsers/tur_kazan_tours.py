import re
import ssl
import urllib.request

from bs4 import BeautifulSoup
from parsing.settings import *
from datetime import *

SITE_URL = 'https://tur-kazan.ru'


def convert(time):
    if type(time) == str:
        temp = time.split(' ')
        size = len(temp)
        time_in_minutes = 0

        if temp[1][0] == 'ч':
            time_in_minutes += (int(temp[0])) * 60
        else:
            time_in_minutes += int(temp[0])

        if size == 4:
            time_in_minutes += int(temp[2])

        return time_in_minutes
    return -1


def get_weekday(s):
    days = {'жеднев': -1, 'уббот': 5, 'онедел': 0,
            'оскресен': 6, 'торник': 1, 'ред': 2,
            'етвер': 3, 'ятни': 4}
    for day in days.keys():
        if s.find(day) > 0:
            return days[day]
    return None


def get_times(s):
    times = list(re.findall(r'[\d]{1,2}[:][\d]{2}', s))
    if s.find('-') >= 0:
        times = [times[0]]
    timedeltas = []
    for time in times:
        split_pos = time.find(':')
        hours = int(time[:split_pos])
        minutes = int(time[split_pos + 1:])
        timedeltas.append(hours * 60 + minutes)
    return timedeltas


def get_html(url):
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    return response.read()


def _parse(url):
    soup = BeautifulSoup(url, 'html.parser')
    tours = []
    tours_block = soup.find('div', class_='tour-list-main clearfix')
    for item in tours_block.find_all('div', class_='item'):
        tour_link = SITE_URL + item.a['href']
        tour_link = tour_link.replace(' ', '%20')
        tours.append(parse_tour(get_html(tour_link)))
    return tours


def parse_tour(tours_soup):
    soup = BeautifulSoup(tours_soup, "html.parser")
    tour = Models.Tour()
    tour.price_id = Models.Price.get_price_id(parse_price(soup))
    tour.title = parse_title(soup)
    tour.duration = parse_duration(soup)
    tour.description = parse_description(soup)
    start_point = parse_start_point(soup)
    if start_point is not None:
        tour.start_point = Models.PickingPlace.get_place_id(start_point)
    else:
        tour.start_point = 8
    tour.save()

    for dates_info in parse_dates(soup):
        dates = Models.Dates()
        dates.start_date = dates_info[0]
        dates.repeat_interval = dates_info[1]
        dates.excursion_id = tour.id
        dates.save()

    return tour


def parse_title(soup):
    title = soup.find('div', class_='title-h1').text
    return title


def parse_dates(soup):
    dates = []
    paragraphs = soup.find('div', class_='description').find_all('p')
    for p in paragraphs:
        if p.text.count(':') > 1:
            dates.extend(parse_date(p.text))
    return dates


def parse_date(date_str):
    weekday = get_weekday(date_str)
    times = get_times(date_str)
    now = datetime.now(TZ)
    result = []
    for first_minutes in times:
        if weekday > -1:
            first_date = datetime(now.year, now.month, now.day, tzinfo=now.tzinfo) - timedelta(
                days=now.weekday()) + timedelta(days=weekday) + timedelta(minutes=first_minutes)

            if now.timestamp() >= first_date.timestamp():
                first_date += timedelta(weeks=1)
            result.append((first_date.timestamp(), MINS_IN_WEEK))

        else:
            first_date = datetime(now.year, now.month, now.day, tzinfo=now.tzinfo) + timedelta(minutes=first_minutes)

            if now.timestamp() >= first_date.timestamp():
                first_date += timedelta(days=1)
            result.append((first_date.timestamp(), MINS_IN_DAY))
    result_formatted = []
    for item in result:
        item_formatted = datetime.fromtimestamp(
            int(item[0])
        ).strftime('%Y-%m-%d %H:%M:%S')
        result_formatted.append((item_formatted, item[1]))
    return result_formatted


def parse_price(soup):
    price_text = ''
    price = soup.find('div', class_='description').find_all('p')
    for p in price:
        if p.text[0:9] == 'Стоимость':
            price_text = p.text
            break
    prices = [x.replace('.', '') for x in re.findall(r"[\d]+[.]*[\d]+", price_text)[0:2]]
    prices.extend('0')
    return prices


def parse_duration(soup):
    duration_text = ''
    duration = soup.find('div', class_='description').find_all('p')
    for p in duration:
        if p.text[0:17] == 'Продолжительность':
            duration_text = p.text.split(":")[1].strip()
            break
    duration_text = convert(duration_text)
    return duration_text


def parse_start_point(soup):
    point_text = ''
    start_point = soup.find('div', class_='description').find_all('p')
    for p in start_point:
        if p.text[0:16] == 'Место проведения' or p.text[0:11] == 'Пункт сбора':
            point_text = p.text
    point_text = point_text.rstrip()
    point_text = re.sub("\s\s+", " ", point_text)
    if ':' in point_text:
        return point_text.split(':')[1].strip(), '0'
    elif 'Пункт сбора на экскурсии' in point_text:
        return point_text.split('Пункт сбора на экскурсии')[1].strip(), '0'
    return point_text, '0'


def parse_description(soup):
    description_text = ''
    description = soup.find('div', class_='description').find_all('p')
    start_ind = -1
    for p in description:
        if p.text[0:16] == 'Место проведения' or p.text[0:11] == 'Пункт сбора':
            start_ind = description.index(p)
        elif p.text[0:9] == 'Стоимость':
            break
        elif start_ind != -1:
            description_text += p.text + " " + '\n'
    return description_text


def parse():
    return _parse(get_html(SITE_URL))


if __name__ == '__main__':
    parse()

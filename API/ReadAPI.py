import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import local_db as db
from settings import *

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Tour info').worksheet('Лист1 (копия)')

pp = pprint.PrettyPrinter()


# result = sheet.get_all_values()
# pp.pprint(result)


def parse_tour(tour_sheet):
    tour_sheet = sheet.get_all_values()
    tour = Models.Tour()
    tour.price_id = Models.Price.get_price_id(*parse_price(tour_sheet))
    tour.title = parse_title(tour_sheet)
    tour.duration = parse_duration(tour_sheet)
    tour.description = parse_description(tour_sheet)
    tour.photo = parse_photo(tour_sheet)
    start_point = parse_start_point(tour_sheet)
    if start_point is not None:
        tour.start_point = Models.PickingPlace.get_place_id(*start_point)
    else:
        tour.start_point = None
    tour.save()
    dates = Models.Dates()
    dates.start_date = parse_dates(tour_sheet)[1]
    dates.repeat_interval = parse_dates(tour_sheet)[0]
    dates.excursion_id = tour.id
    dates.save()
    return tour


def parse_photo(tour_sheet):
    for item in tour_sheet:
        if item[0] == "Экскурсия":
            return item[1]


def parse_dates(tour_sheet):
    date = []
    for item in tour_sheet:
        if item[0] == "Дата начала":
            date.append(item[1])
        if item[0] == "Время начала":
            date.append(item[1])
    return date


def parse_price(tour_sheet):
    price = []
    for item in tour_sheet:
        if item[0] == "Цена для взрослых":
            price.append(item[1])
        if item[0] == "Цена для детей (7-12 лет)":
            price.append(item[1])
        if item[0] == "Цена для детей (до 7 лет)":
            price.append(item[1])
    return price


def parse_title(tour_sheet):
    for item in tour_sheet:
        if item[0] == "Название экскурсии":
            return item[1]


def parse_duration(tour_sheet):
    for item in tour_sheet:
        if item[0] == "Продолжительность":
            return item[1]


def parse_description(tour_sheet):
    for item in tour_sheet:
        if item[0] == "Описание экскурсии":
            return item[1]


def parse_start_point(tour_sheet):
    point = []
    for item in tour_sheet:
        if item[0] == "Описание":
            point.append(item[1])
        if item[0] == "Адрес ":  # Don't delete the space
            point.append(item[1])
    return point


def parse():
    return parse_tour(sheet)


if __name__ == '__main__':
    db.migrate()
    parse()

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import local_db as db
from datetime import *
from settings import *

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Tour info').worksheet('Свияжск и Раифа')

pp = pprint.PrettyPrinter()


def parse_excursion(_sheet):
    excursion_sheet = _sheet.get_all_values()
    excursion = Models.Excursion()
    excursion.price_id = Models.Price.get_price_id(*parse_price(excursion_sheet))
    excursion.name = parse_title(excursion_sheet)
    excursion.description = parse_description(excursion_sheet)
    excursion.duration = parse_duration(excursion_sheet)
    start_point = parse_start_point(excursion_sheet)
    if start_point is not None:
        excursion.start_point = Models.PickingPlace.get_place_id(start_point)
    else:
        excursion.start_point = None
    excursion.save()

    parse_schedules(excursion_sheet, excursion.id)
    parse_sight(excursion_sheet)
    parse_excursion_property(excursion_sheet)
    return excursion


def parse_schedules(excursion_sheet, excursion_id):
    for item in excursion_sheet:
        if item[0][:7] == 'Вариант' and item[3] != '':
            schedule = Models.Schedule()

            schedule.start_date = datetime.strptime(item[1], DATE_FORMAT).strftime(DATE_TZ_FORMAT)
            schedule.end_date = datetime.strptime(item[2], DATE_FORMAT).strftime(DATE_TZ_FORMAT)
            schedule.repeat_day, schedule.repeat_week, schedule.repeat_weekday, schedule.repeat_month \
                = parse_repeat_intervals(item[3], item[4])
            schedule.excursion = excursion_id
            schedule.save()


def parse_price(excursion_sheet):
    price = []
    for item in excursion_sheet:
        if item[0] == "Взрослый":
            adult = round(float(item[1].replace(",", ".")))
            price.append(adult)
        if item[0] == 'Школьный':
            children = round(float(item[1].replace(",", ".")))
            price.append(children)
    return price


def parse_title(excursion_sheet):
    for item in excursion_sheet:
        if item[0] == "Название":
            return item[1]


def parse_description(excursion_sheet):
    for item in excursion_sheet:
        if item[0] == "Описание":
            return item[1]


def parse_start_point(excursion_sheet):
    for item in excursion_sheet:
        if item[0] == "Адрес встречи":
            return item[1]


def parse_repeat_intervals(regularity, day_of_week):
    repeat_weekday = '0'
    repeat_day = '0'
    repeat_week = '0'
    repeat_month = '0'

    if regularity == 'Ежедневно':
        repeat_day = '1'
    elif regularity == 'Еженедельно':
        days = {'Суббота': '5', 'Понедельник': '0',
                'Воскресенье': '6', 'Вторник': '1', 'Среда': '2',
                'Четверг': '3', 'Пятница': '4'}
        repeat_week = '1'
        repeat_weekday = days[day_of_week]
    elif regularity == 'Через неделю':
        repeat_week = '1'
    elif regularity == 'Ежемесячно':
        repeat_month = '1'

    return repeat_day, repeat_week, repeat_weekday, repeat_month


def parse_sight(excursion_sheet):
    for item in excursion_sheet:
        if item[0][:5] == 'Пункт':
            sight = Models.Sight()
            sight.name = item[1]
            sight.image = ''
            sight.save()


def parse_excursion_property(excursion_sheet):
    for item in excursion_sheet:
        if item[0][:1] == '№' and item[1] != '':
            excursionpr = Models.ExcursionProperty()
            excursionpr.name = item[1]
            excursionpr.image = ''
            excursionpr.save()


def parse_duration(excursion_sheet):
    for item in excursion_sheet:
        if item[0][:7] == 'Вариант' and item[7] != '':
            dur = [int(x) for x in item[7].split(':')]
            return 60 * dur[0] + dur[1]


def parse():
    return parse_excursion(sheet)


if __name__ == '__main__':
    db.migrate()
    parse()

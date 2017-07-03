#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from datetime import *
from API.settings import *

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

pp = pprint.PrettyPrinter()

DEFAULT_LINK = 'https://docs.google.com/spreadsheets/d/1KS0ZMaNtgTeH73mxMd5NXNZYKanOnmij9cNlsPfrlIw'

def parse_excursion(excursion_sheet):
    excursion = Models.Excursion()
    excursion.price = Models.Price.get_price_id(*parse_price(excursion_sheet))
    excursion.name = parse_title(excursion_sheet)
    excursion.description = parse_description(excursion_sheet)
    excursion.duration = parse_duration(excursion_sheet)
    start_point = parse_start_point(excursion_sheet)
    if start_point is not None:
        excursion.picking_place = Models.PickingPlace.get_place_id(start_point)
    else:
        excursion.picking_place = None
    excursion.save()

    parse_schedules(excursion_sheet, excursion.id)
    parse_sight(excursion_sheet, excursion.id)
    parse_excursion_property(excursion_sheet, excursion.id)
    return excursion


def parse_schedules(excursion_sheet, excursion_id):
    for item in excursion_sheet:
        if item[0][:7] == 'Вариант' and item[3] != '':
            schedule = Models.Schedule()

            schedule.start_date = datetime.strptime(item[1], DATE_FORMAT).strftime(DATE_DB_FORMAT)
            schedule.start_time = datetime.strptime(item[5], TIME_FORMAT).strftime(TIME_DB_FORMAT)
            if item[3] != 'Единожды' and item[3] != "Ежемесячно":
                schedule.end_date = datetime.strptime(item[2], DATE_FORMAT).strftime(DATE_DB_FORMAT)
                schedule.everyday, schedule.weekday, schedule.odd_even_week \
                    = parse_repeat_intervals(item[3], item[4])
            elif item[3] == "Ежемесячно":
                schedule.end_date = datetime.strptime(item[2], DATE_FORMAT).strftime(DATE_DB_FORMAT)
                schedule.repeat_day = datetime.strptime(item[1], DATE_FORMAT).day
            elif item[3] == 'Единожды':
                schedule.end_date = schedule.start_date
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
    everyday = None
    weekday = None
    odd_even_week = None
    days = {
        'Понедельник': '1',
        'Вторник': '2',
        'Среда': '3',
        'Четверг': '4',
        'Пятница': '5',
        'Суббота': '6',
        'Воскресенье': '7'
    }

    if regularity == 'Ежедневно':
        everyday = '1'
    elif regularity == 'Еженедельно':
        weekday = days[day_of_week]
    elif regularity == 'Нечетная неделя':
        odd_even_week = "1"
        weekday = days[day_of_week]
    elif regularity == 'Четная неделя':
        odd_even_week = "2"
        weekday = days[day_of_week]

    return everyday, weekday, odd_even_week


def parse_sight(excursion_sheet, excursion_id):
    for item in excursion_sheet:
        if item[0][:5] == 'Пункт' and item[1] != '':
            sight = Models.Sight()
            sight.name = item[1]
            sight.image = ''
            sight.save()

            excursion_sight = Models.ExcursionSight()
            excursion_sight.excursion = excursion_id
            excursion_sight.sight = sight.id
            excursion_sight.save()


def parse_excursion_property(excursion_sheet, excursion_id):
    for item in excursion_sheet:
        if item[0][:1] == '№' and item[1] != '':
            excursionpr = Models.ExcursionProperty()
            excursionpr.name = item[1]
            excursionpr.image = ''
            excursionpr.save()

            excursion_excursionpr = Models.ExcursionExcursionProperty()
            excursion_excursionpr.excursion = excursion_id
            excursion_excursionpr.property = excursionpr.id
            excursion_excursionpr.save()


def parse_duration(excursion_sheet):
    for item in excursion_sheet:
        if item[0][:7] == 'Вариант' and item[7] != '':
            dur = [int(x) for x in item[7].split(':')]
            return 60 * dur[0] + dur[1]


def parse(link=DEFAULT_LINK):
    if DEFAULT_LINK != link:
        link = link if link else DEFAULT_LINK
        print("Ссылка: '%s'" % link)
        ans = input('Начинаем парсить (y/n)? ')
        if ans.strip()[0].lower() == "y":
            sheets = client.open_by_url(link).worksheets()
            parsed = 0
            for sheet in sheets:
                excursion_sheet = sheet.get_all_values()
                if excursion_sheet[0][0] == "Экскурсия":
                    print("На очереди: '%s'" % sheet.title)
                    ans = input('Парсим (y/n/e)? ')
                    if ans.strip()[0].lower() == "y":
                        parse_excursion(excursion_sheet)
                        print("Закончили парсить '%s'" % sheet.title)
                        parsed += 1
                    elif ans.strip()[0].lower() == "e":
                        print("Вы отменили парсинг")
                        exit()
                    else:
                        print("Пропущена \n")
                        pass
            print("Всего импортировано экскурсий: %s" % parsed)
            exit()
        else:
            print("Вы отменили парсинг")
            exit()


if __name__ == '__main__':
    while True:
        try:
            input_link = input('Вставь ссылку на таблицу: ')
            parse(input_link.strip())
        except KeyboardInterrupt:
            print("Вы отменили парсинг")

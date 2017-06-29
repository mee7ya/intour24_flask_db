# coding:utf-8

from parsing.db.postgre_connect import DBConnect
from parsing.parsers import tur_kazan_tours, kazantravel
import csv, json

if __name__ == '__main__':
    # database = DBConnect()
    tours = []
    tours.extend(kazantravel.parse())
    print(len(tours))

    with open('eggs.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for tour in tours:
            type(tour.title)
            spamwriter.writerow([
                tour.title,
                tour.price,
                ",\n".join(["{}: {}".format(key, value) for key, value in tour.schedule.items()]),
                tour.description,
                ', '.join(tour.images)
            ])

import local_db as LocalModels
import postgre_connect as PostgreModels
import os
import pytz

Models = LocalModels
# Models = PostgreModels

LOCAL_DB_PATH = os.path.dirname(__file__) + '/tours.db'

TZ = pytz.timezone('Europe/Moscow')

MINS_IN_WEEK = 10080  # 60*24*7
MINS_IN_DAY = 1440  # 60*24

DATE_FORMAT = '%d.%m.%y'

DATE_TZ_FORMAT = '%Y-%m-%d %H:%M:%S+03'

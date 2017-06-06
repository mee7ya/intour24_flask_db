from parsing.db import postgre_connect as PostgreModels
from parsing.db import local_db_connect as LocalModels
import os
import pytz

Models = PostgreModels
# Models = LocalModels
LOCAL_DB_PATH = os.path.dirname(__file__) + '/tours.db'

TZ = pytz.timezone('Europe/Moscow')

MINS_IN_WEEK = 10080  # 60*24*7
MINS_IN_DAY = 1440  # 60*24

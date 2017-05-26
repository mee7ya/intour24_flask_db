from parsing.db.local_db_connect import Tour as LocalTour
from parsing.db.postgre_connect import Tour as PostgreTour

#TourModel = PostgreTour
TourModel = LocalTour

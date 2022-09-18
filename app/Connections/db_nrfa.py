import pymysql as mysql
from app.Connections.db_connect import DB_CONNECT
from pymysql.cursors import DictCursor
from app.utils import data_utils

class DB_NRFA(DB_CONNECT):
    """
    Child class of DB_CONNECT which controls the NRFA DB Connections
    """


    """
    Function used to populate the nrfa table with station name and number
    """
    def populate_nrfa_table(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            with self.connection.cursor() as cur:
                # Attempt to insert a station and if that attempt throws an error 
                # because the station id is already in the table (error thrown because
                # station id is the PK), then IGNORE the error thrown and attempt next
                # insertion
                query_string="""
                INSERT IGNORE INTO nrfa (station_id, station_name) VALUES (%s, %s);
                """
                station_list_of_tuples=data_utils.scrape_nrfa()
                cur.executemany(query_string, station_list_of_tuples)
                self.connection.commit()
        finally:
            self.connection.close()

    def retrieve_all_station_info(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, cursorclass=DictCursor)
        try:
            with self.connection.cursor() as cur:
                query_string="""
                SELECT * FROM nrfa;
                """
                cur.execute(query_string)
                results = cur.fetchall()

                return results
        finally:
            self.connection.close()










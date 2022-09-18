import pymysql as mysql
from app.Connections.db_connect import DB_CONNECT

class DB_WATER_BODY_TYPE(DB_CONNECT):
    """
    Child class of DB_CONNECT which controls the Water Body Type DB connection
    """

    """
    Function used to populate the water body types, currently only 2 different types
    """
    def populate_water_body_type(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
           with self.connection.cursor() as cur:
                query_string = """
                INSERT INTO water_body_type (water_body_type) VALUES (%s);
                """ 
                val = ['1_2_4_6', '3_5_7']
                vals = [ (i,) for i in val ]
                cur.executemany(query_string, vals)
                self.connection.commit()
        finally:
            self.connection.close()

    """
    Function which returns water body id based on water body type
    """
    def retrieve_water_body_id(self, *, water_body_type):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT id FROM water_body_type
                WHERE water_body_type=(%s);
                """
                cur.execute(query_string, water_body_type)
                result = cur.fetchone()
                return result[0]
        finally:
            self.connection.close()
    
    """
    Function which returns water body type based on water body id
    """
    def retrieve_water_body_type(self, *, water_body_id):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT water_body_type FROM water_body_type
                WHERE id=(%s);
                """
                cur.execute(query_string, water_body_id)
                result = cur.fetchone()
                return result[0]
        finally:
            self.connection.close()
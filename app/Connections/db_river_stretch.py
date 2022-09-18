import pymysql as mysql
from app.Connections.db_connect import DB_CONNECT
from app.utils import data_utils

class DB_RIVER_STRETCH(DB_CONNECT):
    """
    Child class of DB_CONNECT which controls the River Stretch DB Connections
    """

    """
    Function used to populate the river stretch names from an excel spreadsheet
    """
    def populate_stretch_names(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
           with self.connection.cursor() as cur:
                query_string = """
                INSERT INTO stretch_name (name) VALUES (%s);
                """ 
                val = data_utils.excel_file_to_river_stretch_names('./app/utils/stretch_names.xlsx')
                vals = [ (i,) for i in val ]
                cur.executemany(query_string, vals)
                self.connection.commit()
        finally:
            self.connection.close()

    """
    Function used to populate the River Stretch name dropdown
    """        
    def retrieve_all_stretch_names(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT name FROM stretch_name;
                """
                cur.execute(query_string)
                result = cur.fetchall()
                return [ i[0] for i in result ]
        finally:
            self.connection.close()

    """
    Function which returns river stretch id based on river name
    """
    def retrieve_river_stretch_id(self, *, river_name):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT ID FROM stretch_name
                WHERE name=(%s);
                """
                cur.execute(query_string, river_name)
                result = cur.fetchone()
                return result[0]
        finally:
            self.connection.close()
    
    """
    Function which returns river stretch name based on river stretch id
    """
    def retrieve_river_stretch_name(self, *, river_stretch_id):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT name FROM stretch_name
                WHERE ID=(%s);
                """
                cur.execute(query_string, river_stretch_id)
                result = cur.fetchone()
                return result[0]
        finally:
            self.connection.close()
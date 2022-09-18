import pymysql as mysql
from pymysql.cursors import DictCursor
from app.Connections.db_connect import DB_CONNECT

class DB_SERIALISED_INPUTS(DB_CONNECT):
    """
    Child class of DB_CONNECT which controls the MIXED CALCULATED DB Connections
    """

    """
    Function which inserts all data relevant to calculation into output_mixed table or links output_mixed table to the other
    tables which hold the values needed for the calculation
    """
    def insert_into_mixed_output_results(self, *, unique_id: str, mean_mixed_flow: float, sd_mixed_flow: float, mean_mixed_bod: float, sd_mixed_bod: float, mean_mixed_nh3: float, sd_mixed_nh3: float):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
           with self.connection.cursor() as cur:
                values = (unique_id, mean_mixed_flow, sd_mixed_flow, mean_mixed_bod, sd_mixed_bod, mean_mixed_nh3, sd_mixed_nh3)
                query_string = """
                INSERT INTO serialised_inputs (id, mean_mixed_flow, sd_mixed_flow, mean_mixed_bod, sd_mixed_bod, mean_mixed_nh3, sd_mixed_nh3) VALUES (%s, %s, %s, %s, %s, %s, %s);
                """ 
                cur.execute(query_string, values)
                self.connection.commit()
        finally:
            self.connection.close()


    """
    Function which returns all the rows in output_mixed table in chronological order from newest to oldest
    Displays all the values currently used in dropdown 
    This can be modified depending on what we wish to display in the dropdown
    """
    def get_all_mixed_results(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, cursorclass=DictCursor)
        try:
           with self.connection.cursor() as cur:
                query_string = """
                SELECT serialised_inputs.id, serialised_inputs.mean_mixed_flow, serialised_inputs.sd_mixed_flow, serialised_inputs.mean_mixed_bod, serialised_inputs.sd_mixed_bod, serialised_inputs.mean_mixed_nh3, serialised_inputs.sd_mixed_nh3, archive.created, archive.name_of_simulation
                FROM serialised_inputs
                INNER JOIN archive ON archive.id = serialised_inputs.id
                ORDER BY created DESC;
                """ 
                cur.execute(query_string)
                result = cur.fetchall()
                return result
        finally:
            self.connection.close()


    def get_mixed_results_by_id(self, id):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, cursorclass=DictCursor)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT * FROM serialised_inputs
                WHERE id = %s;
                """ 
                cur.execute(query_string, id)
                result = cur.fetchall()
                return list(result)
        finally:
            self.connection.close()
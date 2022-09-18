import pymysql as mysql
from pymysql.cursors import DictCursor
from app.Connections.db_connect import DB_CONNECT

class DB_ARCHIVE(DB_CONNECT):
    """
    Child class of DB_CONNECT which controls the Archive DB Connections
    """

    """
    Function which inserts all data relevant to calculation into archive or links archive to the other
    tables which hold the values needed for the calculation
    """
    def insert_into_archive(self, *, unique_id: str, name_of_simulation: str, username: str, river_stretch_id: int, standards_id: str, water_body_id: int, qube_csv: bool, nrfa_csv: bool):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
           with self.connection.cursor() as cur:
                values = (unique_id, name_of_simulation, username, river_stretch_id,standards_id, water_body_id, qube_csv, nrfa_csv)
                query_string = """
                INSERT INTO archive (id, name_of_simulation, username, river_stretch_id, standards_id, water_body_id, qube_csv, nrfa_csv) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """ 
                cur.execute(query_string, values)
                self.connection.commit()
        finally:
            self.connection.close()


    """
    Function which returns all the rows in archive in chronological order from newest to oldest
    Displays all the values currently used on the archive page 
    This can be modified depending on what we wish to display on the archive page
    """
    def get_all_archive_results(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, cursorclass=DictCursor)
        try:
           with self.connection.cursor() as cur:
                query_string = """
                SELECT a.id, a.created, a.name_of_simulation, a.username, w.water_body_type, r_name.name, r.bod_wfd_standard_post_spill, r.bod_soaf_score, r.nh3_wfd_standard_post_spill, r.nh3_soaf_score
                FROM archive a
                INNER JOIN water_body_type w ON w.id = a.water_body_id
                INNER JOIN stretch_name r_name ON r_name.id = a.river_stretch_id
                INNER JOIN results r ON r.ID = a.id
                ORDER BY created DESC;
                """ 
                cur.execute(query_string)
                result = cur.fetchall()
                return result
        finally:
            self.connection.close()

    """
    Get all Output page values
    Given a calculations Unique_id this will return all output page values 
    """
    def get_all_output_page_values(self, *, unique_id :str):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, cursorclass=DictCursor)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT
                a.id AS unique_id,
                a.username AS username,
                a.name_of_simulation AS name_of_sim,
                s.name AS river_stretch_name,
                r.*,
                w.water_body_type AS water_body_type
                FROM archive a
                INNER JOIN stretch_name s ON s.id = a.river_stretch_id
                INNER JOIN water_body_type w ON w.id = a.water_body_id
                INNER JOIN results r ON r.id = a.id
                WHERE a.id = (%s)
                ;
                """ 
                cur.execute(query_string, unique_id)
                result = cur.fetchone()
                return result
        finally:
            self.connection.close()


    """
    Function which returns the id of the most recent simulation run
    """
    def get_most_recent_id(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, cursorclass=DictCursor)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT id FROM archive
                ORDER BY created DESC
                LIMIT 1;
                """ 
                cur.execute(query_string)
                result = cur.fetchall()
                return 0 if not result else result[0]['id']
        finally:
            self.connection.close()


    def get_archive_by_id(self, id):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, cursorclass=DictCursor)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT * FROM archive
                WHERE id = %s;
                """ 
                cur.execute(query_string, id)
                result = cur.fetchall()
                return list(result)
        finally:
            self.connection.close()

    """
    Function which checks that ID is present in the table and returns None if not valid id
    Used to ensure Unique ID given to outputs page exists
    """
    def check_id_exists(self, unique_id):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT id FROM archive
                WHERE id = (%s)
                ;
                """ 
                cur.execute(query_string, unique_id)
                result = cur.fetchone()
                return None if not result else result
        finally:
            self.connection.close()
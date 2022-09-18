import pymysql as mysql
from app.Connections.db_connect import DB_CONNECT
import uuid as id


class DB_WFD_STANDARDS(DB_CONNECT):
    def insert_standards(self, standards: list, user: str):
        self.connection = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        uuid = str(id.uuid4())
        try:
            with self.connection.cursor() as cur:
                update_query_string = """
                INSERT INTO standards_update (ID, update_time, user)
                VALUES (%s, NOW(), %s);
                """
                update_data = (uuid, user)
                cur.execute(update_query_string, update_data)

                standards_query_string = """
                INSERT INTO standards (river_id, concentration_mg_l, ID)
                VALUES (
                    (
                        SELECT ID
                        FROM river_types
                        WHERE river_type = %s AND standard = %s AND pollutant = %s
                    ),
                    %s,
                    %s
                );
                """
                for i in standards:
                    i.append(uuid)
                standards_data = tuple(tuple(i) for i in standards)
                cur.executemany(standards_query_string, standards_data)
                self.connection.commit()
        finally:
            self.connection.close()

    def get_latest_standard(self, river_type: str, standard: str, pollutant: str):
        """
        Returns concentration of standard for given river type, standard and pollutant
        """
        self.connection = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT s.concentration_mg_l
                FROM standards s
                INNER JOIN river_types r ON s.river_id = r.ID
                INNER JOIN standards_update su ON s.ID = su.ID
                WHERE r.river_type = %s 
                    AND r.standard = %s
                    AND r.pollutant = %s
                    AND su.update_time = (SELECT MAX(update_time)
                        FROM standards_update
                    );
                """
                data = (river_type, standard, pollutant)
                cur.execute(query_string, data)
                result = cur.fetchall()
                # result is returned as nested tuple so index 0 and 0 is needed
                return result[0][0]
        finally:
            self.connection.close()
    
    def get_latest_standards_id(self):
        """
        Returns ID for the current standard
        """
        self.connection = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT ID FROM standards_update
                ORDER BY update_time DESC
                LIMIT 1;
                """
                cur.execute(query_string)
                result = cur.fetchone()
                return result[0]
        finally:
            self.connection.close()

    def get_all_standards(self):
        """
        Returns a list of list of the latest standards in the DB
        """
        self.connection = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT r.river_type, r.pollutant, r.standard, s.concentration_mg_l
                FROM standards s
                INNER JOIN river_types r ON s.river_id = r.ID
                INNER JOIN standards_update su ON s.ID = su.ID
                WHERE su.update_time = (SELECT MAX(update_time) FROM standards_update);
                """
                cur.execute(query_string)
                result = cur.fetchall()
                return [list(i) for i in result]
        finally:
            self.connection.close()

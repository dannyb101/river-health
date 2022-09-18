import pymysql as mysql
from pymysql.cursors import DictCursor
from app.Connections.db_connect import DB_CONNECT

class DB_RESULTS(DB_CONNECT):
    """
    Child class of DB_CONNECT which controls the Results DB connection
    """

    """
    Function which saves all results currently shown on the outputs page
    Please note: Not fully normalized, this will be a user story
    """
    def insert_into_results(self, *, 
                            unique_id, 
                            nh3_pre_spill, nh3_post_spill, nh3_wfd_standard_pre_spill, nh3_wfd_standard_post_spill, nh3_in_class_deterioration, nh3_soaf_score,
                            bod_pre_spill, bod_post_spill, bod_wfd_standard_pre_spill, bod_wfd_standard_post_spill, bod_in_class_deterioration, bod_soaf_score
                            ):

        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)

        try:
            with self.connection.cursor() as cur:
                vals = (unique_id, 
                        nh3_pre_spill, nh3_post_spill, nh3_wfd_standard_pre_spill, nh3_wfd_standard_post_spill, nh3_in_class_deterioration, nh3_soaf_score,
                        bod_pre_spill, bod_post_spill, bod_wfd_standard_pre_spill, bod_wfd_standard_post_spill, bod_in_class_deterioration, bod_soaf_score
                )
                query_string = """
                INSERT INTO results (
                    id, 
                    nh3_pre_spill, nh3_post_spill, nh3_wfd_standard_pre_spill, nh3_wfd_standard_post_spill, nh3_in_class_deterioration, nh3_soaf_score,
                    bod_pre_spill, bod_post_spill, bod_wfd_standard_pre_spill, bod_wfd_standard_post_spill, bod_in_class_deterioration, bod_soaf_score
                )
                VALUES (
                    %s, 
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                """
                cur.execute(query_string, vals)                
                self.connection.commit()
        finally:
            self.connection.close()
    

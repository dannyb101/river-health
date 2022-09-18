import pymysql as mysql
from pymysql.cursors import DictCursor
from app.Connections.db_connect import DB_CONNECT
import uuid

class DB_VARIABLES(DB_CONNECT):
    """
    Child class of DB_CONNECT which controls the River Stretch DB Connections
    """

    """
    Function to populate variables table
    """
    def populate_variables(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
           with self.connection.cursor() as cur:
                unique_id = str(uuid.uuid4())
                query_string = """
                INSERT INTO variables (
                id, isDefault, 
                river_bod_mgl, river_bod_mgl_sd, river_nh3_mgl, river_nh3_mgl_sd, river_do_conc_mgl, river_do_conc_mgl_sd, river_temp_celcius, river_temp_celcius_sd, river_ph, river_ph_sd, 
                river_length_stretch_m, river_longslope_m_m, river_bedwidth_m, river_sideslope_m_m,
                reaeration_constant, velocity_exponent, depth_exponent,
                river_mannings_no, river_bod_decay_rate_day, river_nh3_decay_rate_day, river_nh3_gain_bod_gN_gO2, river_nh3_yield_factor_gN_gO2, 
                num_sims, num_years
                )
                VALUES (
                %s, TRUE, 
                3.5, 2.5, 0.2, 0.3, 7, 0.001, 17, 1.82, 8, 0.001,
                1000, 7.815, 45, 7.815,
                3.9, 0.5, -1.5,
                0.03, 0.35, 2, 0.29, 0.109,
                2, 10);
                """
                cur.execute(query_string, unique_id)
                cso_query_string = """
                INSERT INTO cso_inputs (
                    unique_id,
                    bod_conc_mgl,
                    nh3_conc_mgl
                )
                VALUES (%s, 125, 8);
                """ 
                cur.execute(cso_query_string, unique_id)
                self.connection.commit()
        finally:
            self.connection.close()

    """
    Function to insert a new row into the variables table
    """
    def insert_into_variables(self, *, 
                unique_id, isDefault: bool, 
                river_flow_ls, river_flow_ls_sd, 
                river_bod_mgl, river_bod_mgl_sd, river_nh3_mgl, river_nh3_mgl_sd, river_do_conc_mgl, river_do_conc_mgl_sd, river_temp_celcius, river_temp_celcius_sd, river_ph, river_ph_sd, 
                river_length_stretch_m, river_longslope_m_m, river_bedwidth_m, river_sideslope_m_m,
                reaeration_constant, velocity_exponent, depth_exponent,
                river_mannings_no, river_bod_decay_rate_day, river_nh3_decay_rate_day, river_nh3_gain_bod_gN_gO2, river_nh3_yield_factor_gN_gO2, 
                num_sims, num_years):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            with self.connection.cursor() as cur:
                vals = (unique_id, isDefault, 
                river_flow_ls, river_flow_ls_sd, 
                river_bod_mgl, river_bod_mgl_sd, river_nh3_mgl, river_nh3_mgl_sd, river_do_conc_mgl, river_do_conc_mgl_sd, river_temp_celcius, river_temp_celcius_sd, river_ph, river_ph_sd,
                river_length_stretch_m, river_longslope_m_m, river_bedwidth_m, river_sideslope_m_m,
                reaeration_constant, velocity_exponent, depth_exponent,
                river_mannings_no, river_bod_decay_rate_day, river_nh3_decay_rate_day, river_nh3_gain_bod_gN_gO2, river_nh3_yield_factor_gN_gO2, 
                num_sims, num_years)

                query_string = """
                INSERT INTO variables (
                id, isDefault,
                river_flow_ls, river_flow_ls_sd, 
                river_bod_mgl, river_bod_mgl_sd, river_nh3_mgl, river_nh3_mgl_sd, river_do_conc_mgl, river_do_conc_mgl_sd, river_temp_celcius, river_temp_celcius_sd, river_ph, river_ph_sd, 
                river_length_stretch_m, river_longslope_m_m, river_bedwidth_m, river_sideslope_m_m,
                reaeration_constant, velocity_exponent, depth_exponent,
                river_mannings_no, river_bod_decay_rate_day, river_nh3_decay_rate_day, river_nh3_gain_bod_gN_gO2, river_nh3_yield_factor_gN_gO2, 
                num_sims, num_years
                )
                VALUES (
                %s, %s,
                %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s);
                """
                cur.execute(query_string, vals)
                self.connection.commit()
        finally:
            self.connection.close()

    def insert_cso_variables(self, *, cso_data: dict, unique_id: str):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cso_vals = []
        for cso_id, cso_concs in cso_data.items():
            cso_vals.append((unique_id, cso_id, cso_concs['bod_conc'], cso_concs['nh3_conc']))
        try:
            with self.connection.cursor() as cur:
                query_string = """
                INSERT INTO cso_inputs (
                    unique_id,
                    cso_id,
                    bod_conc_mgl,
                    nh3_conc_mgl
                )
                VALUES (%s, %s, %s, %s);
                """
                cur.executemany(query_string, cso_vals)
                self.connection.commit()
        finally:
            self.connection.close()

    """
    Function to retrieve the last saved defaults in the variables table
    Relies on isDefault being True and ordered by timestamp
    """
    def retrieve_most_recent_defaults(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, cursorclass=DictCursor)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SELECT 
                v.id AS id,
                v.isDefault AS isDefault,
                v.created AS created,
                v.river_flow_ls AS river_flow_ls,
                v.river_flow_ls_sd AS river_flow_ls_sd,
                v.river_bod_mgl AS river_bod_mgl,
                v.river_bod_mgl_sd AS river_bod_mgl_sd,
                v.river_nh3_mgl AS river_nh3_mgl,
                v.river_nh3_mgl_sd AS river_nh3_mgl_sd,
                v.river_do_conc_mgl AS river_do_conc_mgl,
                v.river_do_conc_mgl_sd AS river_do_conc_mgl_sd,
                v.river_temp_celcius AS river_temp_celcius,
                v.river_temp_celcius_sd AS river_temp_celcius_sd,
                v.river_ph AS river_ph,
                v.river_ph_sd AS river_ph_sd,

                c.bod_conc_mgl AS cso_bod_conc_mgl,
                c.nh3_conc_mgl AS cso_nh3_conc_mgl,

                v.river_length_stretch_m AS river_length_stretch_m,
                v.river_longslope_m_m AS river_longslope_m_m,
                v.river_bedwidth_m AS river_bedwidth_m,
                v.river_sideslope_m_m AS river_sideslope_m_m,
                
                v.reaeration_constant AS reaeration_constant,
                v.velocity_exponent AS velocity_exponent,
                v.depth_exponent AS depth_exponent,
                v.river_mannings_no AS river_mannings_no,
                v.river_bod_decay_rate_day AS river_bod_decay_rate_day,
                v.river_nh3_decay_rate_day AS river_nh3_decay_rate_day,
                v.river_nh3_gain_bod_gN_gO2 AS river_nh3_gain_bod_gN_gO2,
                v.river_nh3_yield_factor_gN_gO2 AS river_nh3_yield_factor_gN_gO2,
                
                v.num_sims AS num_sims,
                v.num_years AS num_years
                               
                FROM variables v
                INNER JOIN cso_inputs c ON v.id = c.unique_id
                WHERE isDefault = True
                ORDER BY created DESC
                LIMIT 1
                ;
                """
                cur.execute(query_string)
                data = cur.fetchall()[0]
                return data
        finally:
            self.connection.close()


    """
    Function to retrieve the inputs from a calculation given the archive id
    """
    def retrieve_inputs(self, id):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, cursorclass=DictCursor)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                    SELECT 
                        v.depth_exponent AS depth_exponent,
                        v.num_sims AS num_sims,
                        v.num_years AS num_years,
                        v.river_flow_ls AS river_flow_ls,
                        v.river_flow_ls_sd AS river_flow_ls_sd,  
                        v.river_bod_mgl AS river_bod_mgl,
                        v.river_bod_mgl_sd AS river_bod_mgl_sd,
                        v.river_nh3_mgl AS river_nh3_mgl,
                        v.river_nh3_mgl_sd AS river_nh3_mgl_sd,
                        v.river_do_conc_mgl AS river_do_conc_mgl,
                        v.river_do_conc_mgl_sd AS river_do_conc_mgl_sd,
                        v.river_temp_celcius AS river_temp_celcius,
                        v.river_temp_celcius_sd AS river_temp_celcius_sd,
                        v.river_ph AS river_ph,
                        v.river_ph_sd AS river_ph_sd, 
                        v.river_length_stretch_m AS river_length_stretch_m,
                        v.river_longslope_m_m AS river_longslope_m_m,
                        v.river_bedwidth_m AS river_bedwidth_m,
                        v.river_sideslope_m_m AS river_sideslope_m_m,
                        v.reaeration_constant AS reaeration_constant,
                        v.river_mannings_no AS river_mannings_no,
                        v.river_bod_decay_rate_day AS river_bod_decay_rate_day,
                        v.river_nh3_decay_rate_day AS river_nh3_decay_rate_day,
                        v.river_nh3_gain_bod_gN_gO2 AS river_nh3_gain_bod_gN_gO2,
                        v.river_nh3_yield_factor_gN_gO2 AS river_nh3_yield_factor_gN_gO2, 
                        v.velocity_exponent AS velocity_exponent,
                        a.id AS archive_id,
                        a.created AS sim_datetime,
                        s.name AS river_stretch_name,
                        w.water_body_type AS river_type
                    FROM variables v
                        INNER JOIN archive a ON v.id = a.id
                        INNER JOIN stretch_name s ON a.river_stretch_id = s.ID
                        INNER JOIN water_body_type w ON a.water_body_id = w.id
                    WHERE a.id = %s;
                """
                cur.execute(query_string, id)
                result = cur.fetchall()[0]
                return None if not result else result
        finally:
            self.connection.close()

    def retrieve_cso_inputs(self, id):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, cursorclass=DictCursor)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                    SELECT
                        c.bod_conc_mgl AS cso_bod_conc_mgl,
                        c.nh3_conc_mgl AS cso_nh3_conc_mgl,
                        c.cso_id AS cso_id
                    FROM cso_inputs c
                    WHERE c.unique_id = %s;
                """
                cur.execute(query_string, id)
                cso_result = cur.fetchall()
                result = {}
                for i, pollutants in enumerate(cso_result):
                    for key, value in pollutants.items():
                        result[key + f"_{i+1}"] = value
                return result
        finally:
            self.connection.close()


                
       
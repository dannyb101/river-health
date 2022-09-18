import pymysql as mysql

class DB_CONNECT:
    """
    Parent class which declares the connection variables to be used by all DB_CONNECT classes
    Parent class holds any methods which apply to the whole database
    """
    def __init__(self):
        self.host = '10.72.96.202'
        self.user = 'root'
        self.password = 'comsc'
        self.database = 'arup'

    """
    Function which drops all tables in the Arup database.
    NOTES: Please add any newly created tables to the function, also to create_all_tables and tests/database/test_all/test_retireve_all_tables
    WARNING: This function is permenant!! If called you will lose all your data!!!
    """
    def drop_all_tables(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS cso_inputs;
                """
                cur.execute(query_string)
                self.connection.commit()
            
            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS serialised_inputs;
                """
                cur.execute(query_string)
                self.connection.commit()

            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS archive;
                """
                cur.execute(query_string)
                self.connection.commit()
            
            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS water_body_type;
                """
                cur.execute(query_string)
                self.connection.commit()

            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS standards;
                """
                cur.execute(query_string)
                self.connection.commit()   

            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS standards_update;
                """
                cur.execute(query_string)
                self.connection.commit()
            
            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS river_types;
                """
                cur.execute(query_string)
                self.connection.commit()    

            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS variables;
                """
                cur.execute(query_string)
                self.connection.commit()

            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS nrfa;
                """
                cur.execute(query_string)
                self.connection.commit()

            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS stretch_name;
                """
                cur.execute(query_string)
                self.connection.commit()
            
            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS results;
                """
                cur.execute(query_string)
                self.connection.commit()


            with self.connection.cursor() as cur:
                query_string = """
                DROP TABLE IF EXISTS users;
                """
                cur.execute(query_string)
                self.connection.commit()

        finally:
            self.connection.close()

    """
    Function to create all necessary tables in the Arup Database.
    """
    def create_all_tables(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(255) NOT NULL PRIMARY KEY,
                    password VARCHAR(255),
                    email VARCHAR(255)
                );
                """
                cur.execute(query_string)
                self.connection.commit()
        
            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS water_body_type (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    water_body_type VARCHAR(255)
                )
                """
                cur.execute(query_string)
                self.connection.commit()
            
            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS standards_update (
                    ID VARCHAR(255),
                    update_time DATETIME,
                    user VARCHAR(255),
                    PRIMARY KEY (ID),
                    FOREIGN KEY (user)
                        REFERENCES users(username)
                        ON UPDATE CASCADE
                );
                """
                cur.execute(query_string)
                self.connection.commit()

            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS standards (
                    ID VARCHAR(255),
                    river_id INT,
                    concentration_mg_l FLOAT,
                    PRIMARY KEY (ID,river_id),
                    FOREIGN KEY (ID)
                        REFERENCES standards_update(ID)
                );
                """
                cur.execute(query_string)
                self.connection.commit()
            
            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS river_types (
                    ID INT AUTO_INCREMENT,
                    river_type VARCHAR(255) NOT NULL,
                    standard VARCHAR(255) NOT NULL,
                    pollutant VARCHAR(255) NOT NULL,
                    PRIMARY KEY (ID)
                );
                """
                cur.execute(query_string)
                self.connection.commit()

            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS variables (
                    id VARCHAR(36) PRIMARY KEY,
                    isDefault BOOLEAN NOT NULL,
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    river_flow_ls FLOAT NULL,
                    river_flow_ls_sd FLOAT NULL,
                    river_bod_mgl FLOAT NOT NULL,
                    river_bod_mgl_sd FLOAT NOT NULL,
                    river_nh3_mgl FLOAT NOT NULL,
                    river_nh3_mgl_sd FLOAT NOT NULL,
                    river_do_conc_mgl FLOAT NOT NULL,
                    river_do_conc_mgl_sd FLOAT NOT NULL,
                    river_temp_celcius FLOAT NOT NULL,
                    river_temp_celcius_sd FLOAT NOT NULL,
                    river_ph FLOAT NOT NULL,
                    river_ph_sd FLOAT NOT NULL,
                    river_length_stretch_m FLOAT NOT NULL,
                    river_longslope_m_m FLOAT NOT NULL,
                    river_bedwidth_m FLOAT NOT NULL,
                    river_sideslope_m_m FLOAT NOT NULL,
                    reaeration_constant FLOAT NOT NULL,
                    velocity_exponent FLOAT NOT NULL,
                    depth_exponent FLOAT NOT NULL,
                    river_mannings_no FLOAT NOT NULL,
                    river_bod_decay_rate_day FLOAT NOT NULL,
                    river_nh3_decay_rate_day FLOAT NOT NULL,
                    river_nh3_gain_bod_gN_gO2 FLOAT NOT NULL,
                    river_nh3_yield_factor_gN_gO2 FLOAT NOT NULL,
                    num_sims INT NOT NULL,
                    num_years INT NOT NULL
                );
                """
                cur.execute(query_string)
                self.connection.commit()

            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS nrfa (station_id INT PRIMARY KEY, station_name VARCHAR(255));
                """
                cur.execute(query_string)
                self.connection.commit()
            
            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS stretch_name (ID INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255));
                """
                cur.execute(query_string)
                self.connection.commit()
            
            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS results (
                    id VARCHAR(36) PRIMARY KEY,
                    nh3_pre_spill FLOAT NOT NULL,
                    nh3_post_spill FLOAT NOT NULL,
                    nh3_wfd_standard_pre_spill VARCHAR(255) NOT NULL,
                    nh3_wfd_standard_post_spill VARCHAR(255) NOT NULL,
                    nh3_in_class_deterioration FLOAT NOT NULl,
                    nh3_soaf_score INT NOT NULL,
                    bod_pre_spill FLOAT NOT NULL,
                    bod_post_spill FLOAT NOT NULL,
                    bod_wfd_standard_pre_spill VARCHAR(255) NOT NULL,
                    bod_wfd_standard_post_spill VARCHAR(255) NOT NULL,
                    bod_in_class_deterioration FLOAT NOT NULl,
                    bod_soaf_score INT NOT NULL
                )
                """
                cur.execute(query_string)
                self.connection.commit()
            
            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS archive (
                    id VARCHAR(36) PRIMARY KEY,
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    name_of_simulation VARCHAR(255) NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    river_stretch_id INT NOT NULL,
                    standards_id VARCHAR(36) NOT NULL,
                    water_body_id INT NOT NULL,
                    qube_csv BOOLEAN NULL,
                    nrfa_csv BOOLEAN NULL,
                    CONSTRAINT river_stretch_FK FOREIGN KEY (river_stretch_id) REFERENCES stretch_name(ID),
                    CONSTRAINT variables_FK FOREIGN KEY (id) REFERENCES variables(id),
                    CONSTRAINT results_FK FOREIGN KEY (id) REFERENCES results(id),
                    CONSTRAINT standards_FK FOREIGN KEY (standards_id) REFERENCES standards_update(ID),
                    CONSTRAINT water_body_FK FOREIGN KEY (water_body_id) REFERENCES water_body_type(id)
                )
                """
                cur.execute(query_string)
                self.connection.commit()

            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS serialised_inputs (
                    id VARCHAR(36) PRIMARY KEY,
                    mean_mixed_flow FLOAT NOT NULL,
                    sd_mixed_flow FLOAT NOT NULL,
                    mean_mixed_bod FLOAT NOT NULL,
                    sd_mixed_bod FLOAT NOT NULL,
                    mean_mixed_nh3 FLOAT NOT NULL,
                    sd_mixed_nh3 FLOAT NOT NULL,
                    CONSTRAINT id_FK FOREIGN KEY (id) REFERENCES archive(id)
                );
                """
                cur.execute(query_string)
                self.connection.commit()

            with self.connection.cursor() as cur:
                query_string = """
                CREATE TABLE IF NOT EXISTS cso_inputs (
                    entry_id INT AUTO_INCREMENT PRIMARY KEY,
                    unique_id VARCHAR(36) NOT NULL,
                    cso_id VARCHAR(255),
                    bod_conc_mgl FLOAT NOT NULL,
                    nh3_conc_mgl FLOAT NOT NULL,
                    CONSTRAINT var_FK FOREIGN KEY (unique_id) REFERENCES variables(id)
                        ON UPDATE CASCADE ON DELETE CASCADE
                    );
                """
                cur.execute(query_string)
                self.connection.commit()
                
        finally:
            self.connection.close()

    """
    Function solely used to test the database connection
    """
    def show_all_tables(self):
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            with self.connection.cursor() as cur:
                query_string = """
                SHOW TABLES;
                """
                cur.execute(query_string)
                return cur.fetchall()
           
        finally:
            self.connection.close()


from app.Connections import db_connect, db_river_stretch, db_standards, db_river_types, db_users, db_variables, db_water_body_type, db_nrfa
import os, ssl

# WARNING: When testing the application on a Mac computer, the controller methods
# in this class threw SSL: CERTIFICATE_VERIFY_FAILED errors. This was as a result
# of server certificate validation being added by default, in version 2.7.9 of python.
# The following if statement turns this off in the environment variables. This provides
# a temporary fix to the problem but should be replaced.
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

standards = [
	['1_2_4_6', 'high', 'bod', 7],
	['1_2_4_6', 'good', 'bod', 9],
	['1_2_4_6', 'moderate', 'bod', 14],
	['1_2_4_6', 'poor', 'bod', 16],
	['1_2_4_6', 'high', 'nh3', 0.5],
	['1_2_4_6', 'good', 'nh3', 0.7],
	['1_2_4_6', 'moderate', 'nh3', 1.8],
	['1_2_4_6', 'poor', 'nh3', 2.6],
	['3_5_7', 'high', 'bod', 9],
	['3_5_7', 'good', 'bod', 11],
	['3_5_7', 'moderate', 'bod', 14],
	['3_5_7', 'poor', 'bod', 19],
	['3_5_7', 'high', 'nh3', 0.7],
	['3_5_7', 'good', 'nh3', 1.5],
	['3_5_7', 'moderate', 'nh3', 2.6],
	['3_5_7', 'poor', 'nh3', 6]
]
river_types = [
	['1_2_4_6', 'high', 'bod'],
	['1_2_4_6', 'good', 'bod'],
	['1_2_4_6', 'moderate', 'bod'],
	['1_2_4_6', 'poor', 'bod'],
	['1_2_4_6', 'high', 'nh3'],
	['1_2_4_6', 'good', 'nh3'],
	['1_2_4_6', 'moderate', 'nh3'],
	['1_2_4_6', 'poor', 'nh3'],
	['3_5_7', 'high', 'bod'],
	['3_5_7', 'good', 'bod'],
	['3_5_7', 'moderate', 'bod'],
	['3_5_7', 'poor', 'bod'],
	['3_5_7', 'high', 'nh3'],
	['3_5_7', 'good', 'nh3'],
	['3_5_7', 'moderate', 'nh3'],
	['3_5_7', 'poor', 'nh3']
]




# ONLY RUN THIS FILE ONCE WHEN FIRST BUILDING THE APPLCIATION
# THIS WILL CREATE ALL THE TABLES NEEDED AND ADD STARTING DATA

connection = db_connect.DB_CONNECT()
connection_river_stretch = db_river_stretch.DB_RIVER_STRETCH()
connection_standards = db_standards.DB_WFD_STANDARDS()
connection_river_types = db_river_types.DB_RIVER_TYPES()
connection_users = db_users.DB_USERS()
connection_variables = db_variables.DB_VARIABLES()
connection_water_body = db_water_body_type.DB_WATER_BODY_TYPE()
connection_nrfa = db_nrfa.DB_NRFA()

connection.drop_all_tables()
connection.create_all_tables()

connection_river_stretch.populate_stretch_names()
connection_river_types.populate_river_types(river_types)
connection_water_body.populate_water_body_type()
connection_variables.populate_variables()

connection_users.insert_user('unknown', '111111', 'hello@gmail.com')
connection_standards.insert_standards(standards, 'unknown')

connection_nrfa.populate_nrfa_table()

from app.Connections.db_connect import DB_CONNECT
import pymysql as mysql


class DB_RIVER_TYPES(DB_CONNECT):

	def populate_river_types(self, river_types: list):
		self.connection = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
		try:
			with self.connection.cursor() as cur:
				query_string = """
				INSERT INTO river_types (river_type, standard, pollutant)
				VALUES (%s, %s, %s);
				"""
				cur.executemany(query_string, tuple(tuple(river) for river in river_types))
				self.connection.commit()
		finally:
			self.connection.close()
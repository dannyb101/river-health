import pymysql as mysql
from app.Connections.db_connect import DB_CONNECT



class DB_USERS(DB_CONNECT):

	def insert_user(self, user: str, password: str='', email: str=''):
		self.connection = mysql.connect(
			host=self.host,
			user=self.user,
			password=self.password,
			database=self.database,
		)
		try:
			with self.connection.cursor() as cur:
				query_string = """
				INSERT INTO users (username, password, email)
				VALUES (%s, %s, %s);
				"""
				data = (user, password, email)
				cur.execute(query_string, data)
				self.connection.commit()
		finally:
			self.connection.close()

import psycopg2

class market:
	def __init__(self):
		pass

	def connectSql(self):
		connection = psycopg2.connect(
			database = 'darkmemer', user = 'postgres',
			password = 'raj-1',  host = '127.0.0.1',
			port = '5432'
		)
		return connection

	def addItem(self, name: str, price: int, quantity: int):
		conn = self.connectSql()
		if conn:
			cur = conn.cursor()
			sql = """INSERT INTO MARKET (NAME, PRICE, QUANTITY) VALUES (%s, %s, %s)"""
			cur.executemany(sql, [(name, price, quantity)])
			conn.commit()
			cur.close()
			conn.close()
			return True
		return False

	def marketItems(self):
		conn = self.connectSql()
		if conn:
			cur = conn.cursor()
			sql = """SELECT * FROM MARKET"""
			cur.execute(sql)
			items = cur.fetchall()
			cur.close()
			conn.close()
			return items
		return None

	def updateItem(self, id: int, column: str, updateValue: str):
		conn = self.connectSql()
		if conn:
			cur = conn.cursor()
			sql = """UPDATE MARKET SET {column} = %s WHERE ID = %s;""".format(column = column)
			cur.executemany(sql, [(updateValue, id)])
			conn.commit()
			cur.close()
			conn.close()
			return True
		return False

	def removeItem(self, table, id: int, name: str):
		conn = self.connectSql()
		if conn:
			cur = conn.cursor()
			sql = """DELETE FROM {table} WHERE ID = %s OR NAME = %s;""".format(table = table)
			cur.executemany(sql, [(id, name)])
			conn.commit()
			cur.close()
			conn.close()
			return True
		return False

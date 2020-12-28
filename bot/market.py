#!/usr/local/bin/python3.8
import psycopg2

class market:
	def __init__(self):
		pass

	def connectSql(self):
		connection = psycopg2.connect(
			database = 'mydb', user = 'taskmaster',
			password = 'taskmaster',  host = '127.0.0.1',
			port = '5432'
		)
		return connection

	def addItem(self, name: str, price: int, quantity: int):
		res = False
		conn = self.connectSql()
		if conn:
			cur = conn.cursor()
			sql = """INSERT INTO MARKET (NAME, PRICE, QUANTITY) VALUES (%s, %s, %s)"""
			cur.executemany(sql, [(name, price, quantity)])
			conn.commit()
			res = True
		cur.close()
		conn.close()
		return res

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

	def updateItem(self, id: int, column: str, updateValue = None):
		res = False
		conn = self.connectSql()
		if conn and not updateValue is None:
			cur = conn.cursor()
			if not updateValue is None:
				sql = """UPDATE MARKET SET {column} = %s WHERE ID = %s;""".format(column = column)
				cur.executemany(sql, [(updateValue, id)])
				conn.commit()
				res = True
			cur.close()
			conn.close()
		return res

	def removeItem(self, table, id: int, name: str):
		res = False
		conn = self.connectSql()
		if not name is None:
			if conn:
				cur = conn.cursor()
				sql = """DELETE FROM {table} WHERE ID = %s OR NAME = %s;""".format(table = table)
				cur.executemany(sql, [(id, name)])
				conn.commit()
				res = True
			cur.close()
			conn.close()
		return res
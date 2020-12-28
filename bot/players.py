#!/usr/local/bin/python3.8
import psycopg2

class playerData:
	def __init__(self):
		pass

	def connectSql(self):
		connection = psycopg2.connect(
			database = 'mydb', user = 'taskmaster',
			password = 'taskmaster',  host = '127.0.0.1',
			port = '5432'
		)
		return connection

	def playerExist(self, pid, name, pdsc, nick = None):
		res = False
		conn = self.connectSql()
		if conn:
			cur = conn.cursor()
			sql = """SELECT PID, NAME, NICK, PDSC FROM PLAYERS;"""
			cur.execute(sql)
			rows = cur.fetchall()
			for row in rows:
				if row[0] == pid or (row[1] == name or row[2] == nick or row[3] == pdsc):
					res = True
					break
		return res

	def addNewPlayer(self, pid: int, name: str, pdsc: int, nick = None):
		res = False
		pExist = self.playerExist(pid, name, pdsc, nick)
		if pExist == False:
			conn = self.connectSql()
			if conn:
				cur = conn.cursor()
				sql = """INSERT INTO PLAYERS (PID, NAME, NICK, PDSC, BANK, WALLET) VALUES (%s, %s, %s, %s, 200, 100);"""
				cur.executemany(sql, [(pid, name, nick, pdsc)])
				conn.commit()
				res = True
			cur.close()
			conn.close()
		return res
	
	def playerProfile(self, pid, name, pdsc):
		conn = self.connectSql()
		if conn:
			cur = conn.cursor()
			sql = """SELECT * FROM PLAYERS WHERE PID = {pid} AND (NAME = '{name}' OR PDSC = {pdsc});""".format(
				pid = pid,
				name = name,
				pdsc = pdsc
			)
			cur.execute(sql)
			list_rows = cur.fetchall()
			for pdata in list_rows:
				pass
			cur.close()
			conn.close()
		return pdata #returns a list of player data (1, 4, 5, 6) = (Name, bank, wallet, inventory)
	
	def updatePlayerData(self, pid, column, upadteValue, name, pdsc):
		res = False
		conn = self.connectSql()
		if conn:
			cur = conn.cursor()
			sql = """UPDATE PLAYERS SET {column} = %s WHERE PID = %s AND (NAME = '{pname}' OR PDSC = %s);""".format(column = column, pname = name)
			cur.executemany(sql, [(upadteValue, pid, pdsc)])
			conn.commit()
			res = True
		cur.close()
		conn.close()
		return res

	def addItemsTOInventory(self, itemName, itemList, pid, name, pdsc):
		res = False
		conn = self.connectSql()
		if conn:
			itemExist = False
			item_ = None
			inventory_ = self.playerProfile(pid, name, pdsc)
			if not inventory_[6] is None:
				itemNames = [item for item in (ls[0] for ls in inventory_[6])] if len(inventory_[6]) != 4 else inventory_[6][0]
				if itemName in itemNames:
					itemExist = True
					item_ = itemNames.index(itemName) + 1
				else:
					item_ = len([*itemNames])
			else:
				item_ = 1
			cur = conn.cursor()
			if inventory_[6] is None:
				sql = """
				UPDATE PLAYERS SET INVENTORY = ARRAY[['{name_}', '%s', '%s', '%s']] WHERE PID = %s AND (NAME = %s OR PDSC = %s);
				""".format(name_ = itemName)
				#name, price, quantity, id
				cur.executemany(sql, [(itemList[itemName][0], itemList[itemName][1], itemList[itemName][2], pid, name, pdsc)])
				conn.commit()

			elif not itemExist and not inventory_[6] is None:
				sql = """
				UPDATE PLAYERS SET INVENTORY = INVENTORY || ARRAY['{name_}', '%s', '%s', '%s'] WHERE PID = %s AND (NAME = %s OR PDSC = %s);
				""".format(name_ = itemName)
				#name, price, quantity, id
				cur.executemany(sql, [(itemList[itemName][0], itemList[itemName][1], itemList[itemName][2], pid, name, pdsc)])
				conn.commit()

			elif itemExist:
				sql = """
				UPDATE PLAYERS SET INVENTORY[{item}][2] = %s, INVENTORY[{item}][3] = %s, INVENTORY[{item}][4] = %s WHERE PID = %s AND (NAME = %s OR PDSC = %s);
				""".format(item = item_)
				cur.executemany(sql, [(itemList[itemName][0], itemList[itemName][1], itemList[itemName][2], pid, name, pdsc)])
				conn.commit()
			cur.close()
			conn.close()
			res = True
		return res

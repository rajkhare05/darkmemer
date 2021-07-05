import psycopg2

class playerData:
	def __init__(self):
		pass

	def connectSql(self):
		connection = psycopg2.connect(
			database = 'darkmemer', user = 'postgres',
			password = 'raj-1',  host = '127.0.0.1',
			port = '5432'
		)
		return connection

	def playerExist(self, pid):
		conn = self.connectSql()
		if conn:
			cur = conn.cursor()
			sql = """SELECT PID FROM PLAYERS;"""
			cur.execute(sql)
			pids = cur.fetchall()
			for pid_ in pids:
				if pid_[0] == pid:
					cur.close()
					conn.close()
					return True
		return False

	def addNewPlayer(self, pid, name, pdsc):
		pExist = self.playerExist(pid)
		if not pExist:
			conn = self.connectSql()
			if conn:
				cur = conn.cursor()
				sql = """INSERT INTO PLAYERS (PID, NAME, PDSC, BANK, WALLET) VALUES (%s, %s, %s, 200, 100);"""
				cur.executemany(sql, [(pid, name, pdsc)])
				conn.commit()
				cur.close()
				conn.close()
				return True
		return False
	
	def playerProfile(self, pid):
		conn = self.connectSql()
		if conn:
			cur = conn.cursor()
			sql = """SELECT * FROM PLAYERS WHERE PID = {pid};""".format(pid = pid)
			cur.execute(sql)
			player_data = cur.fetchall()
			cur.close()
			conn.close()
		return player_data[0] #returns a list of player data (1, 4, 5, 6) = (Name, bank, wallet, inventory)
	
	def updatePlayerData(self, pid, column, upadteValue):
		conn = self.connectSql()
		if conn:
			cur = conn.cursor()
			sql = """UPDATE PLAYERS SET {column} = %s WHERE PID = %s;""".format(column = column)
			cur.executemany(sql, [(upadteValue, pid)])
			conn.commit()
			cur.close()
			conn.close()
			return True
		return False

	def addItemsToInventory(self, itemName, itemList, pid):
		res = False
		conn = self.connectSql()
		if conn:
			itemExist = False
			item_ = None
			inventory_ = self.playerProfile(pid)
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
				UPDATE PLAYERS SET INVENTORY = ARRAY[['{name_}', '%s', '%s', '%s']] WHERE PID = %s;
				""".format(name_ = itemName)
				#name, price, quantity, id
				cur.executemany(sql, [(itemList[itemName][0], itemList[itemName][1], itemList[itemName][2], pid)])
				conn.commit()

			elif not itemExist and not inventory_[6] is None:
				sql = """
				UPDATE PLAYERS SET INVENTORY = INVENTORY || ARRAY['{name_}', '%s', '%s', '%s'] WHERE PID = %s;
				""".format(name_ = itemName)
				#name, price, quantity, id
				cur.executemany(sql, [(itemList[itemName][0], itemList[itemName][1], itemList[itemName][2], pid)])
				conn.commit()

			elif itemExist:
				sql = """
				UPDATE PLAYERS SET INVENTORY[{item}][2] = %s, INVENTORY[{item}][3] = %s, INVENTORY[{item}][4] = %s WHERE PID = %s;
				""".format(item = item_)
				cur.executemany(sql, [(itemList[itemName][0], itemList[itemName][1], itemList[itemName][2], pid)])
				conn.commit()
			cur.close()
			conn.close()
			res = True
		return res

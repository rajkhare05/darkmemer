from playerData import playerData
from market import market

class player:
	def __init__(self, pid, name, pdsc):
		self.__shop = market()
		self.player_ = playerData()
		self.pid = pid
		self.name = name
		self.pdsc = pdsc
		self.wallet = self.player_.playerProfile(self.pid)[5]
		self.bank = self.player_.playerProfile(self.pid)[4]
		self.userItems = self.inventory() # dict[name] = [price,quantity,id] 
	
	def profile(self):
		profile_ = self.player_.playerProfile(self.pid)
		return 'Name : ' + str(profile_[1]) + '\nWallet : Rs.' + str(profile_[5]) + '\nBank : Rs.' + str(profile_[4])

	def netBalance(self):
		return self.wallet + self.bank
	
	def playerWallet(self):
		return self.wallet
	
	def playerBank(self):
		return self.bank
	
	def spend(self, amount):
		if self.wallet >= amount:
			self.wallet -= amount
			self.player_.updatePlayerData(
				pid = self.pid,
				column = 'wallet',
				upadteValue = self.wallet
			)
			return True
		return False
	
	def addMoney(self, amount):
		'''
		add money to wallet on work or winning games
		'''
		self.wallet += amount
		self.player_.updatePlayerData(
			pid = self.pid,
			column = 'wallet',
			upadteValue = self.wallet
			)
		return True


	def inventory(self):
		itemsOwned = self.player_.playerProfile(self.pid)[6]
		if not itemsOwned is None:
			raw_items = {}
			for item in itemsOwned:
				raw_items[item[0]] = [item[1], item[2], item[3]]
			return raw_items
		return {}

	def withdraw(self, amount: int):
		if self.bank >= amount:
			self.bank -= amount
			self.wallet += amount
			self.player_.updatePlayerData(
				pid = self.pid,
				column = 'wallet',
				upadteValue = self.wallet
			)
			self.player_.updatePlayerData(
				pid = self.pid,
				column = 'bank',
				upadteValue = self.bank
			)
			return True
		return False
	
	def deposit(self, amount: int):
		if self.wallet >= amount:
			self.bank += amount
			self.wallet -= amount
			self.player_.updatePlayerData(
				pid = self.pid,
				column = 'wallet',
				upadteValue = self.wallet
			)
			self.player_.updatePlayerData(
				pid = self.pid,
				column = 'bank',
				upadteValue = self.bank
			)
			return True
		return False
	
	def buyItem(self, name: str, quantity: int):
		#market : id, name, price, quantity
		#items : name, price, quantity, id
		res = False
		globalItems = self.__shop.marketItems()
		for singleItemList in globalItems:
			if name in singleItemList:
				if self.wallet >= quantity * singleItemList[2] and quantity <= singleItemList[3]:
					if self.userItems == {} or not name in [*self.userItems]:
						self.spend(quantity * singleItemList[2])
						self.userItems[name] = [int(singleItemList[2] * quantity), int(quantity), int(singleItemList[0])]
						self.player_.addItemsToInventory(
							itemName = name,
							itemList = self.userItems,
							pid = self.pid
						)
						self.__shop.updateItem(
							id = self.userItems[name][2],
							column = 'quantity',
							updateValue = singleItemList[3] - quantity
						)
						res = True
					else:
						self.spend(quantity * singleItemList[2])
						self.userItems[name][0] = int(self.userItems[name][0]) + int(singleItemList[2] * quantity)
						self.userItems[name][1] = int(self.userItems[name][1]) + quantity
						self.player_.addItemsToInventory(
							itemName = name,
							itemList = self.userItems,
							pid = self.pid
						)
						self.__shop.updateItem(
							id = self.userItems[name][2],
							column = 'quantity',
							updateValue = singleItemList[3] - quantity
						)
						res = True			
		return res

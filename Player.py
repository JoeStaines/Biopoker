class Player():

	def __init__(self, name = "", money = 0):
		self.name = name
		self.money = money
		self.hand = []
		self.betAmount = []
		self.isHandLive = False
		
	def removeMoney(self, amount):
		self.money = self.money - amount
	
	# This function should probably be delegated to main game control class and takes (Player, amount) arguments
	#def makeBet(self, amount):
	
	# This is used when a new round begins
	def resetValues(self):
		self.hand = []
		self.betAmount = 0
		
	def addCard(self, card):
		self.hand.append(card)
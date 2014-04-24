from collections import deque

class Player():
	"""
	Player class that is used in Biopoker
	"""
	
	def __init__(self, name = "", money = 0):
		self.name = name
		self.money = money
		self.hand = []
		self.betAmount = []
		self.isHandLive = False
		
		self.threshValue = 0.0
		self.peaksPerMin = 0
		
		
	def removeMoney(self, amount):
		"""
		Removes from money from the player specified by ``amount``
		"""
		self.money = self.money - amount
	
	
	def resetValues(self):
		"""
		Used when the table needs to make a new round, thus resetting the player's hand and betAmount
		"""
		self.hand = []
		self.betAmount = 0
		
	def addCard(self, card):
		"""
		Add a ``card`` to the player's hand
		"""
		self.hand.append(card)

			
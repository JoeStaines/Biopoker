from collections import deque

class Player():

	def __init__(self, name = "", money = 0):
		self.name = name
		self.money = money
		self.hand = []
		self.betAmount = []
		self.isHandLive = False
		
		self.biodataValuesHigh = deque([], 100)
		self.biodataValuesLow = deque([], 100)
		self.biodataAvgHigh = 0
		self.biodataAvgLow = 0
		
		
	def removeMoney(self, amount):
		self.money = self.money - amount
	
	
	# This is used when a new round begins
	def resetValues(self):
		self.hand = []
		self.betAmount = 0
		
	def addCard(self, card):
		self.hand.append(card)
		
	def addBiodata(self, data):
		if data > 0:
			self.biodataValuesHigh.append(data)
			self.biodataAvgHigh = sum(self.biodataValuesHigh) / len(self.biodataValuesHigh)
			print "Data = {0}".format(data)
			#print "High Avg = {0}\n".format(self.biodataAvgHigh)
		else:
			self.biodataValuesLow.append(data)
			self.biodataAvgLow = sum(self.biodataValuesLow) / len(self.biodataValuesLow)
			print "Data = {0}".format(data)
			#print "Low Avg = {0}\n".format(self.biodataAvgHigh)
			
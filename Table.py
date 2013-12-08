from CustomExceptions import *
import random

class Table():
	def __init__(self):
		self.playerList = [None, None, None, None, None, None]
		self.deck = []
		self.reinitDeck()
		self.pot = 0
		self.currentBet = 0
		self.ante = 0
		self.bigBlind = 0
		self.smallBlind = 0
		self.curDealerSeatNo = 0
		
	def addPlayer(self, player):
		for i in range(len(self.playerList)):
			if self.playerList[i] == None:
				self.playerList[i] = player
				return
		
		# At this point exhausted the list and it's full of players, raise exception
		raise MaxBoundError
		
	def _debugDirectAssign(self, player, pos):
		self.playerList[pos] = player
	
	def removePlayer(self, player):
		for i in range(len(self.playerList)):
			if self.playerList [i] == player:
				self.playerList[i] = None
				return
				
	def reinitDeck(self):
		self.deck = range(52)
		random.shuffle(self.deck)
		
	def addToPot(self, amount):
		self.pot = self.pot + amount
		
	def clearPot(self):
		self.pot = 0
		
	def comparePlayerBet(self, player):
		if player.betAmount < self.currentBet:
			return 1
		elif player.betAmount == self.currentBet:
			return 0
		else:
			return -1
			
	def collectAnte(self):
		for x in self.playerList:
			if x != None:
				x.removeMoney(self.ante)
				self.pot = self.pot + self.ante
	
	def assignDealer(self):
		for n in range(1,6):
			index = (self.curDealerSeatNo + n) % 6
			if self.playerList[index] != None:
				self.curDealerSeatNo = index
				return
				
	# Have to determine whether someone has enough money to pay for blinds, if not then initiate main pot/side pot
		
		
from CustomExceptions import *
import random

class Table():
	def __init__(self):
		self.playerList = [None, None, None, None, None, None]
		self.deck = []
		self.reinitDeck()
		self.pots = [0]
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
		
	def addSidePot(self):
		self.pots.append(0)
		
	def addToPot(self, amount, index):
		self.pots[index] = self.pots[index] + amount
		
	def clearPot(self):
		self.pots = [0]
		
	def comparePlayerBet(self, player):
		if player.betAmount < self.currentBet:
			return 1
		elif player.betAmount == self.currentBet:
			return 0
		else:
			return -1
			
	def collectAnte(self):
		smallest = self._findSmallestMoney()
					
		if smallest < self.ante:
			newAnte = smallest
		else:
			newAnte = self.ante
	
		for x in self.playerList:
			if x != None:
				x.removeMoney(newAnte)
				self.pots[0] = self.pots[0] + newAnte
				
	def _findSmallestMoney(self):
		smallest = 99999999 # Just some high number
		for x in self.playerList:
			if x != None:
				if x.money < smallest:
					smallest = x.money
					
		return smallest
	
	def assignDealer(self):
		_, index = self.findNthPlayerFromDealer(1)
		self.curDealerSeatNo = index
	
	def findNthPlayerFromDealer(self, n):
		for i in range(1,6):
			index = (self.curDealerSeatNo + i) % 6
			if self.playerList[index] != None:
				if n > 1:
					n = n - 1
				else:
					return (self.playerList[index], index)
	
	def noOfPlayers(self):
		number = 0
		for n in range(6):
			if self.playerList[n] != None:
				number = number + 1
		return number
	
	def collectSmallBlind(self):
		if self.noOfPlayers() == 2:
			player = self.playerList[self.curDealerSeatNo]
		else:
			player, seatNo = self.findNthPlayerFromDealer(1)
		player.removeMoney(self.smallBlind)
		self.pots[0] = self.pots[0] + self.smallBlind
		
				
	# Have to determine whether someone has enough money to pay for blinds, if not then initiate main pot/side pot
	
	"""
	if playerbet < potbet
	listOfPlayers = getPlayersInPot(potIndex)
	potBetFotThisIndex = playerbet
	pots[potIndex:potIndex] = playerbet * len(listOfPlayers)
	notifyPlayersPlusPotIndex(listOfPlayers)
	"""
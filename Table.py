from CustomExceptions import *
import random

class Table():
	def __init__(self):
		self.playerList = [None, None, None, None, None, None]
		self.deck = []
		self.reinitDeck()
		self.pots = [0]
		self.potIndex = 0
		self.currentBet = [0] # Bet for each pot if there are side pots
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
		
	def getPlayers(self):
		playerlist = []
		for x in self.playerList:
			if x != None:
				playerlist.append(x)
		return playerlist
		
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
		
	def comparePlayerBet(self, player, i):
		if player.betAmount[i] < self.currentBet[i]:
			return 1
		elif player.betAmount[i] == self.currentBet[i]:
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
		#self.currentBet[0] = self.smallBlind
		if self.noOfPlayers() == 2:
			player = self.playerList[self.curDealerSeatNo]
		else:
			player, seatNo = self.findNthPlayerFromDealer(1)
			
		#self.collectMoney(player, self.smallBlind)
			
		if player.money < self.smallBlind:
			self.pots[self.potIndex:self.potIndex] = [player.money]
			self.currentBet[self.potIndex:self.potIndex] = [player.money]
			player.potContrib = self.potIndex
			player.betAmount.append(player.money)
			player.money = 0
			self.potIndex = self.potIndex + 1
		else:
			player.removeMoney(self.smallBlind)
			self.pots[0] = self.pots[0] + self.smallBlind
			player.potContrib = self.potIndex
			player.betAmount.append(self.smallBlind)
	
	def collectBigBlind(self):
		self.setBigBlindBetAmount()
		if self.noOfPlayers() == 2:
			player, seatNo = self.findNthPlayerFromDealer(1)
		else:
			player, seatNo = self.findNthPlayerFromDealer(2)
		self.collectMoney(player, self.bigBlind)
		self.setBigBlindBetAmount() # Need to do this again because even if blind cant be paid, 
									# next player still has to pay full blind
		
	def setBigBlindBetAmount(self):
		if sum(self.currentBet) < self.bigBlind:
			if self.potIndex > 0:
				newbet = self.bigBlind - sum(self.currentBet)
			else:
				newbet = self.bigBlind
			self.currentBet[self.potIndex] = newbet
			
	def collectMoney(self, player, amount):
		for i in range(self.potIndex + 1):
			if player.money < self.currentBet[i]:
				self._slicePot(player.money, i)
				player.potContrib = i
				player.betAmount[i] = player.money
				player.money = 0
				self.potIndex = self.potIndex + 1
				return
			else:
				player.removeMoney(self.currentBet[i])
				self.pots[i] = self.pots[i] + self.currentBet[i]
				player.potContrib = i
				player.betAmount.append(self.currentBet[i])
				amount = amount - self.currentBet[i]
				
	def _slicePot(self, amount, i):
		self.pots[i:i] = [amount]
		self.pots[i+1] = 0 # Going to re-evaluate this soon
		#print "Before: {0}".format(self.currentBet)
		self.currentBet[i:i] = [amount]
		self.currentBet[i+1] = self.currentBet[i+1] - self.currentBet[i]
		#print "After : {0}".format(self.currentBet)
		for x in self.getPlayers():
			if x.potContrib >= i:
				x.betAmount[i:i] = [amount]
				x.betAmount[i+1] = x.betAmount[i+1] - x.betAmount[i]
				self.pots[i] = self.pots[i] + amount
				self.pots[i+1] = self.pots[i+1] + x.betAmount[i+1]
				x.potContrib = x.potContrib + 1
		self.potIndex = self.potIndex + 1
		
			
		
				
	# Have to determine whether someone has enough money to pay for blinds, if not then initiate main pot/side pot
	
	"""
	if playerbet < potbet
	listOfPlayers = getPlayersInPot(potIndex)
	potBetFotThisIndex = playerbet
	pots[potIndex:potIndex] = playerbet * len(listOfPlayers)
	notifyPlayersPlusPotIndex(listOfPlayers)
	"""
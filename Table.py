from CustomExceptions import *
import random

class Table():
	def __init__(self):
		self.playerList = [None, None, None, None, None, None]
		self.deck = []
		self.reinitDeck()
		self.pots = [0]
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
		_, index = self.findNthPlayerFromSeat(self.curDealerSeatNo, 1)
		self.curDealerSeatNo = index
					
	def findNthPlayerFromSeat(self, seat, n):
		for i in range(1,6):
			index = (seat + i) % 6
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
			player, seatNo = self.findNthPlayerFromSeat(self.curDealerSeatNo, 1)
			
		#self.collectMoney(player, self.smallBlind)
			
		if player.money < self.smallBlind:
			self.pots[-1:-1] = [player.money]
			self.currentBet[-1:-1] = [player.money]
			player.betAmount.append(player.money)
			player.money = 0
		else:
			player.removeMoney(self.smallBlind)
			self.pots[0] = self.pots[0] + self.smallBlind
			player.betAmount.append(self.smallBlind)
	
	def collectBigBlind(self):
	
		self.setBigBlindBetAmount()
		if self.noOfPlayers() == 2:
			player, seatNo = self.findNthPlayerFromSeat(self.curDealerSeatNo, 1)
		else:
			player, seatNo = self.findNthPlayerFromSeat(self.curDealerSeatNo, 2)
		self.collectMoney(player, self.bigBlind)
		self.setBigBlindBetAmount() # Need to do this again because even if blind cant be paid, 
									# next player still has to pay full blind
		
	def setBigBlindBetAmount(self):
		if sum(self.currentBet) < self.bigBlind:
			if len(self.pots) > 1:
				newbet = self.bigBlind - sum(self.currentBet)
			else:
				newbet = self.bigBlind
			self.currentBet[-1] = newbet
			
	def collectMoney(self, player, amount):
		rangestart = len(player.betAmount) if len(player.betAmount) >= 0 else 0
		for i in range(rangestart, len(self.pots)):
			if player.money < self.currentBet[i]:
				self._slicePot(player.money, i)
				player.betAmount.append(player.money)
				player.money = 0
				return
			else:
				player.removeMoney(self.currentBet[i])
				self.pots[i] = self.pots[i] + self.currentBet[i]
				player.betAmount.append(self.currentBet[i])
				amount = amount - self.currentBet[i]
				
		if amount > 0:
			player.removeMoney(amount)
			self.pots[-1] = self.pots[-1] + amount
			player.betAmount[-1] = player.betAmount[-1] + amount
			self.currentBet[-1] = player.betAmount[-1]
				
	def _slicePot(self, amount, i):
		self.pots[i:i] = [amount]
		self.pots[i+1] = 0 # Going to re-evaluate this soon
		self.currentBet[i:i] = [amount]
		self.currentBet[i+1] = self.currentBet[i+1] - self.currentBet[i]
		for x in self.getPlayers():
			if len(x.betAmount)-1 >= i:
				playerBetAmount = x.betAmount[i]
				x.betAmount[i:i] = [amount] if amount < playerBetAmount else [playerBetAmount]
				x.betAmount[i+1] = playerBetAmount - x.betAmount[i]
				self.pots[i] = self.pots[i] + x.betAmount[i]
				self.pots[i+1] = self.pots[i+1] + x.betAmount[i+1]
				self._pruneBetAmount(x)
		
	def _pruneBetAmount(self, player):
		if player.betAmount[-1] == 0:
			player.betAmount.pop()
			
	def makeBet(self, player, amount):
		self.collectMoney(player, amount)
		
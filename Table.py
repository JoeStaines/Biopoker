from CustomExceptions import *
from SevenEval import *
import random, math

class Table():
	
	PRE_FLOP = 0
	FLOP = 1
	TURN = 2
	RIVER = 3
	SHOWDOWN = 4
		
	def __init__(self):
		self.initialiseTable()
		self.evaluator = SevenEval()
		
	def initialiseTable(self):
		self.stateDict = {}
		self.playerList = [None, None, None, None, None, None]
		self.deck = []
		self.reinitDeck()
		self.communityCards = []
		self.pots = [0]
		self.currentBet = [0] # Bet for each pot if there are side pots
		self.ante = 0
		self.bigBlind = 0
		self.smallBlind = 0
		self.curDealerSeatNo = 0
		self.turn = 0
		self.roundEndSeat = 0
		self.gameState = Table.PRE_FLOP
		
	def setState(self):
		self.stateDict = {'playerlist': self.playerList[:], \
							'comcards': self.communityCards[:], \
							'pots':		self.pots[:], \
							'curbet':	self.currentBet[:], \
							'turn':		self.turn }
		
	def addPlayer(self, player):
		for i in range(len(self.playerList)):
			if self.playerList[i] == None:
				self.playerList[i] = player
				return
		
		# At this point exhausted the list and it's full of players, raise exception
		raise MaxBoundError
		
	def getPlayers(self):
		return self.getAndFilterPlayers(lambda x: x)
		
	def getAndFilterPlayers(self, filterFunc):
		playerlist = []
		for x in self.playerList:
			if x != None:
				player = filterFunc(x)
				if player != None:
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
		for i in range(1,7):
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
				self._slicePot(i, player)
				return
			else:
				player.removeMoney(self.currentBet[i])
				self.pots[i] = self.pots[i] + self.currentBet[i]
				player.betAmount.append(self.currentBet[i])
				amount = amount - self.currentBet[i]
				
		if amount > 0:
			if player.money < self.currentBet[-1]:
				self._slicePot(len(self.pots)-1, player)
			else: # TODO: Might need to put something here that expresses when someone raises but will put them all in
				player.removeMoney(amount)
				self.pots[-1] = self.pots[-1] + amount
				player.betAmount[-1] = player.betAmount[-1] + amount
				self.currentBet[-1] = player.betAmount[-1]
				
	def _slicePot(self, i, player):
		if len(player.betAmount) < len(self.currentBet):
			player.betAmount.append(player.money)
		else:
			player.betAmount[i] = player.betAmount[i] + player.money
		player.money = 0
		self.pots[i:i] = [0]
		self.pots[i+1] = 0 # Going to re-evaluate this soon
		self.currentBet[i:i] = [player.betAmount[i]]
		self.currentBet[i+1] = self.currentBet[i+1] - self.currentBet[i]
		for x in self.getPlayers():
			if len(x.betAmount)-1 >= i:
				xBetAmount = x.betAmount[i]
				x.betAmount[i:i] = [player.betAmount[i]] if player.betAmount[i] < xBetAmount else [xBetAmount]
				x.betAmount[i+1] = xBetAmount - x.betAmount[i]
				self.pots[i] = self.pots[i] + x.betAmount[i]
				self.pots[i+1] = self.pots[i+1] + x.betAmount[i+1]
				self._pruneBetAmount(x)
		
	def _pruneBetAmount(self, player):
		if player.betAmount[-1] == 0:
			player.betAmount.pop()

	def determineAmountToCall(self, player):
		return sum(self.currentBet) - sum(player.betAmount)
	
	def makeBet(self, player, amount):
		self.collectMoney(player, amount)
		self.setNextTurn()
		
	def setNextTurn(self):
		liveplayers = self.getLivePlayers()
		if len(liveplayers) == 1:
			winner = liveplayers.pop()
			for i in range(len(winner.betAmount)):
				self.handOutMoney([winner], i)
			self.setUpNextGameRound()	
		else:
			playerUnsuitable = True
			while playerUnsuitable:
				if self.roundEndSeat == self.turn:
					self.setUpNextBetRound()
					playerUnsuitable = False
				else:
					_, self.turn = self.findNthPlayerFromSeat(self.turn, 1)
					if self.playerList[self.turn].money > 0 and self.playerList[self.turn].isHandLive == True:
						playerUnsuitable = False
					
	def findNextSuitablePlayer(self, n):
		while True:
			player, seat = self.findNthPlayerFromSeat(n, 1)
			if self.playerList[seat].money > 0 and self.playerList[seat].isHandLive == True:
				return (player, seat)
			else:
				n = seat

	def deal(self):
		playerList = self.getPlayers()
		start = self.curDealerSeatNo + 1
		for i in range(len(playerList)*2):
			playerList[(start + i) % len(playerList)].hand.append(self.deck.pop())
			playerList[(start + i) % len(playerList)].isHandLive = True
			
	def dealCommunity(self, num):
		for _ in range(num):
			self.communityCards.append(self.deck.pop())
			
	def determineBlinds(self):
		self.smallBlind = 5
		self.bigBlind = 10
		
	def call(self, player):
		self.makeBet(player, self.determineAmountToCall(player))
		self.setState()
		
	def raiseBet(self, player, amount):
		_, self.roundEndSeat = self.findNthPlayerFromSeat(self.turn, self.noOfPlayers()-1)
		self.makeBet(player, self.determineAmountToCall(player)+amount)
		self.setState()
		
	def fold(self, player):
		player.isHandLive = False
		self.setNextTurn()
		self.setState()
	
	def setUpNextBetRound(self):
		if self.gameState == Table.PRE_FLOP:
			self.gameState = Table.FLOP
			self.dealCommunity(3)
			_, self.turn = self.findNextSuitablePlayer(self.curDealerSeatNo)
			self.roundEndSeat = self.curDealerSeatNo
		elif self.gameState == Table.FLOP:
			self.gameState = Table.TURN
			self.dealCommunity(1)
			_, self.turn = self.findNextSuitablePlayer(self.curDealerSeatNo)
			self.roundEndSeat = self.curDealerSeatNo
		elif self.gameState == Table.TURN:
			self.gameState = Table.RIVER
			self.dealCommunity(1)
			_, self.turn = self.findNextSuitablePlayer(self.curDealerSeatNo)
			self.roundEndSeat = self.curDealerSeatNo
		elif self.gameState == Table.RIVER:
			self.gameState = Table.SHOWDOWN
			self.evaluateWinner()
			self.setUpNextGameRound()
			# Do showdown stuff here (evaluate hands, hand out pot, get ready for next game)
		
	def getPlayersInPot(self, potIndex, livePlayers):
		players = []
		for x in livePlayers:
			if len(x.betAmount) > potIndex:
				players.append(x)
		return players
		
	def getLivePlayers(self):
		return self.getAndFilterPlayers(lambda x: x if x.isHandLive == True else None)
	
	def getWinners(self, evaluations, potIndex):
		# What evaluations looks like -> [(playerObj, handScore)]
		winners = []
		evaluations.sort(key=lambda x: x[1], reverse=True)
		highest = evaluations[0][1]
		for x in evaluations:
			if x[1] == highest:
				winners.append(x[0])
			else:
				break
		return winners
		
	def handOutMoney(self, winners, potIndex):
		amountWon = math.floor(self.pots[potIndex] / len(winners))
		remainder = self.pots[potIndex] - (amountWon * len(winners))
		for x in winners:
			x.money = x.money + amountWon
		
		# Player left of dealer is considered 'worst position', so remainder goes to that player
		player = self.findWinnerNextToDealer(winners)
		player.money = player.money + remainder
			
	def findWinnerNextToDealer(self, winners):
		curIndex = self.curDealerSeatNo
		while True:
			player, seat = self.findNthPlayerFromSeat(curIndex, 1)
			for x in winners:
				if x == player:
					return player
			curIndex = seat
		
	
	def evaluateWinner(self):
		livePlayers = self.getLivePlayers()	
		for i in range(len(self.pots)):
			players = self.getPlayersInPot(i, livePlayers)
			evaluations = []
			for x in players:
				combined = x.hand + self.communityCards
				evaluations.append((x, self.evaluator.getRankOfSeven(	combined[0], \
																		combined[1], \
																		combined[2], \
																		combined[3], \
																		combined[4], \
																		combined[5], \
																		combined[6] )))
			winners = self.getWinners(evaluations, i)
			self.handOutMoney(winners, i)
	
	
	# ############ Game Loop Logic ############
	
	def setUpNextGameRound(self):
		self.pots = [0]
		self.currentBet = [0]
		self.reinitDeck()
		self.communityCards = []
		allPlayers = self.getPlayers()
		self.resetPlayerHands(allPlayers)
		self.resetPlayerBetAmount(allPlayers)
		_, seat = self.findNthPlayerFromSeat(self.curDealerSeatNo, 1)
		self.curDealerSeatNo = seat
		self.beginRound()
		
	def resetPlayerHands(self, players):
		for x in players:
			x.hand = []
			
	def resetPlayerBetAmount(self, players):
		for x in players:
			x.betAmount = []
	
	def beginRound(self):
		self.gameState = Table.PRE_FLOP
		self.determineBlinds()
		self.collectSmallBlind()
		self.collectBigBlind()
		self.deal()
		self.setState()
		if self.noOfPlayers == 2:
			self.turn = self.curDealerSeatNo
			self.roundEndSeat = self.findNthPlayerFromSeat(self.turn, 1)
		else:
			_, self.turn = self.findNthPlayerFromSeat(self.curDealerSeatNo, 3)
			_, self.roundEndSeat = self.findNthPlayerFromSeat(self.curDealerSeatNo, 2)
		
		
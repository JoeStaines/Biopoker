from CustomExceptions import *
from SevenEval import *
import random, math
from collections import deque

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
		self.playerRemoveList = [] # Add player to be removed here. Removed at next round
		self.playerList = [None, None, None, None, None, None] # Used for everyone in game and has money to play
		self.deck = []
		self.reinitDeck()
		self.communityCards = []
		self.pots = [0]
		self.currentBet = [0] # Bet for each pot if there are side pots
		self.isGameEnd = False
		self.ante = 0
		self.bigBlind = 0
		self.smallBlind = 0
		self.curDealerSeatNo = 0
		self.turn = 0
		self.roundEndSeat = 0
		self.roundNo = 0
		self.potwinQ = deque([], 100)
		self.allinQ = deque([], 100)
		self.gameState = Table.PRE_FLOP
		
	def setState(self):
		"""
		Sets up a dictionary of the current state of the game that will be sent and used by the clients
		"""
		self.stateDict = {'playerlist': self.playerList[:], \
							'comcards': self.communityCards[:], \
							'pots':		self.pots[:], \
							'curbet':	self.currentBet[:], \
							'turn':		self.turn, \
							'isGameEnd': self.isGameEnd}
		
	def addPlayer(self, player):
		"""
		Adds a ``player`` to the game
		
		Raises a ``MaxBoundError`` if the player list is full and cannot be added
		"""
		for i in range(len(self.playerList)):
			if self.playerList[i] == None:
				self.playerList[i] = player
				return i
		
		# At this point exhausted the list and it's full of players, raise exception
		raise MaxBoundError
		
	def getPlayers(self):
		"""
		Makes a call to :func:`getAndFilterPlayers` and returns all players in the game
		"""
		return self.getAndFilterPlayers(lambda x: x)
		
	def getLivePlayers(self):
		"""
		Makes a call to :func:`getAndFilterPlayers` and returns all players that are still live 
		(a.k.a have not folded)
		"""
		return self.getAndFilterPlayers(lambda x: x if x.isHandLive == True else None)
		
	def getSuitablePlayers(self):
		"""
		Makes a call to :func:`getAndFilterPlayers` and returns all players that are live and have
		more than 0 money
		"""
		return self.getAndFilterPlayers(lambda x: x if x.isHandLive == True and x.money > 0 else None)
		
	def getAndFilterPlayers(self, filterFunc):
		"""
		Central function that is called by other 'getPlayer' like functions
		
		``filterFunc`` is a function which other functions can specify (using lambdas usually)
		in order to filter specific types of players in the game.
		"""
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
		"""
		Removes a player from the playerlist
		"""
		for i in range(len(self.playerList)):
			if self.playerList [i] == player:
				self.playerList[i] = None
				return
				
	def removeFromPlayerList(self):
		"""
		Removes all the players that are defined in ``self.playerRemoveList``
		"""
		for x in self.playerRemoveList:
			self.removePlayer(x)
				
	def reinitDeck(self):
		"""
		Creates a new shuffled deck of cards
		"""
		self.deck = range(52)
		random.shuffle(self.deck)
		
	def addSidePot(self):
		"""
		Adds a new side pot
		"""
		self.pots.append(0)
		
	def addToPot(self, amount, index):
		"""
		Add to pot at ``index`` by ``amount``
		"""
		self.pots[index] = self.pots[index] + amount
		
	def clearPot(self):
		"""
		Resets the pot completely so there is just one mainpot and no sidepots
		"""
		self.pots = [0]
		
	def comparePlayerBet(self, player, i):
		"""
		Compares a player's betAmount with the current bet at index ``i``. Used to determine if the ``player``
		has met the current bet completely
		
		Returns:
		
		* ``1`` if the player's bet amount is less than the current bet amount for the pot
		* ``0`` if the player's bet amount is equal
		* ``-1`` if the player's bet amount is greater
		"""
		if player.betAmount[i] < self.currentBet[i]:
			return 1
		elif player.betAmount[i] == self.currentBet[i]:
			return 0
		else:
			return -1
			
	def removePlayerMoney(self, player, amount):
		"""
		Invoke the function in the ``Player`` class to remove the money from the `player` specified by 
		the `amount`. Then checks if the player's amount is 0 and if it is, will report to the all in 
		event queue that `player` went all in
		"""
		player.removeMoney(amount)
		if player.money == 0:
			self.allinQ.append(player.name)
			
	def collectAnte(self):
		"""
		Collects the ante from all players
		
		If a player has a total amount of money that is less than the defined ante, then it uses that value
		as the new ante that is taken from everyone else
		"""
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
		"""
		Find who has the least amount of money out of all the players and returns the amount that was smallest
		"""
		smallest = 99999999 # Just some high number
		for x in self.playerList:
			if x != None:
				if x.money < smallest:
					smallest = x.money
					
		return smallest
	
	def assignDealer(self):
		"""
		Finds the next player next to the current dealer to be the new dealer
		"""
		_, index = self.findNthPlayerFromSeat(self.curDealerSeatNo, 1)
		self.curDealerSeatNo = index
					
	def findNthPlayerFromSeat(self, seat, n):
		"""
		From a starting point ``seat``, it goes around in clockwise order to find the next player that
		is ``n`` seats away
		"""
		for i in range(1,7):
			index = (seat + i) % 6
			if self.playerList[index] != None:
				if n > 1:
					n = n - 1
				else:
					return (self.playerList[index], index)
	
	def noOfPlayers(self):
		"""
		Return the number of players in the game
		"""
		number = 0
		for n in range(6):
			if self.playerList[n] != None:
				number = number + 1
		return number
	
	def collectSmallBlind(self):
		"""
		Determines who is responsible for paying the small blind and collects it
		"""
		if self.noOfPlayers() == 2:
			player = self.playerList[self.curDealerSeatNo]
		else:
			player, seatNo = self.findNthPlayerFromSeat(self.curDealerSeatNo, 1)
			
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
		"""
		Determines who is responsible for paying the big blind and collects it.
		
		Resets the 'call' value so the next player still has to pay the full amount even if
		the player who pays the big blind couldn't do so because of a lack of money
		"""
		self.setBigBlindBetAmount()
		if self.noOfPlayers() == 2:
			player, seatNo = self.findNthPlayerFromSeat(self.curDealerSeatNo, 1)
		else:
			player, seatNo = self.findNthPlayerFromSeat(self.curDealerSeatNo, 2)
		self.collectMoney(player, self.bigBlind)
		self.setBigBlindBetAmount() # Need to do this again because even if blind cant be paid, 
									# next player still has to pay full blind
		
	def setBigBlindBetAmount(self):
		"""
		Sets the big blind amount
		"""
		if sum(self.currentBet) < self.bigBlind:
			if len(self.pots) > 1:
				newbet = self.bigBlind - sum(self.currentBet)
			else:
				newbet = self.bigBlind
			self.currentBet[-1] = newbet
			
	def collectMoney(self, player, amount):
		"""
		This function is responsible for collecting the money and accurately setting the bet amounts for
		the pots and the players
		
		Steps through all the side bets in turn and pays the current bet for each side pot. If a player
		cannot pay, then the another side pot is created using :func:`_slicePot`
		"""
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
				#player.removeMoney(amount)
				self.removePlayerMoney(player, amount)
				self.pots[-1] = self.pots[-1] + amount
				player.betAmount[-1] = player.betAmount[-1] + amount
				self.currentBet[-1] = player.betAmount[-1]
				
	def _slicePot(self, i, player):
		"""
		Auxiliary function to :func:`collectMoney`. Will create a new side pot and re-evaluates the necessary side
		pots and every player's bet amount so that they accurate reflect the true state of the pots
		"""
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
		"""
		Auxiliary function to :func:`_slicePot`. Just pops the bet amount list if there is an extra ``0``
		on the end
		"""
		if player.betAmount[-1] == 0:
			player.betAmount.pop()

	def determineAmountToCall(self, player):
		"""
		Determines the amount of money the ``player`` has to call to stay in the round
		"""
		return sum(self.currentBet) - sum(player.betAmount)
	
	def makeBet(self, player, amount):
		"""
		Collects the money for the bet through :func:'collectMoney' and sets the next turn through
		:func:`setNextTurn`
		"""
		self.collectMoney(player, amount)
		self.setNextTurn()
		
	def setNextTurn(self):
		"""
		Determines whose turn it is next from the list of live players
		
		Can determine the winner if all previous players have folded and there is only one live player left
		"""
		liveplayers = self.getLivePlayers()
		if len(liveplayers) == 1:
			winner = liveplayers.pop()
			for i in range(len(winner.betAmount)):
				self.handOutMoney([winner], i)
			self.setUpNextGameRound()
		elif len(self.getSuitablePlayers()) == 0:
			self.earlyEvaluation()
		else:
			playerUnsuitable = True
			while playerUnsuitable:
				if self.roundEndSeat == self.turn:
					self.setUpNextBetRound()
					playerUnsuitable = False
				else:
					_, self.turn = self.findNthPlayerFromSeat(self.turn, 1)
					if self.playerList[self.turn] in self.playerRemoveList:
						self.playerList[self.turn].isHandLive = False
					if self.playerList[self.turn].money > 0 and self.playerList[self.turn].isHandLive == True:
						playerUnsuitable = False
					
	def findNextSuitablePlayer(self, n):
		"""
		Finds the next suitable player that can take action.
		"""
		for _ in range(len(self.getPlayers())):
			player, seat = self.findNthPlayerFromSeat(n, 1)
			if self.playerList[seat].money > 0 and self.playerList[seat].isHandLive == True:
				return (player, seat)
			else:
				n = seat

	def deal(self):
		"""
		Deals the cards out from ``self.deck``
		
		Emulates real poker in the sense that it goes through each player one card at a time
		until they all have 2 cards
		"""
		playerList = self.getPlayers()
		start = self.curDealerSeatNo + 1
		for i in range(len(playerList)*2):
			playerList[(start + i) % len(playerList)].hand.append(self.deck.pop())
			playerList[(start + i) % len(playerList)].isHandLive = True
			
	def dealCommunity(self, num):
		"""
		Deal a certain number of community cards from ``self.deck``. The number to deal is determined by the
		parameter ``num``
		"""
		for _ in range(num):
			self.communityCards.append(self.deck.pop())
			
	def determineBlinds(self):
		"""
		Determine the initial big and small blind amounts
		"""
		self.smallBlind = 5
		self.bigBlind = 10
		
	def call(self, player):
		"""
		Makes a call to :func:`makeBet` using the value from :func:`determineAmountToCall`
		"""
		self.makeBet(player, self.determineAmountToCall(player))
		self.setState()
		
	def raiseBet(self, player, amount):
		"""
		Raises the bet. The raise bet is the value returned from :func:`determineAmountToCall` + ``amount``
		"""
		_, self.roundEndSeat = self.findNthPlayerFromSeat(self.turn, self.noOfPlayers()-1)
		self.makeBet(player, self.determineAmountToCall(player)+amount)
		self.setState()
		
	def fold(self, player):
		"""
		Fold the ``player``'s hand
		"""
		player.isHandLive = False
		self.setNextTurn()
		self.setState()
	
	def setUpNextBetRound(self):
		"""
		Determines at what betting round the current game is at (preflop, flop, turn, river).
		
		Depending on what betting round it is, community cards are dealt here and also determines the player
		who starts off the betting round
		"""
		if self.gameState == Table.PRE_FLOP:
			self.gameState = Table.FLOP
			self.dealCommunity(3)
			player = self.findNextSuitablePlayer(self.curDealerSeatNo)
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
			
	def earlyEvaluation(self):
		"""
		Called from :func:`makeBet` when there is a situation where there are no suitable players
		but there are still live hands that need to be won. This happens when multiple players are all in
		and there is no one to check through the rest of the betting rounds
		"""
		self.dealCommunity(5 - len(self.communityCards))
		self.gameState = Table.SHOWDOWN
		self.evaluateWinner()
		self.setUpNextGameRound()
		
	def getPlayersInPot(self, potIndex, livePlayers):
		"""
		Called from :func:`evaluateWinner`. From the list of `livePlayers`, gets all of the players in the
		pot at `potIndex`
		"""
		players = []
		for x in livePlayers:
			if len(x.betAmount) > potIndex:
				players.append(x)
		return players
	
	
	def getWinners(self, evaluations, potIndex):
		"""
		Called from :func:`evaluateWinner`. Determines the winner(s) of the point defined at `potIndex`.
		
		There can be more than one winner if 2 or more players have a hand that has the same rank in poker
		"""
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
		"""
		Called from :func:`evaluateWinner`. Hands out the spoils to all of the winners. This is at the side pot
		level, not the whole pot, so the spoils are distributed evenly if there is more than one winner.
		
		If there is a remainder after the money has been distributed, a call to :func:`findWinnerNextToDealer`
		is made and the remainder goes to that player
		"""
		amountWon = math.floor(self.pots[potIndex] / len(winners))
		remainder = self.pots[potIndex] - (amountWon * len(winners))
		for x in winners:
			x.money = x.money + amountWon
		
		# Player left of dealer is considered 'worst position', so remainder goes to that player
		player = self.findWinnerNextToDealer(winners)
		player.money = player.money + remainder
			
	def findWinnerNextToDealer(self, winners):
		"""
		Called from :func:`handOutMoney`. From the list of `winners`, then winner closest to the dealer 
		is found
		"""
		curIndex = self.curDealerSeatNo
		while True:
			player, seat = self.findNthPlayerFromSeat(curIndex, 1)
			for x in winners:
				if x == player:
					return player
			curIndex = seat
		
	
	def evaluateWinner(self):
		"""
		Top level function for evaluating the winner(s). Gets all the current live players and evaluates
		their 7-card hand in terms of rank and the pot is distributed among the winners 
		"""
		if self.pots[-1] == 0:
			self.pots.pop()
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
			self.potwinQ.append(winners[0].name)
	
	
	# ############ Game Loop Logic ############
	
	def setUpNextGameRound(self):
		"""
		Resets various variables to make a clean game for the next round.
		
		Also responsible for determining the correct seat to be the next dealer
		"""
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
		"""
		From the list of `players`, resets their current hand ready for the next round
		"""
		for x in players:
			x.hand = []
			
	def resetPlayerBetAmount(self, players):
		"""
		From the list of `players`, resets their current bet amount ready for the next round
		"""
		for x in players:
			x.betAmount = []
	
	def beginRound(self):
		"""
		Removes any players who have no money left for this round and starts collecting the blinds 
		"""
		self.gameState = Table.PRE_FLOP
		for p in self.getPlayers():
			if p.money <= 0:
				self.playerRemoveList.append(p)
		self.removeFromPlayerList()
		if len(self.getPlayers()) == 1:
			self.isGameEnd = True
		else:
			self.roundNo += 1
			self.determineBlinds()
			self.collectSmallBlind()
			self.collectBigBlind()
			self.deal()
			self.setState()
			if self.noOfPlayers() == 2:
				self.turn = self.curDealerSeatNo
				_, self.roundEndSeat = self.findNthPlayerFromSeat(self.turn, 1)
			else:
				_, self.turn = self.findNthPlayerFromSeat(self.curDealerSeatNo, 3)
				_, self.roundEndSeat = self.findNthPlayerFromSeat(self.curDealerSeatNo, 2)
		
		
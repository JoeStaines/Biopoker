from SevenEval import *
from CardEnum import CardEnum as C
from Cards import Cards
import random

class PokerGame:
	def __init__(self):
		self.cardsobj = Cards()
		self.deck = range(52)
		self.shuffleDeck(self.deck)
		self.communitycards = []
		self.numplayers = 2
		self.playerhands = [[] for _ in range(0,self.numplayers)]
		self.deal(self.deck, self.numplayers, self.playerhands)
		self.evaluator = SevenEval()
		self.printPlayerHands(self.playerhands)
		
	def printPlayerHands(self, playerhands):
		for n in range(0,len(playerhands)):
			formatted = ', '.join(self.cardsobj.convertNumToCards(playerhands[n]))
			print "Player %d: %s" % (n+1, formatted)
		
	def shuffleDeck(self, deckIn):
		random.shuffle(deckIn)

	def deal(self, deckIn, players, playerhands):
		# players * 2 since need to give each player 2 cards
		for n in range(0,players*2):
			playerhands[n % players].append(deckIn.pop())
	
	def dealCommunity(self, deckIn, num):
		for n in range(0,num):
			self.communitycards.append(deckIn.pop())
			
	def combineCards(self, community, playerhands):
		newhands = [[] for _ in range(0,len(playerhands))]
		for n in range(0,len(playerhands)):
			newhands[n] = playerhands[n] + community
		return newhands
			
	def evaluateHands(self, hands):
		evaluations = [0] * len(hands)
		for n in range(0, len(hands)):
			curhand = hands[n]
			card1 = curhand[0]
			card2 = curhand[1]
			card3 = curhand[2]
			card4 = curhand[3]
			card5 = curhand[4]
			card6 = curhand[5]
			card7 = curhand[6]
			evaluations[n] = self.evaluator.getRankOfSeven(card1, card2, card3, card4, card5, card6, card7)
		return evaluations
		
	def findHighestIndex(self, list):
		highest = 0
		for n in range(1, len(list)):
			if list[n] > list[highest]:
				highest = n
		return highest
	
	def simpleGameLoop(self):
		# Burn + Flop
		self.deck.pop()
		self.dealCommunity(self.deck, 3)
		print self.cardsobj.convertNumToCards(self.communitycards)
		raw_input()

		# Burn + Turn
		self.deck.pop()
		self.dealCommunity(self.deck, 1)
		print self.cardsobj.convertNumToCards(self.communitycards)
		raw_input()
		
		# Burn + River
		self.deck.pop()
		self.dealCommunity(self.deck, 1)
		print self.cardsobj.convertNumToCards(self.communitycards)
		raw_input()
		
		combined = self.combineCards(self.communitycards, self.playerhands)
		results = self.evaluateHands(combined)
		winnerIndex = self.findHighestIndex(results)
		
		self.printPlayerHands(combined)
		print results
		print "Player %d wins" % (winnerIndex+1)
		
		

if __name__ == "__main__":
	pokergame = PokerGame()
	pokergame.simpleGameLoop()
	
	"""
	s = SevenEval()
	rf1 = s.getRankOfSeven(C._As,C._Ks,C._Qs,C._Js,C._Ts,C._Kd,C._Kc)
	print rf1
	rf2 = s.getRankOfSeven(0,4,8,12,16,6,7)
	print rf2
	rf = s.getRankOfSeven(0,4,8,12,16,25,26)
	four = s.getRankOfSeven(0,1,2,3,4,,6)
	sf = s.getRankOfSeven(48,44,40,36,32,28,24)
	f = s.getRankOfSeven(48,44,4,24,16,8,25)
	print rf
	print sf
	print f
	"""
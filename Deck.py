import random

class Deck():
	def __init__(self):
		self.reinitDeck()
		
	def reinitDeck(self):
		self.deck = range(52)
		random.shuffle(self.deck)
import unittest
from ..Player import Player
from ..Deck import Deck

class testPlayerSetUp(unittest.TestCase):
	def setUp(self):
		self.playerObj = Player("John", 1000)
		
class testRemovesMoney(testPlayerSetUp):
	def testRemoveMoney(self):
		self.playerObj.removeMoney(100)
		self.assertEquals(self.playerObj.money, 900)
		
class testResetValues(testPlayerSetUp):
	def testResetValues(self):
		self.playerObj.resetValues()
		self.assertEquals(self.playerObj.hand, [])
		self.assertEquals(self.playerObj.betAmount, 0)
		
class testAddCardToHand(testPlayerSetUp):
	def testAddCard(self):
		self.d = Deck()
		self.playerObj.addCard(self.d.deck.pop())
		self.assertTrue(len(self.playerObj.hand) == 1)

if __name__ == "__main__":
	unittest.main()
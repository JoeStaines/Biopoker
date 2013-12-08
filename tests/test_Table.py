import unittest
from ..Table import Table
from ..Player import Player
from ..CustomExceptions import *

class TestTableSetUp(unittest.TestCase):
	def setUp(self):
		self.table = Table()
		self.p1 = Player("", 1000)
		self.p2 = Player("", 1000)
		self.p3 = Player("", 1000)
		self.p4 = Player("", 1000)
		self.p5 = Player("", 1000)
		self.p6 = Player("", 1000)
		self.p7 = Player("", 1000)

class TestInitPlayerList(TestTableSetUp):
	def testListLengthIsSix(self):
		self.assertTrue(len(self.table.playerList) == 6)

	def testAllListSetToNone(self):
		for x in self.table.playerList:
			self.assertTrue(x == None)
		

class TestAddPlayerToList(TestTableSetUp):
	def testAddSinglePlayer(self):
		self.table.addPlayer(Player())
		self.assertTrue(isinstance(self.table.playerList[0], Player))
		
	def testAddTwoPlayers(self):
		self.table.addPlayer(Player())
		self.table.addPlayer(Player())
		self.assertTrue(isinstance(self.table.playerList[0], Player))
		self.assertTrue(isinstance(self.table.playerList[1], Player))
		
	def testAddSixPlayers(self):
		for i in range(6):
			self.table.addPlayer(Player())
			
		for i in range(6):
			self.assertTrue(isinstance(self.table.playerList[i], Player))
			
	def testRaiseExceptionAddSevenPlayers(self):
		for i in range(6):
			self.table.addPlayer(Player())
			
		with self.assertRaises(MaxBoundError):
			self.table.addPlayer(Player())

			
class TestRemovePlayerFromList(TestTableSetUp):
				
	def testAddOneRemoveOne(self):
		self.table.addPlayer(self.p1)
		self.table.removePlayer(self.p1)
		self.assertTrue(self.table.playerList[0] != self.p1)
		
	def testAddTwoRemoveFirst(self):
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.removePlayer(self.p1)
		self.assertTrue(self.table.playerList[0] != self.p1)
		self.assertTrue(self.table.playerList[1] == self.p2)
		
	def testAddSixRemoveTwoAddOne(self):
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.addPlayer(self.p4)
		self.table.addPlayer(self.p5)
		self.table.addPlayer(self.p6)
		
		self.table.removePlayer(self.p2)
		self.assertTrue(self.table.playerList[1] != self.p2)
		self.table.removePlayer(self.p4)
		self.assertTrue(self.table.playerList[3] != self.p4)
		
		self.table.addPlayer(self.p7)
		self.assertTrue(self.table.playerList[0] == self.p1)
		self.assertTrue(self.table.playerList[1] == self.p7)
		self.assertTrue(self.table.playerList[2] == self.p3)
		self.assertTrue(self.table.playerList[3] == None)
		self.assertTrue(self.table.playerList[4] == self.p5)
		self.assertTrue(self.table.playerList[5] == self.p6)
		
class TestAddToPot(TestTableSetUp):
	def testAddToPot(self):
		self.table.addToPot(200)
		self.assertTrue(self.table.pot == 200)
		
	def testAddToPotMultiple(self):
		self.table.addToPot(200)
		self.table.addToPot(200)
		self.assertTrue(self.table.pot == 400)
		
class TestClearPot(TestTableSetUp):
	def testClearPot(self):
		self.table.addToPot(200)
		self.table.clearPot()
		self.assertTrue(self.table.pot == 0)
		
class TestComparePlayerBet(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.p = Player()

	def testPlayerLowerThanCurrentBet(self):
		self.p.betAmount = 0
		self.table.currentBet = 100
		self.assertTrue(self.table.comparePlayerBet(self.p) == 1)
		
	def testPlayerEqualToCurrentBet(self):
		self.p.betAmount = 100
		self.table.currentBet = 100
		self.assertTrue(self.table.comparePlayerBet(self.p) == 0)
		
	def testPlayerMoreThanCurrentBet(self):
		self.p.betAmount = 200
		self.table.currentBet = 100
		self.assertTrue(self.table.comparePlayerBet(self.p) == -1)
		
class TestCollectAnte(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.ante = 5
		
	def testTwoPlayerCollect(self):
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.collectAnte()
		
		self.assertTrue(self.table.pot == 10)
		self.assertTrue(self.p1.money == 995)
		self.assertTrue(self.p2.money == 995)
		
	def testChangeAnteTwoPlayerCollect(self):
		self.table.ante = 10
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.collectAnte()
		
		self.assertTrue(self.table.pot == 20)
		self.assertTrue(self.p1.money == 990)
		self.assertTrue(self.p2.money == 990)
		
	def testFourPlayerCollect(self):
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.addPlayer(self.p4)
		self.table.collectAnte()
		
		self.assertTrue(self.table.pot == 20)
		self.assertTrue(self.p1.money == 995)
		self.assertTrue(self.p2.money == 995)
		self.assertTrue(self.p3.money == 995)
		self.assertTrue(self.p4.money == 995)
		
class TestAssignDealer(TestTableSetUp):
	def testTwoPlayersAssignDealer(self):
		self.table.curDealerSeatNo = 0
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.assignDealer()
		
		self.assertTrue(self.table.curDealerSeatNo == 1)
		
	def testTwoPlayersAssignDealerNewPosition(self):
		self.table.curDealerSeatNo = 1
		self.table._debugDirectAssign(self.p1, 1)
		self.table._debugDirectAssign(self.p2, 2)
		self.table.assignDealer()
		
		self.assertTrue(self.table.curDealerSeatNo == 2)
		
	def testAssignDealerMaxRange(self):
		self.table.curDealerSeatNo = 2
		self.table._debugDirectAssign(self.p1, 1)
		self.table._debugDirectAssign(self.p2, 5)
		self.table.assignDealer()
		
		self.assertTrue(self.table.curDealerSeatNo == 5)
		
	def testAssignDealerLoopAround(self):
		self.table.curDealerSeatNo = 3
		self.table._debugDirectAssign(self.p1, 1)
		self.table._debugDirectAssign(self.p2, 3)
		self.table.assignDealer()
		
		self.assertTrue(self.table.curDealerSeatNo == 1)
		
	def testThreePlayersAssignDealer(self):
		self.table.curDealerSeatNo = 3
		self.table._debugDirectAssign(self.p1, 1)
		self.table._debugDirectAssign(self.p2, 3)
		self.table._debugDirectAssign(self.p2, 5)
		self.table.assignDealer()
		
		self.assertTrue(self.table.curDealerSeatNo == 5)
		
class TestCollectSmallBlind(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.smallBlind = 5



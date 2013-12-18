import unittest
from ..Table import Table
from ..Player import Player
from ..CustomExceptions import *

class TestTableSetUp(unittest.TestCase):
	def setUp(self):
		self.table = Table()
		self.p1 = Player("p1", 1000)
		self.p2 = Player("p2", 1000)
		self.p3 = Player("p3", 1000)
		self.p4 = Player("p4", 1000)
		self.p5 = Player("p5", 1000)
		self.p6 = Player("p6", 1000)
		self.p7 = Player("p7", 1000)

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
			
class TestGetPlayers(TestTableSetUp):
	def testGetOne(self):
		self.table.addPlayer(self.p1)
		self.assertTrue(self.table.getPlayers() == [self.p1])
		
	def testGetNone(self):
		self.assertTrue(self.table.getPlayers() == [])
		
	def testGetTwo(self):
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.assertTrue(self.table.getPlayers() == [self.p1, self.p2])

			
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
		
class TestAddSidePot(TestTableSetUp):
	def testRaiseExceptionWhenNoSidePot(self):
		with self.assertRaises(IndexError):
			self.table.pots[1]
			
	def testAddSidePot(self):
		self.table.addSidePot()
		self.assertTrue(self.table.pots[1] == 0)
		
class TestAddToPot(TestTableSetUp):
	def testAddToPot(self):
		self.table.addToPot(200, 0)
		self.assertTrue(self.table.pots[0] == 200)
		
	def testAddToPotMultiple(self):
		self.table.addToPot(200, 0)
		self.table.addToPot(200, 0)
		self.assertTrue(self.table.pots[0] == 400)
		
	def testAddToSidePot(self):
		self.table.addSidePot()
		self.table.addToPot(200, 1)
		self.assertTrue(self.table.pots[1] == 200)
		
class TestClearPot(TestTableSetUp):
	def testClearPot(self):
		self.table.addToPot(200, 0)
		self.table.clearPot()
		self.assertTrue(self.table.pots[0] == 0)
		
class TestComparePlayerBet(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.p = Player()

	def testPlayerLowerThanCurrentBet(self):
		self.p.betAmount.append(0)
		self.table.currentBet[0] = 100
		self.assertTrue(self.table.comparePlayerBet(self.p, 0) == 1)
		
	def testPlayerEqualToCurrentBet(self):
		self.p.betAmount.append(100)
		self.table.currentBet[0] = 100
		self.assertTrue(self.table.comparePlayerBet(self.p, 0) == 0)
		
	def testPlayerMoreThanCurrentBet(self):
		self.p.betAmount.append(200)
		self.table.currentBet[0] = 100
		self.assertTrue(self.table.comparePlayerBet(self.p, 0) == -1)
	
class TestFindSmallestMoney(TestTableSetUp):
	def testFindSmallestMoney(self):
		self.p1.money = 10
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		
		self.assertTrue(self.table._findSmallestMoney() == 10)
	
class TestCollectAnte(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.ante = 5
		
	def testTwoPlayerCollect(self):
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.collectAnte()
		
		self.assertTrue(self.table.pots[0] == 10)
		self.assertTrue(self.p1.money == 995)
		self.assertTrue(self.p2.money == 995)
		
	def testChangeAnteTwoPlayerCollect(self):
		self.table.ante = 10
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.collectAnte()
		
		self.assertTrue(self.table.pots[0] == 20)
		self.assertTrue(self.p1.money == 990)
		self.assertTrue(self.p2.money == 990)
		
	def testFourPlayerCollect(self):
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.addPlayer(self.p4)
		self.table.collectAnte()
		
		self.assertTrue(self.table.pots[0] == 20)
		self.assertTrue(self.p1.money == 995)
		self.assertTrue(self.p2.money == 995)
		self.assertTrue(self.p3.money == 995)
		self.assertTrue(self.p4.money == 995)
		
	def testOnePlayerCannotPayAnte(self):
		self.table.ante = 10
		self.p1.money = 5
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.collectAnte()
		
		self.assertTrue(self.table.pots[0] == 10)
		self.assertTrue(self.p1.money == 0)
		self.assertTrue(self.p2.money == 995)

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
		
class TestFindNthPlayerFromSeat(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table._debugDirectAssign(self.p4, 5)
		
	def testFindPlayerNextTo(self):
		self.assertTrue(self.table.findNthPlayerFromSeat(0, 1) == (self.p2, 1))
		
	def testFindPlayerNextToNewPosition(self):
		self.assertTrue(self.table.findNthPlayerFromSeat(1, 1) == (self.p3, 2))
		
	def testFindSecondPlayer(self):
		self.assertTrue(self.table.findNthPlayerFromSeat(0, 2) == (self.p3, 2))
		
	def testFindSecondPlayerLoopAround(self):
		self.assertTrue(self.table.findNthPlayerFromSeat(5, 2) == (self.p2, 1))
		
class TestNoOfPlayers(TestTableSetUp):
	def testWithOnePlayer(self):
		self.table.addPlayer(Player())
		self.assertTrue(self.table.noOfPlayers() == 1)
		
	def testWithSixPlayers(self):
		for i in range(6):
			self.table.addPlayer(Player())
			
		self.assertTrue(self.table.noOfPlayers() == 6)
		
	def testWithThreePlayers(self):
		for i in range(3):
			self.table.addPlayer(Player())
			
		self.assertTrue(self.table.noOfPlayers() == 3)
		
class TestCollectSmallBlind(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.smallBlind = 5
		
	def testThreePlayersSmallBlindCollect(self):
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.collectSmallBlind()
		
		self.assertTrue(self.table.pots[0] == 5)
		self.assertTrue(self.p1.money == 1000)
		self.assertTrue(self.p2.money == 995)
		self.assertTrue(self.p3.money == 1000)
		self.assertTrue(self.p2.betAmount[0] == 5)
	
	# Blinds are switched around when playing heads up
	def testTwoPlayersCollect(self):
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.collectSmallBlind()
		
		self.assertTrue(self.table.pots[0] == 5)
		self.assertTrue(self.p1.money == 995)
		self.assertTrue(self.p2.money == 1000)
		self.assertTrue(self.p1.betAmount[0] == 5)
		
	def testPlayerCannotPaySmallBlind(self):
		self.table.smallBlind = 10
		self.p2.money = 5
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.collectSmallBlind()
		
		self.assertTrue(self.table.pots[0] == 5)
		self.assertTrue(self.table.pots[1] == 0)
		self.assertTrue(self.table.currentBet == [5,0])
		self.assertTrue(self.p1.money == 1000)
		self.assertTrue(self.p2.money == 0)
		self.assertTrue(self.p3.money == 1000)
		self.assertTrue(self.p2.betAmount[0] == 5)

class TestSlicePot(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.addPlayer(self.p4)
		self.table.pots = [20, 30, 20]
		self.table.currentBet = [5, 10, 20]
		self.p1.betAmount = [5]
		self.p2.betAmount = [5, 10]
		self.p3.betAmount = [5, 10, 20]
		self.p4.betAmount = [5, 10]
		
	def testSlicePot(self):
		self.p4.money = 5
	
		self.table._slicePot(2, self.p4)
		self.assertTrue(self.table.pots == [20, 30, 10, 15])
		self.assertTrue(self.table.currentBet == [5, 10, 5, 15])
		self.assertTrue(self.p1.betAmount == [5])
		self.assertTrue(self.p2.betAmount == [5, 10])
		self.assertTrue(self.p3.betAmount == [5, 10, 5, 15])
		self.assertTrue(self.p4.betAmount == [5, 10, 5])
		
	def testSlicePotBetAmountIntegrity(self):
		self.p4.money = 5
		self.table.pots = [20, 30, 30]
		self.p2.betAmount = [5, 10, 10]
		
		self.table._slicePot(2, self.p4)
		self.assertTrue(self.table.pots == [20, 30, 15, 20])
		self.assertTrue(self.table.currentBet == [5, 10, 5, 15])
		self.assertTrue(self.p1.betAmount == [5])
		self.assertTrue(self.p2.betAmount == [5, 10, 5, 5])
		self.assertTrue(self.p3.betAmount == [5, 10, 5, 15])
		self.assertTrue(self.p4.betAmount == [5, 10, 5])
		
	def testSlicePotBetAmountIntegrityTwo(self):
		self.p4.money = 7
		self.table.pots = [20, 30, 20]
		self.p2.betAmount = [5, 10, 10]
		
		self.table._slicePot(2, self.p4)
		self.assertTrue(self.table.pots == [20, 30, 21, 16])
		self.assertTrue(self.table.currentBet == [5, 10, 7, 13])
		self.assertTrue(self.p1.betAmount == [5])
		self.assertTrue(self.p2.betAmount == [5, 10, 7, 3])
		self.assertTrue(self.p3.betAmount == [5, 10, 7, 13])
		self.assertTrue(self.p4.betAmount == [5, 10, 7])
		
	def testSlicePotBetAmountIntegrityThree(self):
		self.p4.money = 7
		self.table.pots = [20, 30, 15]
		self.p2.betAmount = [5, 10, 5]
		
		self.table._slicePot(2, self.p4)
		self.assertTrue(self.table.pots == [20, 30, 19, 13])
		self.assertTrue(self.table.currentBet == [5, 10, 7, 13])
		self.assertTrue(self.p1.betAmount == [5])
		self.assertTrue(self.p2.betAmount == [5, 10, 5])
		self.assertTrue(self.p3.betAmount == [5, 10, 7, 13])
		self.assertTrue(self.p4.betAmount == [5, 10, 7])
		
		
		
class TestSetBigBlindBetAmount(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.bigBlind = 10
		
	def testSetBigBlindBetAmount(self):
		self.table.pots = [5,0]
		self.table.currentBet = [5,0]
		self.table.setBigBlindBetAmount()
		
		self.assertTrue(self.table.currentBet == [5,5])
		
class TestCollectBigBlind(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.smallBlind = 5
		self.table.bigBlind = 10
		
	# CSTB: Collect Small (blind) Then Big (blind)
	def testCSTBThreePlayers(self):
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.collectSmallBlind()
		self.table.collectBigBlind()
		
		self.assertTrue(self.table.pots[0] == 15)
		self.assertTrue(self.table.currentBet[0] == 10)
		self.assertTrue(self.p1.money == 1000)
		self.assertTrue(self.p2.money == 995)
		self.assertTrue(self.p3.money == 990)
		self.assertTrue(self.p2.betAmount[0] == 5)
		self.assertTrue(self.p3.betAmount[0] == 10)
		
	def testCSTBTwoPlayers(self):
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.collectSmallBlind()
		self.table.collectBigBlind()
		
		self.assertTrue(self.table.pots[0] == 15)
		self.assertTrue(self.table.currentBet[0] == 10)
		self.assertTrue(self.p1.money == 995)
		self.assertTrue(self.p2.money == 990)
		self.assertTrue(self.p1.betAmount[0] == 5)
		self.assertTrue(self.p2.betAmount[0] == 10)
		
	def testCSTBCantPaySmall(self):
		self.table.smallBlind = 10
		self.table.bigBlind = 20
		self.p2.money = 5
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.collectSmallBlind()
		self.table.collectBigBlind()
		
		self.assertTrue(self.table.pots == [10, 15])
		self.assertTrue(self.table.currentBet == [5, 15])
		self.assertTrue(self.p2.money == 0)
		self.assertTrue(self.p3.money == 980)
		self.assertTrue(self.p2.betAmount == [5])
		self.assertTrue(self.p3.betAmount == [5, 15])
	
	def testCSTBCantPayBig(self):
		self.table.smallBlind = 10
		self.table.bigBlind = 20
		self.p3.money = 15
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.collectSmallBlind()
		self.table.collectBigBlind()
		
		self.assertTrue(self.table.pots == [25, 0])
		self.assertTrue(self.table.currentBet == [15, 5])
		self.assertTrue(self.p2.money == 990)
		self.assertTrue(self.p3.money == 0)
		self.assertTrue(self.p2.betAmount == [10])
		self.assertTrue(self.p3.betAmount == [15])
	
	def testCSTBCantPayBigAndLessThanSmall(self):
		self.table.smallBlind = 10
		self.table.bigBlind = 20
		self.p3.money = 5
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.collectSmallBlind()
		self.table.collectBigBlind()
		
		self.assertTrue(self.table.pots == [10, 5])
		self.assertTrue(self.table.currentBet == [5, 15])
		self.assertTrue(self.p2.money == 990)
		self.assertTrue(self.p3.money == 0)
		self.assertTrue(self.p2.betAmount == [5, 5])
		self.assertTrue(self.p3.betAmount == [5])
		
	def testCSTBCantPayBigAndSmall(self):
		self.table.smallBlind = 10
		self.table.bigBlind = 20
		self.p2.money = 7
		self.p3.money = 15
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.collectSmallBlind()
		self.table.collectBigBlind()
		
		self.assertTrue(self.table.pots == [14, 8, 0])
		self.assertTrue(self.table.currentBet == [7,8,5])
		self.assertTrue(self.p2.money == 0)
		self.assertTrue(self.p3.money == 0)
		self.assertTrue(self.p2.betAmount == [7])
		self.assertTrue(self.p3.betAmount == [7, 8])
		
		
class TestMakeBet(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.smallBlind = 5
		self.table.bigBlind = 10
		self.table.collectSmallBlind()
		self.table.collectBigBlind()
		
	def testMakeNormalBet(self):
		self.table.makeBet(self.p1, 10)
		
		self.assertTrue(self.table.pots == [25])
		self.assertTrue(self.table.currentBet == [10])
		self.assertTrue(self.p1.betAmount == [10])
		
	def testMakeRaise(self):
		self.table.makeBet(self.p1, 20)
		
		self.assertTrue(self.table.pots == [35])
		self.assertTrue(self.table.currentBet == [20])
		self.assertTrue(self.p1.betAmount == [20])
		self.assertTrue(self.p1.money == 980)
	
	def testCallOnRaise(self):
		self.table.makeBet(self.p1, 20)
		self.table.makeBet(self.p2, 15)
		
		self.assertTrue(self.table.pots == [50])
		self.assertTrue(self.table.currentBet == [20])
		self.assertTrue(self.p2.betAmount == [20])
		self.assertTrue(self.p2.money == 980)
		
	def testRaiseOnRaise(self):
		self.table.makeBet(self.p1, 20)
		self.table.makeBet(self.p2, 25)
		
		self.assertTrue(self.table.pots == [60])
		self.assertTrue(self.table.currentBet == [30])
		self.assertTrue(self.p2.betAmount == [30])
		self.assertTrue(self.p2.money == 970)
		
	def testCallOnRaiseCantPay(self):
		self.p2.money = 10
		self.table.makeBet(self.p1, 20)
		self.table.makeBet(self.p2, 10)
		
		#print self.table.pots
		self.assertTrue(self.table.pots == [40, 5])
		self.assertTrue(self.table.currentBet == [15, 5])
		self.assertTrue(self.p1.betAmount == [15, 5])
		self.assertTrue(self.p2.betAmount == [15])
		self.assertTrue(self.p3.betAmount == [10])
		self.assertTrue(self.p2.money == 0)
	
class TestDetermineAmountToCall(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		self.table.smallBlind = 5
		self.table.bigBlind = 10
		self.table.collectSmallBlind()
		self.table.collectBigBlind()

	def testDetermineAfterBlinds(self):
		self.assertTrue(self.table.determineAmountToCall(self.p1) == 10)
		
	def testDetermineAfterBet(self):
		self.table.makeBet(self.p1, 10)
		self.assertTrue(self.table.determineAmountToCall(self.p2) == 5)
		
	def testDetermineAfterRaise(self):
		self.table.makeBet(self.p1, 20)
		self.assertTrue(self.table.determineAmountToCall(self.p2) == 15)
		
class TestSetNextTurn(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table._debugDirectAssign(self.p3, 4)
		
	def testSetNextTurn(self):
		self.table.turn = 0
		self.table.setNextTurn()
		
		self.assertTrue(self.table.turn == 1)
		
	def testSetNextTurnLoop(self):
		self.table.turn = 4
		self.table.setNextTurn()
		
		self.assertTrue(self.table.turn == 0)
		
class TestDeal(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.deck = range(52) # Unrandomize the deck so it's determinate
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		
	def testDealThreePlayers(self):
		self.table.deal()
		
		self.assertTrue(self.p1.hand == [49,46])
		self.assertTrue(self.p2.hand == [51,48])
		self.assertTrue(self.p3.hand == [50,47])
		
	def testDealChangeDealer(self):
		self.table.curDealerSeatNo = 1
		self.table.deal()
		
		self.assertTrue(self.p1.hand == [50,47])
		self.assertTrue(self.p2.hand == [49,46])
		self.assertTrue(self.p3.hand == [51,48])
		
class TestDealCommunity(TestTableSetUp):
	def setUp(self):
		TestTableSetUp.setUp(self)
		self.table.deck = range(52) # Unrandomize the deck so it's determinate
		self.table.addPlayer(self.p1)
		self.table.addPlayer(self.p2)
		self.table.addPlayer(self.p3)
		
	def testDealCommunityOne(self):
		self.table.dealCommunity(1)
		
		self.assertTrue(self.table.communityCards == [51])
		
	def testDealCommunityThree(self):
		self.table.dealCommunity(3)
		
		self.assertTrue(self.table.communityCards == [51, 50, 49])


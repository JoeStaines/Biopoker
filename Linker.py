from Table import Table
from Player import Player
from UI import UI
import Cards

class Linker():
	def __init__(self):
		self.stateDict = {}
	
		print "starting Table init"
		self.tableObj = Table()
		p1 = Player("p1", 1000)
		p2 = Player("p2", 1000)
		p3 = Player("p3", 1000)
		self.tableObj.addPlayer(p1)
		self.tableObj.addPlayer(p2)
		self.tableObj.addPlayer(p3)
		self.tableObj.beginRound()
		print "starting UI"
		self.UIObj = UI(self)
		self.UIObj.loop()
		
	def linkCall(self):
		self.tableObj.call(self.tableObj.playerList[self.tableObj.turn])
		
	def linkRaise(self, amount):
		self.tableObj.raiseBet(self.tableObj.playerList[self.tableObj.turn], amount)
		
	def linkFold(self):
		self.tableObj.fold(self.tableObj.playerList[self.tableObj.turn])
		
	def checkForUpdate(self):
		if self.tableObj.stateDict != {}:
			stateCopy = self.tableObj.stateDict
			self.tableObj.stateDict = {}
			return stateCopy
		else:
			return None
		
	def printTableState(self):
		gameStateMapping = ["PREFLOP","FLOP","TURN","RIVER"]
	
		print "Betting Round: {0}".format(gameStateMapping[self.tableObj.gameState])
		print "Pots: {0}\tCurrent Bet: {1}".format(self.tableObj.pots, self.tableObj.currentBet)
		print "Player: {0}\tHand: {1}".format(	self.tableObj.playerList[self.tableObj.turn].name, \
												Cards.convertNumToCards(self.tableObj.playerList[self.tableObj.turn].hand) )
		print "Money: {0}\tBet Amount: {1}".format(self.tableObj.playerList[self.tableObj.turn].money, self.tableObj.playerList[self.tableObj.turn].betAmount)
		print "Community: {0}".format(Cards.convertNumToCards(self.tableObj.communityCards))
		
if __name__ == "__main__":
	link = Linker()
	#UIStart = UI()
	#UIStart.loop()
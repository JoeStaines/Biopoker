from Table import Table
from Player import Player
import Cards

if __name__ == "__main__":
	table = Table()
	p1 = Player("p1", 1000)
	p2 = Player("p2", 1000)
	p3 = Player("p3", 1000)
	p4 = Player("p4", 1000)
	table.addPlayer(p1)
	table.addPlayer(p2)
	table.addPlayer(p3)
	table.addPlayer(p4)
	table.beginRound()
	
	gameStateMapping = ["PREFLOP","FLOP","TURN","RIVER"]
	
	gameRunning = True
	while gameRunning:
		print "Betting Round: {0}".format(gameStateMapping[table.gameState])
		print "Pots: {0}\tCurrent Bet: {1}".format(table.pots, table.currentBet)
		print "Player: {0}\tHand: {1}".format(	table.playerList[table.turn].name, \
												Cards.convertNumToCards(table.playerList[table.turn].hand) )
		print "Money: {0}\tBet Amount: {1}".format(table.playerList[table.turn].money, table.playerList[table.turn].betAmount)
		print "Community: {0}".format(Cards.convertNumToCards(table.communityCards))
		print "\n1. Call"
		print "2. Raise"
		print "3. Fold"
		print "0. Exit"
		
		c = int(raw_input())
		if c == 1:
			table.call(table.playerList[table.turn])
		elif c == 2:
			r = int(raw_input("Raise: "))
			table.raiseBet(table.playerList[table.turn], r)
		elif c == 3:
			table.fold(table.playerList[table.turn])
		elif c == 0:
			break
		
		
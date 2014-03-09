# -*- coding: utf-8 -*-

# FIGURE OUT HOW TO UPDATE ONLY NEEDED STATES. PLAY LIST IS STILL BEING PASSED BY POINTER

import pygame, sys, cPickle
from Player import Player
from pygame.locals import *
from lib import inputbox

imageCache = {}
def getImage(key):
	if not key in imageCache:
		imageCache[key] = pygame.image.load(key).convert()
		imageCache[key] = pygame.transform.scale(imageCache[key], (50, 67))
	return imageCache[key]
	
cardImages = [	"AS.png", "AH.png", "AD.png", "AC.png", \
				"KS.png", "KH.png", "KD.png", "KC.png", \
				"QS.png", "QH.png", "QD.png", "QC.png", \
				"JS.png", "JH.png", "JD.png", "JC.png", \
				"10S.png", "10H.png", "10D.png", "10C.png", \
				"9S.png", "9H.png", "9D.png", "9C.png", \
				"8S.png", "8H.png", "8D.png", "8C.png", \
				"7S.png", "7H.png", "7D.png", "7C.png", \
				"6S.png", "6H.png", "6D.png", "6C.png", \
				"5S.png", "5H.png", "5D.png", "5C.png", \
				"4S.png", "4H.png", "4D.png", "4C.png", \
				"3S.png", "3H.png", "3D.png", "3C.png", \
				"2S.png", "2H.png", "2D.png", "2C.png", \
				"Back.png"]
	
class UI():
	wW, wH = 800, 600
	
	def __init__(self, linker):
		pygame.init()
		self.linker = linker
		self.fps = pygame.time.Clock()
		self.initStateVariables()
		self.setDisplay()
		
		#NOTE: If the background changes to an image, change all instances of playArea.fill
		self.bgColour = pygame.Color(0,169,11)
		self.playArea.fill(self.bgColour)
		
		self.layoutTest()
		pygame.display.set_caption('Biopoker')
		
	def setDisplay(self):
		self.window = pygame.display.set_mode((UI.wW, UI.wH), 0, 32)
		self.playArea = pygame.display.get_surface()
		
	def initStateVariables(self):
		self.UIplayerList = []
		self.UIcommunityCards = []
		self.UIpots = []
		self.UIcurrentBet = []
		self.UIpreviousTurn = None
		self.UIturn = None
		
	def applyState(self, update):
		self.UIplayerList = update['playerlist']
		self.UIcommunityCards = update['comcards']
		self.UIpots = update['pots']
		self.UIcurrentBet = update['curbet']
		self.UIpreviousTurn = self.UIturn
		self.UIturn = update['turn']
	
	def updateState(self):
		for i, x in enumerate(self.UIplayerList):
			if x != None:
				#print "{0}: {1}".format(x.name, x.money)
				self.seats[i].setName(x.name)
				self.seats[i].setMoney(x.money)
				self.seats[i].setCards(x.hand)
				
		self.seats[self.UIturn].addTurnMarker()
		if self.UIpreviousTurn != None:
			self.seats[self.UIpreviousTurn].removeTurnMarker()
			
		self.displayCommunityCards()
		
	def displayState(self):
		print "Player List: {0}".format(self.UIplayerList)
		print "Community Cards: {0}".format(self.UIcommunityCards)
		print "Pots: {0}".format(self.UIpots)
		print "currentBet: {0}".format(self.UIcurrentBet)
		print "turn: {0}".format(self.UIturn)
		
	def getRaiseAmount(self):
		surfaceCopy = self.playArea.copy()
		textBoxRect = pygame.Rect((self.playArea.get_width() / 2) - 100,self.playArea.get_height() - 50,200,20)
		amount = inputbox.ask(self.playArea, "Amount", textBoxRect)
		clearRect = pygame.Rect((self.playArea.get_width() / 2) - 120,self.playArea.get_height() - 60,240,40)
		self.playArea.blit(surfaceCopy, clearRect, clearRect)
		if amount.isdigit():
			return int(amount)
		else:
			return None
			
	def determineAmountToCall(self, player):
		return sum(self.UIcurrentBet) - sum(player.betAmount)
		
	def loop(self):
		while 1:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						if self.buttonCall.clicked(event.pos) == 1:
							#print "Call"
							self.linker.linkCall()
						elif self.buttonRaise.clicked(event.pos) == 1:
							#r = int(raw_input("Raise: "))
							r = self.getRaiseAmount()
							if r != None:
								bettingAmount = self.determineAmountToCall(self.UIplayerList[self.UIturn]) + r
								if bettingAmount <= self.UIplayerList[self.UIturn].money:
									self.linker.linkRaise(r)
									
						elif self.buttonFold.clicked(event.pos) == 1:
							self.linker.linkFold()
				elif event.type == pygame.KEYDOWN:
					if event.key == K_SPACE:
						self.linker.printTableState()
					elif event.key == K_1:
						self.displayState()
						
			updatePickle = self.linker.checkForUpdate()
			if updatePickle != None:
				updateState = cPickle.loads(updatePickle)
				self.applyState(updateState)
				self.updateState()
			pygame.display.update()
			self.fps.tick(10)
	
	def displayCommunityCards(self):
		self.cardyoffset = 50
		self.cardheight = UI.wH/2-self.cardyoffset
		
		for _ in range(5 - len(self.UIcommunityCards)):
			self.UIcommunityCards.append(52);
		
		self.card1 = UICard((UI.wW/2-50*2+3, self.cardheight), self.UIcommunityCards[0])
		self.card2 = UICard((UI.wW/2-50*1, self.cardheight), self.UIcommunityCards[1])
		self.card3 = UICard((UI.wW/2, self.cardheight), self.UIcommunityCards[2])
		self.card4 = UICard((UI.wW/2+50*1, self.cardheight), self.UIcommunityCards[3])
		self.card5 = UICard((UI.wW/2+50*2, self.cardheight), self.UIcommunityCards[4])
		self.playArea.blit(self.card1.image, self.card1.rect)
		self.playArea.blit(self.card2.image, self.card2.rect)
		self.playArea.blit(self.card3.image, self.card3.rect)
		self.playArea.blit(self.card4.image, self.card4.rect)
		self.playArea.blit(self.card5.image, self.card5.rect)
	
	def layoutTest(self):
		self.displayCommunityCards()
		
		self.seats = []
		self.seats.append( UISeat(self.playArea, (UI.wW/2-300, self.cardheight)) )
		self.seats.append( UISeat(self.playArea, (UI.wW/2-100, self.cardheight-150)) )
		self.seats.append( UISeat(self.playArea, (UI.wW/2+100, self.cardheight-150)) )
		self.seats.append( UISeat(self.playArea, (UI.wW/2+300, self.cardheight)) )
		self.seats.append( UISeat(self.playArea, (UI.wW/2+100, self.cardheight+170)) )
		self.seats.append( UISeat(self.playArea, (UI.wW/2-100, self.cardheight+170)) )
		
		# self.seat1 = UISeat(self.playArea, (UI.wW/2-300, self.cardheight))
		# self.seat2 = UISeat(self.playArea, (UI.wW/2-100, self.cardheight-150))
		# self.seat3 = UISeat(self.playArea, (UI.wW/2+100, self.cardheight-150))
		# self.seat4 = UISeat(self.playArea, (UI.wW/2+300, self.cardheight))
		# self.seat5 = UISeat(self.playArea, (UI.wW/2+100, self.cardheight+170))
		# self.seat6 = UISeat(self.playArea, (UI.wW/2-100, self.cardheight+170))
		
		# Buttons
		
		
		self.buttonCall = UIButton("resources/images/ButtonCall.jpg", (100, UI.wH - 150))
		self.buttonRaise = UIButton("resources/images/ButtonRaise.jpg", (100, UI.wH - 100 + 5))
		self.buttonFold = UIButton("resources/images/ButtonFold.jpg", (100, UI.wH - 50 + 5*2))
		self.playArea.blit(self.buttonCall.image, self.buttonCall.rect)
		self.playArea.blit(self.buttonRaise.image, self.buttonRaise.rect)
		self.playArea.blit(self.buttonFold.image, self.buttonFold.rect)
	

class UIImage(pygame.sprite.Sprite):
	def __init__(self, src):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(src).convert()
	
	

class UICard(pygame.sprite.Sprite):
	def __init__(self, location, cardNo):
		pygame.sprite.Sprite.__init__(self)
		self.image = getImage("resources/images/cards/" + cardImages[cardNo])
		self.rect = self.image.get_rect()
		self.rect.center = location
	
class UISeat():
	def __init__(self, playArea, location):
		self.playArea = playArea
		# These variables will probably be replaced by some 'Player' object that contains these
		self.name = "-"
		self.money = -1
		self.cards = (52, 52) # 52nd card is back face
		
		self.fontObj = pygame.font.Font("resources/fonts/arialbd.ttf", 14)
		self.colour = (0, 200, 11)
		
		self.seatsurface = pygame.Surface((150,150), pygame.SRCALPHA)
		self.seatsurface.fill((255, 255, 255, 0))
		self.seatrect = self.seatsurface.get_rect()
		self.seatrect.center = location
		
		self._makeAv()
		self.avwidth = self.avatar.get_width()
		self.avheight = self.avatar.get_height()
		self.seatsurface.blit(self.avatar, (0,0))
		
		self._makeName()
		self._makeMoney()
		#self._makeCardArea()
		self._initTurnMarker()
		self._displayCards()
		
		self.playArea.blit(self.seatsurface, self.seatrect)
		
	def _makeAv(self):
		self.avatar = pygame.image.load("resources/images/avatar.png").convert()
		self.avrect = self.avatar.get_rect()
	
	def _makeName(self):
		x, y = (self.avwidth, 0)
		width, height = (self.seatrect.topright[0]-x, self.avheight/2)
		
		# Make the name box surface
		self.boxcolour = (82,82,82)
		self.nameboxsurface = pygame.Surface((width, height))
		
		# Put name on surface
		self._blitName()
		
		self.seatsurface.blit(self.nameboxsurface, (x, y))
		
	
	def _blitBoxName(self):
		width, height = (self.seatrect.width-self.avwidth, self.avheight/2)
		
		self.nameboxsurface.fill(self.boxcolour)
		
		# Separate name box from avatar and money box
		pygame.draw.line(self.nameboxsurface, (62, 62, 62), (0, 0), (0, height))
		pygame.draw.line(self.nameboxsurface, (62, 62, 62), (0, height-1), (width, height-1))
	
	def _blitName(self):
		self._blitBoxName()
		self.namesurface = self.fontObj.render(self.name, True, (200, 200, 200))
		self.nameboxsurface.blit(self.namesurface, (5, 5))
		
	def _makeMoney(self):
		x, y = (self.avwidth, self.avheight/2)
		width, height = (self.seatrect.width-x, self.avheight/2)
		
		self.moneyboxsurface = pygame.Surface((width, height))
		self._blitMoney()
		self.seatsurface.blit(self.moneyboxsurface, (x, y))
		
	def _blitBoxMoney(self):
		height = self.avheight/2
		self.moneyboxsurface.fill(self.boxcolour)
		pygame.draw.line(self.moneyboxsurface, (62, 62, 62), (0, 0), (0, height))
		
	def _blitMoney(self):
		self._blitBoxMoney()
		self.moneysurface = self.fontObj.render(u'\xA3{0}'.format(self.money), True, (255, 255, 255))
		self.moneyboxsurface.blit(self.moneysurface, (5, 5))
		
	def _makeCardArea(self):
		x, y = (0, self.avheight)
		width, height = (self.seatrect.width, self.seatrect.height - self.avheight)
		
		self.cardAreaSurface = pygame.Surface((width, height))
		self.cardAreaSurface.set_alpha(128)
		self.cardAreaSurface.fill(self.boxcolour)
		self.seatsurface.blit(self.cardAreaSurface, (x,y))
		
	def _displayCards(self):		
		self.pcard1 = UICard((0,0), self.cards[0])
		self.pcard2 = UICard((0,0), self.cards[1])
		self.playArea.blit(self.pcard1.image, (self.seatrect.topleft[0]+5, self.seatrect.topleft[1]+self.avheight+5))
		self.playArea.blit(self.pcard2.image, (self.seatrect.topleft[0]+5+(self.pcard1.image.get_width()/2), self.seatrect.topleft[1]+self.avheight+5))
		
		#x, y = (0, self.avheight)
		#self.seatsurface.blit(self.cardAreaSurface, (x,y))
		
		
	def setName(self, name):
		self.name = name
		self._blitName()
		self.seatsurface.blit(self.nameboxsurface, (self.avwidth, 0))
		self.playArea.blit(self.seatsurface, self.seatrect)
		
	def setMoney(self, money):
		self.money = money
		self._blitMoney()
		self.seatsurface.blit(self.moneyboxsurface, (self.avwidth, self.avheight/2))
		self.playArea.blit(self.seatsurface, self.seatrect)
		
	def _initTurnMarker(self):
		self.TMthickness = 3
		x, y = (self.seatrect.topleft[0], self.seatrect.topleft[1]-self.TMthickness)
		width, height = (self.seatrect.width, self.TMthickness)
		self.turnMarker = pygame.Surface((width, height))
		self.turnMarkerRect = self.turnMarker.get_rect()
		self.turnMarkerRect.topleft = (x, y)
		self.turnMarker.fill((233,202,0))
		
	def addTurnMarker(self):
		self.playArea.blit(self.turnMarker, self.turnMarkerRect)
		
	def removeTurnMarker(self):
		self.playArea.fill(pygame.Color(0,169,11), self.turnMarkerRect)
		
	def setCards(self, hand):
		self.cards = hand
		self._displayCards()
		
		
class UIButton(pygame.sprite.Sprite):
    def __init__(self, src, rectcenter):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(src).convert()
		self.rect = self.image.get_rect()
		self.rect.center = rectcenter

    def clicked(self,pos):
        if (self.rect.left < pos[0] < self.rect.right) and (self.rect.top < pos[1] < self.rect.bottom):
            return 1 


"""		
if __name__ == "__main__":
	UIStart = UI()
	UIStart.loop()
"""
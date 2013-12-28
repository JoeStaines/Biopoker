cardMappings = ["As","Ah","Ad","Ac", \
				"Ks","Kh","Kd","Kc", \
				"Qs","Qh","Qd","Qc", \
				"Js","Jh","Jd","Jc", \
				"Ts","Th","Td","Tc", \
				"9s","9h","9d","9c", \
				"8s","8h","8d","8c", \
				"7s","7h","7d","7c", \
				"6s","6h","6d","6c", \
				"5s","5h","5d","5c", \
				"4s","4h","4d","4c", \
				"3s","3h","3d","3c", \
				"2s","2h","2d","2c"]
				
def convertNumToCards(cards):
	newcards = []
	for c in cards:
		newcards.append(cardMappings[c])
	return newcards
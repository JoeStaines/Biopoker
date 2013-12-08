class Cards:
	def convertNumToCards(self, cards):
		newcards = []
		for c in cards:
			if c == 0:
				newcards.append("As")
			elif c == 1:
				newcards.append("Ah")
			elif c == 2:
				newcards.append("Ad")
			elif c == 3:
				newcards.append("Ac")
			elif c == 4:
				newcards.append("Ks")
			elif c == 5:
				newcards.append("Kh")
			elif c == 6:
				newcards.append("Kd")
			elif c == 7:
				newcards.append("Kc")
			elif c == 8:
				newcards.append("Qs")
			elif c == 9:
				newcards.append("Qh")
			elif c == 10:
				newcards.append("Qd")
			elif c == 11:
				newcards.append("Qc")
			elif c == 12:
				newcards.append("Js")
			elif c == 13:
				newcards.append("Jh")
			elif c == 14:
				newcards.append("Jd")
			elif c == 15:
				newcards.append("Jc")
			elif c == 16:
				newcards.append("Ts")
			elif c == 17:
				newcards.append("Th")
			elif c == 18:
				newcards.append("Td")
			elif c == 19:
				newcards.append("Tc")
			elif c == 20:
				newcards.append("9s")
			elif c == 21:
				newcards.append("9h")
			elif c == 22:
				newcards.append("9d")
			elif c == 23:
				newcards.append("9c")
			elif c == 24:
				newcards.append("8s")
			elif c == 25:
				newcards.append("8h")
			elif c == 26:
				newcards.append("8d")
			elif c == 27:
				newcards.append("8c")
			elif c == 28:
				newcards.append("7s")
			elif c == 29:
				newcards.append("7h")
			elif c == 30:
				newcards.append("7d")
			elif c == 31:
				newcards.append("7c")
			elif c == 32:
				newcards.append("6s")
			elif c == 33:
				newcards.append("6h")
			elif c == 34:
				newcards.append("6d")
			elif c == 35:
				newcards.append("6c")
			elif c == 36:
				newcards.append("5s")
			elif c == 37:
				newcards.append("5h")
			elif c == 38:
				newcards.append("5d")
			elif c == 39:
				newcards.append("5c")
			elif c == 40:
				newcards.append("4s")
			elif c == 41:
				newcards.append("4h")
			elif c == 42:
				newcards.append("4d")
			elif c == 43:
				newcards.append("4c")
			elif c == 44:
				newcards.append("3s")
			elif c == 45:
				newcards.append("3h")
			elif c == 46:
				newcards.append("3d")
			elif c == 47:
				newcards.append("3c")
			elif c == 48:
				newcards.append("2s")
			elif c == 49:
				newcards.append("2h")
			elif c == 50:
				newcards.append("2d")
			elif c == 51:
				newcards.append("2c")
		return newcards
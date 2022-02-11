from time import sleep as sleep
from gpiozero import LED, Button
from unicodedata import normalize

#this is the table with the algarisms and the main words
#the element (8, 6) means that the caracter was duplicated eg: in he word 'access' it must be shown that there are duplicated leters to avoid confusion
table = [		["A", "B", "C", "D", "E", "F", "G", "H", "I"],
			["J", "K", "L", "M", "N", "O", "P", "Q", "R"],
			["S", "T", "U", "V", "W", "X", "Y", "Z", "0"],
			["1", "2", "3", "4", "5", "6", "7", "8", "9"],
			[" ", "OI", "BOM", "DIA", "TARDE", "NOITE", "TCHAU", "OBRIGADO", "POR"], 
			["FAVOR", "", "", "", "", "", "", "", ""], 
			["", "", "", "", "", "", "", "", ""], 
			["", "", "", "", "", "", "", "", ""], 
			["", "", "", "", "", "", "###", "ERROR"]
		]

#set accordingly with the circuit
out_rp = LED(21)
out_rr = LED(20)
out_rm = LED(16)
out_ri = LED(12)
out_rt = LED(7)

out_lp = LED(14)
out_lr = LED(15)
out_lm = LED(18)
out_li = LED(23)
out_lt = LED(24)

#returns the right and left position of the element
#if not found returns -1, -1
def getElementPos(element):
	#running through rows
	for r, i in enumerate(table):
		try:
			#trying to fin the elemnt in the current row
			c = i.index(element)
		except ValueError:
			continue
		return r, c
	return -1, -1

#sets all outputs to off
def clearAll():
	out_rp.off()
	out_rr.off()
	out_rm.off()
	out_ri.off()
	out_rt.off()
	
	out_lp.off()
	out_lr.off()
	out_lm.off()
	out_li.off()
	out_lt.off()

#turns on the outputs
#if no parameters are passed, outputs ERROR (table[8][8])
def makeOut(r_hand=8, l_hand=8):
	clearAll()
	if r_hand == 0:
		out_rt.on()
	elif r_hand == 1:
		out_ri.on()
	elif r_hand == 2:
		out_rm.on()
	elif r_hand == 3:
		out_rr.on()
	elif r_hand == 4:
		out_rp.on()
	elif r_hand == 5:
		out_rt.on()
		out_ri.on()
	elif r_hand == 6:
		out_rt.on()
		out_rm.on()
	elif r_hand == 7:
		out_rt.on()
		out_rr.on()
	elif r_hand == 8:
		out_rt.on()
		out_rp.on()

	if l_hand == 0:
		out_lt.on()
	elif l_hand == 1:
		out_li.on()
	elif l_hand == 2:
		out_lm.on()
	elif l_hand == 3:
		out_lr.on()
	elif l_hand == 4:
		out_lp.on()
	elif l_hand == 5:
		out_lt.on()
		out_li.on()
	elif l_hand == 6:
		out_lt.on()
		out_lm.on()
	elif l_hand == 7:
		out_lt.on()
		out_lr.on()
	elif l_hand == 8:
		out_lt.on()
		out_lp.on()

	sleep(0.7)
	clearAll()

while True:
	phrase = input('Ready....\n')
	words = phrase.split(' ')
	#running word by word
	for word in words:
		#removing any kind of accent
		word = normalize('NFKD', word).encode('ASCII', 'ignore').decode('utf-8')
		#setting to uppercase
		word = word.upper()
		#both words means 'good', so they can be assigned as the same
		word = word.replace("BOA", "BOM")
		r_hand, l_hand = getElementPos(word)
		#if the word exists in the array table, outputs it to save time
		if r_hand>=0 & l_hand>=0:
			makeOut(r_hand, l_hand)
		#if doesn't outputs letter by letter of the word
		else:
			prev_r = prev_l = ''
			for char in word:
				r_hand, l_hand = getElementPos(char)
				#prev_r and prev_l are used to compare with previous letters, therefore knowing when there's duplicated			
				if r_hand==prev_r and l_hand==prev_l:
					makeOut(8, 6)
					continue
				prev_r = r_hand
				prev_l = l_hand
				if r_hand>=0 & l_hand>=0:
					makeOut(r_hand, l_hand)
				#in the case of an unknown elemnet, outputs ERROR
				else:
					makeOut(8, 8)
		#sends a space inbetween words
		makeOut(4, 0)
		sleep(0.5)

#coding: utf-8
#for python3
from PIL import Image
import random
from stegano import lsb

def stegapixEncode(message,passe,infile,outfile):
	caracts = list("0123456789AZERTYUIOPMLKJHGFDSQWXCVBN?. !()+-*#@_")
	secret = lsb.hide(infile, str(len(message)))
	secret.save(infile)
	i=Image.open(infile)
	(l, h) = i.size
	mattx = []
	random.seed(passe)
	for v in range(0,len(message)):
		mattx.append([random.randint(1,l),random.randint(1,h)])
	canal = 1
	msg = list(message)
	for j in mattx:
		x, y = j[0], j[1]
		r,g,b = i.getpixel((x, y))
		c = caracts.index(msg.pop(0).upper())
		canal = (1+canal)%4
		if canal == 0: canal = 1
		if canal == 1:
			r = c
		if canal == 2:
			g = c
		if canal == 3:
			b = c
		i.putpixel((x, y), (r,g,b))
		if len(msg)<1: break
	i.save(outfile, "PNG")


def stegapixDecode(message,passe,infile):
	caracts = list("0123456789AZERTYUIOPMLKJHGFDSQWXCVBN?. !()+-*#@_")
	taille = int(lsb.reveal(infile))
	i=Image.open(infile)
	(l, h) = i.size
	mattx = []
	random.seed(passe)
	for v in range(0,l*h):
		mattx.append([random.randint(1,l),random.randint(1,h)])
	msg = []
	canal = 1
	for j in mattx:
		x, y = j[0], j[1]
		r,g,b = i.getpixel((x, y))
		canal = (1+canal)%4
		if canal == 0: canal = 1
		if canal == 1:
			c = r
		if canal == 2:
			c = g
		if canal == 3:
			c = b
		msg.append(caracts[c])
		if len(msg)>taille-1: break
	msg = "".join(msg)
	return msg


choix = input("stegapix (E)nc/(D)ec ? ")
if (choix.lower()=="e"):
	message = input("Message: ")
	passe = input("Password: ")
	infile = input("Input File Path and Name: ")
	outfile = input("Out File Path and Name: ")
	stegapixEncode(message,passe,infile,outfile)
if (choix.lower()=="d"):
	message = input("Message: ")
	passe = input("Password: ")
	infile = input("Input File Path and Name: ")
	stegapixDecode(message,passe,infile)






# ===========
# invaderStub
# ===========
#
# This is a kind of simple python replacement for the incredible PixelInvaders Java application
#
# This program, invaderStub, is released as Free Software.
#
# First written by LM Croisez, on 5 Aug 2014
#
# Programme d'interfaçage avec des panneaux du type PixelInvaders
# This program makes the itf between 2d xy plan and PixelInvaders-type panels.
#
# The frame can be either sent by TCPIP, or by serial port direct connection.
# If using TCPIP, you must setup a ser2net daemon to make the via.
# See www.pixelinvaders.ch for more info on this setup.
#
# GENERAL TIPS:
# You must use the p(x,y) plan to put there the pixels where you want, and in the 15bit color you want.
# Once this is done, you must use the refreshPanels() function to latch your picture to the panels.
#
# The following functions are available:
#
#  clear
#  convert24To15Bit(r,g,b): convert 24bit color to 15bit color
#  UpdatePanels 
#  ScrollPanelsLeft
#  ScrollPanelsRight
#  ScrollPanelsUp
#  ScrollPanelsDown
#  Circle(xc,yc,radius,r,g,b,[max_x],[max_y])
#  Sprite(x,y,data,r,g,b)
#
#  For the sprite, a dictionnary has been initiated, containing a big part of the alphabet.


########## USER DEFS ########## USER DEFS ########### USER DEFS ##### USER DEFS ###############
NUM_PANEL = 2
USE_TCPIP = 1
#Needed if using TCPIP comm
TCP_IP = "192.168.99.187"
TCP_PORT = 5333
#Needed if using Serial comm
SERIAL_PORT = 'COM45'
########## USER DEFS ########## USER DEFS ########### USER DEFS ##### USER DEFS ###############

dico = { # 4x6 matrix sprite dictionnary
 'A': 'AEAA40', 'B': 'CACAC0', 'C': '688860', 'D': 'CAAAC0', 'E': 'E8C8E0', 'F': '88C8E0', 'G': '6B8860',
 'H': 'AAEAA0', 'I': '444440', 'J': 'CC4440', 'K': '9ACA90', 'L': 'E88880', 'M': 'AAAEA0', 'N': '99BD90', 
 'O': 'EAAAE0', 'P': '88EAE0', 'Q': '3EAAE0', 'R': 'AACAE0', 'S': 'C24860', 'T': '4444E0', 'U': 'EAAAA0', 
 'V': '4AAAA0', 'W': 'AEAAA0', 'X': 'AA4AA0', 'Y': '44AAA0', 'Z': 'E842E0', 
 '0': '4AAA40', '1': '444C40', '2': 'F42A40', '3': '', '4': '', 
 '5': '', '6': '', '7': '', '8': 'EA4AE0', '9': 'E2EAE0',
 ' ': '000000'
}

import socket
import serial
from time import sleep
import random
import math

TPM2NET_HEADER_SIZE = 4
TPM2NET_HEADER_SIMULATE = 0x74
TPM2NET_HEADER_IDENT = 0x9c
TPM2NET_CMD_DATAFRAME = 0xda
TPM2NET_CMD_COMMAND = 0xc0
TPM2NET_CMD_ANSWER = 0xaa
TPM2NET_FOOTER_IDENT = 0x36

NO_ROTATE = 0
ROTATE_90 = 1
ROTATE_90_FLIPPEDY = 2
ROTATE_180 = 3
ROTATE_180_FLIPPEDY = 4
ROTATE_180_FLIPPEDX = 5
ROTATE_270 = 6
	

if (USE_TCPIP):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
else:		
	s = serial.Serial(
		port=SERIAL_PORT,
		baudrate=115200,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=8
	)

#Array creation
VIRTPLAN_MULT_SIZE = 3
p = [[] for _ in range(8*NUM_PANEL*VIRTPLAN_MULT_SIZE)]
for x in range(8*NUM_PANEL*VIRTPLAN_MULT_SIZE):
	for y in range(8*VIRTPLAN_MULT_SIZE):
		p[x].append(0)
q = [[] for _ in range(8*NUM_PANEL)]
for x in range(8*NUM_PANEL):
	for y in range(8):
		q[x].append(0)

#Returns the height of a plan (either p or q, for example)
def height(o):
	return len(o[0])
	
#Returns the width of a plan (either p or q, for example)
def width(o):
	return len(o)
	
def clear():
	for x in range(width(p)):
		for y in range(height(p)):
			p[x][y]=0
	UpdatePanels()

def sendFrame(buf):
	if (USE_TCPIP):
		s.send(buf)
	else:
		s.write(buf)

#Conversion of a 24 bit (3x1 byte) color to a 15 bit (2bytes) color
#Beware that each input rgb color components must already be shrinked to 5bit, meaning values from 0 to 31 only.
def convert24To15Bit(r,g,b):
	# BBBBBBBB BBBBBBBB
	# 11111111 22222222
	# -bbbbbgg gggrrrrr
	
	B1=(b<<2) + ((g&~0b111)>>3)
	B2=((g&~0b11000)<<5) + r
	return B1*256 + B2

#Validate if given coordinates is inside the virtualplan
def is_pcoord_valid(x, y):
	if x < width(p) and x >= 0 and y < height(p) and y >= 0:
		return 1
	#print(x,y)
	return 0
	
#Plan transformation. p(x,y) => q(x,y). Note that this is q(x,y) which is latched to the panels
def transformPanel(panel, transform, vx=0, vy=0):
	# Note: descriptions des transformations:
	# flippedy: x <= x  , y <= 7-y
	# flippedx: x <= 7-x, y <= y
	# vx & vy allows to displace the viewport inside the virtualplan p(x,y),
	#   which is useful for scrolling in a big picture map, for example.
	###############################################################

	if (transform == NO_ROTATE):
		#retourner lignes impaires
		for x in range(0, 8, 2):
			for y in range(8):

				if is_pcoord_valid(vx+x+panel*8, vy+y):
					q[x + panel*8][y] = p[vx+x+panel*8][vy+y]
				else:
					q[x + panel*8][y] = 0
					
		for x in range(1, 8, 2):
			for y in range(8):
				if is_pcoord_valid(vx+x+panel*8,vy+7-y):
					q[x + panel*8][y] = p[vx+x+panel*8][vy+7-y]
				else:
					q[x + panel*8][y] = 0
					
	###############################################################
	if (transform == ROTATE_90):
		pass
	###############################################################			
	if (transform == ROTATE_90_FLIPPEDY):
		pass
	###############################################################			
	if (transform == ROTATE_180):
		pass
	###############################################################	
	if (transform == ROTATE_180_FLIPPEDY):
		for x in range(0, 8, 2):
			for y in range(8):
				if is_pcoord_valid(vx+7-y+panel*8, vy+7-x):
					q[x + panel*8][y] = p[vx+7-y+panel*8][vy+7-x]
				else:
					q[x + panel*8][y] = 0
					
		for x in range(1, 8, 2):
			for y in range(8):
				if is_pcoord_valid(vx+y+panel*8, vy+7-x):
					q[x + panel*8][y] = p[vx+y+panel*8][vy+7-x]
				else:
					q[x + panel*8][y] = 0
					
	###############################################################	
	if (transform == ROTATE_180_FLIPPEDX):
		#retourner lignes impaires et symetrie sur la diagonale
		for x in range(0, 8, 2):
			for y in range(8):
				if is_pcoord_valid(vx+y+panel*8, vy+x):
					q[x + panel*8][y] = p[vx+y+panel*8][vy+x]
				else:
					q[x + panel*8][y] = 0
					
		for x in range(1, 8, 2):
			for y in range(8):
				if is_pcoord_valid(vx+7-y+panel*8, vy+x):
					q[x + panel*8][y] = p[vx+7-y+panel*8][vy+x]
				else:
					q[x + panel*8][y] = 0
					
	###############################################################			
	if (transform == ROTATE_270):
		pass
	###############################################################

	
	
#A panel update.
def UpdatePanel(panel, transform, virtplan_offset_x=0, virtplan_offset_y=0):
	frame = bytearray()
	frame.append(TPM2NET_HEADER_IDENT)
	frame.append(TPM2NET_CMD_DATAFRAME)
	frame.append(0)   #hsb
	frame.append(128) #lsb
	frame.append(panel)
	frame.append(1)
	
	transformPanel(panel, transform, virtplan_offset_x, virtplan_offset_y)
	
	for x in range(panel*8, panel*8 + 8):
		for y in range(8):
			B1 = (q[x][y]) >> 8
			B2 = (q[x][y]) % 256
			frame.append(B1)
			frame.append(B2)
	
	frame.append(TPM2NET_FOOTER_IDENT)
	sendFrame(frame)

#Update of all panels
def UpdatePanels(virtplan_offset_x=0, virtplan_offset_y=0):
	UpdatePanel(0,ROTATE_180_FLIPPEDY, virtplan_offset_x, virtplan_offset_y)
	sleep(0.006) #delay needed for the Teensy Arduino board to digest the received information
	UpdatePanel(1,ROTATE_180_FLIPPEDX, virtplan_offset_x, virtplan_offset_y)
	sleep(0.006)
	
def ScrollPanelsLeft():
	for x in range(1, 8*NUM_PANEL):
		for y in range(8):
			p[x-1][y]=p[x][y]

def ScrollPanelsRight():
	x=8*NUM_PANEL-1
	while (x>0):
		x=x-1
		for y in range(8):
			p[x+1][y]=p[x][y]

def ScrollPanelsUp():
	y=7
	while (y>0):
		y=y-1
		for x in range(8*NUM_PANEL):
			p[x][y+1]=p[x][y]
	
def ScrollPanelsDown():
	for y in range(1,8):
		for x in range(8*NUM_PANEL):
			p[x][y-1]=p[x][y]

def Circle(xc,yc,radius, r, g, b, max_x=8*NUM_PANEL, max_y=8):
	k = 0
	while (k <= 2*math.pi):
		k = k + .1
		x = math.floor(math.sin(k) * radius + xc)
		y = math.floor(math.cos(k) * radius + yc)
		if x >= 0 and x < max_x and y >= 0 and y < max_y:
			p[x][y] = convert24To15Bit(r,g,b)

def Sprite(x,y,data, r,g,b):
	x0 = x
	y0 = y
	for i in range(len(data)):
		bindata = "{0:04b}".format(int(data[i],16))
		for j in range(4):
			c = convert24To15Bit(r,g,b)
			if bindata[j] == '0':
				if is_pcoord_valid(x,y):
					c = p[x][y] #if nothing is displayed, we leave the former content of the pixel
				else:
					c = 0
			if x >= 0 and x < width(p) and y >= 0 and y < height(p):
				if is_pcoord_valid(x,y):
					p[x][y] = c
			x = x + 1
		y = y + 1
		x = x0

#Function that displays a text, which bottom-left coordinates are (x,y), with (rgb) as color.
#w is the spacing between each letters, which is equal to 4 by default.
#Beware that there is no check for the existence of an entry in the dictionnary.
def Text(x, y, buf, r, g, b, w=4):
	x0 = x
	for i in range(len(buf)):
		Sprite(x0,y, dico[buf[i]], r, g, b)
		x0 = x0 + w
		
def DoAnimationRandPanels():
	r = random.randint(0,31)
	g = random.randint(0,31)
	b = random.randint(0,31)
	for x in range(8*NUM_PANEL):
		for y in range(8):
			p[x][y] = convert24To15Bit(r,g,b)
	UpdatePanels()
	sleep(0.2)
	
def DoAnimationRandPixels():
	for x in range(8*NUM_PANEL):
		for y in range(8):
			r = random.randint(0,31)
			g = random.randint(0,31)
			b = random.randint(0,31)
			p[x][y] = convert24To15Bit(r,g,b)
	UpdatePanels()
	sleep(0.2)
	
def DoAnimationRandHLINE():
	for y in range(8):
		r = random.randint(0,31)
		g = random.randint(0,31)
		b = random.randint(0,31)
		for x in range(8*NUM_PANEL):
			p[x][y] = convert24To15Bit(r,g,b)
	UpdatePanels()
	sleep(0.2)

def DoAnimationRandVLINE():
	for x in range(8*NUM_PANEL):
		r = random.randint(0,31)
		g = random.randint(0,31)
		b = random.randint(0,31)
		for y in range(0,8):
			p[x][y] = convert24To15Bit(r,g,b)
	UpdatePanels()
	sleep(0.2)
			
def DoAnimationRandVLineScrollLeft():
	r = random.randint(0,31)
	g = random.randint(0,31)
	b = random.randint(0,31)
	for y in range(8):
		p[8*NUM_PANEL-1][y] = convert24To15Bit(r,g,b)
	ScrollPanelsLeft();
	UpdatePanels()
	sleep(0.1)
		
def DoAnimationRandVLineScrollRight():
		r = random.randint(0,31)
		g = random.randint(0,31)
		b = random.randint(0,31)
		for y in range(8):
			p[0][y] = convert24To15Bit(r,g,b)
		ScrollPanelsRight();
		UpdatePanels()
		sleep(0.1)

def DoAnimationRandHLineScrollUp():
	r = random.randint(0,31)
	g = random.randint(0,31)
	b = random.randint(0,31)
	for x in range(8*NUM_PANEL):
		p[x][0] = convert24To15Bit(r,g,b)
	ScrollPanelsUp();
	UpdatePanels()
	sleep(0.1)

def DoAnimationRandHLineScrollDown():
	r = random.randint(0,31)
	g = random.randint(0,31)
	b = random.randint(0,31)
	for x in range(8*NUM_PANEL):
		p[x][7] = convert24To15Bit(r,g,b)
	ScrollPanelsDown();
	UpdatePanels()
	sleep(0.1)

def DoAnimationCircle():
	x = random.randint(0,8*NUM_PANEL)
	y = random.randint(0,8)
	radius = random.randint(1,6)
	r = random.randint(0,31)
	g = random.randint(0,31)
	b = random.randint(0,31)
	Circle( x,y,radius, r,g,b )
	UpdatePanels()
	sleep(0.3)

def DoAnimationSprite(scroll):
	clear()
	r = random.randint(0,31); g = random.randint(0,31); b = random.randint(0,31); Sprite(1,2,  dico['C'], r,g,b)
	r = random.randint(0,31); g = random.randint(0,31); b = random.randint(0,31); Sprite(4,2,  dico['E'], r,g,b)
	r = random.randint(0,31); g = random.randint(0,31); b = random.randint(0,31); Sprite(7,2,  dico['T'], r,g,b)
	r = random.randint(0,31); g = random.randint(0,31); b = random.randint(0,31); Sprite(9,2,  dico['I'], r,g,b)
	r = random.randint(0,31); g = random.randint(0,31); b = random.randint(0,31); Sprite(11,2, dico['C'], r,g,b)
	UpdatePanels()
	sleep(0.2)

	if scroll=="Left":
		for j in range(8*NUM_PANEL):
			ScrollPanelsLeft()
			UpdatePanels()
			sleep(0.1)
	if scroll=="Right":
		for j in range(8*NUM_PANEL):
			ScrollPanelsRight()
			UpdatePanels()
			sleep(0.1)
	if scroll=="Up":
		for j in range(8):
			ScrollPanelsUp()
			UpdatePanels()
			sleep(0.1)
	if scroll=="Down":
		for j in range(8):
			ScrollPanelsDown()
			UpdatePanels()
			sleep(0.1)
	sleep(0.1)

def DoAnimationVirtualPlan():
	clear()
	#Put some text in the virtualplan
	Text(1,2,   "CETIC", random.randint(0,31),random.randint(0,31),random.randint(0,31) ,3)
	Text(21,2,  "ECS LAB", random.randint(0,31),random.randint(0,31),random.randint(0,31), 4)
	Text(1,12,  "CETIC", random.randint(0,31),random.randint(0,31),random.randint(0,31) ,3)
	Text(21,12, "SST LAB", random.randint(0,31),random.randint(0,31),random.randint(0,31), 4)
	
	doIt = 200
	posx = 0; posy = 0; incx = 1; incy = 1;
	while (doIt):
		posx = posx + incx
		posy = posy + incy
		
		if posx < 0 or posx > width(p) - 8*NUM_PANEL:
			incx = -incx
			posx = posx + incx
			
		if posy < 0 or posy > height(p) - 8:
			incy = -incy
			poxy = posy + incy
			
		UpdatePanels(posx, posy); sleep(0.2)
		doIt = doIt - 1

	
def DoAnimationAll():
	LengthOfEachDemo = 30
	while True:
		for i in range(LengthOfEachDemo):
			clear()
			DoAnimationVirtualPlan()
		for i in range(LengthOfEachDemo):
			DoAnimationSprite("Left")
			DoAnimationSprite("Right")
			DoAnimationSprite("Down")
			DoAnimationSprite("Up")
		for i in range(LengthOfEachDemo):
			DoAnimationRandVLineScrollLeft()
		for i in range(LengthOfEachDemo):
			DoAnimationRandVLineScrollRight()
		for i in range(LengthOfEachDemo):
			DoAnimationRandHLineScrollUp()
		for i in range(LengthOfEachDemo):
			DoAnimationRandHLineScrollDown()
		for i in range(LengthOfEachDemo):
			DoAnimationRandPanels()
		for i in range(LengthOfEachDemo):
			DoAnimationRandPixels()
		for i in range(LengthOfEachDemo):
			DoAnimationRandHLINE()
		for i in range(LengthOfEachDemo):
			DoAnimationRandVLINE()
		for i in range(LengthOfEachDemo):
			DoAnimationCircle()

if __name__ == "__main__":
	clear()
	DoAnimationAll()


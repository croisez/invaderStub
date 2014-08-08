invaderStub
===========

This is a kind of simple python replacement for the incredible PixelInvaders Java application

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
#  Circle(xc,yc,radius,r,g,b)
#  Sprite(x,y,data,r,g,b)
#
#  For the sprite, a dictionnary has been initiated, containing a big part of the alphabet.


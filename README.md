invaderStub
===========

This is a kind of simple python replacement for the incredible PixelInvaders Java application

This program, invaderStub, is released as Free Software.

First written by LM Croisez, on 5 Aug 2014

Programme d'interfaçage avec des panneaux du type PixelInvaders
This program makes the itf between 2d xy plan and PixelInvaders-type panels.

The frame can be either sent by TCPIP, or by serial port direct connection.
If using TCPIP, you must setup a ser2net daemon to make the via.
See www.pixelinvaders.ch for more info on this setup.

GENERAL TIPS:
You must use the p(x,y) plan to put there the pixels where you want, and in the 15bit color you want.
Once this is done, you must use the refreshPanels() function to latch your picture to the panels.

The following functions are available:

<pre><code>
clear()                                                   clears the entire screen<br>
UpdatePanels(virtplan_offset_x=0, virtplan_offset_y=0)    Updates content of all LED panels<br>
ScrollPanelsLeft()                                        Scrolls content of panels to left direction<br>
ScrollPanelsRight()                                       Scrolls content of panels to right direction<br>
ScrollPanelsUp()                                          Scrolls content of panels to top direction<br>
ScrollPanelsDown()                                        Scrolls content of panels to bottom direction<br>
Circle(xc,yc,radius, r, g, b, max_x=8*NUM_PANEL, max_y=8) draws a circle<br>
Sprite(x,y,data, r,g,b)                                   draws a predefined sprite (a custom character)<br>
Text(x, y, buf, r, g, b, w=4)                             draws text (using Sprites)<br>
LoadImage(name)                                           loads an external image (PNG, JPG, GIF, BMP)<br>
</code></pre>

 For the Sprite function, a dictionnary has been initiated, containing a big part of the alphabet.


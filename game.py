import time
import math
import random
pi = math.pi
import sys
import curses
import PIL.Image as Image ,PIL.ImageDraw as ImageDraw

from player import player
from lane import lane
from definitions import *
from consoleconvert import consoleconvert
class Game:

   # These are the lane speeds. They are in pairs as the frog moves 2 of these lanes per one jump. This was so I could make better cars. 
   speedmap = [ 0, -8, -8, 10, 10, 5, 5 , 0, 0, 15, 15, -19, -19, 0,0] 

   # This is the lane data. Each character represents a type of tile, and there are some colours for each defined in lane.py 
   lanemap = [ 
         "kmWkmkmWkmkmkWkmkmkmk",    
         "k...kk...kmk...k.....",    
         "nno~~~~nno~~~~~~~~~~nno~~~~~~", #LOGS 2
         "nno~~~~nno~~~~~~~~~~nno~~~~~~", #LOGS 2
         "~~~~nnno~~~~nno~~nno~~~~~",     # LOGS 1
         "~~~~nnno~~~~nno~~nno~~~~~",     # LOGS 1
         "_____________________",         # Safe zone
         "_____________________",         # Safe zone
         "..pp.........c.................b....",    
         ".w..w.......O.O...............ObO...",
         "....ccc....ccc............nnnn....", # CAR LANE 2
         "....ObOb...ObOb...........OOnOn...", # CAR LANE 2
         "....O......r.....O........",         # CAR LANE 1 
         "...bbb....OrO...ggg.......",         # CAR LANE 1
         "_____________________"               # Safe zone
   ]

   # Anything in this list is safe for frogger to be on. put ~ in it and suddenly your frog can swim, like every other frog in the world! 
   safeSpaces = [  ".", ",", "_", "n", "o", "W" ]

   lanes = []
   gamestate = True 
   won = False 
   level = 1

   def __init__(self,  unicornHatController, stdscr, screenWidth=16, screenHeight=16): 
        self.stdscr = stdscr
        self.framecount = 0 
        self.screenWidth = screenWidth; 
        self.screenHeight = screenHeight; 
        self.unicornHatController = unicornHatController; 
        self.image = Image.new('RGBA', (self.screenWidth, self.screenWidth)) 
        self.level = 1
        self.startScreen = True 
        self.xvelocity = 0 
        self.yvelocity = 0 

   def start(self):
        self.startScreen = False 

   def draw(self, xvelocity, yvelocity):
        self.framecount += 1
        self.image = Image.new('RGBA', (self.screenWidth, self.screenWidth))  #This is our blank image, a canvas on which will will draw our game
        self.xvelocity = xvelocity;
        self.yvelocity = yvelocity;

        self.checkGameState() 
        if(self.startScreen):
          self.unicornHatController.splashPlayScreen()
        else:
          if(self.gamestate):
            self.drawLanes()
            self.drawLifeCounter()
            self.drawPlayer()
            self.unicornHatController.draw(self.image)  
          else:
            if(self.won):
                self.gamestate = True
                self.won = False
            else:
                self.showGameOver()
                self.gamestate = False
                self.won = False
                
   def drawPlayer(self):
         self.image = self.player.draw(self.image, self.xvelocity, self.yvelocity)

   def drawLifeCounter(self):
        lives = self.player.lives
        draw = ImageDraw.Draw(self.image)
        for q in range(0, lives):
            draw.point((15, q), fill="purple") 
   
   def addPlayer(self):
     self.player = player(self.lanemap, self.stdscr, self.safeSpaces)

   def checkGameState(self):
        if not self.player.alive : 
            self.player.lives -= 1
            time.sleep(1)
            self.player.resetFrog()

        if self.player.lives < 1: 
            self.gamestate = False 
            self.won = False
            self.level = 1
        else:
           self.player.alive = True

   def log(self, message):
        return message

   def showGameOver(self ):
       self.unicornHatController.gameOver(self.player.score)  
       
   def addLanes(self):
       for (idx, l) in enumerate(self.lanemap[::-1]): 
          self.lanes.append(lane(15 - (idx),self.image, l,self.speedmap[idx] )) 
   
   def drawLanes(self):
      self.level = self.player.level
      level = int(self.player.level/2)
      self.sendToConsole(0,80,"LEVEL"+str(self.level))
      for (idx, l) in enumerate(self.lanes): 
          newlane =  l.lanemap
          if(l.velocity > 0):
            if(self.framecount % (l.velocity - level) == 0 ):
              if(l.lanetype == 'water' and self.player.y == l.x ): #Move the player with the logs if they're in one of the water lanes
                self.player.x += 1
              lastChar = l.lanemap[-1]
              newlane = lastChar + l.lanemap[:-1]
          elif(l.velocity < 0):
            if(self.framecount %  (abs(l.velocity) - level) == 0 ):
              if(l.lanetype == 'water' and self.player.y == l.x ): #Move the player with the logs if they're in one of the water lanes
                self.player.x -= 1
              firstChar = l.lanemap[0]
              newlane =  l.lanemap[1:] + firstChar
          l.lanemap = newlane
          self.lanes[idx] = l;
          self.sendToConsole(10 + l.x, 0, newlane);
          self.image = l.draw(self.image)

   def sendToConsole(self, x,y, message):
          if(SHOW_CONSOLE_VERSION):
             message = consoleconvert(message, EMOJI_ENABLE)
             curses.start_color()
             curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
             self.stdscr.addstr(x, y, message, curses.color_pair(1))

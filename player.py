import PIL.Image as Image ,PIL.ImageDraw as ImageDraw
from definitions import * 
class player:
  def __init__(self, lanes, stdscr, safeSpaces): 
      self.lives = 5
      self.stdscr = stdscr
      self.safeSpaces = safeSpaces
      self.xvelocity = 0
      self.yvelocity = 0
      self.direction = 0
      self.x = 7 
      self.y = 17 
      self.colour = 'rgb(0,123,0)'
      self.colour2 = 'rgb(0,123,0)'
      self.score = 0
      self.level = 1
      self.frogsSafe = 0
      self.alive = True
      self.lanes = lanes

  def draw(self, image, xvelocity, yvelocity ): 

      self.image = image
      self.x = self.x + xvelocity
      self.y = self.y - yvelocity

      #keep player in the screen boundaries 
      if(self.y < 4 and self.x < 0):
          self.alive = False
      if(self.y < 4 and self.x > 15):
          self.alive = False
      if(self.x < 0):
          self.x = 15;
      if(self.x > 15):
          self.x = 0;
      if(self.y < 0):
          self.y = 0;
      if(self.y > 15):
          self.y = 15;


      draw = ImageDraw.Draw(self.image)
      draw.point((self.y, self.x), fill=self.colour2) 
      draw.point((self.y-1, self.x), fill=self.colour) 
      #draw.point((self.y, self.x-1), fill=self.colour) 
      #draw.point((self.y, self.x+1), fill=self.colour) 

      for n in range(0,  16):
        self.drawToConsole(10 +  16,n," ")

      self.drawToConsole(10 + self.y,self.x,"@")
      self.drawToConsole(10 + self.y+1,self.x,"@")
      #self.drawToConsole(11 + self.y,self.x+1,"🦵")
      #self.drawToConsole(11 + self.y,self.x-1,"🦵")

      return self.image

  def drawToConsole(self, x,y, message):
        if(x > 0 and y > 0 ): 
          if(SHOW_CONSOLE_VERSION):
             self.stdscr.addstr(x, y, message)

  def resetFrog(self):
        self.y = 15 # frog starting position
        self.x = 7

  def checkPlayerPosition(self, lanes):
          lanes = lanes[::-1] #Reverse this array to make it make sense 
          try:
            lmap = lanes[self.y].lanemap
            currentTile = lmap[self.x] # This is where we check what the tile type we are on is and if it's safe
            #self.drawToConsole(8,120,currentTile)
            if str(currentTile) not in self.safeSpaces:
                self.alive=False # The frog is dead, let the game class handle it. 
            lmap = lanes[self.y-1].lanemap

            currentTile = lmap[self.x] # This is where we check if the frog got a point
            if str(currentTile) == 'W': # Frog got to the bridge! W for Winner 
               self.score += 1
               self.level += 1
               self.resetFrog()

            self.drawToConsole(8,20,currentTile)
            self.drawToConsole(12,20,"SCORE:" + str(self.score))
            if str(currentTile) not in self.safeSpaces:
                self.alive=False # The frog is dead, let the game handle it. 
      
          except Exception as e: 
               err = True
               #self.drawToConsole(14,20,str(e))
          return lanes[::-1]

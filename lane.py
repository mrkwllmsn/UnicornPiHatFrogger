import PIL.Image as Image ,PIL.ImageDraw as ImageDraw
import time
class lane:
  def __init__(self, x, image, lanemap, velocity ):
    self.image = image
    self.lanemap = lanemap
    self.velocity = velocity
    self.colour = 'rgb(40,40,40)'
    self.lanetype = 'road'
    self.x = x
    if "~" in self.lanemap:
      self.lanetype = 'water'

  def draw(self, image):
      if "~" in self.lanemap:
          self.lanetype = 'water'
      self.image = image
      draw = ImageDraw.Draw(self.image) 

      for ( y, pixel) in enumerate(self.lanemap):
          x = self.x-1
          colour = 'none' 

          if pixel == '_':
              colour = 'rgb(10,10,10)' 
          if pixel == 'O':
              colour = 'rgb(80,80,80)' 
          if pixel == 'r':
              colour = 'red' 
          if pixel == 'W':
              colour = 'green' 
          if pixel == 'F':
              colour = 'green' 
          if pixel == 'k':
              colour = 'red' 
          if pixel == 'm':
              colour = 'rgb(200,40,80)' 
          if pixel == 'g':
              colour = 'rgb(0,100,30)' 
          if pixel == 'b':
              colour = 'blue' 
          if pixel == '~':
              colour = 'rgb(0,13,105)' 
          if pixel == 'c':
              colour = 'cyan' 
          if pixel == 'o':
              colour = 'orange' 
          if pixel == 'n':
              colour = 'rgb(177,85,93)' 
          if pixel == 'p':
              colour = 'pink' 
          if pixel == 'y':
              colour = 'yellow' 
          if pixel == 'w':
              colour = 'white' 

          if colour != "none":
            draw.point((x,y), fill=colour) 
          if(self.lanetype == 'water' and pixel == '~' and y % 2 == 0):
            draw.point((x,y), fill='rgb(0,100,245)')  
      return self.image


import lib.stddraw as stddraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles
import random
# A class for modeling numbered tiles as in 2048
class Tile:
   # Class variables shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.006
   # font family and font size used for displaying the tile number
   font_family, font_size, font_color = "Cascadia Mono", 22, Color(254,254,254)

   # A constructor that creates a tile with 2 as the number on it
   def __init__(self):
      # set the number on this tile
      self.number = random.choice([2,4])
      # set the colors of this tile
      self.background_color_2 = Color(249, 186, 114)  # background (tile) color for 2
      self.background_color_4 = Color(227, 135, 65)  # bg color for number 4
      self.background_color_8 = Color(215, 108, 41)  # bg color for number 8
      self.background_color_16 = Color(202, 84, 23)  # bg color for number 16
      self.background_color_32 = Color(193, 82, 23)  # bg color for number 32
      self.background_color_64 = Color(186, 69, 24)  # bg color for number 64
      self.background_color_128 = Color(181, 63, 24)  # bg color for number 128
      self.background_color_256 = Color(165, 58, 23)  # bg color for number 256
      self.background_color_512 = Color(143, 38, 19)  # bg color for number 512
      self.background_color_1024 = Color(124, 35, 16)  # bg color for number 1024
      self.background_color_2048 = Color(104, 31, 11)  # bg color for number 2048
      self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      self.box_color = Color(14, 98, 148)  # box (boundary) color

   # A method for drawing this tile at a given position with a given length
   def draw(self, position, length=1):  # length defaults to 1
      # draw the tile as a filled square
      if self.number == 2:
         stddraw.setPenColor(self.background_color_2)
      if self.number == 4:
         stddraw.setPenColor(self.background_color_4)
      if self.number == 8:
         stddraw.setPenColor(self.background_color_8)
      if self.number == 16:
         stddraw.setPenColor(self.background_color_16)
      if self.number == 32:
         stddraw.setPenColor(self.background_color_32)
      if self.number == 64:
         stddraw.setPenColor(self.background_color_64)
      if self.number == 128:
         stddraw.setPenColor(self.background_color_128)
      if self.number == 256:
         stddraw.setPenColor(self.background_color_256)
      if self.number == 512:
         stddraw.setPenColor(self.background_color_512)
      if self.number == 1024:
         stddraw.setPenColor(self.background_color_1024)
      if self.number == 2048:
         stddraw.setPenColor(self.background_color_2048)
      if self.number == 5096:
         stddraw.setPenColor(self.background_color_2048)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.font_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.text(position.x, position.y, str(self.number))

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
    font_family, font_size, font_color = "Cascadia Mono", 22, Color(254, 254, 254)

    # A constructor that creates a tile with 2 as the number on it
    def __init__(self):
        # set the number on this tile
        self.number = random.choice([2, 4])
        # set the colors of this tile (Pastel Pembe Tema)
        self.background_color_2 = Color(255, 220, 235)
        self.background_color_4 = Color(235, 210, 250)
        self.background_color_8 = Color(255, 180, 220)
        self.background_color_16 = Color(240, 170, 220)
        self.background_color_32 = Color(225, 150, 200)
        self.background_color_64 = Color(210, 130, 180)
        self.background_color_128 = Color(190, 120, 170)
        self.background_color_256 = Color(175, 110, 160)
        self.background_color_512 = Color(160, 100, 150)
        self.background_color_1024 = Color(140, 90, 140)
        self.background_color_2048 = Color(255, 192, 203)
        self.foreground_color = Color(255, 255, 255)  # Yazı beyaz
        self.box_color = Color(255, 255, 255)  # Kenar hafif pastel pembe

    # A method for drawing this tile at a given position with a given length
    def draw(self, position, length=1):  # length defaults to 1
        # draw the tile as a filled square
        if self.number == 2:
            stddraw.setPenColor(self.background_color_2)
        elif self.number == 4:
            stddraw.setPenColor(self.background_color_4)
        elif self.number == 8:
            stddraw.setPenColor(self.background_color_8)
        elif self.number == 16:
            stddraw.setPenColor(self.background_color_16)
        elif self.number == 32:
            stddraw.setPenColor(self.background_color_32)
        elif self.number == 64:
            stddraw.setPenColor(self.background_color_64)
        elif self.number == 128:
            stddraw.setPenColor(self.background_color_128)
        elif self.number == 256:
            stddraw.setPenColor(self.background_color_256)
        elif self.number == 512:
            stddraw.setPenColor(self.background_color_512)
        elif self.number == 1024:
            stddraw.setPenColor(self.background_color_1024)
        elif self.number == 2048:
            stddraw.setPenColor(self.background_color_2048)
        else:
            # Eğer başka bir sayı varsa, 2048 rengiyle çizsin
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

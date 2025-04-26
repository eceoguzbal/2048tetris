import os  # the os module is used for file and directory operations
from lib.picture import Picture  # used for displaying an image on the game menu
import lib.stddraw as stddraw  # used for displaying the game grid
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
import sys
# A class for modeling the game grid
class GameGrid:
   # A constructor for creating the game grid based on the given arguments


   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      #Add Score qualification to user itterration
      self.score = 0

      self.next_block = None

      self.text_color = Color(14, 98, 148)
      # create a tile matrix to store the tiles locked on the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)

      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(245, 245, 245)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(0, 100, 200)
      self.boundary_color = Color(0, 100, 200)
      # thickness values used for the grid lines and the grid boundaries
      self.line_thickness = 0.001
      self.box_thickness = 4 * self.line_thickness
   # A method for displaying the game grid


   def display(self):
      # clear the background to empty_cell_color
      stddraw.clear(self.empty_cell_color)
      # draw the game grid
      self.draw_grid()
      # draw the current/active tetromino if it is not None
      # (the case when the game grid is updated)
      if self.current_tetromino is not None:
         self.current_tetromino.draw()
      # draw a box around the game grid
      self.draw_boundaries()

       # Draw total score text
      stddraw.setFontFamily("Poppins Bold")
      stddraw.setFontSize(40)
      stddraw.setPenColor(self.text_color)
      stddraw.text(self.grid_width +2.2, self.grid_height - 2, "Total Score")
      stddraw.setFontSize(50)
      stddraw.text(self.grid_width +2.2, self.grid_height - 4.2, ""  + str(self.score))
      stddraw.setFontSize(35)
      stddraw.text(self.grid_width + 2.2, self.grid_height - 9, "Next Tetromino")
      current_dir = os.path.dirname(os.path.realpath(__file__))
      img_file = current_dir + "/images/frame1_updated.png"
      img_center_x, img_center_y = (self.grid_width+2.2), self.grid_height - 11
      image_to_display = Picture(img_file)
      stddraw.picture(image_to_display, img_center_x, img_center_y)
      #Display Control Recive for user
      stddraw.text(self.grid_width + 1.4, self.grid_height - 17, "   P  --> Pause")
      stddraw.text(self.grid_width + 1.5, self.grid_height - 18, "   S  --> Smash")
      stddraw.text(self.grid_width + 2.1, self.grid_height - 19, "Space --> Rotate")

      # Next Block'un altındaki başlangıç koordinatları
      next_block_x = 13.2
      next_block_y = self.grid_height - 12
      # Bir sonraki bloğu çizme
      if self.next_block is not None:
         self.next_block.draw_next_block(next_block_x, next_block_y)

      # show the resulting drawing with a pause duration = 250 ms
      stddraw.show(250)
   
   def exit_game(self):
      sys.exit()  # Terminate the program to close the stddraw window

   def display_end_game(self):
      current_dir = os.path.dirname(os.path.realpath(__file__))
      img_file = current_dir + "/images/end_bg_updated.png"
      img_center_x, img_center_y = (self.grid_width-3.8), self.grid_height - 10.5
      image_to_display = Picture(img_file)
      stddraw.picture(image_to_display, img_center_x, img_center_y)
      stddraw.setFontFamily("Poppins Bold")
      stddraw.setFontSize(80)
      stddraw.setPenColor(Color(245,245,245))
      stddraw.text(self.grid_width -2., self.grid_height - 14.85, ""  + str(self.score))
      stddraw.setFontSize(70)
      stddraw.setPenColor(Color(103,179,46))
      text_yes = "YES"
      stddraw.text(img_center_x-4, 1, text_yes)
      stddraw.setFontSize(70)
      stddraw.setPenColor(Color(166,83,155))
      text_no = "NO"
      stddraw.text(img_center_x+4, 1, text_no)  
      
      while True:
         stddraw.show(50)
         
         # check the mouse reactsion
         if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= 2 and mouse_x <= 6:
               if mouse_y >= 0 and mouse_y <= 2:
                  # If clicked YES, call the display method to restart the game
                  #self.reset_game()
                  from Tetris_2048 import start
                  start()
                  break

            if  mouse_x >= 10 and mouse_x <= 14:
               if mouse_y >= 0 and mouse_y <= 2:
                # If clicked NO, exit the game
                  self.exit_game()    
   
   # A method for drawing the cells and the lines of the game grid
   def draw_grid(self):

      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # if the current grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               # draw this tile
               self.tile_matrix[row][col].draw(Point(col, row))
      # draw the inner lines of the game grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method for drawing the boundaries around the game grid
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method used checking whether the grid cell with the given row and column
   # indexes is occupied by a tile or not (i.e., empty)
   def is_occupied(self, row, col):
      # considering the newly entered tetrominoes to the game grid that may
      # have tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False  # the cell is not occupied as it is outside the grid
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None

   # A method for checking whether the cell with the given row and col indexes
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # A method that locks the tiles of a landed tetromino on the grid checking
   # if the game is over due to having any tile above the topmost grid row.
   # (This method returns True when the game is over and False otherwise.)
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the grid
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):
            # place each tile (occupied cell) onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True

      # Remove filled lines
      self.remove_filled_lines()
      self.merge_tiles()




      # return the value of the game_over flag
      return self.game_over

   # A method to remove filled lines from the grid
   def remove_filled_lines(self):
      lines_to_remove = []
      
      for row in range(self.grid_height):
         if all(self.tile_matrix[row]):
            lines_to_remove.append(row)
            
      for row in reversed(lines_to_remove):
         current_point_from_removing = 0
         
         for tile in self.tile_matrix[row]: 
               if tile is not None:
                  current_point_from_removing += tile.number
         self.score += current_point_from_removing
      
         # Shift the lines above the removed line down
         for r in range(row, self.grid_height - 1):
            self.tile_matrix[r] = self.tile_matrix[r + 1]
         # Fill the top line with None values
         self.tile_matrix[self.grid_height - 1] = [None] * self.grid_width
         

   def merge_tiles(self):
      merged = False  # Flag to keep track of whether any merging occurred in this iteration

      # Iterate over each row and column in the grid
      for row in range(1, self.grid_height):
         for col in range(self.grid_width):
            # Get the current tile and the tile below it
            current_tile = self.tile_matrix[row][col]
            below_tile = self.tile_matrix[row - 1][col]

            # Check if both tiles are not None and have the same number
            if current_tile is not None and below_tile is not None and current_tile.number == below_tile.number:
               # Double the value of the current tile
               current_tile.number *= 2
               
               # add merging tile to the score based on 2048 game idea
               self.score += current_tile.number
               
               # Clear the below tile
               self.tile_matrix[row - 1][col] = None
               merged = True  # Set the merged flag to True

               self.make_tiles_fall_down()  # After merging, make tiles fall down
      self.remove_filled_lines()


      # If any merging occurred in this iteration, recursively call merge_tiles
      if merged:
         self.merge_tiles()


   def make_tiles_fall_down(self):
      # Flag to keep track of whether any tiles have been moved down in this iteration
      moved = False

      # Iterate over each column in the grid
      for col in range(self.grid_width):
         # Iterate over each row  from top to bottom
         for row in range(self.grid_height - 2, -1, -1):  # start from second-to-last row
            # Get the current tile and the tile below it
            current_tile = self.tile_matrix[row][col]
            below_tile = self.tile_matrix[row + 1][col]

            # If the current tile is None and there is a tile below it, move the below tile up
            if current_tile is None and below_tile is not None:
               # Move the below tile up
               self.tile_matrix[row][col] = below_tile
               self.tile_matrix[row + 1][col] = None
               # Set the moved flag to True
               moved = True

      # If any tiles were moved down in this iteration, recursively call make_tiles_fall_down
      if moved:
         self.make_tiles_fall_down()
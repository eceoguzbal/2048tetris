from tile import Tile  # used for modeling each tile on the tetrominoes
from point import Point  # used for tile positions
import copy as cp  # the copy module is used for copying tiles and positions
import random  # the random module is used for generating random values
import numpy as np  # the fundamental Python module for scientific computing


class Tetromino:
   grid_height, grid_width = None, None
 
   def __init__(self, shape):
      self.type = shape  # set the type of this tetromino
      # determine the occupied (non-empty) cells in the tile matrix based on
      # the shape of this tetromino (see the documentation given with this code)
      occupied_cells = []
      if self.type == 'I':
         n = 4  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino I in its initial orientation
         occupied_cells.append((1, 0))  # (column_index, row_index)
         occupied_cells.append((1, 1))
         occupied_cells.append((1, 2))
         occupied_cells.append((1, 3))
      elif self.type == 'O':
         n = 2  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino O in its initial orientation
         occupied_cells.append((0, 0))  # (column_index, row_index)
         occupied_cells.append((1, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
      elif self.type == 'Z':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         occupied_cells.append((0, 0))  # (column_index, row_index)
         occupied_cells.append((1, 0))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
      elif self.type == 'J':
         n = 3
         occupied_cells.append((1, 0))
         occupied_cells.append((1, 1))
         occupied_cells.append((1, 2))
         occupied_cells.append((0, 2))
      elif self.type == 'L':
         n = 3
         occupied_cells.append((0, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((0, 2))
         occupied_cells.append((1, 2))
      elif self.type == 'S':
         n = 3
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((1, 0))
         occupied_cells.append((2, 0))
      elif self.type == 'T':
         n = 3
         occupied_cells.append((0, 0))
         occupied_cells.append((1, 0))
         occupied_cells.append((2, 0))
         occupied_cells.append((1, 1))

      self.tile_matrix = np.full((n, n), None)
      
      for i in range(len(occupied_cells)):
         col_index, row_index = occupied_cells[i][0], occupied_cells[i][1]
        
         self.tile_matrix[row_index][col_index] = Tile()
     
      self.bottom_left_cell = Point()
      self.bottom_left_cell.y = Tetromino.grid_height - 1
      self.bottom_left_cell.x = random.randint(0, Tetromino.grid_width - n)

  
   def get_cell_position(self, row, col):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      position = Point()
      
      position.x = self.bottom_left_cell.x + col
    
      position.y = self.bottom_left_cell.y + (n - 1) - row
      return position

  
   def draw_next_block(self, x, y):
      
      for row_index in range(len(self.tile_matrix)):
         for col_index in range(len(self.tile_matrix[0])):
           
            if self.tile_matrix[row_index][col_index] is not None:
               
               cell_x = x + col_index
               cell_y = y - row_index  # Y ekseni ters yönde olduğu için -
               cell_position = Point(cell_x, cell_y)
               
               self.tile_matrix[row_index][col_index].draw(cell_position)

   def get_min_bounded_tile_matrix(self, return_position=False):
      n = len(self.tile_matrix)  
      # determine rows and columns to copy (omit empty rows and columns)
      min_row, max_row, min_col, max_col = n - 1, 0, n - 1, 0
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               if row < min_row:
                  min_row = row
               if row > max_row:
                  max_row = row
               if col < min_col:
                  min_col = col
               if col > max_col:
                  max_col = col
      
      copy = np.full((max_row - min_row + 1, max_col - min_col + 1), None)
      for row in range(min_row, max_row + 1):
         for col in range(min_col, max_col + 1):
            if self.tile_matrix[row][col] is not None:
               row_ind = row - min_row
               col_ind = col - min_col
               copy[row_ind][col_ind] = cp.deepcopy(self.tile_matrix[row][col])
     
      if not return_position:
         return copy
      
      else:
         blc_position = cp.copy(self.bottom_left_cell)
         blc_position.translate(min_col, (n - 1) - max_row)
         return copy, blc_position

   def draw(self):
      n = len(self.tile_matrix)  
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               position = self.get_cell_position(row, col)
               if position.y < Tetromino.grid_height:
                  self.tile_matrix[row][col].draw(position)

   def move(self, direction, game_grid):
      if not (self.can_be_moved(direction, game_grid)):
         return False  
      if direction == "left":
         self.bottom_left_cell.x -= 1
      elif direction == "right":
         self.bottom_left_cell.x += 1
      elif direction == "space":
         n = len(self.tile_matrix)
         copy_tile_for_rotation = np.full((n,n), None)
         for row in range(n):
            for col in range(n):
               copy_tile_for_rotation[col][n-1-row] = self.tile_matrix[row][col]
         self.tile_matrix = copy_tile_for_rotation
      else:  
         self.bottom_left_cell.y -= 1
      return True  

   def can_be_moved(self, direction, game_grid):
      n = len(self.tile_matrix)  
      if direction == "left" or direction == "right" or direction == "space":
         for row_index in range(n):
            for col_index in range(n):
               row, col = row_index, col_index
               if direction == "left" and self.tile_matrix[row][col] is not None:
                  
                  leftmost = self.get_cell_position(row, col)
                  
                  if leftmost.x == 0:
                     return False  
                  
                  if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                     return False  
                  
                  break  
              
               row, col = row_index, n - 1 - col_index
               if direction == "right" and self.tile_matrix[row][col] is not None:
                  rightmost = self.get_cell_position(row, col)
                  if rightmost.x == Tetromino.grid_width - 1:
                     return False  
                  if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                     return False  
                  break  
               
               if direction == "space" and self.tile_matrix[row][col] is not None:
                  leftmost = self.get_cell_position(row, col)
                  rightmost = self.get_cell_position(row, n - 1 - col_index)
                  if leftmost.x == 0 or rightmost.x == Tetromino.grid_width - 1:
                     return False 
                  if game_grid.is_occupied(leftmost.y, leftmost.x - 1) or game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                     return False  
                   
                  break  
               
     
      else:
         for col in range(n):
            for row in range(n - 1, -1, -1):
              
               if self.tile_matrix[row][col] is not None:
                  
                  bottommost = self.get_cell_position(row, col)
                  
                  if bottommost.y == 0:
                     return False 
                 
                  if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                     return False  
                 
                  break 
    
      return True 

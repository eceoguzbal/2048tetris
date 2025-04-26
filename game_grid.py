import os
import sys
import numpy as np
import lib.stddraw as stddraw
from lib.picture import Picture
from lib.color import Color
from point import Point

class GameGrid:
    def __init__(self, grid_h, grid_w):
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.score = 0
        self.next_block = None
        self.current_tetromino = None
        self.game_over = False

        self.tile_matrix = np.full((grid_h, grid_w), None)
        self.empty_cell_color = Color(255, 255, 255)
        self.line_color = Color(230, 150, 200)
        self.boundary_color = Color(210, 130, 190)
        self.text_color = Color(220, 120, 180)

        self.line_thickness = 0.001
        self.box_thickness = 4 * self.line_thickness

    def display(self):
        stddraw.clear(self.empty_cell_color)
        self.draw_grid()

        if self.current_tetromino:
            self.current_tetromino.draw()

        self.draw_boundaries()
        self.draw_ui()
        stddraw.show(250)

    def draw_ui(self):
        stddraw.setFontFamily("Poppins Bold")
        stddraw.setFontSize(40)
        stddraw.setPenColor(self.text_color)
        stddraw.text(self.grid_width + 2.2, self.grid_height - 2, "Total Score")

        stddraw.setFontSize(50)
        stddraw.text(self.grid_width + 2.2, self.grid_height - 4.2, str(self.score))

        stddraw.setFontSize(35)
        stddraw.text(self.grid_width + 2.2, self.grid_height - 9, "Next Tetromino")

        current_dir = os.path.dirname(os.path.realpath(__file__))
        img_path = os.path.join(current_dir, "images/frame1_updated.png")
        frame_image = Picture(img_path)
        stddraw.picture(frame_image, self.grid_width + 2.2, self.grid_height - 11)

        stddraw.text(self.grid_width + 1.4, self.grid_height - 17, "P  --> Pause")
        stddraw.text(self.grid_width + 1.5, self.grid_height - 18, "S  --> Smash")
        stddraw.text(self.grid_width + 2.1, self.grid_height - 19, "Space --> Rotate")

        if self.next_block:
            self.next_block.draw_next_block(13.2, self.grid_height - 12)

    def exit_game(self):
        sys.exit()

    def display_end_game(self):
        stddraw.clear(self.empty_cell_color)
        current_dir = os.path.dirname(os.path.realpath(__file__))
        img_path = os.path.join(current_dir, "images/end_bg_updated.png")
        end_image = Picture(img_path)

        img_center_x, img_center_y = self.grid_width - 3.8, self.grid_height - 10.5
        stddraw.picture(end_image, img_center_x, img_center_y)

        stddraw.setFontFamily("Poppins Bold")
        stddraw.setFontSize(80)
        stddraw.setPenColor(Color(245, 245, 245))
        stddraw.text(self.grid_width - 2, self.grid_height - 14.85, str(self.score))

        stddraw.setFontSize(70)
        stddraw.setPenColor(Color(103, 179, 46))
        stddraw.text(img_center_x - 4, 1, "YES")

        stddraw.setPenColor(Color(166, 83, 155))
        stddraw.text(img_center_x + 4, 1, "NO")

        while True:
            stddraw.show(50)
            if stddraw.mousePressed():
                mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                if 2 <= mouse_x <= 6 and 0 <= mouse_y <= 2:
                    from Tetris_2048 import start
                    start()
                    break
                elif 10 <= mouse_x <= 14 and 0 <= mouse_y <= 2:
                    self.exit_game()

    def draw_grid(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                tile = self.tile_matrix[row][col]
                if tile:
                    tile.draw(Point(col, row))

        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)

        for x in np.arange(0.5, self.grid_width, 1):
            stddraw.line(x - 1, -0.5, x - 1, self.grid_height - 0.5)
        for y in np.arange(0.5, self.grid_height, 1):
            stddraw.line(-0.5, y - 1, self.grid_width - 0.5, y - 1)

        stddraw.setPenRadius()

    def draw_boundaries(self):
        stddraw.setPenColor(self.boundary_color)
        stddraw.setPenRadius(self.box_thickness)
        stddraw.rectangle(-0.5, -0.5, self.grid_width, self.grid_height)
        stddraw.setPenRadius()

    def is_inside(self, row, col):
        return 0 <= row < self.grid_height and 0 <= col < self.grid_width

    def is_occupied(self, row, col):
        return self.is_inside(row, col) and self.tile_matrix[row][col] is not None

    def update_grid(self, tiles_to_lock, blc_position):
        self.current_tetromino = None
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])

        for col in range(n_cols):
            for row in range(n_rows):
                tile = tiles_to_lock[row][col]
                if tile:
                    pos = Point(blc_position.x + col, blc_position.y + (n_rows - 1) - row)
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tile
                    else:
                        self.game_over = True

        self.remove_filled_lines()
        self.merge_tiles()
        return self.game_over

    def remove_filled_lines(self):
        filled_rows = [row for row in range(self.grid_height) if all(self.tile_matrix[row])]
        for row in reversed(filled_rows):
            self.score += sum(tile.number for tile in self.tile_matrix[row] if tile)
            for r in range(row, self.grid_height - 1):
                self.tile_matrix[r] = self.tile_matrix[r + 1]
            self.tile_matrix[self.grid_height - 1] = [None] * self.grid_width

    def merge_tiles(self):
        merged = False
        for row in range(1, self.grid_height):
            for col in range(self.grid_width):
                curr = self.tile_matrix[row][col]
                below = self.tile_matrix[row - 1][col]
                if curr and below and curr.number == below.number:
                    curr.number *= 2
                    self.score += curr.number
                    self.tile_matrix[row - 1][col] = None
                    merged = True
                    self.make_tiles_fall_down()

        self.remove_filled_lines()
        if merged:
            self.merge_tiles()

    def make_tiles_fall_down(self):
        moved = False
        for col in range(self.grid_width):
            for row in range(self.grid_height - 2, -1, -1):
                curr = self.tile_matrix[row][col]
                below = self.tile_matrix[row + 1][col]
                if curr is None and below:
                    self.tile_matrix[row][col] = below
                    self.tile_matrix[row + 1][col] = None
                    moved = True
        if moved:
            self.make_tiles_fall_down()

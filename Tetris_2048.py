//Main code

# Import necessary modules and classes
import os
import random
import game_grid
import lib.stddraw as stddraw
from lib.picture import Picture
from lib.color import Color
from game_grid import GameGrid
from tetromino import Tetromino

class Tetris2048:
    def __init__(self):
        # Initialize game attributes
        self.paused = False
        self.grid_h, self.grid_w = 20, 12
        self.canvas_h, self.canvas_w = 40 * self.grid_h, 40 * self.grid_w

        # Set up canvas
        stddraw.setCanvasSize(self.canvas_w + 200, self.canvas_h)
        stddraw.setXscale(-0.5, self.grid_w + 5.0)
        stddraw.setYscale(-0.5, self.grid_h - 0.5)

        # Set grid dimensions in Tetromino class
        Tetromino.grid_height = self.grid_h
        Tetromino.grid_width = self.grid_w

        # Create initial game grid and tetromino
        self.grid = GameGrid(self.grid_h, self.grid_w)
        self.current_tetromino = self.create_tetromino()
        self.grid.current_tetromino = self.current_tetromino

        self.score = 0

        # Create next tetromino
        self.next_block = self.create_tetromino()
        self.grid.next_block = self.next_block

        # Display game menu
        self.display_game_menu()

    def start(self):
        while True:
            key_typed = None

            if stddraw.hasNextKeyTyped():
                key_typed = stddraw.nextKeyTyped()

                if key_typed == "p":
                    self.toggle_pause()
                    if self.paused:
                        self.display_pause_menu()
                elif key_typed in ["left", "right", "down", "space"]:
                    self.current_tetromino.move(key_typed, self.grid)

                stddraw.clearKeysTyped()

            if not self.paused:
                if key_typed == "s":
                    while True:
                        success = self.current_tetromino.move("down", self.grid)
                        if not success:
                            tiles, pos = self.current_tetromino.get_min_bounded_tile_matrix(True)
                            game_over = self.grid.update_grid(tiles, pos)

                            if game_over:
                                break

                            self.current_tetromino = self.next_block
                            self.grid.current_tetromino = self.current_tetromino
                            self.next_block = self.create_tetromino()
                            self.grid.next_block = self.next_block
                            break
                else:
                    success = self.current_tetromino.move("down", self.grid)
                    if not success:
                        tiles, pos = self.current_tetromino.get_min_bounded_tile_matrix(True)
                        game_over = self.grid.update_grid(tiles, pos)

                        if game_over:
                            break

                        self.current_tetromino = self.next_block
                        self.grid.current_tetromino = self.current_tetromino
                        self.next_block = self.create_tetromino()
                        self.grid.next_block = self.next_block

            self.grid.display()

        self.grid.display_end_game()
        print("Game over")

    def toggle_pause(self):
        self.paused = not self.paused

    def create_tetromino(self):
        tetromino_types = ['I', 'O', 'Z', 'J', 'L', 'S', 'T']
        random_type = random.choice(tetromino_types)
        return Tetromino(random_type)

    def display_game_menu(self):
        # Set menu colors
        background_color = Color(245, 245, 245)
        button_color = Color(245, 245, 245)
        text_color = Color(14, 98, 148)

        # Clear canvas
        stddraw.clear(background_color)

        # Load and display background image
        current_dir = os.path.dirname(os.path.realpath(__file__))
        img_file = os.path.join(current_dir, "images", "Tetris_bg_v5.png")
        image_to_display = Picture(img_file)

        img_center_x, img_center_y = (self.grid_w - 3.7), self.grid_h - 11
        stddraw.picture(image_to_display, img_center_x, img_center_y)

        # Draw start game button
        button_w, button_h = self.grid_w - 1, 2
        button_blc_x, button_blc_y = img_center_x - button_w / 2, 3

        stddraw.setPenColor(button_color)
        stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)

        stddraw.setFontFamily("Poppins Bold")
        stddraw.setFontSize(30)
        stddraw.setPenColor(text_color)
        stddraw.text(img_center_x, 4, "Click Here to Start the Game")

        # Wait for mouse click to start game
        while True:
            stddraw.show(50)
            if stddraw.mousePressed():
                mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                if (button_blc_x <= mouse_x <= button_blc_x + button_w and
                    button_blc_y <= mouse_y <= button_blc_y + button_h):
                    break

    def display_pause_menu(self):
        print("Game Paused")
        pass

# Entry point
if __name__ == '__main__':
    tetris_game = Tetris2048()
    tetris_game.start()

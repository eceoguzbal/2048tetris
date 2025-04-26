################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

# Import necessary modules and classes
import game_grid  # Module for the game grid
import lib.stddraw as stddraw  # Module for creating an animation with user interactions
from lib.picture import Picture  # Module for displaying an image on the game menu
from lib.color import Color  # Module for coloring the game menu
import os  # Module for file and directory operations
from game_grid import GameGrid  # Class for modeling the game grid
from tetromino import Tetromino  # Class for modeling the tetrominoes
import random  # Module for generating random numbers

class Tetris2048:
    def __init__(self):
        # Initialize game attributes
        self.paused = False
        self.grid_h, self.grid_w = 20, 12  # Define grid height and width
        self.canvas_h, self.canvas_w = 40 * self.grid_h, 40 * self.grid_w  # Define canvas dimensions
        # Set up canvas
        stddraw.setCanvasSize(self.canvas_w + 200, self.canvas_h)
        stddraw.setXscale(-0.5, self.grid_w + 5.0)
        stddraw.setYscale(-0.5, self.grid_h - 0.5)
        Tetromino.grid_height = self.grid_h
        Tetromino.grid_width = self.grid_w
        # Create game grid and initial tetromino
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
                # Toggle pause if 'p' key is pressed
                if key_typed == "p":
                    self.toggle_pause()
                    if self.paused:
                        self.display_pause_menu()
                # Move tetromino left, right, down, or rotate with arrow keys or spacebar
                elif key_typed in ["left", "right", "down", "space"]:
                    self.current_tetromino.move(key_typed, self.grid)
                stddraw.clearKeysTyped()

            if not self.paused:
                # Move tetromino down automatically unless paused
                if key_typed == "s":
                    while True:
                        success = self.current_tetromino.move("down", self.grid)
                        if not success:
                            # Update grid and check for game over when tetromino cannot move down further
                            tiles, pos = self.current_tetromino.get_min_bounded_tile_matrix(True)
                            game_over = self.grid.update_grid(tiles, pos)
                            if game_over:
                                break
                            # Move to next tetromino
                            self.current_tetromino = self.next_block
                            self.grid.current_tetromino = self.current_tetromino
                            self.next_block = self.create_tetromino()
                            self.grid.next_block = self.next_block
                            break
                else:
                    # Move tetromino down and update grid when it cannot move down further
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

        # Display end game message
        self.grid.display_end_game()
        print("Game over")

    def toggle_pause(self):
        # Toggle pause state
        self.paused = not self.paused

    def create_tetromino(self):
        # Create a new tetromino with a random shape
        tetromino_types = ['I', 'O', 'Z', 'J', 'L', 'S', 'T']
        random_index = random.randint(0, len(tetromino_types) - 1)
        random_type = tetromino_types[random_index]
        tetromino = Tetromino(random_type)
        return tetromino

    def display_game_menu(self):
        # Display the game menu
        # the colors used for the menu
        background_color = Color(245, 245, 245)
        button_color = Color(245, 245, 245)
        text_color = Color(14, 98, 148)
        # clear the background drawing canvas to background_color
        stddraw.clear(background_color)
        # get the directory in which this python code file is placed
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # compute the path of the image file
        img_file = current_dir + "/images/Tetris_bg_v5.png"
        # the coordinates to display the image centered horizontally
        img_center_x, img_center_y = (self.grid_w - 3.7), self.grid_h - 11
        # the image is modeled by using the Picture class
        image_to_display = Picture(img_file)
        # add the image to the drawing canvas
        stddraw.picture(image_to_display, img_center_x, img_center_y)
        # the dimensions for the start game button
        button_w, button_h = self.grid_w - 1, 2
        # the coordinates of the bottom left corner for the start game button
        button_blc_x, button_blc_y = img_center_x - button_w / 2, 3
        # add the start game button as a filled rectangle
        stddraw.setPenColor(button_color)
        stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
        # add the text on the start game button
        stddraw.setFontFamily("Poppins Bold")
        stddraw.setFontSize(30)
        stddraw.setPenColor(text_color)
        text_to_display = "Click Here to Start the Game"
        stddraw.text(img_center_x, 4, text_to_display)

      # the user interaction loop for the simple menu
        while True:
            # display the menu and wait for a short time (50 ms)
            stddraw.show(50)
            # check if the mouse has been left-clicked on the start game button
            if stddraw.mousePressed():
               # get the coordinates of the most recent location at which the mouse
               # has been left-clicked
                mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                # check if these coordinates are inside the button         
                if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                    if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                        break # break the loop to end the method and start the game

    def display_pause_menu(self):
        # Display the pause menu
        print("Game Paused")
        pass


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    # Start the Tetris 2048 game
    tetris_game = Tetris2048()
    tetris_game.start()

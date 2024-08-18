import random
import numpy as np

class Game2048:
    def __init__(self, size=4):
        # Initialize the game with a board of the given size (default is 4x4)
        self.size = size
        self.board = np.zeros((size, size), dtype=int)  # Create a board filled with zeros
        self.add_new_tile()  # Add the first tile to the board
        self.add_new_tile()  # Add the second tile to the board

    def add_new_tile(self):
        # Find all empty cells on the board (those with a value of 0)
        empty_cells = list(zip(*np.where(self.board == 0)))
        if empty_cells:  # If there are empty cells available
            i, j = random.choice(empty_cells)  # Randomly select one of the empty cells
            self.board[i][j] = 2 if random.random() < 0.9 else 4  # Place a 2 or 4 on the selected cell

    def compress(self):
        # Slide all non-zero tiles to the left
        new_board = np.zeros_like(self.board)  # Create a new board filled with zeros
        for i in range(self.size):
            position = 0  # Start at the leftmost position
            for j in range(self.size):
                if self.board[i][j] != 0:  # If the cell is not empty
                    new_board[i][position] = self.board[i][j]  # Move the tile to the left
                    position += 1  # Move to the next position on the row
        self.board = new_board  # Update the board with the compressed version

    def merge(self):
        # Combine adjacent tiles with the same value
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.board[i][j] == self.board[i][j + 1] and self.board[i][j] != 0:
                    self.board[i][j] *= 2  # Double the value of the tile
                    self.board[i][j + 1] = 0  # Empty the next cell

    def reverse(self):
        # Reverse the order of tiles in each row (used for right moves)
        self.board = np.fliplr(self.board)

    def transpose(self):
        # Transpose the board (used for up/down moves)
        self.board = self.board.T

    def move_left(self):
        # Perform a left move
        self.compress()  # Slide all tiles to the left
        self.merge()     # Combine adjacent tiles
        self.compress()  # Slide again after merging

    def move_right(self):
        # Perform a right move
        self.reverse()   # Reverse the rows to simulate a right move
        self.move_left() # Apply the left move logic
        self.reverse()   # Reverse back to original order

    def move_up(self):
        # Perform an upward move
        self.transpose() # Transpose to simulate a vertical move
        self.move_left() # Apply the left move logic
        self.transpose() # Transpose back to original orientation

    def move_down(self):
        # Perform a downward move
        self.transpose() # Transpose to simulate a vertical move
        self.move_right()# Apply the right move logic
        self.transpose() # Transpose back to original orientation

    def check_game_over(self):
        # Check if there are any moves left
        if any(0 in row for row in self.board):
            return False  # If there's an empty cell, the game is not over
        for i in range(self.size):
            for j in range(self.size - 1):
                # Check for possible merges horizontally and vertically
                if self.board[i][j] == self.board[i][j + 1] or self.board[j][i] == self.board[j + 1][i]:
                    return False  # If a merge is possible, the game is not over
        return True  # No moves left, the game is over

    def play(self):
        # Main game loop
        while True:
            print(self.board)  # Print the current state of the board
            move = input("Enter move (w/a/s/d): ")  # Get user input for the move
            if move == 'w':
                self.move_up()
            elif move == 'a':
                self.move_left()
            elif move == 's':
                self.move_down()
            elif move == 'd':
                self.move_right()
            else:
                print("Invalid move!")  # If the input is not valid, ask again
                continue

            self.add_new_tile()  # Add a new tile after each move

            if self.check_game_over():  # Check if the game is over
                print("Game Over!")
                print(self.board)  # Print the final board state
                break

if __name__ == "__main__":
    game = Game2048()  # Create a new game instance
    game.play()  # Start playing the game

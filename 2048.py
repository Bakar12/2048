import tkinter as tk
import random
import numpy as np


class Game2048GUI:
    def __init__(self, master):
        # Initialize the main window
        self.master = master
        self.master.title("2048 Game")

        # Set the grid size (4x4)
        self.size = 4

        # Initialize the game board as a 4x4 matrix filled with zeros
        self.board = np.zeros((self.size, self.size), dtype=int)

        # List to store the GUI elements for each cell
        self.grid_cells = []

        # Setting up the grid GUI
        self.grid_frame = tk.Frame(self.master, bg='azure3')
        self.grid_frame.grid(padx=10, pady=10)

        # Create the grid and store label references in grid_cells
        for i in range(self.size):
            row = []
            for j in range(self.size):
                # Create a frame for each cell
                cell = tk.Frame(self.grid_frame, bg='azure4', width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)

                # Create a label inside each frame to display the tile value
                label = tk.Label(cell, text="", bg='azure4', justify=tk.CENTER,
                                 font=("Arial", 24, "bold"), width=4, height=2)
                label.grid()
                row.append(label)
            self.grid_cells.append(row)

        # Add the first two tiles to the board
        self.add_new_tile()
        self.add_new_tile()

        # Update the grid to reflect the initial board state
        self.update_grid()

        # Bind arrow keys to the corresponding move methods
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)

    def add_new_tile(self):
        # Add a new tile (2 or 4) to a random empty cell
        empty_cells = list(zip(*np.where(self.board == 0)))
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid(self):
        # Update the grid GUI based on the current state of the board
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                if value == 0:
                    # Empty cell
                    self.grid_cells[i][j].configure(text="", bg='azure4')
                else:
                    # Cell with a tile, update text and background color
                    self.grid_cells[i][j].configure(text=str(value), bg=self.get_tile_color(value))

        # Ensure the GUI is updated immediately
        self.master.update_idletasks()

    @staticmethod
    def get_tile_color(value):
        # Return the background color based on the tile's value
        colors = {
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }
        return colors.get(value, "#3c3a32")  # Default color for tiles above 2048

    def compress(self):
        # Slide all non-zero tiles to the left, leaving zeros to the right
        new_board = np.zeros_like(self.board)
        for i in range(self.size):
            position = 0
            for j in range(self.size):
                if self.board[i][j] != 0:
                    new_board[i][position] = self.board[i][j]
                    position += 1
        self.board = new_board

    def merge(self):
        # Merge adjacent tiles of the same value
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.board[i][j] == self.board[i][j + 1] and self.board[i][j] != 0:
                    self.board[i][j] *= 2  # Double the value of the merged tile
                    self.board[i][j + 1] = 0  # Set the next cell to 0

    def reverse(self):
        # Reverse the order of tiles in each row (used for right moves)
        self.board = np.fliplr(self.board)

    def transpose(self):
        # Transpose the board (used for up/down moves)
        self.board = self.board.T

    def move_left(self, event=None):
        # Perform a left move
        self.compress()  # Slide tiles to the left
        self.merge()  # Merge adjacent tiles
        self.compress()  # Slide again after merging
        self.add_new_tile()  # Add a new tile after the move
        self.update_grid()  # Update the GUI to reflect the new state
        if self.check_game_over():
            self.show_game_over()

    def move_right(self, event=None):
        # Perform a right move
        self.reverse()  # Reverse the rows to simulate a right move
        self.move_left()  # Apply the left move logic (which now acts as right due to the reverse)
        self.reverse()  # Reverse back to the original order

    def move_up(self, event=None):
        # Perform an upward move
        self.transpose()  # Transpose the board to simulate a vertical move
        self.move_left()  # Apply the left move logic (which now acts as up due to the transpose)
        self.transpose()  # Transpose back to the original orientation

    def move_down(self, event=None):
        # Perform a downward move
        self.transpose()  # Transpose the board to simulate a vertical move
        self.move_right()  # Apply the right move logic (which now acts as down due to the transpose)
        self.transpose()  # Transpose back to the original orientation

    def check_game_over(self):
        # Check if there are any moves left (game over condition)
        if any(0 in row for row in self.board):
            return False  # If there's an empty cell, the game is not over
        for i in range(self.size):
            for j in range(self.size - 1):
                # Check for possible merges horizontally and vertically
                if self.board[i][j] == self.board[i][j + 1] or self.board[j][i] == self.board[j + 1][i]:
                    return False  # If a merge is possible, the game is not over
        return True  # No moves left, the game is over

    def show_game_over(self):
        # Display a "Game Over" message and a restart button
        game_over_frame = tk.Frame(self.master, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(game_over_frame, text="Game Over!", bg="red", fg="white", font=("Arial", 24, "bold")).pack()
        tk.Button(game_over_frame, text="Restart", command=self.restart_game).pack()

    def restart_game(self):
        # Restart the game by reinitializing the board and adding new tiles
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()


if __name__ == "__main__":
    # Create the main window and start the game
    root = tk.Tk()
    game = Game2048GUI(root)
    root.mainloop()

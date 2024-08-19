import tkinter as tk
import random
import numpy as np


class Game2048Logic:
    """Class that handles the core logic for the 2048 game."""

    def __init__(self, size=4):
        """
        Initialize the game board and add the first two tiles.
        Args:
            size (int): The size of the game board (default is 4x4).
        """
        try:
            self.size = size  # Size of the game board (e.g., 4x4)
            self.board = np.zeros((self.size, self.size), dtype=int)  # Initialize the board with zeros
            self.add_new_tile()  # Add the first tile
            self.add_new_tile()  # Add the second tile
        except Exception as e:
            print(f"Error initializing the game: {e}")

    def add_new_tile(self):
        """Adds a new tile (either 2 or 4) to a random empty cell on the board."""
        try:
            empty_cells = list(zip(*np.where(self.board == 0)))  # Find all empty cells
            if empty_cells:  # Check if there are any empty cells
                i, j = random.choice(empty_cells)  # Select a random empty cell
                self.board[i][j] = 2 if random.random() < 0.9 else 4  # Place a 2 or 4 tile
        except Exception as e:
            print(f"Error adding a new tile: {e}")

    def compress(self):
        """
        Slides all non-zero tiles to the left, leaving zeros to the right.
        Returns:
            bool: True if any tile was moved, False otherwise.
        """
        try:
            moved = False
            new_board = np.zeros_like(self.board)  # Create a new board filled with zeros
            for i in range(self.size):
                position = 0
                for j in range(self.size):
                    if self.board[i][j] != 0:  # If the tile is non-zero, move it to the leftmost empty spot
                        new_board[i][position] = self.board[i][j]
                        if position != j:
                            moved = True  # A move was made if the tile moved from its original position
                        position += 1
            self.board = new_board  # Update the board with the compressed version
            return moved
        except Exception as e:
            print(f"Error compressing the board: {e}")
            return False

    def merge(self):
        """
        Merges adjacent tiles of the same value.
        Returns:
            bool: True if any merge happened, False otherwise.
        """
        try:
            merged = False
            for i in range(self.size):
                for j in range(self.size - 1):
                    if self.board[i][j] == self.board[i][j + 1] and self.board[i][j] != 0:
                        self.board[i][j] *= 2  # Double the value of the tile
                        self.board[i][j + 1] = 0  # Set the next tile to zero
                        merged = True  # A merge occurred
            return merged
        except Exception as e:
            print(f"Error merging the tiles: {e}")
            return False

    def reverse(self):
        """Reverses the order of tiles in each row (used for right moves)."""
        try:
            self.board = np.fliplr(self.board)  # Flip the board horizontally
        except Exception as e:
            print(f"Error reversing the board: {e}")

    def transpose(self):
        """Transposes the board (used for up/down moves)."""
        try:
            self.board = self.board.T  # Transpose the board (swap rows and columns)
        except Exception as e:
            print(f"Error transposing the board: {e}")

    def move_left(self):
        """
        Performs a left move, including compressing and merging.
        Returns:
            bool: True if the board changed (tiles moved or merged), False otherwise.
        """
        try:
            moved = self.compress()  # Slide tiles to the left
            merged = self.merge()  # Merge tiles if possible
            if merged:
                self.compress()  # Slide again after merging
            if moved or merged:
                self.add_new_tile()  # Add a new tile if the board changed
            return moved or merged
        except Exception as e:
            print(f"Error moving tiles left: {e}")
            return False

    def move_right(self):
        """
        Performs a right move by reversing, moving left, and reversing back.
        Returns:
            bool: True if the board changed, False otherwise.
        """
        try:
            self.reverse()  # Reverse the board to simulate a right move as a left move
            moved_or_merged = self.move_left()  # Move left
            self.reverse()  # Reverse back to restore the original orientation
            return moved_or_merged
        except Exception as e:
            print(f"Error moving tiles right: {e}")
            return False

    def move_up(self):
        """
        Performs an upward move by transposing, moving left, and transposing back.
        Returns:
            bool: True if the board changed, False otherwise.
        """
        try:
            self.transpose()  # Transpose the board to simulate an up move as a left move
            moved_or_merged = self.move_left()  # Move left
            self.transpose()  # Transpose back to restore the original orientation
            return moved_or_merged
        except Exception as e:
            print(f"Error moving tiles up: {e}")
            return False

    def move_down(self):
        """
        Performs a downward move by transposing, moving right, and transposing back.
        Returns:
            bool: True if the board changed, False otherwise.
        """
        try:
            self.transpose()  # Transpose the board to simulate a down move as a right move
            moved_or_merged = self.move_right()  # Move right
            self.transpose()  # Transpose back to restore the original orientation
            return moved_or_merged
        except Exception as e:
            print(f"Error moving tiles down: {e}")
            return False

    def check_game_over(self):
        """
        Checks if the game is over by verifying available moves and merges.
        Returns:
            bool: True if no moves or merges are possible, False otherwise.
        """
        try:
            if any(0 in row for row in self.board):  # If there's an empty cell, the game is not over
                return False
            for i in range(self.size):
                for j in range(self.size - 1):
                    if self.board[i][j] == self.board[i][j + 1] or self.board[j][i] == self.board[j + 1][i]:
                        return False  # If adjacent tiles can be merged, the game is not over
            return True  # No moves left, game over
        except Exception as e:
            print(f"Error checking game over condition: {e}")
            return True


class Game2048GUI:
    """Class that handles the graphical user interface (GUI) for the 2048 game."""

    def __init__(self, master, game_logic):
        """
        Initialize the main window and link it with the game logic.
        Args:
            master (tk.Tk): The root window for the GUI.
            game_logic (Game2048Logic): The game logic instance.
        """
        try:
            self.master = master
            self.master.title("2048 Game")  # Set the window title
            self.game_logic = game_logic  # Link the GUI with the game logic

            self.grid_cells = []  # List to store the GUI elements for each cell

            # Animation parameters
            self.animation_steps = 10  # Number of steps for the animation
            self.animation_delay = 20  # Delay between animation steps (in milliseconds)

            # Setting up the grid GUI
            self.grid_frame = tk.Frame(self.master, bg='azure3')
            self.grid_frame.grid(padx=10, pady=10)

            # Create the grid and store label references in grid_cells
            for i in range(self.game_logic.size):
                row = []
                for j in range(self.game_logic.size):
                    cell = tk.Frame(self.grid_frame, bg='azure4', width=100, height=100)
                    cell.grid(row=i, column=j, padx=5, pady=5)
                    label = tk.Label(cell, text="", bg='azure4', justify=tk.CENTER, font=("Arial", 24, "bold"), width=4,
                                     height=2)
                    label.grid()
                    row.append(label)
                self.grid_cells.append(row)

            self.update_grid()  # Update the grid to reflect the initial board state

            # Bind arrow keys to the corresponding move methods
            self.master.bind("<Up>", self.move_up)
            self.master.bind("<Down>", self.move_down)
            self.master.bind("<Left>", self.move_left)
            self.master.bind("<Right>", self.move_right)
        except Exception as e:
            print(f"Error initializing the GUI: {e}")

    def update_grid(self):
        """Updates the grid GUI based on the current state of the board."""
        try:
            for i in range(self.game_logic.size):
                for j in range(self.game_logic.size):
                    value = self.game_logic.board[i][j]
                    if value == 0:  # If the cell is empty
                        self.grid_cells[i][j].configure(text="", bg="azure4")
                    else:  # If the cell has a number
                        self.grid_cells[i][j].configure(text=str(value), bg="orange", fg="white")
        except Exception as e:
            print(f"Error updating the grid: {e}")

    def animate_merge(self, start_pos, end_pos):
        """
        Animates the merging of tiles by moving a label from the start to the end position.
        Args:
            start_pos (tuple): The starting position of the tile (row, column).
            end_pos (tuple): The ending position of the tile (row, column).
        """
        try:
            start_x = start_pos[1] * 110  # X-coordinate based on the column
            start_y = start_pos[0] * 110  # Y-coordinate based on the row
            end_x = end_pos[1] * 110  # X-coordinate for the destination column
            end_y = end_pos[0] * 110  # Y-coordinate for the destination row

            animation_label = tk.Label(self.grid_frame, text=str(self.game_logic.board[end_pos[0]][end_pos[1]]),
                                       bg="orange", fg="white", font=("Arial", 24, "bold"), width=4, height=2)
            animation_label.place(x=start_x, y=start_y)

            dx = (end_x - start_x) / self.animation_steps  # Horizontal step distance
            dy = (end_y - start_y) / self.animation_steps  # Vertical step distance

            # Move the label step by step
            for step in range(self.animation_steps):
                self.master.after(step * self.animation_delay,
                                  lambda x=start_x + step * dx, y=start_y + step * dy:
                                  animation_label.place(x=x, y=y))

            # Destroy the label after the animation completes
            self.master.after(self.animation_steps * self.animation_delay, animation_label.destroy)
        except Exception as e:
            print(f"Error during merge animation: {e}")

    def move_left(self, event=None):
        """Handles the left arrow key event and updates the GUI after the move."""
        try:
            if self.game_logic.move_left():  # Move tiles left
                self.update_grid()  # Update the grid GUI
                if self.game_logic.check_game_over():  # Check if the game is over
                    self.show_game_over()  # Show the game over screen if necessary
        except Exception as e:
            print(f"Error processing left move: {e}")

    def move_right(self, event=None):
        """Handles the right arrow key event and updates the GUI after the move."""
        try:
            if self.game_logic.move_right():  # Move tiles right
                self.update_grid()  # Update the grid GUI
                if self.game_logic.check_game_over():  # Check if the game is over
                    self.show_game_over()  # Show the game over screen if necessary
        except Exception as e:
            print(f"Error processing right move: {e}")

    def move_up(self, event=None):
        """Handles the up arrow key event and updates the GUI after the move."""
        try:
            if self.game_logic.move_up():  # Move tiles up
                self.update_grid()  # Update the grid GUI
                if self.game_logic.check_game_over():  # Check if the game is over
                    self.show_game_over()  # Show the game over screen if necessary
        except Exception as e:
            print(f"Error processing up move: {e}")

    def move_down(self, event=None):
        """Handles the down arrow key event and updates the GUI after the move."""
        try:
            if self.game_logic.move_down():  # Move tiles down
                self.update_grid()  # Update the grid GUI
                if self.game_logic.check_game_over():  # Check if the game is over
                    self.show_game_over()  # Show the game over screen if necessary
        except Exception as e:
            print(f"Error processing down move: {e}")

    def show_game_over(self):
        """Displays a 'Game Over' message and a restart button."""
        try:
            game_over_frame = tk.Frame(self.master, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="Game Over!", bg="red", fg="white",
                     font=("Arial", 24, "bold")).pack()
            tk.Button(game_over_frame, text="Restart", command=self.restart_game).pack()
        except Exception as e:
            print(f"Error displaying game over screen: {e}")

    def restart_game(self):
        """Resets the game to its initial state and updates the GUI."""
        try:
            self.game_logic.__init__()  # Re-initialize the game logic
            self.update_grid()  # Update the grid to reflect the new game state
        except Exception as e:
            print(f"Error restarting the game: {e}")


if __name__ == "__main__":
    try:
        # Initialize the game logic and the GUI
        root = tk.Tk()
        game_logic = Game2048Logic()
        game = Game2048GUI(root, game_logic)
        root.mainloop()
    except Exception as e:
        print(f"Error starting the game: {e}")

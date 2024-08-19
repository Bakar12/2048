import tkinter as tk
import random
import numpy as np


class Game2048Logic:
    def __init__(self, size=4):
        try:
            # Initialize the game board with the specified size (default 4x4)
            self.size = size
            self.board = np.zeros((self.size, self.size), dtype=int)
            # Add two initial tiles to start the game
            self.add_new_tile()
            self.add_new_tile()
        except Exception as e:
            print(f"Error initializing the game: {e}")

    def add_new_tile(self):
        """Adds a new tile (2 or 4) to a random empty cell on the board."""
        try:
            empty_cells = list(zip(*np.where(self.board == 0)))
            if empty_cells:
                i, j = random.choice(empty_cells)
                self.board[i][j] = 2 if random.random() < 0.9 else 4
        except Exception as e:
            print(f"Error adding a new tile: {e}")

    def compress(self):
        """Slides all non-zero tiles to the left, leaving zeros to the right."""
        try:
            moved = False
            new_board = np.zeros_like(self.board)
            for i in range(self.size):
                position = 0
                for j in range(self.size):
                    if self.board[i][j] != 0:
                        new_board[i][position] = self.board[i][j]
                        if position != j:
                            moved = True
                        position += 1
            self.board = new_board
            return moved
        except Exception as e:
            print(f"Error compressing the board: {e}")
            return False

    def merge(self):
        """Merges adjacent tiles of the same value and returns if any merge happened."""
        try:
            merged = False
            for i in range(self.size):
                for j in range(self.size - 1):
                    if self.board[i][j] == self.board[i][j + 1] and self.board[i][j] != 0:
                        self.board[i][j] *= 2
                        self.board[i][j + 1] = 0
                        merged = True
            return merged
        except Exception as e:
            print(f"Error merging the tiles: {e}")
            return False

    def reverse(self):
        """Reverses the order of tiles in each row (used for right moves)."""
        try:
            self.board = np.fliplr(self.board)
        except Exception as e:
            print(f"Error reversing the board: {e}")

    def transpose(self):
        """Transposes the board (used for up/down moves)."""
        try:
            self.board = self.board.T
        except Exception as e:
            print(f"Error transposing the board: {e}")

    def move_left(self):
        """Performs a left move, including compressing and merging."""
        try:
            moved = self.compress()
            merged = self.merge()
            if merged:
                self.compress()  # Slide again after merging
            if moved or merged:
                self.add_new_tile()
            return moved or merged
        except Exception as e:
            print(f"Error moving tiles left: {e}")
            return False

    def move_right(self):
        """Performs a right move by reversing, moving left, and reversing back."""
        try:
            self.reverse()
            moved_or_merged = self.move_left()
            self.reverse()
            return moved_or_merged
        except Exception as e:
            print(f"Error moving tiles right: {e}")
            return False

    def move_up(self):
        """Performs an upward move by transposing, moving left, and transposing back."""
        try:
            self.transpose()
            moved_or_merged = self.move_left()
            self.transpose()
            return moved_or_merged
        except Exception as e:
            print(f"Error moving tiles up: {e}")
            return False

    def move_down(self):
        """Performs a downward move by transposing, moving right, and transposing back."""
        try:
            self.transpose()
            moved_or_merged = self.move_right()
            self.transpose()
            return moved_or_merged
        except Exception as e:
            print(f"Error moving tiles down: {e}")
            return False

    def check_game_over(self):
        """Checks if the game is over by verifying available moves and merges."""
        try:
            if any(0 in row for row in self.board):
                return False
            for i in range(self.size):
                for j in range(self.size - 1):
                    if self.board[i][j] == self.board[i][j + 1] or self.board[j][i] == self.board[j + 1][i]:
                        return False
            return True
        except Exception as e:
            print(f"Error checking game over condition: {e}")
            return True


class Game2048GUI:
    def __init__(self, master, game_logic):
        try:
            # Initialize the main window and link it with the game logic
            self.master = master
            self.master.title("2048 Game")
            self.game_logic = game_logic

            # List to store the GUI elements for each cell
            self.grid_cells = []

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
                    # Create a frame for each cell
                    cell = tk.Frame(self.grid_frame, bg='azure4', width=100, height=100)
                    cell.grid(row=i, column=j, padx=5, pady=5)

                    # Create a label inside each frame to display the tile value
                    label = tk.Label(cell, text="", bg='azure4', justify=tk.CENTER, font=("Arial", 24, "bold"), width=4,
                                     height=2)
                    label.grid()
                    row.append(label)
                self.grid_cells.append(row)

            # Update the grid to reflect the initial board state
            self.update_grid()

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
                    if value == 0:
                        # Empty cell
                        self.grid_cells[i][j].configure(text="", bg='azure4')
                    else:
                        # Cell with a tile, update text and background color
                        self.grid_cells[i][j].configure(text=str(value), bg=self.get_tile_color(value))

            # Ensure the GUI is updated immediately
            self.master.update_idletasks()
        except Exception as e:
            print(f"Error updating the grid: {e}")

    @staticmethod
    def get_tile_color(value):
        """Returns the background color based on the tile's value."""
        try:
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
        except Exception as e:
            print(f"Error getting tile color: {e}")
            return "#3c3a32"

    def animate_merge(self, start_coords, end_coords, value):
        """
        Creates an animation by moving a temporary label from the start position
        to the end position over a specified number of steps.
        """
        try:
            start_i, start_j = start_coords
            end_i, end_j = end_coords

            # Calculate pixel position based on grid position
            start_x = start_j * 105 + 5
            start_y = start_i * 105 + 5
            end_x = end_j * 105 + 5
            end_y = end_i * 105 + 5

            # Create a label for the animation
            animation_label = tk.Label(self.grid_frame, text=str(value), bg=self.get_tile_color(value),
                                       font=("Arial", 24, "bold"), width=4, height=2)
            animation_label.place(x=start_x, y=start_y)

            # Calculate step size for animation
            dx = (end_x - start_x) / self.animation_steps
            dy = (end_y - start_y) / self.animation_steps

            # Move the label step by step
            for step in range(self.animation_steps):
                self.master.after(step * self.animation_delay,
                                  lambda x=start_x + step * dx, y=start_y + step * dy: animation_label.place(x=x, y=y))

            # Destroy the label after animation completes
            self.master.after(self.animation_steps * self.animation_delay, animation_label.destroy)
        except Exception as e:
            print(f"Error during merge animation: {e}")

    def move_left(self, event=None):
        """Handles the left arrow key event and updates the GUI after the move."""
        try:
            if self.game_logic.move_left():
                self.update_grid()
                if self.game_logic.check_game_over():
                    self.show_game_over()
        except Exception as e:
            print(f"Error processing left move: {e}")

    def move_right(self, event=None):
        """Handles the right arrow key event and updates the GUI after the move."""
        try:
            if self.game_logic.move_right():
                self.update_grid()
                if self.game_logic.check_game_over():
                    self.show_game_over()
        except Exception as e:
            print(f"Error processing right move: {e}")

    def move_up(self, event=None):
        """Handles the up arrow key event and updates the GUI after the move."""
        try:
            if self.game_logic.move_up():
                self.update_grid()
                if self.game_logic.check_game_over():
                    self.show_game_over()
        except Exception as e:
            print(f"Error processing up move: {e}")

    def move_down(self, event=None):
        """Handles the down arrow key event and updates the GUI after the move."""
        try:
            if self.game_logic.move_down():
                self.update_grid()
                if self.game_logic.check_game_over():
                    self.show_game_over()
        except Exception as e:
            print(f"Error processing down move: {e}")

    def show_game_over(self):
        """Displays a 'Game Over' message and a restart button."""
        try:
            game_over_frame = tk.Frame(self.master, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="Game Over!", bg="red", fg="white", font=("Arial", 24, "bold")).pack()
            tk.Button(game_over_frame, text="Restart", command=self.restart_game).pack()
        except Exception as e:
            print(f"Error displaying game over screen: {e}")

    def restart_game(self):
        """Resets the game to its initial state and updates the GUI."""
        try:
            self.game_logic.__init__()  # Re-initialize the game logic
            self.update_grid()
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

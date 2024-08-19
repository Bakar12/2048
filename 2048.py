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
            self.size = size
            self.board = np.zeros((self.size, self.size), dtype=int)
            self.add_new_tile()
            self.add_new_tile()
        except Exception as e:
            print(f"Error initializing the game: {e}")

    def add_new_tile(self):
        """Adds a new tile (either 2 or 4) to a random empty cell on the board."""
        try:
            empty_cells = list(zip(*np.where(self.board == 0)))
            if empty_cells:
                i, j = random.choice(empty_cells)
                self.board[i][j] = 2 if random.random() < 0.9 else 4
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
        """
        Performs a left move, including compressing and merging.
        Returns:
            bool: True if the board changed (tiles moved or merged), False otherwise.
        """
        try:
            moved = self.compress()
            merged = self.merge()
            if merged:
                self.compress()
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
            self.master.title("2048 Game")
            self.game_logic = game_logic

            self.grid_cells = []

            # Animation parameters
            self.animation_steps = 5  # Reduced number of steps for faster animation
            self.animation_delay = 10  # Reduced delay for smoother animation

            # Setting up the grid GUI
            self.grid_frame = tk.Frame(self.master, bg='azure3')
            self.grid_frame.grid(padx=10, pady=10)

            for i in range(self.game_logic.size):
                row = []
                for j in range(self.game_logic.size):
                    cell = tk.Frame(self.grid_frame, bg='azure4', width=100, height=100)
                    cell.grid(row=i, column=j, padx=5, pady=5)
                    label = tk.Label(cell, text="", bg='azure4', justify=tk.CENTER,
                                     font=("Arial", 24, "bold"), width=4, height=2)
                    label.grid()
                    row.append(label)
                self.grid_cells.append(row)

            self.update_grid()  # Update the grid to reflect the initial board state

            self.master.bind("<Up>", self.move_up)
            self.master.bind("<Down>", self.move_down)
            self.master.bind("<Left>", self.move_left)
            self.master.bind("<Right>", self.move_right)
        except Exception as e:
            print(f"Error initializing the GUI: {e}")

    def update_grid(self, changed_positions=None):
        """
        Updates the grid GUI based on the current state of the board.
        Args:
            changed_positions (list of tuples): Positions of the tiles that have changed. If None, updates all tiles.
        """
        try:
            if changed_positions is None:
                changed_positions = [(i, j) for i in range(self.game_logic.size) for j in range(self.game_logic.size)]

            for i, j in changed_positions:
                value = self.game_logic.board[i][j]
                if value == 0:
                    self.grid_cells[i][j].configure(text="", bg="azure4")
                else:
                    self.grid_cells[i][j].configure(text=str(value), bg="orange", fg="white")
        except Exception as e:
            print(f"Error updating the grid: {e}")

    def animate_merge(self, start_pos, end_pos):
        """Animates the merging of tiles by moving a label from the start to the end position."""
        try:
            start_x = start_pos[1] * 110
            start_y = start_pos[0] * 110
            end_x = end_pos[1] * 110
            end_y = end_pos[0] * 110

            animation_label = tk.Label(self.grid_frame, text=str(self.game_logic.board[end_pos[0]][end_pos[1]]),
                                       bg="orange", fg="white", font=("Arial", 24, "bold"), width=4, height=2)
            animation_label.place(x=start_x, y=start_y)

            dx = (end_x - start_x) / self.animation_steps
            dy = (end_y - start_y) / self.animation_steps

            for step in range(self.animation_steps):
                self.master.after(step * self.animation_delay,
                                  lambda x=start_x + step * dx, y=start_y + step * dy:
                                  animation_label.place(x=x, y=y))

            self.master.after(self.animation_steps * self.animation_delay, animation_label.destroy)
        except Exception as e:
            print(f"Error during merge animation: {e}")

    def move_left(self, event=None):
        """Handles the left arrow key event and updates the GUI after the move."""
        try:
            changed_positions = []
            original_board = self.game_logic.board.copy()
            if self.game_logic.move_left():
                # Determine changed positions
                for i in range(self.game_logic.size):
                    for j in range(self.game_logic.size):
                        if self.game_logic.board[i][j] != original_board[i][j]:
                            changed_positions.append((i, j))
                self.update_grid(changed_positions)
                if self.game_logic.check_game_over():
                    self.show_game_over()
        except Exception as e:
            print(f"Error processing left move: {e}")

    def move_right(self, event=None):
        """Handles the right arrow key event and updates the GUI after the move."""
        try:
            changed_positions = []
            original_board = self.game_logic.board.copy()
            if self.game_logic.move_right():
                for i in range(self.game_logic.size):
                    for j in range(self.game_logic.size):
                        if self.game_logic.board[i][j] != original_board[i][j]:
                            changed_positions.append((i, j))
                self.update_grid(changed_positions)
                if self.game_logic.check_game_over():
                    self.show_game_over()
        except Exception as e:
            print(f"Error processing right move: {e}")

    def move_up(self, event=None):
        """Handles the up arrow key event and updates the GUI after the move."""
        try:
            changed_positions = []
            original_board = self.game_logic.board.copy()
            if self.game_logic.move_up():
                for i in range(self.game_logic.size):
                    for j in range(self.game_logic.size):
                        if self.game_logic.board[i][j] != original_board[i][j]:
                            changed_positions.append((i, j))
                self.update_grid(changed_positions)
                if self.game_logic.check_game_over():
                    self.show_game_over()
        except Exception as e:
            print(f"Error processing up move: {e}")

    def move_down(self, event=None):
        """Handles the down arrow key event and updates the GUI after the move."""
        try:
            changed_positions = []
            original_board = self.game_logic.board.copy()
            if self.game_logic.move_down():
                for i in range(self.game_logic.size):
                    for j in range(self.game_logic.size):
                        if self.game_logic.board[i][j] != original_board[i][j]:
                            changed_positions.append((i, j))
                self.update_grid(changed_positions)
                if self.game_logic.check_game_over():
                    self.show_game_over()
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


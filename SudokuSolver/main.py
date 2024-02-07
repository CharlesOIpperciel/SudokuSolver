import tkinter as tk
from tkinter import messagebox


# Function to check if a Sudoku grid is valid
def is_valid_sudoku(grid):
    seen = set()
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                num = grid[i][j]
                # Check if the current number has already been seen in its row, column, or subgrid
                if (i, num) in seen or (num, j) in seen or (i // 3, j // 3, num) in seen:
                    return False
                seen.add((i, num))
                seen.add((num, j))
                seen.add((i // 3, j // 3, num))
    return True


# Function to check if a number is used in the subgrid
def used_in_subgrid(grid, start_row, start_col, num):
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return True
    return False


# Function to check if a number is used in a column
def used_in_col(grid, col, num):
    for i in range(9):
        if grid[i][col] == num:
            return True
    return False


# Function to check if a number is used in a row
def used_in_row(grid, row, num):
    return num in grid[row]


# Function to check if a move is valid
def is_valid_move(grid, row, col, num):
    return not used_in_row(grid, row, num) and \
        not used_in_col(grid, col, num) and \
        not used_in_subgrid(grid, row - row % 3, col - col % 3, num)


# Function to find an empty cell in the grid
def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None


# Class for the Sudoku Solver UI
class SudokuSolverUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")

        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack()

        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(self.grid_frame, width=2, font=('Arial', 16), justify='center', bg='white')
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry)
            self.cells.append(row)

        self.solve_button = tk.Button(self.master, text="Solve", command=self.solve)
        self.solve_button.pack(pady=5)

        self.clear_button = tk.Button(self.master, text="Clear", command=self.clear)
        self.clear_button.pack(pady=5)

    # Method to solve the Sudoku puzzle
    def solve(self):
        grid = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                value = self.cells[i][j].get()
                if value.isdigit():
                    grid[i][j] = int(value)
                else:
                    grid[i][j] = 0

        # Check if the initial Sudoku configuration is valid
        if not is_valid_sudoku(grid):
            messagebox.showinfo("Invalid Sudoku", "Sudoku is invalid")
            return

        # Attempt to solve the Sudoku puzzle
        if self.solve_sudoku(grid):
            for i in range(9):
                for j in range(9):
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(grid[i][j]))
        else:
            print("No solution exists")

    # Method to clear the Sudoku grid
    def clear(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)

    # Recursive method to solve the Sudoku puzzle
    def solve_sudoku(self, grid):
        empty_cell = find_empty_cell(grid)
        if not empty_cell:
            return True  # Puzzle solved successfully

        row, col = empty_cell

        # Try placing numbers from 1 to 9 in the empty cell
        for num in range(1, 10):
            if is_valid_move(grid, row, col, num):
                grid[row][col] = num

                # Recursively attempt to solve the puzzle
                if self.solve_sudoku(grid):
                    return True

                grid[row][col] = 0  # Undo the current cell if no solution found

        return False  # Backtrack if no valid number can be placed in the current cell


# Main function to initialize the application
def main():
    root = tk.Tk()
    app = SudokuSolverUI(root)
    root.mainloop()


# Entry point of the program
if __name__ == "__main__":
    main()

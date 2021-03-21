class SudokuSolver:
    def __init__(self, board: list) -> None:
        self.board = board
        self.board_length = 9
        self.board_width = 9
        self.sub_grid_length = 3
        self.sub_grid_width = 3

    def print_board(self) -> None:
        for row in range(self.board_length):
            if row % 3 == 0 and row !=0:
                print("- - - - - - - - - - - - ")
            
            for col in range(self.board_width):
                if col % 3 == 0 and col != 0:
                    print(" | ", end="")

                if col == self.board_width - 1:
                    print(self.board[row][col])
                else:
                    print(str(self.board[row][col]) + " ", end="")

    '''
    The next function will check where is the closest empty box
    and will return it's coordinates.
    '''
    def find_empty(self) -> list:
        coor: list = []
        for row in range(self.board_length):
            for col in range(self.board_width):
                if not self.board[row][col]:
                    coor.append(row)
                    coor.append(col)
                    return coor
        
        return [-1, -1]
    
    ''' 
    In this function first, we check each row by going through the 
    columns and see if we can actually place a number there.
    The "pos[1] != i" is to skip checking the box 
    we just inserted a number to.
    If we have two of the same numbers in the same row, that means
    the number can not be there, and we'll have to change it.

    Then we check each column by going through the rows, completely analog
    to what we did with in the beginning of the function.
    '''
    def number_valid_in_board(self, number_to_try: int, position: tuple) -> bool:
        row, col = position
        # Checking row
        for i in range(self.board_length):
            if self.board[row][i] == number_to_try and i != col:
                return False
        # Checking col
        for i in range(self.board_width):
            if self.board[i][col] == number_to_try and i != row:
                return False

        # Checking 3x3 subgrid
        first_element_in_row, first_element_in_col = row, col

        first_element_in_row = row - row % self.sub_grid_length
        first_element_in_col = col - col % self.sub_grid_width
        
        for i in range(first_element_in_row, first_element_in_row + 3):
            for j in range(first_element_in_col, first_element_in_col + 3):
                if self.board[i][j] == number_to_try:
                    return False

        return True

    ''' 
    The next function will combine all of the other functions
    in order to solve the Sudoku board.
    We will start with our base case.
    The only way to know if we completed the board successfully is
    to determine whether or not our board is full with numbers. 
    If it is, we made it and the function will return true, otherwise, we failed,
    and the function will return false.

    Now we try to put numbers in empty boxes by going through them.
    If we pick a valid number that doesn't have the same number in the same
    row/col/3x3 box we'll add it into the board.
    Then we will recursively try to finish the solution with the number we just added.
    It will keep going like that until we either find a solution or we looped through all the numbers
    and couldn't reach a full board.
    '''
    def solve(self) -> bool:
        find = self.find_empty()
        if find != [-1, -1]:
            row = find[0]
            col = find[1]
        else:
            return True

        for num in range(1, 10):
            if(self.number_valid_in_board(num, (row, col))):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        
        return False




# if __name__ == "__main__":
#     board = [
#         [7,8,0,4,0,0,1,2,0],
#         [6,0,0,0,7,5,0,0,9],
#         [0,0,0,6,0,1,0,7,8],
#         [0,0,7,0,4,0,2,6,0],
#         [0,0,1,0,5,0,9,3,0],
#         [9,0,4,0,6,0,0,0,5],
#         [0,7,0,3,0,0,0,1,2],
#         [1,2,0,0,0,7,4,0,0],
#         [0,4,9,2,0,6,0,0,7]]

#     board2 = [
#         [8,0,0,2,5,0,4,0,0],
#         [0,0,0,0,0,9,0,1,0],
#         [3,4,5,0,0,0,0,0,0],
#         [0,0,0,1,0,0,0,5,0],
#         [0,6,0,0,0,0,0,0,3],
#         [0,3,8,7,0,0,2,9,0],
#         [0,1,0,0,0,0,0,0,6],
#         [0,0,7,9,0,0,0,2,0],
#         [0,0,0,0,8,3,0,0,0]]

#     board3 = [
#         [3,0,6,5,0,8,4,0,0],
#         [5,2,0,0,0,0,0,0,0],
#         [0,8,7,0,0,0,0,3,1],
#         [0,0,3,0,1,0,0,8,0],
#         [9,0,0,8,6,3,0,0,5],
#         [0,5,0,0,9,0,6,0,0],
#         [1,3,0,0,0,0,2,5,0],
#         [0,0,0,0,0,0,0,7,4],
#         [0,0,5,2,0,6,3,0,0]]


#     # grid = SudokuSolver(board)
#     # SudokuSolver.print_board(grid)
#     # SudokuSolver.solve(grid)
#     # print("\n")
#     # SudokuSolver.print_board(grid)
















# from typing import List, Union
# import math

board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

# board2 = [
#     [8,0,0,2,5,0,4,0,0],
#     [0,0,0,0,0,9,0,1,0],
#     [3,4,5,0,0,0,0,0,0],
#     [0,0,0,1,0,0,0,5,0],
#     [0,6,0,0,0,0,0,0,3],
#     [0,3,8,7,0,0,2,9,0],
#     [0,1,0,0,0,0,0,0,6],
#     [0,0,7,9,0,0,0,2,0],
#     [0,0,0,0,8,3,0,0,0]
# ]

# board3 =[
#     [3,0,6,5,0,8,4,0,0],
#     [5,2,0,0,0,0,0,0,0],
#     [0,8,7,0,0,0,0,3,1],
#     [0,0,3,0,1,0,0,8,0],
#     [9,0,0,8,6,3,0,0,5],
#     [0,5,0,0,9,0,6,0,0],
#     [1,3,0,0,0,0,2,5,0],
#     [0,0,0,0,0,0,0,7,4],
#     [0,0,5,2,0,6,3,0,0]
#  ]


def print_board(board: list) -> None:
    for i in range(len(board)):
        if i % 3 == 0 and i !=0:
            print("- - - - - - - - - - - - ")
        
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")
                
# '''
# The next function will check where is the closest empty box
# and will return it's coordinates.
# '''
def find_empty(board: list) -> list:
    coor: list = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if not board[i][j]:
                # i = row, j = col
                coor.append(i)
                coor.append(j)
                return coor
    
    return [-1, -1]

# ''' 
# In this function first, we check each row by going through the 
# columns and see if we can actually place a number there.
# The "pos[1] != i" is to skip checking the box 
# we just inserted a number to.
#  If we have two of the same numbers in the same row, that means
# the number can not be there, and we'll have to change it.

# Then we check each column by going through the rows, completely analog
# to what we did with in the beginning of the function.
# '''
def number_valid_in_board(board: list, number_to_try: int, position: tuple) -> bool:
    row, col = position
    # Checking row
    for i in range(len(board)):
        if board[row][i] == number_to_try and i != col:
            return False
    # Checking col
    for i in range(len(board)):
        if board[i][col] == number_to_try and i != row:
            return False

    # Checking 3x3 subgrid
    first_element_in_row, first_element_in_col = row, col

    first_element_in_row = row - row % 3
    first_element_in_col = col - col % 3
        
    for i in range(first_element_in_row, first_element_in_row + 3):
        for j in range(first_element_in_col, first_element_in_col + 3):
            if board[i][j] == number_to_try:
                return False

    return True

# ''' 
# The next function will combine all of the other functions
# in order to solve the Sudoku board.
# We will start with our base case.
# The only way to know if we completed the board successfully is
# to determine whether or not our board is full with numbers. 
# If it is, we made it, otherwise, we failed.

# Now we try to put numbers in empty boxes by going through them.
# If we picked a valid number that doesn't have the same number in the same
# row/col/3x3 box we'll add it into the board.
# Then we will recursively try to finish the solution with the number we just added.
# It will keep going like that until we either find a solution or we looped through all the numbers
# and couldn't reach a full board.
# '''
def solve(board: list) -> bool:
    find = find_empty(board)
    if find != [-1, -1]:
        row = find[0]
        col = find[1]
    else:
        return True

    for num in range(1, 10):
        if(number_valid_in_board(board, num, (row, col))):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0
        
    return False



if __name__ == "__main__":
    print_board(board)
    solve(board)
    print("\n")
    print_board(board)
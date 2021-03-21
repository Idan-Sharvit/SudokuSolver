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
        for row in range(9):
            for col in range(9):
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
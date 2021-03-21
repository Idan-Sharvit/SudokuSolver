import pygame, sys
from Settings import *
from buttonClass import *
from Sudoku import *

class GUI:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = board
        self.selected = None
        self.mouse_position = None
        self.state = "playing"
        self.finished = False
        self.cell_changed = False
        self.playing_buttons = []
        self.locked_cells = []
        self.incorrect_cells = []
        self.font = pygame.font.SysFont(("arial"), CELL_SIZE//2)
        self.load()
    
    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()
        sys.exit()

    ##### PLAYING STATE FUNCTIONS #####

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # User clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouse_on_grid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.playing_buttons:
                        if button.highlighted:
                            button.click()
            # User inserts a number
            if event.type == pygame.KEYDOWN:
                if self.selected != None and self.selected not in self.locked_cells:
                    if event.unicode.isdigit():
                        # Cell is changed
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cell_changed = True

    def playing_update(self):
        self.mouse_position = pygame.mouse.get_pos()
        for button in self.playing_buttons:
            button.update(self.mouse_position)
        
        if self.cell_changed:
            self.incorrect_cells = []
            if self.all_cells_done():
                # Checks if board is correct
                self.check_all_cells()
                if not len(self.incorrect_cells):
                    self.finished = True
                    print("Congratulations")

    def playing_draw(self):
        self.window.fill(WHITE)
        for button in self.playing_buttons:
            button.draw(self.window)

        if self.selected:
            self.draw_selection(self.selected)

        self.shade_locked_cells(self.locked_cells)
        self.shade_incorrect_cells(self.incorrect_cells)

        self.draw_numbers(self.window)
        self.draw_grid(self.window)
        pygame.display.update()
        self.cell_changed = False

    ##### BOARD CHECKING FUNCTIONS #####
    
    def all_cells_done(self):
        for row in self.grid:
            for num in row:
                if num == 0:
                    return False
        return True

    def number_valid_in_board(self, number_to_try: int, position: tuple) -> bool:
        row, col = position
        # Checks row
        for i in range(9):
            if self.grid[row][i] == number_to_try and i != col:
                return False
        # Checks col
        for i in range(9):
            if self.grid[i][col] == number_to_try and i != row:
                return False

        # Checks 3x3 subgrid
        first_element_in_row, first_element_in_col = row, col

        first_element_in_row = row - row % 3
        first_element_in_col = col - col % 3
        
        for i in range(first_element_in_row, first_element_in_row + 3):
            for j in range(first_element_in_col, first_element_in_col + 3):
                if self.grid[i][j] == number_to_try:
                    return False

        return True

    def check_all_cells(self):
        self.check_rows()
        self.check_cols()
        self.check_sub_grid()

    def check_rows(self):
        for yidx, row in enumerate(self.grid):
            possibles = [1,2,3,4,5,6,7,8,9]
            for xidx in range(9):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                        self.incorrect_cells.append([xidx, yidx])
                    if [xidx, yidx] in self.locked_cells:
                        for k in range(9):
                            if self.grid[yidx][k] == self.grid[yidx][xidx] and [k, yidx] not in self.locked_cells:
                                self.incorrect_cells.append([k, yidx])

    def check_cols(self):
        for xidx in range(9):
            possibles = [1,2,3,4,5,6,7,8,9]
            for yidx, row in enumerate(self.grid):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                        self.incorrect_cells.append([xidx, yidx])
                    if [xidx, yidx] in self.locked_cells:
                        for k, row in enumerate(self.grid):
                            if self.grid[k][xidx] == self.grid[yidx][xidx] and [xidx, k] not in self.locked_cells:
                                self.incorrect_cells.append([xidx, k])

    def check_sub_grid(self):
        for x in range(3):
            for y in range(3):
                possibles = [1,2,3,4,5,6,7,8,9]
                for i in range(3):
                    for j in range(3):
                        xidx = x*3+i
                        yidx = y*3+j
                        if self.grid[yidx][xidx] in possibles:
                            possibles.remove(self.grid[yidx][xidx])
                        else:
                            if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                                self.incorrect_cells.append([xidx, yidx])
                            if [xidx, yidx] in self.locked_cells:
                                for k in range(3):
                                    xidx2 = x*3+k
                                    yidx2 = y*3+1
                                    if self.grid[yidx2][xidx2] == self.grid[yidx][xidx] and [xidx2, yidx] not in self.locked_cells:
                                        self.incorrect_cells.append*[xidx2, yidx2]

    ##### HELPER FUNCTIONS #####

    def draw_numbers(self, window):
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    position = [xidx*CELL_SIZE + X_GRID_POSITION, yidx*CELL_SIZE + Y_GRID_POSITION]
                    self.text_to_screen(window, str(num), position)
      
    def draw_selection(self, position):
        x = (position[0]*CELL_SIZE)+X_GRID_POSITION
        y = (position[1]*CELL_SIZE)+Y_GRID_POSITION
        rect_coor = (x, y, CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(self.window, LIGHTBLUE, rect_coor)
    
    def draw_grid(self, window):
        pygame.draw.rect(window, BLACK, (X_GRID_POSITION, Y_GRID_POSITION, WIDTH - PADDING, HEIGHT - PADDING), THICKNESS)
        for x in range(9):
            vertical_starting_point = (X_GRID_POSITION + x * CELL_SIZE, Y_GRID_POSITION)
            vertical_ending_point = (X_GRID_POSITION + (x*CELL_SIZE), GRID_HEIGHT)
            horizontal_starting_point = (X_GRID_POSITION, (x*CELL_SIZE) + Y_GRID_POSITION)
            horizontal_ending_point = (GRID_WIDTH, (x*CELL_SIZE) + Y_GRID_POSITION)
            bold_line_offset = 3 if x % 3 == 0 else 1

            pygame.draw.line(self.window, BLACK, vertical_starting_point, vertical_ending_point, bold_line_offset)
            pygame.draw.line(self.window, BLACK, horizontal_starting_point, horizontal_ending_point, bold_line_offset)

    def mouse_on_grid(self):
        for mouse_pos, grid_pos in zip(self.mouse_position, GRID_POSITION):
            if grid_pos >= mouse_pos or mouse_pos >= grid_pos + GRID_SIZE:
                return False

        cell_x = (self.mouse_position[0] - X_GRID_POSITION) // CELL_SIZE
        cell_y = (self.mouse_position[1] - Y_GRID_POSITION) // CELL_SIZE
        return (cell_x, cell_y)

    def load_buttons(self):
        check_button_position = (75, 40, WIDTH//7, 40)
        solve_button_position = (440, 40, WIDTH//7, 40)

        self.playing_buttons.append(Button(*check_button_position,
                                           function=self.check_all_cells,
                                           colour='blue', text="Check"))

        self.playing_buttons.append(Button(*solve_button_position,
                                           function=self.call_solver,
                                           colour='green', text="SOLVE!"))


    '''
    I used the "position" variable to center the numbers in the cells
    '''
    def text_to_screen(self, window, text, position):
        font = self.font.render(text, False, BLACK)
        font_width = font.get_width()
        font_height = font.get_height()
        position[0] += (CELL_SIZE - font_width) // 2
        position[1] += (CELL_SIZE - font_height) // 2
        window.blit(font, position)

    # Setting locked cells from original board
    def load(self):
        self.load_buttons()
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.locked_cells.append([xidx, yidx])

    def shade_locked_cells(self, locked):
        for cell in locked:
            pygame.draw.rect(self.window, LOCKEDCELLCOLOUR, (cell[0]*CELL_SIZE + X_GRID_POSITION, cell[1]*CELL_SIZE + Y_GRID_POSITION, CELL_SIZE, CELL_SIZE))

    def shade_incorrect_cells(self, incorrect):
        for cell in incorrect:
            pygame.draw.rect(self.window, INCORRECTCELLCOLOUR, (cell[0]*CELL_SIZE + X_GRID_POSITION, cell[1]*CELL_SIZE + Y_GRID_POSITION, CELL_SIZE, CELL_SIZE))

    def call_solver(self):
        solver = SudokuSolver(self.grid)
        return solver.solve()
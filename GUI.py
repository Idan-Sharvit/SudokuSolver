import pygame, sys
from Settings import *
from buttonClass import *

class GUI:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = board
        print(self.grid)
        self.selected = None
        self.mouse_position = None
        self.state = "playing"
        self.finished = False
        self.cell_changed = False
        self.playing_buttons = []
        self.locked_cells = []
        self.incorrect_cells = []
        self.font = pygame.font.SysFont(("arial"), cell_size//2)
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
                    if self.is_int(event.unicode):
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
                if len(self.incorrect_cells) == 0:
                    self.finished = True
                    print("Congratulations")

    def playing_draw(self):
        self.window.fill(WHITE)
        for button in self.playing_buttons:
            button.draw(self.window)

        if self.selected:
            self.draw_selection(self.window, self.selected)

        self.shade_locked_cells(self.window, self.locked_cells)
        self.shade_incorrect_cells(self.window, self.incorrect_cells)

        self.draw_numbers(self.window)
        self.drawGrid(self.window)
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
        # Checking row
        for i in range(9):
            if self.grid[row][i] == number_to_try and i != col:
                return False
        # Checking col
        for i in range(9):
            if self.grid[i][col] == number_to_try and i != row:
                return False

        # Checking 3x3 subgrid
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
                possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
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
                    position = [xidx*cell_size + grid_position[0], yidx*cell_size + grid_position[1]]
                    self.text_to_screen(window, str(num), position, BLACK)
      
    def draw_selection(self, window, position):
        pygame.draw.rect(window, LIGHTBLUE, ((position[0]*cell_size)+grid_position[0], (position[1]*cell_size)+grid_position[1], cell_size, cell_size))
    
    def drawGrid(self, window):
        x_pos_grid, y_pos_grid = grid_position
        pygame.draw.rect(window, BLACK, (x_pos_grid, y_pos_grid, WIDTH - 150, HEIGHT - 150), 2)
        for x in range(9):
            pygame.draw.line(self.window, BLACK, (x_pos_grid + (x*cell_size), y_pos_grid), (x_pos_grid + (x*cell_size), y_pos_grid + 450), 3 if x % 3 == 0 else 1)
            pygame.draw.line(self.window, BLACK, (x_pos_grid, (x*cell_size) + y_pos_grid), (x_pos_grid + 450, (x*cell_size) + y_pos_grid), 3 if x % 3 == 0 else 1)

    def mouse_on_grid(self):
        if self.mouse_position[0] < grid_position[0] or self.mouse_position[1] < grid_position[1]:
            return False
        
        if self.mouse_position[0] > grid_position[0] + grid_size or self.mouse_position[1] > grid_position[1] + grid_size:
            return False

        return ((self.mouse_position[0] - grid_position[0])//cell_size, (self.mouse_position[1] - grid_position[1])//cell_size)

    def load_buttons(self):
        self.playing_buttons.append(Button(75, 40, WIDTH//7, 40,
                                           function = self.check_all_cells,
                                           colour = (27, 142, 207), text = "Check"))

        self.playing_buttons.append(Button(440, 40, WIDTH//7, 40,
                                           function = self.solve,
                                           colour = (3, 162, 2), text = "SOLVE!"))

    def text_to_screen(self, window, text, position, colour):
        font = self.font.render(text, False, BLACK)
        font_width = font.get_width()
        font_height = font.get_height()
        position[0] += (cell_size - font_width) // 2
        position[1] += (cell_size - font_height) // 2
        window.blit(font, position)

    # Setting locked cells from original board
    def load(self):
        self.load_buttons()
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.locked_cells.append([xidx, yidx])

    def shade_locked_cells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, LOCKEDCELLCOLOUR, (cell[0]*cell_size + grid_position[0], cell[1]*cell_size + grid_position[1], cell_size, cell_size))

    def shade_incorrect_cells(self, window, incorrect):
        for cell in incorrect:
            pygame.draw.rect(window, INCORRECTCELLCOLOUR, (cell[0]*cell_size + grid_position[0], cell[1]*cell_size + grid_position[1], cell_size, cell_size))

    def is_int(self, string):
        try:
            int(string)
            return True
        except:
            return False

    def find_empty(self):
        coor = []
        for row in range(9):
            for col in range(9):
                if not self.grid[row][col]:
                    coor.append(row)
                    coor.append(col)
                    return coor
        
        return [-1, -1]

    def solve(self):
        find = self.find_empty()
        if find != [-1, -1]:
            row = find[0]
            col = find[1]
        else:
            return True

        for num in range(1, 10):
            if(self.number_valid_in_board(num, (row, col))):
                self.grid[row][col] = num
                if self.solve():
                    return True
                self.grid[row][col] = 0
        
        return False
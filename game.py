import tkinter
from tkinter import Frame, Label, Radiobutton, Entry, Button, DISABLED, NORMAL, END, Canvas

TIC_TAC_TOE = "Tic Tac Toe"
BG_COLOR = "light blue"
BG_COLOR2 = "dark blue"
HEADER_FONT_TYPE = "Verdana"
FONT_COLOR = "white"
HEADER_FONT_SIZE = 30
WINDOW_SIZE = "700x500"
PLAYERX = 'X'
PLAYERO = 'O'
CELL_PADDING = 20
XCOLOR = 'blue'
OCOLOR = 'red'
LINE_COLOR = '#D4FF00'
BOARD_COLOR = 'black'
LINE_WIDTH = 3
SHAPE_WIDTH = 7
GAME_IN_PROGRESS = 'game in progress'
GAME_OVER = 'Wins'
GAME_CLOSE = 'Game Close'
GAME_TIED = 'Draw'
GAME_FONTS = 'Helvetica 50 bold'
GAME_FONTS_2 = 'Helvetica 30 bold'
INVALID_NAME = "type your name in here"

class UI:
    def __init__(self):
        '''Main Window'''
        self.game_state = GAME_IN_PROGRESS
        self.main_win = tkinter.Tk()
        self.main_win.title(TIC_TAC_TOE)
        self.main_win.config(bg = BG_COLOR)
        self.settings_frame = Frame(self.main_win, bg = BG_COLOR)
        self.settings_frame.pack()
        self.main_win.geometry(WINDOW_SIZE)
        blank = Label(self.settings_frame, bg = BG_COLOR)
        blank.pack()
        header = Label(self.settings_frame, text = TIC_TAC_TOE, font = (HEADER_FONT_TYPE, HEADER_FONT_SIZE , "bold", "italic"), bg = BG_COLOR)
        header.pack()
        self.num_of_player = tkinter.IntVar()
        single_player = Radiobutton(self.settings_frame, text = "Single Player", variable = self.num_of_player, value = 1, bg = BG_COLOR, command = self.player_1_settings)
        single_player.pack()
        multi_player = Radiobutton(self.settings_frame, text = "Multi Player", variable = self.num_of_player, value = 2, bg = BG_COLOR, command = self.player_2_settings)
        multi_player.pack()
        single_player.select()
        player_1_name = Label(self.settings_frame, text = "Player 1 Name:", bg = BG_COLOR)
        player_1_name.pack()
        self.player_1_textfield = Entry(self.settings_frame, bg = BG_COLOR2, fg = FONT_COLOR)
        self.player_1_textfield.pack()
        player_2_name = Label(self.settings_frame, text = "Player 2 Name:", bg = BG_COLOR)
        player_2_name.pack()
        self.player_2_textfield = Entry(self.settings_frame, bg = BG_COLOR2, fg = FONT_COLOR)
        self.player_2_textfield.pack()
        blank2 = Label(self.settings_frame, bg = BG_COLOR)
        blank2.pack()
        start_button = Button(self.settings_frame, text = "Start", bg = BG_COLOR2, fg = FONT_COLOR, command = self.start_game)
        start_button.pack()
        self.player_1_settings()
        self.game_frame = Frame(self.main_win, bg = BG_COLOR)
        self.canvas = Canvas(self.game_frame, width = 700, height = 500, bg = BG_COLOR)
        self.canvas.bind('<Button-1>',self.on_press)
        self.canvas.pack()

        self.current_player_index = 0
        
        self.main_win.mainloop()
        
    def on_press(self, event):
        if self.game_state == GAME_IN_PROGRESS and isinstance(self.current_player[self.current_player_index], Human):
            for k in range(9):
                if self.board.cells[k].topleft.x < event.x and event.x < self.board.cells[k].bottomright.x and self.board.cells[k].topleft.y < event.y and event.y < self.board.cells[k].bottomright.y and self.board.cells[k].shape == None:
                    self.board.cells[k].shape = self.current_player[self.current_player_index].shape
                    self.current_player_index = (self.current_player_index + 1)%2
                    self.display_player()
            self.draw_board()
            self.check_win()
        if self.game_state == GAME_IN_PROGRESS and isinstance(self.current_player[self.current_player_index], CPU):
            self.current_player[self.current_player_index].move(self.board, self.current_player[(self.current_player_index + 1)%2].shape)
            self.current_player_index = (self.current_player_index + 1)%2
            self.display_player()
            self.draw_board()
            self.check_win()
        if self.game_state == GAME_OVER:
            self.game_over()
        if self.check_draw() == True:
            self.game_tied()

    def display_player(self):
        if self.current_player_index == 0:
            player1_color = "blue"
            player2_color = "black"
        else:
            player1_color = "black"
            player2_color = "red"
        self.canvas.create_text(105, 130, text = self.player_1_textfield.get(), fill = player1_color, font = GAME_FONTS_2)
        self.canvas.create_text(595, 370, text = self.player_2_textfield.get(), fill = player2_color, font = GAME_FONTS_2)
    
    def game_over(self):
        if self.current_player_index == 1:
            name = self.player_1_textfield.get()
        else:
            name = self.player_2_textfield.get()
        self.canvas.create_text(350, 250, text = name + " " + GAME_OVER, fill = BOARD_COLOR, font = GAME_FONTS)
        self.game_state = GAME_CLOSE
        
    def game_tied(self):
        self.canvas.create_text(350, 250, text = GAME_TIED, fill = BOARD_COLOR, font = GAME_FONTS)
        self.game_state = GAME_CLOSE
        
    def check_win(self):
        for l in range(3):
            if self.board.cells[l * 3].shape !=None and self.board.cells[l * 3].shape == self.board.cells[l * 3 + 1].shape and self.board.cells[l * 3 + 1].shape == self.board.cells[l * 3 + 2].shape:
                self.canvas.create_line(self.board.cells[l * 3].topleft.x, (self.board.cells[l * 3].topleft.y + self.board.cells[l * 3].bottomright.y) / 2, self.board.cells[l * 3 + 2].bottomright.x, (self.board.cells[l * 3 + 2].topleft.y + self.board.cells[l * 3 + 2].bottomright.y) / 2, width = LINE_WIDTH, fill = LINE_COLOR)
                self.game_state = GAME_OVER
            if self.board.cells[l].shape !=None and self.board.cells[l].shape == self.board.cells[l + 3].shape and self.board.cells[l + 3].shape == self.board.cells[l + 6].shape:
                self.canvas.create_line((self.board.cells[l].topleft.x + self.board.cells[l].bottomright.x) / 2, self.board.cells[l].topleft.y, (self.board.cells[l + 6].topleft.x + self.board.cells[l + 6].bottomright.x) / 2, self.board.cells[l + 6].bottomright.y, width = LINE_WIDTH, fill = LINE_COLOR)   
                self.game_state = GAME_OVER
        if self.board.cells[0].shape !=None and self.board.cells[0].shape == self.board.cells[4].shape and self.board.cells[4].shape == self.board.cells[8].shape:
            self.canvas.create_line(self.board.cells[0].topleft.x, self.board.cells[0].topleft.y, self.board.cells[8].bottomright.x, self.board.cells[8].bottomright.y, width = LINE_WIDTH, fill = LINE_COLOR)
            self.game_state = GAME_OVER
        if self.board.cells[2].shape !=None and self.board.cells[2].shape == self.board.cells[4].shape and self.board.cells[4].shape == self.board.cells[6].shape:
            self.canvas.create_line(self.board.cells[2].bottomright.x, self.board.cells[2].topleft.y, self.board.cells[6].topleft.x, self.board.cells[6].bottomright.y, width = LINE_WIDTH, fill = LINE_COLOR)
            self.game_state = GAME_OVER
        
        
    def check_draw(self):
        for k in range(9):
            if self.board.cells[k].shape == None:
                return False
        return True
        
            
    def player_1_settings(self):
        self.player_2_textfield.delete(0, END)
        self.player_2_textfield.insert(0, "CPU")
        self.player_2_textfield.config(state = DISABLED, fg = "black")
        
    def player_2_settings(self):
        self.player_2_textfield.config(state = NORMAL, fg = "white")
        self.player_2_textfield.delete(0, END)
        
    def start_game(self):
        skip = False
        if self.player_1_textfield.get() == "" or self.player_1_textfield.get() == INVALID_NAME:
            self.player_1_textfield.delete(0, END)
            self.player_1_textfield.insert(0, INVALID_NAME)
            skip = True
        if self.player_2_textfield.get() == "" or self.player_2_textfield.get() == INVALID_NAME:
            self.player_2_textfield.delete(0, END)
            self.player_2_textfield.insert(0, INVALID_NAME)
            skip = True
        if skip == True:
            return
        self.settings_frame.forget()
        self.game_frame.pack()
        if self.num_of_player.get() == 1:
            self.current_player = (Human(PLAYERX), CPU(PLAYERO))
        else:
            self.current_player = (Human(PLAYERX), Human(PLAYERO))
        self.board = Board()
        self.draw_board()
        self.display_player()
        
    def draw_board(self):
        self.canvas.create_line(self.board.cells[1].topleft.x, self.board.cells[1].topleft.y, self.board.cells[6].bottomright.x, self.board.cells[6].bottomright.y, fill = BOARD_COLOR, width = LINE_WIDTH)
        self.canvas.create_line(self.board.cells[2].topleft.x, self.board.cells[2].topleft.y, self.board.cells[7].bottomright.x, self.board.cells[7].bottomright.y, fill = BOARD_COLOR, width = LINE_WIDTH)
        self.canvas.create_line(self.board.cells[3].topleft.x, self.board.cells[3].topleft.y, self.board.cells[2].bottomright.x, self.board.cells[2].bottomright.y, fill = BOARD_COLOR, width = LINE_WIDTH)
        self.canvas.create_line(self.board.cells[6].topleft.x, self.board.cells[6].topleft.y, self.board.cells[5].bottomright.x, self.board.cells[5].bottomright.y, fill = BOARD_COLOR, width = LINE_WIDTH)
        for cell in self.board.cells:
            if cell.shape == PLAYERX:
                self.canvas.create_line(cell.topleft.x + CELL_PADDING, cell.topleft.y + CELL_PADDING, cell.bottomright.x - CELL_PADDING, cell.bottomright.y - CELL_PADDING, width = SHAPE_WIDTH, fill = XCOLOR)
                self.canvas.create_line(cell.bottomright.x - CELL_PADDING, cell.topleft.y + CELL_PADDING, cell.topleft.x + CELL_PADDING, cell.bottomright.y - CELL_PADDING, width = SHAPE_WIDTH, fill = XCOLOR)
            if cell.shape == PLAYERO:
                self.canvas.create_oval(cell.topleft.x + CELL_PADDING, cell.topleft.y + CELL_PADDING, cell.bottomright.x - CELL_PADDING, cell.bottomright.y - CELL_PADDING, width = SHAPE_WIDTH, outline = OCOLOR)
        
CELL_LENGTH = 100
X_START = 200
Y_START = 100
class Board:
    def __init__(self):
        self.cells = []
        for i in range(3):
            for j in range(3):
                topleft = Point(j * CELL_LENGTH + X_START, (i + 1) * Y_START)
                bottomright = Point((j + 1) * CELL_LENGTH + X_START , (i + 1) * Y_START + CELL_LENGTH)
                cell = Cell(topleft, bottomright)
                self.cells.append(cell)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Cell:
    def __init__(self, topleft, bottomright):
        self.topleft = topleft
        self.bottomright = bottomright
        self.shape = None
        
class Player:
    def __init__(self, shape):
        self.shape = shape
        
        
class CPU(Player):
    def __init__(self, shape):
        Player.__init__(self, shape)
        
    def move(self, board, opponent_shape):
        value = self.almost_win(board, opponent_shape)
        if value != -1:
            board.cells[value].shape = self.shape
            return        
        value = self.almost_win(board, self.shape)
        if value != -1:
            board.cells[value].shape = self.shape
            return
        if board.cells[4].shape == None:
            board.cells[4].shape = self.shape
        elif (board.cells[0].shape == PLAYERX and board.cells[8].shape == PLAYERX) or (board.cells[2].shape == PLAYERX and board.cells[6].shape == PLAYERX):
            if board.cells[1].shape == None:
                board.cells[1].shape = PLAYERO
            elif board.cells[3].shape == None:
                board.cells[3].shape = PLAYERO
            elif board.cells[5].shape == None:
                board.cells[5].shape = PLAYERO
            elif board.cells[7].shape == None:
                board.cells[7].shape = PLAYERO
        else:
            if board.cells[0].shape == None:
                board.cells[0].shape = self.shape
            elif board.cells[2].shape == None:
                board.cells[2].shape = self.shape
            elif board.cells[6].shape == None:
                board.cells[6].shape = self.shape
            elif board.cells[8].shape == None:
                board.cells[8].shape = self.shape
            else:
                for i in range(9):
                    if board.cells[i].shape == None:
                        board.cells[i].shape = self.shape
                        break
                        
    def almost_win(self, board, shape):
        for l in range(3):
            if board.cells[l * 3].shape !=None and board.cells[l * 3].shape !=shape and board.cells[l * 3].shape == board.cells[l * 3 + 1].shape and board.cells[l * 3 + 2].shape==None:
                return l * 3 + 2
            if board.cells[l * 3 + 1].shape !=None and board.cells[l * 3 + 1].shape !=shape and board.cells[l * 3 + 1].shape == board.cells[l * 3 + 2].shape and board.cells[l * 3].shape==None:
                return l * 3
            if board.cells[l * 3 + 2].shape !=None and board.cells[l * 3 + 2].shape !=shape and board.cells[l * 3].shape == board.cells[l * 3 + 2].shape and board.cells[l * 3 + 1].shape==None:
                return l * 3 + 1
            if board.cells[l].shape !=None and board.cells[l].shape !=shape and board.cells[l].shape == board.cells[l + 3].shape and board.cells[l + 6].shape == None:
                return l + 6
            if board.cells[l + 3].shape !=None and board.cells[l + 3].shape !=shape and board.cells[l + 3].shape == board.cells[l + 6].shape and board.cells[l].shape == None:
                return l
            if board.cells[l].shape !=None and board.cells[l].shape !=shape and board.cells[l].shape == board.cells[l + 6].shape and board.cells[l + 3].shape == None:
                return l + 3
        if board.cells[0].shape !=None  and board.cells[0].shape !=shape and board.cells[0].shape == board.cells[4].shape and board.cells[8].shape == None:
            return 8
        if board.cells[2].shape !=None  and board.cells[2].shape !=shape and board.cells[2].shape == board.cells[4].shape and board.cells[6].shape == None:
            return 6
        if board.cells[4].shape !=None  and board.cells[4].shape !=shape and board.cells[4].shape == board.cells[8].shape and board.cells[0].shape == None:
            return 0
        if board.cells[4].shape !=None  and board.cells[4].shape !=shape and board.cells[4].shape == board.cells[6].shape and board.cells[2].shape == None:
            return 2
        if board.cells[0].shape !=None  and board.cells[0].shape !=shape and board.cells[0].shape == board.cells[8].shape and board.cells[4].shape == None:
            return 4
        if board.cells[2].shape !=None  and board.cells[2].shape !=shape and board.cells[2].shape == board.cells[6].shape and board.cells[4].shape == None:
            return 4
        return -1
            
            
class Human(Player):
    def __init__(self, shape):
        Player.__init__(self, shape)
import winsound
import tkinter
import board
from piece import *

WIDTH = 800
HEIGHT = 800

last_game = open("last_game.txt", "w")

root = tkinter.Tk()
c = tkinter.Canvas(width=WIDTH, height=HEIGHT, bg='white')
c.pack()

BOARD = board.Board(c)
BOARD.draw()

res = None # result of the game
turn = "white" # white or black

def try_promote(board):
    for i in range(8):
        if board[0][i] and board[0][i].type == "P" and board[0][i].color == "white" and not board[0][i].promoted:
            board[0][i].promote()
        if board[7][i] and board[7][i].type == "P" and board[7][i].color == "black" and not board[7][i].promoted:
            board[7][i].promote()

def check_draw(board):
    for i in range(8):
        for j in range(8):
            if board[i][j] and board[i][j].type in ["P", "N", "B", "R"]:
                return False
    return True

def check_win(board):
    white_king = False
    black_king = False
    for i in range(8):
        for j in range(8):
            if board[i][j] and board[i][j].type == "K":
                if board[i][j].color == "white":
                    white_king = True
                else:
                    black_king = True
                    
    if not white_king: return "black"
    if not black_king: return "white"
    else: return None

selected = None # i, j of selected piece
highlighted = [] # rectangle object

def deselect():
    global selected, highlighted
    
    selected = None
    for i in highlighted: c.delete(i)
    highlighted = []

def select(square):
    global selected, highlighted, turn, res
    if res: return # game is over
    
    if selected:
        i, j = selected
        
        # if is_my_turn and it is possible to reach square
        if BOARD.board[i][j].color == turn and square in BOARD.board[i][j].possible(BOARD.board): 
            mv = BOARD.move(selected, square, special = BOARD.board[i][j].type == "Q"); play_sound()
            
            res = f"{mv}"; res += ", " if turn == "white" else "\n"
            last_game.write(res)

            try_promote(BOARD.board)

            res = check_draw(BOARD.board) # check if game is draw after last move
            if res: c.create_text(WIDTH/2, HEIGHT/2, text="Draw!", font="Arial 50", fill="black")
            
            res = check_win(BOARD.board) # check if game is over after last move
            if res: c.create_text(WIDTH/2, HEIGHT/2, text=f"{res} wins!", font="Arial 50", fill="black")
        
            turn = "white" if turn == "black" else "black"
            
        # after move, or after some click, deselect
        deselect()
        
    else:
        i, j = square
        if BOARD.board[i][j] and BOARD.board[i][j].color == turn:
            selected = square
            
            highlighted.append( c.create_rectangle(
                square[1] * BOARD.tile_size, square[0] * BOARD.tile_size, 
                (square[1] + 1) * BOARD.tile_size, (square[0] + 1) * BOARD.tile_size, 
                outline="blue", width=5
            ) )
            
            for pos in BOARD.board[i][j].possible(BOARD.board):
                # create small dot on possible moves
                highlighted.append( c.create_oval(
                    pos[1] * BOARD.tile_size + BOARD.tile_size/2 - 5, pos[0] * BOARD.tile_size + BOARD.tile_size/2 - 5,
                    pos[1] * BOARD.tile_size + BOARD.tile_size/2 + 5, pos[0] * BOARD.tile_size + BOARD.tile_size/2 + 5,
                    fill="blue"
                ) )
    
def play_sound():
    winsound.PlaySound("img/chess_sfx.wav", winsound.SND_ASYNC)

root.bind("<Button-1>", lambda event: select(BOARD.get_square(event.y, event.x)))
root.bind("<Button-3>", lambda event: deselect()) # deselect on right click
# it was important to implement deselect(), as you can capture your own pieces by mistake

# from top left to bottom right, row by row.
# e.g. r = black rook, N = white knight, # = empty square
BOARD.set_board("rnbqkbnrpppppppp################################PPPPPPPPRNBQKBNR")
#BOARD.set_board("####k###########################################N###########K###") # king and knight endgame
c.mainloop()
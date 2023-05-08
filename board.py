from piece import *

class Board:
    def __init__(self, canvas):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.img_board = [[None for _ in range(8)] for _ in range(8)]
        
        self.canvas = canvas
        
        self.canvas.update()
        self.tile_size = self.canvas.winfo_width()/8
        
        self.offset = self.tile_size/5 # because the images are not exactly tileXtile
    
        
    def move(self, f, t, special = False):
        fi, fj = f
        ti, tj = t
        
        if special: # teleporting
            self.board[fi][fj], self.board[ti][tj] = self.board[ti][tj], self.board[fi][fj] # swapping the pieces
            self.board[ti][tj].i, self.board[ti][tj].j = ti, tj
            self.board[fi][fj].i, self.board[fi][fj].j = fi, fj
            
            self.img_board[fi][fj], self.img_board[ti][tj] = self.img_board[ti][tj], self.img_board[fi][fj] # swapping pictures
            self.canvas.moveto(self.img_board[ti][tj], tj * self.tile_size + self.offset, ti * self.tile_size)
            self.canvas.moveto(self.img_board[fi][fj], fj * self.tile_size + self.offset, fi * self.tile_size)
            
            
        if not special: # not teleporting
            self.board[ti][tj] = self.board[fi][fj] # moving the piece
            self.board[fi][fj] = None
            
            if self.img_board[ti][tj]: self.canvas.delete(self.img_board[ti][tj]) # first clear the tile
            self.img_board[ti][tj] = self.img_board[fi][fj]
            self.img_board[fi][fj] = None
            
            self.canvas.moveto(self.img_board[ti][tj], tj * self.tile_size + self.offset, ti * self.tile_size)
            self.board[ti][tj].i = ti
            self.board[ti][tj].j = tj
            
        return self.format_move(f, t)
            
    def format_move(self, f, t):
        return chr(f[1] + 97) + str(8 - f[0]) + ' ' + chr(t[1] + 97) + str(8 - t[0])
    
    def free(self, pos):
        i, j = pos
        return 0 <= i < 8 and 0 <= j < 8 and self.board[i][j] is None
        
    def draw(self):
        for i in range(8):
            for j in range(8):
                color = "#e8c597" if (i + j) % 2 == 0 else "#836354"

                self.canvas.create_rectangle(i * self.tile_size, j * self.tile_size, (i + 1) * self.tile_size, (j + 1) * self.tile_size, fill=color)
                
    def get_square(self, mouseY, mouseX):
        return int(mouseY//self.tile_size), int(mouseX//self.tile_size)
    
    def set_board(self, string):
        # string = "rnbqkbnrpppppppp################################PPPPPPPPRNBQKBNR"
        hashtable = {
            "r": Rook, "R": Rook,
            "n": Knight, "N": Knight,
            "b": Bishop, "B": Bishop,
            "q": Queen, "Q": Queen,
            "k": King, "K": King,
            "p": Pawn, "P": Pawn,
            "#": None
        }
        
        idx = 0
        
        for i in range(8):
            for j in range(8):
                if hashtable.get(string[idx]):
                    self.board[i][j] = hashtable[string[idx]]("white" if string[idx].isupper() else "black")
                    self.board[i][j].i = i
                    self.board[i][j].j = j
                    
                    self.img_board[i][j] = self.canvas.create_image(j * self.tile_size + self.offset, i * self.tile_size, image=self.board[i][j].img, anchor="nw")
                idx += 1
          
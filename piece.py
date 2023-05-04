import tkinter

class Piece:
    def __init__(self, type, color):
        self.type = type
        self.color = color
        
        self.i = None
        self.j = None
        
        self.img = None
        
    def possible(self, board):
        res = []
        for i in range(8):
            for j in range(8):
                res.append((i, j))
                
        return res
        
class Pawn(Piece):
    def __init__(self, color):
        super().__init__("P", color)
        
        self.img = tkinter.PhotoImage(file=f"img/{self.color}_pawn.png").zoom(3).subsample(4)
        
        self.promoted = False
        
    def possible(self, tmp_board):
        res = []
        if self.promoted:
            d = (-1, 0, 1)
        else:
            d = []
            if self.color == "white":
                d.append(-1)
            else:
                d.append(1)
        
        for di in d:
            for dj in (-1,0,1):
                if 0 <= self.i + di < 8 and 0 <= self.j + dj < 8: res.append((self.i + di, self.j + dj))
        
        return res
    
    def promote(self):
        self.promoted = True
        
        self.type = "P" # promoted pawn
        
class Knight(Piece):
    def __init__(self, color):
        super().__init__("N", color)
        
        self.img = tkinter.PhotoImage(file=f"img/{self.color}_knight.png").zoom(3).subsample(4)
        
    def possible(self, board):
        res = []
        
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            i = self.i + di
            j = self.j + dj
            
            if 0 <= i < 8 and 0 <= j < 8 and board[i][j] is None:
                for Di in (-1, 0, 1):
                    for Dj in (-1, 0, 1):
                        if 0 <= i + Di < 8 and 0 <= j + Dj < 8 and (Di, Dj) != (0, 0):
                            res.append((i + Di, j + Dj))
                            
        return res
        
class Bishop(Piece):
    def __init__(self, color):
        super().__init__("B", color)
        
        self.img = tkinter.PhotoImage(file=f"img/{self.color}_bishop.png").zoom(3).subsample(4)
        
    def possible(self, board):
        res = []
        
        for di in (-1, 1):
            for dj in (-1, 1):
                i = self.i + di
                j = self.j + dj
                
                while 0 <= i < 8 and 0 <= j < 8:
                    if board[i][j] is None: res.append((i, j))
                    else: 
                        res.append((i, j))
                        break
                    
                    i += di
                    j += dj
                    
        return res
        
class Rook(Piece):
    def __init__(self, color):
        super().__init__("R", color)
        
        self.img = tkinter.PhotoImage(file=f"img/{self.color}_rook.png").zoom(3).subsample(4)
        
    def possible(self, board):
        res = []
        
        for di in (-1, 1):
            i = self.i + di
            j = self.j
            
            while 0 <= i < 8:
                if board[i][j] is None: res.append((i, j))
                else: 
                    res.append((i, j))
                    break
                
                i += di
                
        for dj in (-1, 1):
            i = self.i
            j = self.j + dj
            
            while 0 <= j < 8:
                if board[i][j] is None: res.append((i, j))
                else: 
                    res.append((i, j))
                    break
                
                j += dj
                
        return res

class Queen(Piece):
    def __init__(self, color):
        super().__init__("Q", color)
        
        self.img = tkinter.PhotoImage(file=f"img/{self.color}_queen.png").zoom(3).subsample(4)
        
    def possible(self, board):
        res = []
        
        for i in range(8):
            for j in range(8):
                if board[i][j] and board[i][j].color == self.color and board[i][j].type not in "QK":
                    res.append((i, j))
        return res
        
class King(Piece):
    def __init__(self, color):
        super().__init__("K", color)
        
        self.img = tkinter.PhotoImage(file=f"img/{self.color}_king.png").zoom(3).subsample(4)
        
    def possible(self, board):
        res = []
        
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if 0 <= self.i + di < 8 and 0 <= self.j + dj < 8: res.append((self.i + di, self.j + dj))
                
        return res



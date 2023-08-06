#!python
''' queens8.py Places 8 queens on chessboard so that they are mutually
    unthreatening.  Allows user to place the 1st queen anywhere on the
    1st row; then the program places the rest of the queens by a
    recursive backtracking algorithm. Prints out all the moves,
    including the moves that may be "taken back" as well as the moves
    that "take back". The algorithm, due to Dijkstra and Wirth, is
    justly famous for its elegant method of keeping track of
    threatened squares.

    28-Jan-2022 2:47:48 pm added queens8all and selection diaglog
'''

# tkinter used to show boards.
import sys
import tkinter as tk
roots = list()

def Queens8 (all : bool, sym=False, equiv=0):
    global roots, AllBoards
    roots = list()
    out = not(all or sym or (equiv > 0))
    
    def Initialize ():
        # the following variables belong to the scope of Queens8 but
        # are initialized here. Often with an unused element index 0.
        # It is easier and more intuitive to waste an element than
        # to program around it.
        nonlocal Rows, Cols, UpDiagSafe, DownDiagSafe, RowSafe
        nonlocal Ctr, QueensPlaced
        Ctr = 0
        QueensPlaced = 0
        RowSafe = [False] + [True] * 8
        UpDiagSafe = [True] * 17          # R+C {1..16}
        DownDiagSafe = UpDiagSafe.copy()  # R-C {-7..7}
        Rows = [None] + [0] * 8
        Cols = Rows.copy()

    def PlaceQueenOn (r: int, c: int):
        # RowSafe, UpDiagSafe, DownDiagSafe are all True.
        # So, we place a queen here and make all the above False.
        nonlocal Rows, Cols, UpDiagSafe, DownDiagSafe, RowSafe
        nonlocal Ctr, QueensPlaced
        Ctr += 1
        if out:
            print(f'{Ctr:3}: Place Queen {c:1} on Row {r:1}')
        QueensPlaced += 1
        RowSafe[r]          = False
        UpDiagSafe[r + c]   = False
        DownDiagSafe[r - c] = False
        Rows[r] = c
        Cols[c] = r

    def TakeQueen (r, c):
        # Can't proceed so we take back a Queen and relocate it.
        nonlocal Rows, Cols, UpDiagSafe, DownDiagSafe, RowSafe
        nonlocal Ctr, QueensPlaced
        if out:
            print(f'{Ctr:3}: Take Queen {c:1} from row {r:1}')
        Ctr                += 1
        QueensPlaced       -= 1
        RowSafe[r]          = True
        UpDiagSafe[r + c]   = True
        DownDiagSafe[r - c] = True
        Rows[r]             = 0
        Cols[c]             = 0

    def PlaceRestOfQueens ():
        global AllBoards
        nonlocal Ctr, QueensPlaced, NumberSolutions

        c = QueensPlaced + 1

        if all:
            for r in range(1, 9):
                if RowSafe[r] and UpDiagSafe[r + c] and DownDiagSafe[r - c]:
                    PlaceQueenOn(r, c)
                    if QueensPlaced < 8:    # More to go. Call ourself to complete.
                        PlaceRestOfQueens()
                    if QueensPlaced == 8:   # Done! So return.
                        if Cols not in AllBoards:
                            for i in range(1, 9):
                                if out:
                                    print(Cols[i], end="")
                                    print()
                            LogAllSymmetries(Cols)
                            NumberSolutions += 1
                            if display_queens:
                                DoDisplayBoard(Cols)
                    TakeQueen(r, c)  # must backtrack
        else:
            for r in range(1, 9):
                if RowSafe[r] and UpDiagSafe[r + c] and DownDiagSafe[r - c]:
                    PlaceQueenOn(r, c)
                    if QueensPlaced < 8:    # More to go. Call ourself to complete.
                        PlaceRestOfQueens()
                    if QueensPlaced == 8:   # Done! So return.
                        return
                    TakeQueen(r, c)  # must backtrack
        return

    # Let these variables exist in the Queens8 scope. Any attempt to
    # reference  one while it still is None, will be futile.
    Rows         = None
    Cols         = None
    UpDiagSafe   = None
    DownDiagSafe = None
    RowSafe      = None
    QueensPlaced = None
    Ctr          = None
    NumberSolutions = 0
    if all:
        AllBoards = list()
        display_queens = input("Display Queens Y or N?").upper()[0] == 'Y'
        for first in range(1, 9):
            Initialize()
            PlaceQueenOn(first, 1)
            PlaceRestOfQueens()
            TakeQueen(first, 1)
        print('Number of Distinct Solutions = ', end='')
        print(f'{NumberSolutions} Total Solutions = {len(AllBoards)}')
        input("Enter to Proceed!")
        if display_queens:
            KillBoards()
    else:
        while True:
            Initialize()
            if equiv > 0:
                first=equiv
            else:
                print('On which row do you want the first Queen?')
                print('valid entries an in range 1..8')
                print('enter any other integer to halt.')
                while True:
                    first = input('?:')
                    if first.isnumeric():
                        first = int(first)
                        break
                    print("Not numeric. Try Again.")
            if first in range(1, 9):
                PlaceQueenOn(first, 1)
                PlaceRestOfQueens()
                if QueensPlaced == 8:
                    if sym:
                        DoColSym(Cols)
                    elif equiv > 0:
                        return Cols
                    else:
                        for i in range(1, 9):
                            print(Rows[i], end=' ')
                        print()
                        DoDisplayBoard(Cols)
                        input("Enter to Proceed")
                        KillBoards()
            else:
                return


# a global so the symmetry functions, especially Log1State has access
AllBoards = list()


def KillBoards ():
    global roots
    while len(roots) > 0:
        root = roots.pop()
        root.destroy()
        root.update()
        #del roots.pop(0)


BLACKQUEEN = '\u265b'
WHITEQUEEN = '\u2655'
WHITESPACE = '\u3000'   # This white space big as Queen. Ascii ' ' not so.


# Tkinter windows interface to display chess board
# Tkinter will be discussed in Volume 2
# until then this is Windows magic.
# each row it's own frame. Each column a label in all
# frames at the same index.
def DoDisplayBoard (cols):
    global roots
    root = tk.Tk()
    roots.append(root)
    root.title('Chess Board')
    ROW = [None] * 9
    Board = [ROW[:] for i in range(9)]
    del ROW
    F = [None] * 9
    F[8] = tk.Frame(root)
    F[8].pack()
    for i in range(7, 0, -1):
        F[i] = tk.Frame(root)
        F[i].pack(side='top')
    for i in range(1, 9):
        for j in range(1, 9):
            Board[i][j] = tk.Label(F[i], text=WHITESPACE,
                                   fg=['white', 'black'][(i + j) % 2],
                                   bg=['black', 'white'][(i + j) % 2],
                                   font=('Times', 24))
            Board[i][j].pack(side='left')

    for i in range(1, 9):
        Board[i][cols[i]].config(text=[BLACKQUEEN, WHITEQUEEN][(i+cols[i])%2]) # noqa
    root.update()

def DoColSym (cols):
    global AllBoards, roots
    AllBoards = list()
    Log1State(cols)
    index = 0
    while index < len(AllBoards):
        board = AllBoards[index]
        LogAllSymmetries(board)
        index += 1
    for board in AllBoards:
        DoDisplayBoard(board)
    input("Enter to Continue")
    KillBoards()


def Queens8All ():
    Queens8(True)


def Queens8Simple ():
    Queens8(False)


def RowCol (row : list) -> list:
    '''
    For a 8 Queens board representation there is a list 0 to 9 indexed by
    column (with index 0) not being used. In each list element is what row the
    Queen with that element is stored. For some opporations indexing by rows
    makes more sense. RowCol will take either representation and return the
    other.
    '''
    col = [None] * 9
    for i in range(1, 9):
        col[row[i]] = i
    return col


def Reflect_x (row : list) -> list:
    '''
    Take a board indexed by column and flip it around the x-axis. This axis is
    the line dividing row 4 from row 5. the new row being 9 - old row
    '''
    rx = [None] * 9
    for i in range(1, 9):
        rx[i] = 9 - row[i]
    return rx


def Reflect_y (row : list) -> list:
    '''
    Take a board indexed by column and flip it around the y-axis. This axis is
    between row 4 and 5. Also called the king column and the queen column.
    To do this we convert to row indexed representation and let Reflect_x do
    the work. Then convert the result back to column indexed.
    '''
    col = RowCol(row)
    col = Reflect_x(col)
    return RowCol(col)


def Rot90 (row : list) -> list:
    '''
    Rotate the board by 90 degrees counter clock wise.
    we make a row indexed representation of the Board where each column
    is 9 - the origonal row of the same number in the column with the
    same index. Then convert the row indexed representation into a
    column indexed representation.
    '''
    col = row[:]
    for i in range(1, 9):
        col[i] = 9 - col[i]
    return RowCol(col)


def RotDiagUp (row : list) -> list:
    '''
    Rotate the board along the up diagonal. This is Kings Rook 1 to Queens
    rook 8. Reflect on x-axis and rotate CCW 90 degrees.
    '''
    return Rot90(Reflect_x(row))


def RotDiagDn (row : list) -> list:
    '''
    Rotate the board along the down diagonal. Kings Rook 8 to Queens rook 1.
    Rotate CCW by 90 degrees, then reflect on the x-axis.
    '''
    return Reflect_x(Rot90(row))


def LogAllRotations (board : list):
    work = board[:]         # our work space is a copy of board
    work[0] = None          # make sure the in tests will really really work
    Log1State(work)        # add the base case
    work = Rot90(work)      # and all three 90 degree CCW rotations
    Log1State(work)
    work = Rot90(work)
    Log1State(work)
    work = Rot90(work)
    Log1State(work)


def Log1State (board : list):
    global AllBoards
    work = board[:]
    if work in AllBoards:
        return
    AllBoards.append(work)


def LogAllSymmetries (board : list):
    work = board[:]
    LogAllRotations(work)
    LogAllRotations(Reflect_x(work))
    LogAllRotations(Reflect_y(work))
    LogAllRotations(RotDiagUp(work))
    LogAllRotations(RotDiagDn(work))


def Queens8Sym ():
    Queens8(False, sym=True)


def SetOfBoards (board : list) -> set:
    global AllBoards
    AllBoards = list()
    AllBoards.append(board)
    LogAllSymmetries(board)
    aSetOfBoards = set()
    for brd in AllBoards:
        tup = tuple(brd[1:8])
        aSetOfBoards.add(tup)
    return aSetOfBoards


def print_answer (a : list):
    if a is None:
        return
    print("{", end="")
    l = len(a)
    for x in a:
        l -= 1
        print(x, end="")
        if l == 0:
            print("}")
        else:
            print(", ", end="")

        
def Queens8Equivalence ():
    BaseBoards = [None]
    for i in range(1, 9):
        BaseBoards.append(Queens8(False, equiv=i))
    Set = [None]
    for i in range(1, 9):
        Set.append(SetOfBoards(BaseBoards[i]))
    answers = [None, [1], [2], [3], [4], [5], [6], [7], [8]]
    for i in range(1,8):
        if answers[i] is None:
            continue
        for j in range((i+1),9):
            if Set[i].isdisjoint(Set[j]):
                continue
            answers[i].append(j)
            answers[j] = None
            Set[i].union(Set[j])
            Set[j] = set()
    for i in range(1, 9):
        print_answer(answers[i])
            

def NoEntry ():
    print("Not an Option, Try again")


selection = {'A' : (Queens8Simple,      "The orginal Dijkstra and Wirth solution to the 8 queens problem."),
             'B' : (Queens8All,         "Do all solutions with no symmetries"),
             'C' : (Queens8Sym,         "Like Queens8 only show the symmetries too"),
             'E' : (Queens8Equivalence, "Of the 8 returned by Queens8 as equivalence sets (no graphics)"),
             'Q' : (sys.exit,           "To Quit "),
             'X' : (sys.exit,           "Same as Q"),
            }
def Go ():
    while True:
        for k, i in selection.items():
            print(k, " :", i[1])
        reply = input("select:").upper()
        func = selection.get(reply, (NoEntry, ))[0]
        func()

                
if __name__ == "__main__":
    Go()


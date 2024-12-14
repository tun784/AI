import turtle
import random
import time
from tkinter import messagebox
global move_history

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def is_empty(board):
    return board == [[' ']*len(board)]*len(board)

def is_in(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board)

def is_win(board):
    
    black = score_of_col(board,'b')
    white = score_of_col(board,'w')
    
    sum_sumcol_values(black)
    sum_sumcol_values(white)
    
    if 5 in black and black[5] == 1:
        return 'Black won'
    elif 5 in white and white[5] == 1:
        return 'White won'
        
    if sum(black.values()) == black[-1] and sum(white.values()) == white[-1] or possible_moves(board)==[]:
        return 'Draw'
        
    return 'Continue playing'



def march(board,y,x,dy,dx,length):
    '''
    tìm vị trí xa nhất trong dy,dx trong khoảng length

    '''
    yf = y + length*dy 
    xf = x + length*dx
    # chừng nào yf,xf không có trong board
    while not is_in(board,yf,xf):
        yf -= dy
        xf -= dx
        
    return yf,xf
    
def score_ready(scorecol):
    '''
    Khởi tạo hệ thống điểm

    '''
    sumcol = {0: {},1: {},2: {},3: {},4: {},5: {},-1: {}}
    for key in scorecol:
        for score in scorecol[key]:
            if key in sumcol[score]:
                sumcol[score][key] += 1
            else:
                sumcol[score][key] = 1
            
    return sumcol
    
def sum_sumcol_values(sumcol):
    '''
    hợp nhất điểm của mỗi hướng
    '''
    
    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        else:
            sumcol[key] = sum(sumcol[key].values())
            
def score_of_list(lis,col):
    
    blank = lis.count(' ')
    filled = lis.count(col)
    
    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled

def row_to_list(board,y,x,dy,dx,yf,xf):
    '''
    trả về list của y,x từ yf,xf
    
    '''
    row = []
    while y != yf + dy or x !=xf + dx:
        row.append(board[y][x])
        y += dy
        x += dx
    return row
    
def score_of_row(board,cordi,dy,dx,cordf,col):
    '''
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối

    '''
    colscores = []
    y,x = cordi
    yf,xf = cordf
    row = row_to_list(board,y,x,dy,dx,yf,xf)
    for start in range(len(row)-4):
        score = score_of_list(row[start:start+5],col)
        colscores.append(score)
    
    return colscores

def score_of_col(board,col):
    '''
    tính toán điểm số mỗi hướng của column dùng cho is_win;
    '''

    f = len(board)
    #scores của 4 hướng đi
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
    for start in range(len(board)):
        scores[(0,1)].extend(score_of_row(board,(start, 0), 0, 1,(start,f-1), col))
        scores[(1,0)].extend(score_of_row(board,(0, start), 1, 0,(f-1,start), col))
        scores[(1,1)].extend(score_of_row(board,(start, 0), 1,1,(f-1,f-1-start), col))
        scores[(-1,1)].extend(score_of_row(board,(start,0), -1, 1,(0,start), col))
        
        if start + 1 < len(board):
            scores[(1,1)].extend(score_of_row(board,(0, start+1), 1, 1,(f-2-start,f-1), col)) 
            scores[(-1,1)].extend(score_of_row(board,(f -1 , start + 1), -1,1,(start+1,f-1), col))
            
    return score_ready(scores)
    
def score_of_col_one(board,col,y,x):
    '''
    trả lại điểm số của column trong y,x theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    '''
    
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
    
    scores[(0,1)].extend(score_of_row(board,march(board,y,x,0,-1,4), 0, 1,march(board,y,x,0,1,4), col))
    
    scores[(1,0)].extend(score_of_row(board,march(board,y,x,-1,0,4), 1, 0,march(board,y,x,1,0,4), col))
    
    scores[(1,1)].extend(score_of_row(board,march(board,y,x,-1,-1,4), 1, 1,march(board,y,x,1,1,4), col))

    scores[(-1,1)].extend(score_of_row(board,march(board,y,x,-1,1,4), 1,-1,march(board,y,x,1,-1,4), col))
    
    return score_ready(scores)
    
def possible_moves(board):  
    '''
    khởi tạo danh sách tọa độ có thể có tại danh giới các nơi đã đánh phạm vi 3 đơn vị
    '''
    
    taken = []
    
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]
    # cord: lưu các vị trí không đi 
    cord = {}
    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != ' ':
                taken.append((i,j))
    ''' duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với 
    nước đã có trên bàn cờ)
    '''
    for direction in directions:
        dy,dx = direction
        for coord in taken:
            y,x = coord
            for length in [1,2]:
                move = march(board,y,x,dy,dx,length)
                if move not in taken and move not in cord:
                    cord[move]=False
    return cord
    
def TF34score(score3,score4):
    '''
    trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp)
    '''
    for key4 in score4:
        if score4[key4] >=1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >=2:
                        return True
    return False
    
def stupid_score(board,col,anticol,y,x):
    '''
    cố gắng di chuyển y,x
    trả về điểm số tượng trưng lợi thế 
    '''
    
    global colors
    M = 1000
    res,adv, dis = 0, 0, 0
    
    
    board[y][x]=col

    sumcol = score_of_col_one(board,col,y,x)       
    a = winning_situation(sumcol)
    adv += a * M
    sum_sumcol_values(sumcol)
    
    adv +=  sumcol[-1] + sumcol[1] + 4*sumcol[2] + 8*sumcol[3] + 16*sumcol[4]
    
    #phòng thủ
    board[y][x]=anticol
    sumanticol = score_of_col_one(board,anticol,y,x)  
    d = winning_situation(sumanticol)
    dis += d * (M-100)
    sum_sumcol_values(sumanticol)
    dis += sumanticol[-1] + sumanticol[1] + 4*sumanticol[2] + 8*sumanticol[3] + 16*sumanticol[4]

    res = adv + dis
    
    board[y][x]=' '
    return res
    
def winning_situation(sumcol):
    '''
    trả lại tình huống chiến thắng dạng như:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
    -1 là rơi vào trạng thái tồi, cần phòng thủ
    '''
    
    if 1 in sumcol[5].values():
        return 5
    elif len(sumcol[4])>=2 or (len(sumcol[4])>=1 and max(sumcol[4].values())>=2):
        return 4
    elif TF34score(sumcol[3],sumcol[4]):
        return 4
    else:
        score3 = sorted(sumcol[3].values(),reverse = True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0
    

def evaluate_board(board, col, anticol):
    """
    Hàm đánh giá trạng thái của bàn cờ
    """
    score = 0
    
    # Điểm cho người chơi hiện tại
    player_score = score_of_col(board, col)
    sum_sumcol_values(player_score)
    score += 4 * player_score[3] + 8 * player_score[4] + 1000 * player_score[5]

    
    opponent_score = score_of_col(board, anticol)
    sum_sumcol_values(opponent_score)
    score -= 4 * opponent_score[3] + 8 * opponent_score[4] + 1000 * opponent_score[5]

    return score

def minimax(board, depth, maximizingPlayer, col, anticol, alpha, beta):
    """
    Thuật toán minimax kết hợp alpha-beta pruning.
    """
    if depth == 0 or is_win(board) != 'Continue playing':
        return evaluate_board(board, col, anticol), None

    moves = possible_moves(board)
    best_move = None

    if maximizingPlayer:  # Lượt của AI 
        max_eval = float('-inf')
        for move in moves:
            y, x = move
            board[y][x] = col  
            eval, _ = minimax(board, depth - 1, False, col, anticol, alpha, beta)
            board[y][x] = ' '  # Hoàn tác nước đi
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:  
        min_eval = float('inf')
        for move in moves:
            y, x = move
            board[y][x] = anticol  
            eval, _ = minimax(board, depth - 1, True, col, anticol, alpha, beta)
            board[y][x] = ' '  
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def best_move(board, col):
    """
    Trả lại nước đi tốt nhất sử dụng thuật toán minimax.
    """
    if col == 'w':
        anticol = 'b'
    else:
        anticol = 'w'

    if is_empty(board):  # Nếu bàn cờ rỗng, chọn nước đi ngẫu nhiên
        return (len(board) // 2, len(board) // 2)

    _, move = minimax(board, depth=2 if len(board) > 10 else 3, maximizingPlayer=True, col=col, anticol=anticol, alpha=float('-inf'), beta=float('inf'))
    return move



def click(x, y):
    global board, colors, win, move_history, mode, current_turn
    
    x, y = getindexposition(x, y)
    
    
    if x == -1 and y == -1 and len(move_history) != 0:
        x, y = move_history[-1]
        del (move_history[-1])
        board[y][x] = " "
        x, y = move_history[-1]
        del (move_history[-1])
        board[y][x] = " "
        return

    if not is_in(board, y, x):
        return

    if board[y][x] == ' ' and not win:
        if mode == 1:  # Người vs Người
            draw_stone(x, y, colors[current_turn])
            board[y][x] = current_turn
            move_history.append((x, y))
            
            game_res = is_win(board)
            if game_res in ["White won", "Black won", "Draw"]:
                print(game_res)
                messagebox.showinfo('',game_res)
                win = True
                return
            
        
            current_turn = 'w' if current_turn == 'b' else 'b'

        elif mode == 2:  # Người vs Máy
            # Lượt của người chơi (đen)
            draw_stone(x, y, colors['b'])
            board[y][x] = 'b'
            move_history.append((x, y))
            
            game_res = is_win(board)
            if game_res in ["White won", "Black won", "Draw"]:
                print(game_res)
                messagebox.showinfo('',game_res)
                win = True
                return

            # Lượt của máy (trắng)
            ay, ax = best_move(board, 'w')
            draw_stone(ax, ay, colors['w'])
            board[ay][ax] = 'w'
            move_history.append((ax, ay))
            
            game_res = is_win(board)
            if game_res in ["White won", "Black won", "Draw"]:
                print(game_res)
                messagebox.showinfo('',game_res)
                win = True
                return
       
    
def initialize():
    global win, board, screen, colors, move_history, mode, current_turn

    move_history = []
    win = False

    # Nhập kích thước bàn cờ
    size = None
    while not isinstance(size, int) or size < 5 or size > 25:  # Kích thước tối thiểu 5x5, tối đa 25x25
        try:
            size = int(turtle.textinput("Kích thước bàn cờ", "Nhập kích thước bàn cờ (5-25):"))
        except:
            continue

    board = make_empty_board(size)

    # Lựa chọn chế độ chơi
    mode = None
    while mode not in [1, 2]:
        try:
            mode = int(turtle.textinput("Chọn chế độ chơi", "1: Người vs Người\n2: Người vs Máy\nNhập lựa chọn:"))
        except:
            continue

    if mode == 1:
        current_turn = 'b'  # Lượt đầu tiên là đen
    elif mode == 2:
        current_turn = None  # Không cần trong chế độ người vs máy

    screen = turtle.Screen()
    screen.onclick(click)
    screen.setup(screen.screensize()[1] * 2, screen.screensize()[1] * 2)
    screen.setworldcoordinates(-1, size, size, -1)
    screen.bgcolor('orange')
    screen.tracer(500)

    colors = {'w': turtle.Turtle(), 'b': turtle.Turtle(), 'g': turtle.Turtle()}
    colors['w'].color('white')
    colors['b'].color('black')

    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(0)

    border = turtle.Turtle()
    border.speed(9)
    border.penup()

    side = (size - 1) / 2

    i = -1
    for start in range(size):
        border.goto(start, side + side * i)
        border.pendown()
        i *= -1
        border.goto(start, side + side * i)
        border.penup()

    i = 1
    for start in range(size):
        border.goto(side + side * i, start)
        border.pendown()
        i *= -1
        border.goto(side + side * i, start)
        border.penup()

    border.ht()

    screen.listen()
    screen.mainloop()
    
def getindexposition(x,y):
    '''
    lấy index
    '''
    intx,inty = int(x),int(y)
    dx,dy = x-intx,y-inty
    if dx > 0.5:
        x = intx +1
    elif dy<-0.5:
        y = inty -1
    else:
        x = intx
    if dy > 0.5:
        y = inty +1
    elif dx<-0.5:
        y = inty -1
    else:
        y = inty
    return x,y

def draw_stone(x,y,colturtle):
    colturtle.goto(x,y-0.3)
    colturtle.pendown()
    colturtle.begin_fill()
    colturtle.circle(0.3)
    colturtle.end_fill()
    colturtle.penup()
    
if __name__ == '__main__':
    initialize()

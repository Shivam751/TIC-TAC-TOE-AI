from math import inf
import random
from tkinter import *
from tkinter import messagebox

from torch import channel_shuffle

COLOR = {'O': 'deep sky blue', 'X': 'lawn green'}

def button(frame):
    return Button(frame, padx=1, bg="papaya whip", width=3, text="   ",
                    font=('arial',60,'bold'), relief='sunken', bd=10)

def change_mark():
    global a
    for mark in ['O','X']:
        if not(mark==a):
            a=mark
            break

def reset_game():
    global a
    for row in range(3):
        for col in range(3):
            board[row][col]['text'] = " "
            board[row][col]['state'] = NORMAL
    a = random.choice(['O', 'X'])
    current_player = "AI"
    scores[a] = 1
    change_mark()
    scores[a] = -1
    change_mark()
    board[1][1].config(text=a, state=DISABLED, disabledforeground=COLOR[a])
    change_mark()
    label.config(text = a + "'s Turn")

def check_for_tie():
    for i in range(3):
        for j in range(3):
            if board[i][j]['state'] != DISABLED:
                return False
    return True

def check_for_end():
    for i in range(3):
        if((board[i][0]['text'] == board[i][1]['text'] == board[i][2]['text']==a)
                                    or 
           (board[0][i]['text'] == board[1][i]['text'] == board[2][i]['text'] == a)):
            return a

    if((board[0][0]['text'] == board[1][1]['text'] == board[2][2]['text'] == a)
                                    or
        (board[0][2]['text'] == board[1][1]['text'] == board[2][0]['text'] == a)):
        return a
    
    elif(check_for_tie()):
        return "tie"

    return "NO_RES"

def click(row, col):
    board[row][col].config(text=a, state=DISABLED, disabledforeground=COLOR[a])
    res = check_for_end()
    if(res != "NO_RES"):
        if(res=="tie"):
            messagebox.showinfo("RESULT","The game has tied")
            reset_game()
        else:
            messagebox.showinfo("Congo!", a+" has won the game!")
            reset_game()
        return
    change_mark()
    label.config(text = a + "'s Turn")
    bestMove()

def minimax(obj):
    res = check_for_end()
    if res != "NO_RES":
        return scores[res]
    if(obj=='max'):
        best_score = -inf
        for i in range(3):
            for j in range(3):
                if (board[i][j]['state'] != DISABLED):
                    board[i][j].config(text=a, state=DISABLED, disabledforeground=COLOR[a])
                    change_mark()
                    score = minimax('min')
                    change_mark()
                    board[i][j].config(text=" ", state=NORMAL)
                    best_score = max((best_score, score))
        return best_score
    else:
        best_score = inf
        for i in range(3):
            for j in range(3):
                if (board[i][j]['state'] != DISABLED):
                    board[i][j].config(text=a, state=DISABLED, disabledforeground=COLOR[a])
                    change_mark()
                    score = minimax('max')
                    change_mark()
                    board[i][j].config(text=" ", state=NORMAL)
                    best_score = min((best_score, score))
        return best_score

def bestMove():
    bestScore = -inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if (board[i][j]['state'] != DISABLED):
                board[i][j].config(text=a, state=DISABLED, disabledforeground=COLOR[a])
                change_mark()
                score = minimax('min')
                change_mark()
                board[i][j].config(text=" ", state=NORMAL)
                if(score > bestScore):
                    bestScore = score
                    move = (i, j)
    
    board[move[0]][move[1]].config(text=a, state=DISABLED, disabledforeground=COLOR[a])
    
    res = check_for_end()
    if(res != "NO_RES"):
        if(res=="tie"):
            messagebox.showinfo("RESULT", "The game has tied")
            reset_game()
        else:
            messagebox.showinfo("Congo", a+" has won the game!")
            reset_game()
        return
    
    change_mark()
    label.config(text = a + "'s Turn")

root = Tk()
root.title("TIC-TAC-TOE")
a=random.choice(['O', 'X'])
global current_player
current_player = input("Start with: HUMAN OR AI: ")
scores={'tie':0}
if(current_player == "HUMAN"):
    scores[a] = -1
    if(a=='O'):
        scores['X'] = 1
    else:
        scores['O'] = 1
else:
    scores[a] = 1
    if(a=='O'):
        scores['X'] = -1
    else:
        scores['O'] = -1
board = [[], [], []]

for i in range(3):
    for j in range(3):
        board[i].append(button(root))
        board[i][j].config(command = lambda row=i,col=j:click(row,col))
        board[i][j].grid(row=i,column=j)

label=Label(text=a+"'s Turn",font=('arial',20,'bold'))
label.grid(row=3,column=0,columnspan=3)

if current_player == "AI":
    board[1][1].config(text=a, state=DISABLED, disabledforeground=COLOR[a])
    change_mark()
    label.config(text = a + "'s Turn")

root.mainloop()

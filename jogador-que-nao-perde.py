import tkinter as tk
from tkinter import messagebox

# Função que verifica se alguém ganhou
def check_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return [player, player, player] in win_conditions

# Função para determinar se há jogadas restantes
def is_moves_left(board):
    for row in board:
        if " " in row:
            return True
    return False

# Algoritmo que faz a máquina sempre vencer
def find_best_move(board):
    # Primeiro, verifica se a máquina pode ganhar
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                if check_winner(board, "O"):
                    return i, j
                board[i][j] = " "

    # Se não puder ganhar, bloqueia o jogador
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "X"
                if check_winner(board, "X"):
                    board[i][j] = "O"
                    return i, j
                board[i][j] = " "

    # Se não houver ameaças, preenche a primeira célula vazia
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return i, j

# Função que processa as jogadas
def button_click(row, col):
    if board[row][col] == " " and not game_over:
        board[row][col] = "X"
        buttons[row][col].config(text="X", state="disabled")

        if check_winner(board, "X"):
            end_game("Você ganhou!")
            return
        elif not is_moves_left(board):
            end_game("Empate!")
            return

        # Jogada da máquina
        row, col = find_best_move(board)
        board[row][col] = "O"
        buttons[row][col].config(text="O", state="disabled")

        if check_winner(board, "O"):
            end_game("A máquina venceu!")
        elif not is_moves_left(board):
            end_game("Empate!")

# Função para encerrar o jogo
def end_game(result):
    global game_over
    game_over = True
    messagebox.showinfo("Fim de jogo", result)
    root.quit()

# Função que faz a máquina jogar primeiro
def machine_first_move():
    row, col = find_best_move(board)
    board[row][col] = "O"
    buttons[row][col].config(text="O", state="disabled")

# Criação da janela principal
root = tk.Tk()
root.title("Jogo da Velha")

# Inicialização do tabuleiro e variáveis
board = [[" " for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
game_over = False

# Criação dos botões do tabuleiro
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text=" ", font=("Arial", 24), width=5, height=2,
                                  command=lambda row=i, col=j: button_click(row, col))
        buttons[i][j].grid(row=i, column=j)

# Máquina faz a primeira jogada
machine_first_move()

# Inicia o loop do tkinter
root.mainloop()

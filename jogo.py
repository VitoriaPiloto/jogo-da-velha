import random
import csv

def imprimir_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def verificar_vencedor(board, player):
    condicoes_vencer = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]]
    ]
    return [player, player, player] in condicoes_vencer

def verifica_se_esta_completo_board(board):
    return all(cell != " " for row in board for cell in row)

def jogada_campeao(board):
    # Tentar vencer na jogada atual
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "X"
                if verificar_vencedor(board, "X"):
                    return (i, j)
                board[i][j] = " "

    # Bloquear o jogador aleatório (O) se ele estiver prestes a vencer
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                if verificar_vencedor(board, "O"):
                    board[i][j] = "X"
                    return (i, j)
                board[i][j] = " "

    # Priorizar jogar no centro
    if board[1][1] == " ":
        return (1, 1)

    # Jogar em um dos cantos, se possível
    for i, j in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[i][j] == " ":
            return (i, j)

    # Jogar na primeira posição disponível
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return (i, j)


def jogada_aleatorio(board):
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(available_moves)

def jogar(turnoEscolhido):
    board = [[" " for _ in range(3)] for _ in range(3)]
    turno = turnoEscolhido
    movimentos = 0

    while True:
        if turno == "X":
            movimento = jogada_campeao(board)
        else:
            movimento = jogada_aleatorio(board)

        board[movimento[0]][movimento[1]] = turno
        movimentos += 1

        if verificar_vencedor(board, turno):
            return turno, movimentos
        if verifica_se_esta_completo_board(board):
            return "VELHA", movimentos

        turno = "O" if turno == "X" else "X"

def jogadas_sequenciais(num_jogos):
    results = []
    turnoEscolhido = ("Digite por quem quer começar (X para vencedor O para aleatorio)")
    for _ in range(num_jogos):
        vencedor, movimentos = jogar(turnoEscolhido)
        results.append([vencedor, movimentos])

    # Escrever resultados em CSV
    with open("relatorio.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["vencedor", "numero jogadas"])
        writer.writerows(results)

    print(f"{num_jogos} jogos finalizados. Resultados salvos em 'relatorio.csv'.")

jogadas_sequenciais(1000)

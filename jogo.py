import csv
import random
from collections import defaultdict

# Tabela de conhecimento com recompensas
tabela_conhecimento = defaultdict(lambda: [0] * 9)
exploration_rate = 0.5

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

def verificar_vencedor_diagonal(board, player):
    return ([board[0][0], board[1][1], board[2][2]] == [player, player, player] or
            [board[2][0], board[1][1], board[0][2]] == [player, player, player])

def jogada_campeao(board):
    # ATACAR
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "X"
                if verificar_vencedor(board, "X"):
                    return (i, j)
                board[i][j] = " "

    # BLOQUEAR
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                if verificar_vencedor(board, "O"):
                    board[i][j] = "X"
                    return (i, j)
                board[i][j] = " "

    # JOGA NO CENTRO
    if board[1][1] == " ":
        return (1, 1)

    # CANTO
    for i, j in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[i][j] == " ":
            return (i, j)

    # PRIMEIRA POSIÇÃO
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return (i, j)

# Converter o tabuleiro para uma representação única (string)
def converter_tabuleiro(board):
    return "".join("".join(row) for row in board)

def jogada_aprendizado(board):
    estado = converter_tabuleiro(board)
    jogadas_possiveis = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

    if not jogadas_possiveis:
        return None

    if random.random() < exploration_rate:
        return random.choice(jogadas_possiveis)
    else:
        recompensas = [tabela_conhecimento[estado][i * 3 + j] for i, j in jogadas_possiveis]
        
        if recompensas:
            melhor_jogada = jogadas_possiveis[recompensas.index(max(recompensas))]
            return melhor_jogada
        else:
            return random.choice(jogadas_possiveis)

    
def jogar(turnoEscolhido):
    board = [[" " for _ in range(3)] for _ in range(3)]  
    turno = "X" if turnoEscolhido == "X" else "O"
    vencedor = None
    movimentos = 0
    historico_jogadas = []

    while vencedor is None and movimentos < 9: 
        if turno == "X":  
            movimento = jogada_campeao(board)
        else:  
            movimento = jogada_aprendizado(board)

        if movimento is None:
            break 

        historico_jogadas.append((converter_tabuleiro(board), movimento[0] * 3 + movimento[1]))

        board[movimento[0]][movimento[1]] = turno
        movimentos += 1

        if verificar_vencedor(board, turno):
            vencedor = turno
            for estado, jogada in historico_jogadas:
                if vencedor == "O":
                    tabela_conhecimento[estado][jogada] += 5
                elif vencedor == "X":
                    penalidade = 5 if verificar_vencedor_diagonal(board, "X") else 3
                    tabela_conhecimento[estado][jogada] -= penalidade
                else:
                    tabela_conhecimento[estado][jogada] += 5

        turno = "O" if turno == "X" else "X"

    if vencedor is None:
        vencedor = "VELHA" 

    return vencedor, movimentos


def jogadas_sequenciais(num_jogos):
    global exploration_rate
    results = []
    turnoEscolhido = input("Digite por quem quer começar (X para vencedor O para jogador aprendizado)")
    for _ in range(num_jogos):
        vencedor, movimentos = jogar(turnoEscolhido)
        results.append([vencedor, movimentos])
        if _ % 2000 == 0 and exploration_rate > 0.05:
            exploration_rate *= 0.9 

    # Escrever resultados em CSV
    with open("relatorio.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["vencedor", "numero jogadas"])
        writer.writerows(results)

    print(f"{num_jogos} jogos finalizados. Resultados salvos em 'relatorio.csv'.")

jogadas_sequenciais(500000)
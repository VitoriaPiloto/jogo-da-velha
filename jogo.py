import tkinter as tk
import random
from tkinter import messagebox

tabuleiro = [""] * 10
tabuleiro[0] = 0 

def verificarVencedor():
    combinacoes = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Linhas
        (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Colunas
        (1, 5, 9), (3, 5, 7)              # Diagonais
    ]

    for a, b, c in combinacoes:
        if tabuleiro[a] == tabuleiro[b] == tabuleiro[c] and tabuleiro[a] != "":
            return True

    return False

def clicarBotao(index, botao):
    global tabuleiro
    
    if tabuleiro[index] == "":
        jogador = "X" 
        tabuleiro[index] = jogador
        botao.config(text='X')
        tabuleiro[0] += 1  
        
        posicaoAleatoria = random.randint(1,9)
        
        while tabuleiro[posicaoAleatoria] == 'X' or tabuleiro[posicaoAleatoria] == 'O':
            posicaoAleatoria = random.randint(1,9)

        btn = botoes[posicaoAleatoria-1]
        btn.config(text = 'O')

        if verificarVencedor():
            messagebox.showinfo("Fim de Jogo", f"Jogador {jogador} venceu!")
            resetarJogo()
        elif tabuleiro[0] == 9:
            messagebox.showinfo("Fim de Jogo", "Empate!")
            resetarJogo()

def resetarJogo():
    global tabuleiro
    tabuleiro = [""] * 10
    tabuleiro[0] = 0
    for button in botoes:
        button.config(text="")

window = tk.Tk()
window.title("Jogo da Velha")

botoes = []
for i in range(1, 10):
    botao = tk.Button(window, text="", font=('normal', 40), width=5, height=2,
                       command=lambda i=i, button=None: clicarBotao(i, botoes[i-1]))
    botao.grid(row=(i-1)//3, column=(i-1) % 3)
    botoes.append(botao)

# Executa o loop principal da interface gráfica
window.mainloop()

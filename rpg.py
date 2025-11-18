from gettext import install
import pip
import random
import time
import sys
import json
import os
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except Exception:
    # Fallback when colorama isn't available: provide minimal no-op attributes
    class _Fallback:
        pass

    Fore = _Fallback()
    Fore.CYAN = ""
    Fore.RED = ""
    Fore.GREEN = ""
    Fore.YELLOW = ""
    Fore.BLUE = ""
    Fore.MAGENTA = ""
    Fore.WHITE = ""
    Fore.RESET = ""

    Style = _Fallback()
    Style.RESET_ALL = ""

    def init(autoreset=True):
        return None
import habilidade
import inventario
import itens
import karma
import mapa
import menu
import personagens
import savegame
import torneio
import treinamento

init(autoreset=True)

def criar_novo_heroi():
    nome = input("Digite o nome do herói: ").strip()
    if not nome:
        nome = "Herói"
    class Hero:
        def __init__(self, nome):
            self.nome = nome
            self.nivel = 1
            self.vida = 100
            self.forca = 10
            self.inventario = []
    return Hero(nome)

def main():
    print(f"{Fore.CYAN}*** RPG DO GUERREIRO DO PUNHO ***{Style.RESET_ALL}")
    
    heroi, config_data = savegame.load_game()
    
    if heroi:
        print(f"\nBem-vindo de volta, {heroi.nome}!")
    else:
        print("\nNenhum jogo salvo encontrado. Iniciando novo jogo.")
        heroi = criar_novo_heroi()
        
    menu.menu_jogo(heroi)

if __name__ == "__main__":
    main()
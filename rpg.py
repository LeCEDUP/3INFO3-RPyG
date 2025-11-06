import random
import time
import sys
import json
import os
from colorama import Fore, Style, init
from .item import Item
from .personagem import Personagem
from itens.arma import Arma
from itens.armadura import Armadura

init(autoreset=True)

def main():
    print(f"{Fore.CYAN}*** RPG DO GUERREIRO DO PUNHO ***{Style.RESET_ALL}")
    
    heroi, config_data = load_game()
    
    if heroi:
        print(f"\nBem-vindo de volta, {heroi.nome}!")
    else:
        print("\nNenhum jogo salvo encontrado. Iniciando novo jogo.")
        heroi = criar_novo_heroi()
        
    menu_jogo(heroi)

if __name__ == "__main__":
    main()
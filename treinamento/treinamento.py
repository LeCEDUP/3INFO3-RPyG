from missoes.missao import OPONENTE_MODELOS, MISSOES_DISPONIVEIS, ITENS_LOJA
import importlib
import savegame
import personagens
import habilidade
import karma
import mapa
import missoes
import torneio
import itens
import inventario
import menu
import random
from colorama import Fore, Style

def menu_treinamento(heroi):
    while True:
        print(f"\n{Fore.YELLOW}--- TREINAMENTO ---{Style.RESET_ALL}")
        print(f"Pontos de Treinamento (PTs): {Fore.CYAN}{heroi.pontos_treinamento}{Style.RESET_ALL}")
        print("1. Aumentar Atributo Base (+5 por 1 PT)")
        print("2. Melhorar Habilidade (Aumenta Nível por 2 PTs)")
        print("0. Voltar ao Menu Principal")
        
        escolha = input("Escolha a opção: ")
        
        if escolha == '0':
            savegame(heroi, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})
            break
        
        elif escolha == '1':
            if heroi.pontos_treinamento < 1:
                print(f"{Fore.RED}PTs insuficientes.{Style.RESET_ALL}")
                continue
            
            print("\nEscolha o Atributo para Aumentar (+5):")
            print("1. Ataque Base")
            print("2. Defesa Base")
            print("3. Velocidade Base")
            
            sub_escolha = input("Opção: ")
            
            if sub_escolha == '1':
                heroi.ataque_base += 5
                heroi.pontos_treinamento -= 1
                print(f"{Fore.GREEN}Ataque Base aumentado para {heroi.ataque_base}.{Style.RESET_ALL}")
            elif sub_escolha == '2':
                heroi.defesa_base += 5
                heroi.pontos_treinamento -= 1
                print(f"{Fore.GREEN}Defesa Base aumentada para {heroi.defesa_base}.{Style.RESET_ALL}")
            elif sub_escolha == '3':
                heroi.velocidade_base += 5
                heroi.pontos_treinamento -= 1
                print(f"{Fore.GREEN}Velocidade Base aumentada para {heroi.velocidade_base}.{Style.RESET_ALL}")
            else:
                print("Opção inválida.")
                
        elif escolha == '2':
            if heroi.pontos_treinamento < 2:
                print(f"{Fore.RED}PTs insuficientes (Custo: 2 PT).{Style.RESET_ALL}")
                continue
            
            print("\nEscolha a Habilidade para Aumentar o Nível (2 PT):")
            habilidades_melhoraveis = [h for h in heroi.habilidades if h.nivel_habilidade < h.max_nivel and h.nome != "Jab Rápido"]
            
            if not habilidades_melhoraveis:
                print("Nenhuma habilidade para melhorar.")
                continue
            
            for i, h in enumerate(habilidades_melhoraveis):
                print(f"{i+1}. {h.nome} (Nível {h.nivel_habilidade}/{h.max_nivel})")
            
            sub_escolha = input("Opção: ")
            
            if sub_escolha.isdigit() and 1 <= int(sub_escolha) <= len(habilidades_melhoraveis):
                habilidade_escolhida = habilidades_melhoraveis[int(sub_escolha) - 1]
                if habilidade_escolhida.melhorar():
                    heroi.pontos_treinamento -= 2
                    print(f"{Fore.GREEN}Habilidade {habilidade_escolhida.nome} melhorada para Nível {habilidade_escolhida.nivel_habilidade}.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Habilidade já está no nível máximo.{Style.RESET_ALL}")
            else:
                print("Opção inválida.")
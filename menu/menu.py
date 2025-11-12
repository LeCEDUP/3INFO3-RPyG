
from inventario.inventario import menu_inventario
from karma.karma import mostrar_status
from mapa.locais import ITENS_LOJA, menu_dojo, menu_lojas
from missoes.missao import MISSOES_DISPONIVEIS
from personagens.monstro import OPONENTE_MODELOS
import torneio
import rpg
import personagens
import savegame
import mapa
import karma
from torneio.torneio import iniciar_torneio
import treinamento

from personagens import Missao
import random
from colorama import Fore, Style

from treinamento.treinamento import menu_treinamento

def menu_jogo(heroi):
    print("\n" + Fore.YELLOW + "="*50)
    print(f" CIDADE DE KAIRU - DOJO CENTRAL")
    print("="*50 + Style.RESET_ALL)

    if not heroi.missao_ativa and "TORNEIO" not in heroi.missoes_completas:
        heroi.missao_ativa = Missao("TORNEIO", "Conquistar o título de Mestre Invicto no Torneio do Punho Ascendente.", "vencer_torneio", "Torneio", 1, 0, 500, 1000)

    if "TORNEIO" in heroi.missoes_completas and "DERROTAR_MESTRES" not in heroi.missoes_completas and not heroi.missao_ativa:
        heroi.missao_ativa = Missao("DERROTAR_MESTRES", "Derrote 3 Mestres para receber uma recompensa especial.", "derrotar_monstro", "Mestre", 3, 0, 150, 300)

    while heroi.esta_vivo():

        if heroi.missao_ativa and heroi.missao_ativa.progresso >= heroi.missao_ativa.quantidade:
            print(f"\n{Fore.YELLOW} MISSÃO COMPLETA: {heroi.missao_ativa.nome}!{Style.RESET_ALL}")
            heroi.gold += heroi.missao_ativa.gold_recompensa
            heroi.ganhar_experiencia(heroi.missao_ativa.exp_recompensa)
            heroi.missoes_completas.append(heroi.missao_ativa.id)
            heroi.missao_ativa = None
            input("Pressione ENTER para continuar...")

        if random.random() < 0.1: 
            print(f"\n{Fore.YELLOW}Um jovem monge se aproxima de você no Dojo.{Style.RESET_ALL}")
            print("Ele lhe pergunta: 'Qual é o caminho mais rápido para a vitória?'")
            print("1. O caminho da força bruta.")
            print("2. O caminho da defesa inabalável.")
            print("3. O caminho da velocidade e agilidade.")
            
            escolha_karma = input("Sua resposta (1/2/3): ")
            if escolha_karma == '1':
                heroi.karma = max(-100, heroi.karma - 5)
                print(f"{Fore.RED}O monge se afasta com um olhar de desaprovação. Karma: {heroi.karma}{Style.RESET_ALL}")
            elif escolha_karma == '2' or escolha_karma == '3':
                heroi.karma = min(100, heroi.karma + 5)
                print(f"{Fore.GREEN}O monge sorri e se curva em respeito. Karma: {heroi.karma}{Style.RESET_ALL}")
            
            savegame(heroi, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})

        print(f"\n{Fore.CYAN}--- MENU PRINCIPAL ---{Style.RESET_ALL}")
        print(f"PV: {Fore.RED}{heroi.vida}/{heroi.vida_max}{Style.RESET_ALL} | Vigor: {Fore.BLUE}{heroi.vigor}/{heroi.vigor_max}{Style.RESET_ALL} | Gold: {Fore.YELLOW}{heroi.gold}{Style.RESET_ALL}")
        print(f"Nível: {heroi.nivel} | EXP: {heroi.experiencia}/{heroi.exp_para_proximo_nivel}")
        
        print("\nOpções:")
        print("1. Status do Herói")
        print("2. Inventário e Equipamento")
        print("3. Treinamento (Usar PTs)")
        print("4. Dojo (Combate)")
        print("5. Lojas de Kairu")
        print("6. Torneio do Punho Ascendente")
        print("7. Salvar Jogo")
        print("0. Sair do Jogo")
        
        escolha = input("Escolha a opção: ")
        
        if escolha == '1':
            mostrar_status(heroi)
        elif escolha == '2':
            menu_inventario(heroi)
        elif escolha == '3':
            menu_treinamento(heroi)
        elif escolha == '4':
            menu_dojo(heroi)
        elif escolha == '5':
            menu_lojas(heroi)
        elif escolha == '6':
            iniciar_torneio(heroi)
        elif escolha == '7':
            savegame(heroi, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})
        elif escolha == '0':
            print(f"\n{Fore.YELLOW}Salvando e saindo...{Style.RESET_ALL}")
            savegame(heroi, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})
            break
        else:
            print("Opção inválida.")

    print(f"\n{Fore.RED}FIM DE JOGO!{Style.RESET_ALL}")
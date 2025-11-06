def menu_dojo(heroi):
    while True:
        print(f"\n{Fore.YELLOW}--- DOJO DE TREINAMENTO ---{Style.RESET_ALL}")
        print("Escolha o oponente para treinar:")
        
        opcoes = list(OPONENTE_MODELOS.keys())
        for i, nome in enumerate(opcoes):
            modelo = OPONENTE_MODELOS[nome]
            print(f"{i+1}. {nome} (Nível {modelo['nivel']} | {modelo['subclasse']}) - Recompensa: {modelo['exp_recompensa']} EXP / {modelo['gold_recompensa']} Gold")
            
        print("0. Voltar ao Menu Principal")
        
        escolha = input("Opção: ")
        
        if escolha == '0':
            break
        
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            nome_oponente = opcoes[int(escolha) - 1]
            oponente = OponenteIA(nome_oponente)
            iniciar_combate(heroi, oponente)
        else:
            print("Opção inválida.")

def loja_consumiveis(heroi):
    itens_loja = [
        Consumivel("Poção de PV Pequena", 10, "Restaura 50 Pontos de Vida.", efeito_pv=50),
        Consumivel("Elixir de Vigor Pequeno", 15, "Restaura 30 Pontos de Vigor.", efeito_vigor=30),
        Consumivel("Bandagem de Seda", 25, "Remove a condição Sangramento.", remove_condicao="Sangramento"),
        Consumivel("Antídoto", 30, "Remove a condição Veneno.", remove_condicao="Veneno"),
        Consumivel("Pomada Refrescante", 35, "Remove a condição Queimadura.", remove_condicao="Queimadura")
    ]
    
    while True:
        print(f"\n{Fore.YELLOW}--- LOJA DE CONSUMÍVEIS ---{Style.RESET_ALL}")
        print(f"Seu Gold: {Fore.YELLOW}{heroi.gold}{Style.RESET_ALL}")
        
        for i, item in enumerate(itens_loja):
            print(f"{i+1}. {item.nome} (Preço: {item.preco} Gold) - {item.descricao}")
            
        print("0. Voltar ao Menu Principal")
        
        escolha = input("Digite o número do item para comprar (0 para voltar): ")
        
        if escolha == '0':
            save_game(heroi, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})
            break
        
        if escolha.isdigit() and 1 <= int(escolha) <= len(itens_loja):
            item_escolhido = itens_loja[int(escolha) - 1]
            
            if heroi.gold >= item_escolhido.preco:
                heroi.gold -= item_escolhido.preco
                heroi.inventario.append(item_escolhido)
                print(f"{Fore.GREEN} {item_escolhido.nome} comprado! Gold restante: {heroi.gold}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Gold insuficiente para comprar {item_escolhido.nome}.{Style.RESET_ALL}")
        else:
            print("Escolha inválida.")

def vender_item(heroi):
    while True:
        print(f"\n{Fore.YELLOW}--- VENDA DE ITENS ---{Style.RESET_ALL}")
        print(f"Seu Gold: {Fore.YELLOW}{heroi.gold}{Style.RESET_ALL}")
        
        itens_vendaveis = []
        for item in heroi.inventario:
            if item.nome != "Punho do Destino":
                itens_vendaveis.append(item)

        if not itens_vendaveis:
            print("Você não tem itens vendáveis no inventário.")
            input("Pressione ENTER para continuar...")
            break

        print("\nItens no Inventário:")
        for i, item in enumerate(itens_vendaveis):
            preco_venda = int(item.preco * 0.5)
            status_equipado = ""
            if item in heroi.equipamento.values():
                status_equipado = f" ({Fore.RED}EQUIPADO{Style.RESET_ALL})"

            print(f"{i+1}. {item.nome} (Venda: {Fore.YELLOW}{preco_venda} Gold{Style.RESET_ALL}){status_equipado}")
            
        print("0. Voltar ao Menu Principal")
        
        escolha = input("Digite o número do item para vender (0 para voltar): ")
        
        if escolha == '0':
            save_game(heroi, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})
            break
        
        if escolha.isdigit() and 1 <= int(escolha) <= len(itens_vendaveis):
            item_escolhido = itens_vendaveis[int(escolha) - 1]
            
            if item_escolhido in heroi.equipamento.values():
                print(f"{Fore.RED} Você precisa desequipar {item_escolhido.nome} antes de vendê-lo.{Style.RESET_ALL}")
                continue

            preco_venda = int(item_escolhido.preco * 0.5)
            heroi.gold += preco_venda
            heroi.inventario.remove(item_escolhido)
            
            print(f"{Fore.GREEN} {item_escolhido.nome} vendido por {preco_venda} Gold! Total: {heroi.gold}{Style.RESET_ALL}")
        else:
            print("Escolha inválida.")

def loja_equipamentos(heroi):
    itens_loja = [
        Luva("Luvas de Couro Reforçado", 50, 8, "Aumenta o ataque."),
        Quimono("Quimono de Treino Avançado", 60, 5, "Aumenta a defesa."),
        Acessorio("Peso Corporal Leve", 40, 2, "Aumenta a velocidade."),
        Luva("Manoplas de Ferro", 120, 15, "Aumenta muito o ataque."),
        Quimono("Quimono de Seda Reforçada", 150, 10, "Aumenta a defesa e a velocidade."),
        Acessorio("Faixa da Agilidade", 100, 5, "Aumenta muito a velocidade.")
    ]
    
    while True:
        print(f"\n{Fore.YELLOW}--- LOJA DE EQUIPAMENTOS ---{Style.RESET_ALL}")
        print(f"Seu Gold: {Fore.YELLOW}{heroi.gold}{Style.RESET_ALL}")
        
        for i, item in enumerate(itens_loja):
            print(f"{i+1}. {item.nome} (Preço: {item.preco} Gold) - Slot: {item.slot.capitalize()}")
            
        print("0. Voltar ao Menu Principal")
        
        escolha = input("Digite o número do item para comprar (0 para voltar): ")
        
        if escolha == '0':
            save_game(heroi, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})
            break
        
        if escolha.isdigit() and 1 <= int(escolha) <= len(itens_loja):
            item_escolhido = itens_loja[int(escolha) - 1]
            
            if heroi.gold >= item_escolhido.preco:
                heroi.gold -= item_escolhido.preco
                heroi.inventario.append(item_escolhido)
                print(f"{Fore.GREEN} {item_escolhido.nome} comprado! Gold restante: {heroi.gold}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Gold insuficiente para comprar {item_escolhido.nome}.{Style.RESET_ALL}")
        else:
            print("Escolha inválida.")

def menu_lojas(heroi):
    while True:
        print(f"\n{Fore.YELLOW}--- LOJAS DE KAIRU ---{Style.RESET_ALL}")
        print("1. Loja de Consumíveis")
        print("2. Loja de Equipamentos")
        print("3. Vender Itens")
        print("0. Voltar ao Menu Principal")
        
        escolha = input("Escolha a loja: ")
        
        if escolha == '1':
            loja_consumiveis(heroi)
        elif escolha == '2':
            loja_equipamentos(heroi)
        elif escolha == '3':
            vender_item(heroi)
        elif escolha == '0':
            break
        else:
            print("Opção inválida.")

ITENS_LOJA = [
    Consumivel("Poção de PV Pequena", 10, "Restaura 50 Pontos de Vida.", efeito_pv=50),
    Consumivel("Elixir de Vigor Pequeno", 15, "Restaura 30 Pontos de Vigor.", efeito_vigor=30),
    Luva("Luvas de Couro Reforçado", 50, 8, "Aumenta o ataque."),
    Quimono("Quimono de Treino Avançado", 60, 5, "Aumenta a defesa."),
    Acessorio("Peso Corporal Leve", 40, 2, "Aumenta a velocidade.")
]
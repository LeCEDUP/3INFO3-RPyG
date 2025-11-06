def menu_inventario(heroi):
    while True:
        print(f"\n{Fore.YELLOW}--- INVENTÁRIO ---{Style.RESET_ALL}")
        
        if not heroi.inventario:
            print("O inventário está vazio.")
            input("Pressione ENTER para continuar...")
            break
            
        print("Itens:")
        for i, item in enumerate(heroi.inventario):
            print(f"{i+1}. {item}")
            
        print("\nOpções:")
        print("E. Equipar Item")
        print("D. Desequipar Item")
        print("U. Usar Consumível")
        print("0. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção (E/D/U/0) ou o número do item para inspecionar: ").upper()
        
        if escolha == '0':
            break
        
        elif escolha == 'E':
            if not any(isinstance(item, Equipamento) for item in heroi.inventario):
                print(f"{Fore.RED}Nenhum equipamento no inventário para equipar.{Style.RESET_ALL}")
                continue
                
            while True:
                try:
                    num = input("Digite o número do item para EQUIPAR (0 para cancelar): ")
                    if num == '0':
                        break
                    num = int(num)
                    if 1 <= num <= len(heroi.inventario):
                        item = heroi.inventario[num - 1]
                        if isinstance(item, Equipamento):
                            heroi.equipar_item(item)
                            break
                        else:
                            print(f"{Fore.RED}O item {item.nome} não é um equipamento.{Style.RESET_ALL}")
                    else:
                        print("Número inválido.")
                except ValueError:
                    print("Entrada inválida.")
        
        elif escolha == 'D':
            if not any(item for item in heroi.equipamento.values()):
                print(f"{Fore.RED}Nenhum item equipado para desequipar.{Style.RESET_ALL}")
                continue
                
            print("\nSlots Equipados:")
            slots_equipados = [slot for slot, item in heroi.equipamento.items() if item]
            for i, slot in enumerate(slots_equipados):
                print(f"{i+1}. {slot.capitalize()} ({heroi.equipamento[slot].nome})")
                
            while True:
                try:
                    num = input("Digite o número do slot para DESEQUIPAR (0 para cancelar): ")
                    if num == '0':
                        break
                    num = int(num)
                    if 1 <= num <= len(slots_equipados):
                        slot_escolhido = slots_equipados[num - 1]
                        heroi.desequipar_item(slot_escolhido)
                        break
                    else:
                        print("Número inválido.")
                except ValueError:
                    print("Entrada inválida.")

        elif escolha == 'U':
            if not any(isinstance(item, Consumivel) for item in heroi.inventario):
                print(f"{Fore.RED}Nenhum consumível no inventário para usar.{Style.RESET_ALL}")
                continue
                
            while True:
                try:
                    num = input("Digite o número do item para USAR (0 para cancelar): ")
                    if num == '0':
                        break
                    num = int(num)
                    if 1 <= num <= len(heroi.inventario):
                        indice_real = num - 1
                        if isinstance(heroi.inventario[indice_real], Consumivel):
                            heroi.usar_consumivel(indice_real)
                            break
                        else:
                            print(f"{Fore.RED}O item {heroi.inventario[indice_real].nome} não é um consumível.{Style.RESET_ALL}")
                    else:
                        print("Número inválido.")
                except ValueError:
                    print("Entrada inválida.")
        
        elif escolha.isdigit() and 1 <= int(escolha) <= len(heroi.inventario):
            item = heroi.inventario[int(escolha) - 1]
            print(f"\nDetalhes do Item: {item.nome}")
            print(f"  Descrição: {item.descricao}")
            print(f"  Preço de Compra: {item.preco} Gold")
            if isinstance(item, Equipamento):
                print(f"  Slot: {item.slot.capitalize()}")
                print(f"  Bônus Ataque: {item.bonus_ataque}")
                print(f"  Bônus Defesa: {item.bonus_defesa}")
                print(f"  Bônus Velocidade: {item.bonus_velocidade}")
            elif isinstance(item, Consumivel):
                print(f"  Efeito PV: {item.efeito_pv}")
                print(f"  Efeito Vigor: {item.efeito_vigor}")
                print(f"  Remove Condição: {item.remove_condicao if item.remove_condicao else 'Nenhuma'}")
            input("Pressione ENTER para continuar...")
            
        else:
            print("Opção inválida.")
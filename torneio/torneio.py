def iniciar_torneio(heroi):
    
    if heroi.nivel < 5:
        print(f"{Fore.RED}Você deve ser no mínimo Nível 5 para entrar no Torneio do Punho Ascendente!{Style.RESET_ALL}")
        return False

    missao_torneio = heroi.missao_ativa and heroi.missao_ativa.id == "TORNEIO"
    
    if missao_torneio:
        print(f"{Fore.YELLOW}Iniciando o Torneio, objetivo da Missão Principal!{Style.RESET_ALL}")

    print(f"\n{Fore.MAGENTA}*** TORNEIO DO PUNHO ASCENDENTE INICIADO! ***{Style.RESET_ALL}")

    oponentes = ["Lutador", "Mestre", "Desafiante", "Lenda"]
    vitorias = 0
    
    for nome_oponente in oponentes:
        oponente = OponenteIA(nome_oponente)
        print(f"\n{Fore.YELLOW}--- PRÓXIMO OPONENTE: {oponente.nome} ({oponente.subclasse}) ---{Style.RESET_ALL}")
        time.sleep(1)
        
        if not iniciar_combate(heroi, oponente):
            print(f"{Fore.RED}Você foi derrotado por {oponente.nome} e eliminado do Torneio!{Style.RESET_ALL}")
            return False
        
        vitorias += 1
        print(f"\n{Fore.GREEN}Vitória contra {oponente.nome}! Prepare-se para o próximo round.{Style.RESET_ALL}")
        heroi.vida = heroi.vida_max 
        heroi.vigor = heroi.vigor_max
        heroi.usos_foco_vigor = 1
        input("Pressione ENTER para continuar para o próximo round...")

    print(f"\n{Fore.YELLOW}*** PARABÉNS! VOCÊ É O CAMPEÃO DO TORNEIO DO PUNHO ASCENDENTE! ***{Style.RESET_ALL}")

    gold_premio = 500
    exp_premio = 1000
    
    heroi.gold += gold_premio
    heroi.ganhar_experiencia(exp_premio)

    item_unico = Luva("Punho do Destino", 1000, 25, "Luvas lendárias. +25 Ataque. Não pode ser vendido.")
    heroi.inventario.append(item_unico)
    
    print(f"{Fore.YELLOW}Recompensa: {gold_premio} Gold, {exp_premio} EXP e o item lendário '{item_unico.nome}'!{Style.RESET_ALL}")

    save_game(heroi, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})
    
    return True

def menu_combate(heroi, alvo):
    while True:
        print(f"\n{Fore.GREEN}--- SEU TURNO ---{Style.RESET_ALL}")
        print(f"PV: {Fore.RED}{heroi.vida}/{heroi.vida_max}{Style.RESET_ALL} | Vigor: {Fore.BLUE}{heroi.vigor}/{heroi.vigor_max}{Style.RESET_ALL} | Condições: {', '.join(heroi.condicoes.keys()) if heroi.condicoes else 'Nenhuma'}")
        print(f"Alvo PV: {Fore.RED}{alvo.vida}/{alvo.vida_max}{Style.RESET_ALL} | Alvo Condições: {', '.join(alvo.condicoes.keys()) if alvo.condicoes else 'Nenhuma'}")
        
        print("\nOpções:")
        print("1. Ataque Básico (Gera Vigor)")
        print("2. Habilidades de Combate")
        print("3. Usar Item Consumível")
        
        escolha = input("Escolha a ação: ")
        
        if escolha == '1':
            heroi.atacar(alvo)
            break
        elif escolha == '2':
            if menu_habilidades(heroi, alvo):
                break
        elif escolha == '3':
            if acao_item_combate(heroi):
                break
        else:
            print("Opção inválida.")

def menu_habilidades(heroi, alvo):
    habilidades_validas = [h for h in heroi.habilidades if h.nome != "Jab Rápido"]
    
    if not habilidades_validas:
        print("Você não possui Habilidades de Ação.")
        return False

    print(f"\n{Fore.YELLOW}--- HABILIDADES DISPONÍVEIS ---{Style.RESET_ALL}")
    for i, h in enumerate(habilidades_validas):
        custo_final = h.custo_vigor
        if heroi.talento == "Vigor Incansável":
            custo_final = int(h.custo_vigor * 0.9)

        if heroi.vigor >= custo_final:
            print(f"{i+1}. {h.nome} (Nível {h.nivel_habilidade}/{h.max_nivel} | Custo: {Fore.BLUE}{custo_final} Vigor{Style.RESET_ALL}) - {h.descricao}")
        else:
            print(f"{i+1}. {h.nome} (Nível {h.nivel_habilidade} | {Fore.RED}Vigor Insuficiente - Custo: {custo_final}{Style.RESET_ALL})")
    
    print("0. Voltar")

    while True:
        escolha = input("Escolha a Habilidade (0 para voltar): ")
        if escolha == '0':
            return False
        
        if escolha.isdigit() and 1 <= int(escolha) <= len(habilidades_validas):
            habilidade_escolhida = habilidades_validas[int(escolha) - 1]
            
            if habilidade_escolhida.nome == "Bloqueio de Guarda":
                custo = habilidade_escolhida.custo_vigor
                if heroi.vigor < custo:
                    print(f"{Fore.RED}Vigor insuficiente para Bloqueio de Guarda.{Style.RESET_ALL}")
                    continue
                heroi.aplicar_condicao("Bloqueio de Guarda", 1)
                heroi.vigor -= custo
                print(f"{Fore.BLUE} {heroi.nome} assume Postura de Bloqueio de Guarda.{Style.RESET_ALL}")
                return True
            
            elif habilidade_escolhida.nome == "Gancho Poderoso":
                if heroi.atacar(alvo, habilidade_escolhida):
                    if random.random() < 0.3: 
                        alvo.aplicar_condicao("Atordoado", 1)
                    return True
                return False
            
            elif habilidade_escolhida.nome == "Foco de Vigor":
                if heroi.usos_foco_vigor > 0:
                    heroi.vigor = min(heroi.vigor_max, heroi.vigor + 15)
                    heroi.usos_foco_vigor -= 1
                    print(f"{Fore.YELLOW} {heroi.nome} foca o Vigor. +15 Vigor. Usos restantes: {heroi.usos_foco_vigor}{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}Você já usou Foco de Vigor nesta batalha.{Style.RESET_ALL}")
                    continue
            
            elif habilidade_escolhida.nome == "Soco no Corpo":
                if heroi.atacar(alvo, habilidade_escolhida):
                    alvo.vigor_max = max(10, alvo.vigor_max - 5) 
                    alvo.vigor = min(alvo.vigor, alvo.vigor_max)
                    print(f"{Fore.YELLOW}Vigor Máximo de {alvo.nome} reduzido para {alvo.vigor_max}.{Style.RESET_ALL}")
                    return True
                return False

            elif habilidade_escolhida.nome == "Terremoto de Punho":
                if heroi.atacar(alvo, habilidade_escolhida):
                    alvo.aplicar_condicao("Atordoado", 1)
                    return True
                return False
            
            elif habilidade_escolhida.nome == "Combo Giratório":
                if heroi.atacar(alvo, habilidade_escolhida): 
                    dano_adicional = heroi.get_ataque_total() * 0.5
                    alvo.receber_dano(int(dano_adicional), heroi)
                    alvo.receber_dano(int(dano_adicional), heroi)
                    return True
                return False

            elif heroi.atacar(alvo, habilidade_escolhida):
                return True
            return False

        else:
            print("Escolha inválida.")

def acao_item_combate(heroi):
    consumiveis = [item for item in heroi.inventario if isinstance(item, Consumivel)]
    
    if not consumiveis:
        print("Você não tem itens consumíveis no inventário.")
        return False

    print(f"\n{Fore.YELLOW}--- CONSUMÍVEIS DISPONÍVEIS ---{Style.RESET_ALL}")
    for i, item in enumerate(consumiveis):
        print(f"{i+1}. {item.nome} - {item.descricao}")
    
    print("0. Voltar")

    while True:
        escolha = input("Escolha o Item para usar (0 para voltar): ")
        if escolha == '0':
            return False
        
        if escolha.isdigit() and 1 <= int(escolha) <= len(consumiveis):
            item_escolhido = consumiveis[int(escolha) - 1]
            
            indice_real = heroi.inventario.index(item_escolhido)
            
            if heroi.usar_consumivel(indice_real):
                return True
            else:
                continue 
        else:
            print("Escolha inválida.")

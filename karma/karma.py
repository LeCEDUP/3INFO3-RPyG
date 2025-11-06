def mostrar_status(heroi):
    print(f"\n{Fore.GREEN}--- STATUS DO HERÓI ---{Style.RESET_ALL}")
    print(f"Nome: {heroi.nome}")
    print(f"Classe: Guerreiro do Punho ({heroi.subclasse})")
    print(f"Nível: {heroi.nivel}")
    print(f"Experiência: {heroi.experiencia}/{heroi.exp_para_proximo_nivel}")
    print(f"Pontos de Treinamento: {Fore.CYAN}{heroi.pontos_treinamento}{Style.RESET_ALL}")
    print(f"Gold: {Fore.YELLOW}{heroi.gold}{Style.RESET_ALL}")
    
    karma_status = "Neutro"
    karma_cor = Style.RESET_ALL
    if heroi.karma > 50:
        karma_status = "Bom"
        karma_cor = Fore.GREEN
    elif heroi.karma < -50:
        karma_status = "Ruim"
        karma_cor = Fore.RED
        
    print(f"Karma: {karma_cor}{karma_status} ({heroi.karma}){Style.RESET_ALL}")
    
    print(f"\nAtributos Base:")
    print(f"  PV Máximo: {heroi.vida_max}")
    print(f"  Vigor Máximo: {heroi.vigor_max}")
    print(f"  Ataque Base: {heroi.ataque_base}")
    print(f"  Defesa Base: {heroi.defesa_base}")
    print(f"  Velocidade Base: {heroi.velocidade_base}")
    
    print(f"\nAtributos Totais:")
    print(f"  Ataque Total: {heroi.get_ataque_total()}")
    print(f"  Defesa Total: {heroi.get_defesa_total()}")
    print(f"  Velocidade Total: {heroi.get_velocidade_total()}")
    
    print(f"\nTalento: {Fore.MAGENTA}{heroi.talento if heroi.talento else 'Nenhum'}{Style.RESET_ALL}")
    
    print(f"\nEquipamento:")
    for slot, item in heroi.equipamento.items():
        print(f"  {slot.capitalize()}: {item.nome if item else 'Vazio'}")
        
    print(f"\nHabilidades:")
    for h in heroi.habilidades:
        print(f"  - {h}")
        
    print(f"\nMissão Ativa:")
    if heroi.missao_ativa:
        print(f"  ID: {heroi.missao_ativa.id}")
        print(f"  Nome: {heroi.missao_ativa.nome}")
        print(f"  Progresso: {heroi.missao_ativa.progresso}/{heroi.missao_ativa.quantidade}")
    else:
        print("  Nenhuma")
        
    print(f"\nMissões Completas: {', '.join(heroi.missoes_completas) if heroi.missoes_completas else 'Nenhuma'}")
    
    input("\nPressione ENTER para continuar...")
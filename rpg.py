ITENS_DO_JOGO = {
    "espada_longa": Arma("Espada Longa", "Aumenta o dano de ataque.", 350, bonus_ataque=10),
    "gume_do_infinito": Arma("Gume do Infinito", "Item lendário de dano de ataque.", 3400, bonus_ataque=70),
    "armadura_de_pano": Armadura("Armadura de Pano", "Aumenta a defesa.", 300, bonus_defesa=15),
    "capa_negra": Armadura("Capa Negra", "Aumenta a resistência mágica.", 450, bonus_resistencia_magica=15),
    "cajado_do_vazio": Arma("Cajado do Vazio", "Aumenta o poder de habilidade.", 2800, bonus_poder_habilidade=70)
}

HABILIDADES_DO_JOGO = {
    "disparo_mistico": Magia("Disparo Místico (Q)", "magico", 80, 40, "Dispara um projétil de energia mágica."),
    "golpe_decisivo": Magia("Golpe Decisivo (Q)", "fisico", 60, 30, "Aplica um golpe rápido e poderoso."),
    "barreira_arcana": Magia("Barreira Arcana (W)", "magico", 0, 50, "Cria um escudo mágico (simulado como cura)."),
}


def criar_campeao(nome):
    campeao = Heroi(nome, 500, 55, 30, 300, "Lutador")
    campeao.adicionar_habilidade("Q", HABILIDADES_DO_JOGO["golpe_decisivo"])
    campeao.adicionar_habilidade("W", HABILIDADES_DO_JOGO["disparo_mistico"])
    return campeao


def criar_monstro(tipo="Tropa"):
    if tipo == "Tropa":
        return Monstro("Minion Guerreiro", 150, 15, 5, tipo="Tropa")
    elif tipo == "Monstro da Selva":
        return Monstro("Lobo Ancestral", 400, 35, 10, tipo="Monstro da Selva")


def introducao():
    print("=" * 60)
    print("BEM-VINDO AO SIMULADOR DE COMBATE DE LEAGUE OF LEGENDS: A ARENA DE TEXTO")
    print("=" * 60)
    print("A névoa de guerra se dissipa. Você é um Campeão convocado para a Luta.")
    print("Seu objetivo é treinar, adquirir itens e derrotar as criaturas da selva.")
    print("Prepare-se para subir de nível e dominar a arena!")
    print("-" * 60)


def menu_principal(campeao):
    while campeao.esta_vivo():
        print("\n--- MENU PRINCIPAL ---")
        print("1. Exibir Status do Campeão")
        print("2. Ir para a Loja (Comprar/Equipar Item)")
        print("3. Entrar em Combate (Caçar Monstro)")
        print("4. Sair do Jogo")
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            campeao.exibir_status()
        elif escolha == '2':
            menu_loja(campeao)
        elif escolha == '3':
            simular_combate(campeao)
        elif escolha == '4':
            print("Obrigado por jogar! O Campeão retorna à base.")
            break
        else:
            print("Opção inválida. Tente novamente.")


def menu_loja(campeao):
    print("\n--- LOJA DE ITENS ---")
    print("Itens disponíveis:")
    itens_lista = list(ITENS_DO_JOGO.keys())
    for i, nome_item in enumerate(itens_lista):
        item = ITENS_DO_JOGO[nome_item]
        print(f"{i+1}. {item.nome} (Preço: {item.preco}) - {item.descricao}")
    print("0. Voltar ao Menu Principal")
    while True:
        try:
            escolha = input("Escolha o número do item para equipar (ou 0 para voltar): ")
            if escolha == '0':
                break
            indice = int(escolha) - 1
            if 0 <= indice < len(itens_lista):
                nome_item = itens_lista[indice]
                item_escolhido = ITENS_DO_JOGO[nome_item]
                campeao.equipar_item(item_escolhido)
                break
            else:
                print("Escolha inválida.")
        except ValueError:
            print("Entrada inválida. Digite um número.")


def simular_combate(campeao):
    monstro = criar_monstro("Monstro da Selva")
    print(f"\n** INÍCIO DO COMBATE **")
    print(f"{campeao.nome} encontra um {monstro.nome}!")
    turno = 1
    while campeao.esta_vivo() and monstro.esta_vivo():
        print(f"\n--- Turno {turno} ---")
        campeao.exibir_status()
        print("\nEscolha sua ação:")
        print("1. Ataque Básico")
        habilidades_opcoes = {}
        idx = 2
        for tecla, magia in campeao.habilidades.items():
            op = f"{idx}. Usar Habilidade {tecla} ({magia.nome})"
            print(op)
            habilidades_opcoes[str(idx)] = tecla
            idx += 1
        escolha = input("Sua escolha: ")
        if escolha == '1':
            campeao.atacar(monstro)
        elif escolha in habilidades_opcoes:
            tecla_habilidade = habilidades_opcoes[escolha]
            campeao.usar_habilidade(tecla_habilidade, monstro)
        else:
            print("Ação inválida. O campeão hesita e perde o turno.")
        if not monstro.esta_vivo():
            print(f"\n{monstro.nome} foi derrotado!")
            xp_ganha = 150
            campeao.ganhar_experiencia(xp_ganha)
            break
        if monstro.esta_vivo():
            monstro.atacar(campeao)
        turno += 1
    if not campeao.esta_vivo():
        print("\n** FIM DE JOGO **")
        print(f"O Campeão {campeao.nome} foi derrotado. Tente novamente!")


def main():
    introducao()
    nome_campeao = input("Digite o nome do seu Campeão: ")
    meu_campeao = criar_campeao(nome_campeao)
    menu_principal(meu_campeao)


if __name__ == "__main__":
    main()

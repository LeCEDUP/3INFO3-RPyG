


class Armadura(Item):
    def __init__(self, nome, descricao, preco, bonus_defesa=0, bonus_resistencia_magica=0):
        super().__init__(nome, descricao, preco)
        self.bonus_defesa = bonus_defesa
        self.bonus_resistencia_magica = bonus_resistencia_magica

    def aplicar_bonus(self, personagem):
        personagem.defesa += self.bonus_defesa
        personagem.resistencia_magica += self.bonus_resistencia_magica
        print(f"{personagem.nome} equipou {self.nome}. Bônus aplicados.")

    def remover_bonus(self, personagem):
        personagem.defesa -= self.bonus_defesa
        personagem.resistencia_magica -= self.bonus_resistencia_magica


class Magia:
    def __init__(self, nome, tipo_dano, dano_base, custo_mana, descricao):
        self.nome = nome
        self.tipo_dano = tipo_dano
        self.dano_base = dano_base
        self.custo_mana = custo_mana
        self.descricao = descricao

    def lancar(self, conjurador, alvo):
        if self.tipo_dano == 'fisico':
            dano_bruto = self.dano_base + (conjurador.ataque * 0.5)
        elif self.tipo_dano == 'magico':
            dano_bruto = self.dano_base + (conjurador.poder_habilidade * 0.7)
        else:
            dano_bruto = self.dano_base
        if conjurador.mana >= self.custo_mana:
            conjurador.mana -= self.custo_mana
            print(f"[{conjurador.nome}] lança a habilidade '{self.nome}' em [{alvo.nome}].")
            alvo.receber_dano(dano_bruto, self.tipo_dano)
            return True
        else:
            print(f"[{conjurador.nome}] não tem mana suficiente para lançar '{self.nome}'.")
            return False


class Heroi(Personagem):
    def __init__(self, nome, vida_base, ataque_base, defesa_base, mana_base, classe="Lutador"):
        super().__init__(nome, vida_base, ataque_base, defesa_base)
        self.nivel = 1
        self.experiencia = 0
        self.mana_maxima = mana_base
        self.mana = mana_base
        self.classe = classe
        self.habilidades = {}
        self.item_equipado = None

    def ganhar_experiencia(self, exp):
        self.experiencia += exp
        print(f"{self.nome} ganhou {exp} de experiência. Total: {self.experiencia}")
        xp_para_proximo_nivel = self.nivel * 100
        while self.experiencia >= xp_para_proximo_nivel:
            self.subir_nivel()
            xp_para_proximo_nivel = self.nivel * 100

    def subir_nivel(self):
        self.nivel += 1
        print(f"\n** {self.nome} subiu para o NÍVEL {self.nivel}! **")
        self.vida_maxima += 50
        self.vida = self.vida_maxima
        self.ataque += 5
        self.defesa += 2
        self.mana_maxima += 20
        self.mana = self.mana_maxima
        print(f"Status aumentados: Vida Máxima (+50), Ataque (+5), Defesa (+2), Mana Máxima (+20).")

    def equipar_item(self, item):
        if self.item_equipado:
            print(f"Desequipando {self.item_equipado.nome} antes de equipar o novo item.")
            self.item_equipado.remover_bonus(self)
        if isinstance(item, (Arma, Armadura)):
            item.aplicar_bonus(self)
            self.item_equipado = item
            self.inventario.append(item)
        else:
            print(f"Não é possível equipar {item.nome}.")

    def adicionar_habilidade(self, tecla, magia):
        self.habilidades[tecla] = magia
        print(f"Habilidade '{magia.nome}' adicionada à tecla '{tecla}'.")

    def usar_habilidade(self, tecla, alvo):
        if tecla in self.habilidades:
            magia = self.habilidades[tecla]
            return magia.lancar(self, alvo)
        else:
            print(f"Tecla '{tecla}' não corresponde a nenhuma habilidade.")
            return False

    def exibir_status(self):
        super().exibir_status()
        print(f"Nível: {self.nivel} (XP: {self.experiencia}/{self.nivel * 100})")
        print(f"Mana: {self.mana}/{self.mana_maxima}")
        print(f"Classe: {self.classe}")
        print("Habilidades:")
        for tecla, magia in self.habilidades.items():
            print(f"  [{tecla}] {magia.nome}: {magia.descricao} (Custo: {magia.custo_mana})")
        print("-" * 25)


class Monstro(Personagem):
    def __init__(self, nome, vida_base, ataque_base, defesa_base, tipo="Tropa"):
        super().__init__(nome, vida_base, ataque_base, defesa_base)
        self.tipo = tipo

    def atacar(self, alvo):
        dano_bruto = self.ataque
        print(f"[{self.nome}] ({self.tipo}) ataca [{alvo.nome}].")
        alvo.receber_dano(dano_bruto, tipo_dano="fisico")


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

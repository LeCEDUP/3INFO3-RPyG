import random

# ---------- Classes base de Personagem ----------

class Personagem:
    def __init__(self, nome, vida, ataque, defesa, agilidade, mana):
        self.nome = nome
        self.vida_max = vida
        self.mana_max = mana
        self.vida = vida
        self.mana = mana
        self.ataque = ataque
        self.defesa = defesa
        self.agilidade = agilidade
        self.slot_arma = None
        self.slot_armadura = None
        self.slots_itens_comuns = [None]*5
        self.slots_tesouros = [None]*2
        self.nivel = 1
        self.xp = 0
        self.xp_para_subir = [0, 50, 150, 350, 700]

        # Inicializa moedas ao criar personagem
        self.moedas = 200

    def esta_vivo(self):
        return self.vida > 0

    def subir_de_nivel(self):
        max_nivel = 5
        if self.nivel < max_nivel and self.xp >= self.xp_para_subir[self.nivel]:
            self.nivel +=1
            self.aumentar_status_por_nivel()
            print(f"{self.nome} subiu para o nível {self.nivel}!")
        elif self.nivel >= max_nivel:
            print(f"{self.nome} já está no nível máximo.")

    def aumentar_status_por_nivel(self):
        self.vida_max = int(self.vida_max * 1.35)
        self.mana_max = int(self.mana_max * 1.35)
        self.ataque = int(self.ataque * 1.35)
        self.defesa = int(self.defesa * 1.35)
        self.agilidade = int(self.agilidade * 1.35)
        self.vida = self.vida_max
        self.mana = self.mana_max
        print(f"{self.nome} melhorou todos os status em 35%!")

    def calcular_ataque(self):
        base = self.ataque
        if self.slot_arma:
            base += getattr(self.slot_arma, 'poder', 0)
        return base

    def calcular_defesa(self):
        base = self.defesa
        if self.slot_armadura:
            base += getattr(self.slot_armadura, 'defesa', 0)
        return base

    def atacar(self, monstro):
        dano = max(self.calcular_ataque() - monstro.defesa, 0)
        monstro.vida -= dano
        print(f"{self.nome} atacou {monstro.nome} causando {dano} de dano. Vida do monstro: {max(monstro.vida,0)}")


class Ladino(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 90, 6, 7, 18, 11)
        print(f"{self.nome} nasceu como Ladino.")

class Guerreiro(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 120, 10, 18, 8, 5)
        print(f"{self.nome} nasceu como Guerreiro.")

class Mago(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 90, 0, 13, 7, 22)
        print(f"{self.nome} nasceu como Mago.")

# ---------- Classes Monstro e Boss ----------

class Monstro:
    def __init__(self, nome, vida, ataque, defesa, tamanho, nivel):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.tamanho = tamanho
        self.nivel = nivel

    def esta_vivo(self):
        return self.vida > 0

    def atacar(self, personagem):
        dano = max(self.ataque - personagem.calcular_defesa(), 0)
        personagem.vida -= dano
        print(f"{self.nome} atacou {personagem.nome} causando {dano} de dano. Vida do herói: {max(personagem.vida,0)}")

class BossFinal(Monstro):
    def __init__(self):
        super().__init__("Boss Final", 1000, 80, 66, "Enorme", "Boss")
        self.mana = 59
        self.agilidade = 35

# ---------- Dados de monstros ----------

monstros_nivel = {
    "Baixa": [
        Monstro("Goblin", 30, 12, 5, "Pequeno", "Baixa"),
        Monstro("Rato Gigante", 25, 10, 4, "Pequeno", "Baixa")
    ],
    "Media": [
        Monstro("Orc Guerreiro", 60, 20, 15, "Médio", "Média"),
        Monstro("Troll Jovem", 75, 23, 18, "Grande", "Média")
    ],
    "Alta": [
        Monstro("Dragão Ancião", 350, 50, 40, "Enorme", "Alta"),
    ]
}

xp_por_monstro = {'Baixa': 20, 'Média': 50, 'Alta': 100}

# ---------- Eventos ----------

def shop(personagem):
    print("\nVocê encontrou um Shop!")
    print("1. Poção de Vida Pequena (50 moedas) - recupera 25% vida")
    print("2. Poção de Vida Média (100 moedas) - recupera 50% vida")
    print("3. Sair da loja")
    escolha = input("Escolha o que comprar: ")
    if escolha == "1":
        if personagem.moedas >= 50:
            personagem.moedas -= 50
            cura = int(personagem.vida_max * 0.25)
            personagem.vida = min(personagem.vida + cura, personagem.vida_max)
            print(f"Você comprou Poção de Vida Pequena e recuperou {cura} de vida.")
        else:
            print("Moedas insuficientes.")
    elif escolha == "2":
        if personagem.moedas >= 100:
            personagem.moedas -= 100
            cura = int(personagem.vida_max * 0.5)
            personagem.vida = min(personagem.vida + cura, personagem.vida_max)
            print(f"Você comprou Poção de Vida Média e recuperou {cura} de vida.")
        else:
            print("Moedas insuficientes.")
    else:
        print("Você saiu do Shop.")

def hospedaria(personagem):
    print("\nVocê encontrou uma Hospedaria.")
    print("Descansar aqui custa 125 moedas e cura 60% de vida e mana.")
    quer = input("Deseja descansar? (sim/nao): ")
    if quer.lower() == "sim":
        if personagem.moedas >= 125:
            personagem.moedas -= 125
            personagem.vida = min(int(personagem.vida_max * 0.6) + personagem.vida, personagem.vida_max)
            personagem.mana = min(int(personagem.mana_max * 0.6) + personagem.mana, personagem.mana_max)
            print(f"Você descansou e recuperou 60% de vida e mana.")
        else:
            print("Moedas insuficientes para descansar.")

def aldeia_amistosa(personagem):
    print("\nVocê chegou a uma Aldeia Amistosa.")
    personagem.vida = personagem.vida_max
    personagem.mana = personagem.mana_max
    print("Vida e mana totalmente recuperadas!")

def antigo_santuario(personagem):
    print("\nVocê encontrou um Antigo Santuário.")
    personagem.vida = min(personagem.vida + int(personagem.vida_max * 0.5), personagem.vida_max)
    personagem.mana = min(personagem.mana + int(personagem.mana_max * 0.5), personagem.mana_max)
    print("Você recuperou 50% de vida e mana.")

def treinar(personagem):
    print(f"\n{personagem.nome}, escolha um atributo para melhorar:\n1.Vida\n2.Ataque\n3.Defesa\n4.Agilidade\n5.Mana")
    escolha = input("Digite o número do atributo: ")
    attrs = {'1':'vida_max', '2':'ataque', '3':'defesa', '4':'agilidade', '5':'mana_max'}
    attr = attrs.get(escolha)
    if attr:
        setattr(personagem, attr, getattr(personagem, attr) + 1)
        dano_exaustao = int(personagem.vida * 0.1)
        personagem.vida -= dano_exaustao
        print(f"Treinou {attr} +1 e sofreu {dano_exaustao} de dano por exaustão. Vida atual: {personagem.vida}")
        if personagem.vida <= 0:
            print(f"{personagem.nome} caiu por exaustão.")
    else:
        print("Escolha inválida.")

def torneio(personagem):
    chance_vencer = min(25 + (personagem.nivel - 1) * 10, 65)
    escolha = input("Quer participar do Torneio na corte do rei? (sim/nao) ").lower()
    if escolha == "sim":
        if random.randint(1,100) <= chance_vencer:
            personagem.ataque = int(personagem.ataque * 1.1)
            personagem.defesa = int(personagem.defesa * 1.1)
            personagem.agilidade = int(personagem.agilidade * 1.1)
            personagem.vida_max = int(personagem.vida_max * 1.1)
            personagem.mana_max = int(personagem.mana_max * 1.1)
            personagem.vida = personagem.vida_max
            personagem.mana = personagem.mana_max
            print(f"{personagem.nome} venceu o torneio e aumentou seus atributos em 10%!")
            return True
        else:
            dano = int(personagem.vida * 0.35)
            personagem.vida -= dano
            print(f"{personagem.nome} perdeu o torneio e sofreu {dano} de dano! Vida atual: {personagem.vida}")
            return True
    return False

def evento_caminho(personagem):
    chance = random.randint(1, 100)
    if chance <= 20:
        shop(personagem)
        return True
    elif chance <= 40:
        hospedaria(personagem)
        return True
    elif chance <= 50:
        aldeia_amistosa(personagem)
        return True
    elif chance <= 55:
        antigo_santuario(personagem)
        return True
    else:
        print("\nNenhum evento especial. A jornada continua.")
        return False

# ---------- Funções de combate ----------

def enfrentar_batalha(personagem, nivel_monstro):
    print(f"\n{personagem.nome} enfrenta monstros de nível {nivel_monstro}!")
    grupos = monstros_nivel[nivel_monstro]
    for monstro in grupos:
        while monstro.esta_vivo() and personagem.esta_vivo():
            personagem.atacar(monstro)
            if monstro.esta_vivo():
                monstro.atacar(personagem)
            if personagem.esta_vivo():
                xp_ganha = sum(xp_por_monstro[nivel_monstro] for _ in grupos)
                personagem.xp += xp_ganha
                print(f"{personagem.nome} ganhou {xp_ganha} de XP.")
                personagem.subir_de_nivel()
                print("Você venceu a Batalha!")
                return True
            else:
                print(f"{personagem.nome} foi derrotado...")
                return False

def enfrentar_boss(personagem):
    boss = BossFinal()
    print('\nO Boss Final surge diante de você e diz: "Você ganhou a minha atenção, Camponês. Defenda-se!"\n')

    while boss.esta_vivo() and personagem.esta_vivo():
        personagem.atacar(boss)
        if boss.esta_vivo():
            boss.atacar(personagem)

    if personagem.esta_vivo():
        print(f"\nMuito bom, {personagem.nome}, pouparei estas terras... Por hora.")
        print("O Boss Final desaparece. Você ouve as pessoas vibrando ao longe e, aos poucos, tochas se aproximando.")
        print("Os monstros se foram. O Reino está salvo.")
        return True
    else:
        print("Você falhou em sua missão.")
        return False

# ---------- Função principal do jogo ----------

def jogo():
    nome = input("Digite o nome do seu herói: ")
    classe = input("Escolha a classe (Ladino, Guerreiro, Mago): ")
    if classe.lower() == "ladino":
        heroi = Ladino(nome)
    elif classe.lower() == "guerreiro":
        heroi = Guerreiro(nome)
    else:
        heroi = Mago(nome)

    batalhas_vencidas = 0
    total_batalhas = 12
    niveis_monstros = ["Baixa"]*4 + ["Media"]*5 + ["Alta"]*3 # Progressão dos 12 combates

    while batalhas_vencidas < total_batalhas and heroi.esta_vivo():
        print("\nVocê pode escolher:")
        print("1. Treinar (ganha +1 em atributo, sofre 10% de dano)")
        print("2. Participar do Torneio")
        print("3. Seguir na Jornada sem eventos (combater monstros)")
        escolha = input("Escolha sua ação (1/2/3): ")
        if escolha == "1":
            treinar(heroi)
            if not heroi.esta_vivo():
                print("Você caiu por exaustão. Fim de jogo.")
                return
        elif escolha == "2":
            if torneio(heroi):
                continue
        elif escolha != "3":
            print("Opção inválida.")
            continue

        tem_evento = evento_caminho(heroi)
        if not tem_evento:
            if enfrentar_batalha(heroi, niveis_monstros[batalhas_vencidas]):
                batalhas_vencidas += 1
            else:
                print("Game Over.")
                return

        print(f"Moedas restantes: {heroi.moedas}")

    if heroi.esta_vivo():
        boss_vencido = enfrentar_boss(heroi)
        if not boss_vencido:
            print("Você falhou em sua missão.")
    else:
        print("Você falhou em sua missão.")

if __name__ == "__main__":
    jogo()


class TesouroComum:
    def __init__(self, nome, descricao, bonus_atributo=None, bonus_valor=0, efeito_especial=None):
        self.nome = nome
        self.descricao = descricao
        self.bonus_atributo = bonus_atributo
        self.bonus_valor = bonus_valor
        self.efeito_especial = efeito_especial  # função para efeitos especiais

    def usar(self, heroi):
        if self.bonus_atributo and hasattr(heroi, self.bonus_atributo):
            atual = getattr(heroi, self.bonus_atributo)
            setattr(heroi, self.bonus_atributo, atual + self.bonus_valor)
            print(f"{heroi.nome} usou {self.nome} e ganhou +{self.bonus_valor} {self.bonus_atributo}.")
        elif self.efeito_especial:
            self.efeito_especial(heroi)
        else:
            print(f"{heroi.nome} usou {self.nome}.")

# ---------- Tesouros raros do Ladino ----------

class KrisNaga(Arma):
    def __init__(self):
        super().__init__("Kris Naga", "Adaga rara que concede +8 de ataque para Ladino.", poder=8)

class PedraMalverde(TesouroComum):
    def __init__(self):
        super().__init__("Pedra de Malverde", "Dobra a defesa do Ladino.")

class AmuletoSaraKali(TesouroComum):
    def __init__(self):
        super().__init__("Amuleto de Sara Kali", "Aumenta +6 de agilidade para Ladino.", "agilidade", 6)

class PergaminhoSokeHatsumi(TesouroComum):
    def __init__(self):
        super().__init__("Pergaminho de Soke Hatsumi", "Aumenta +7 de mana máxima para Ladino.", "mana_max", 7)

# ---------- Tesouros raros do Guerreiro ----------

class EspadaDeAres(Arma):
    def __init__(self):
        super().__init__("Espada de Ares", "Espada lendária que concede +10 de ataque para Guerreiro.", poder=10)

class EscudoDeAegis(Armadura):
    def __init__(self):
        super().__init__("Escudo de Aegis", "Escudo poderoso que concede +10 de defesa para Guerreiro.", defesa=10)

class BotasDeOricalco(TesouroComum):
    def __init__(self):
        super().__init__("Botas de Oricalco", "Botas que aumentam +10 de agilidade para Guerreiro.","agilidade", 10)

class ManuscritoDoLegionario(TesouroComum):
    def __init__(self):
        super().__init__("Manuscrito do Legionário", "Manuscrito que aumenta +10 de mana máxima para Guerreiro.","mana_max",10)

# ---------- Tesouros raros do Mago ----------

class RuyiJinguBang(Arma):
    def __init__(self):
        super().__init__("Ruyi Jingu Bang", "Arma rara que concede +10 de ataque e +10 de agilidade para o Mago.", 10)
        self.bonus_agilidade = 10

class PedraChintamani(TesouroComum):
    def __init__(self):
        super().__init__("Pedra Chintamani", "Pedra preciosa que aumenta +10 de mana máxima para o Mago.", "mana_max", 10)

class VasoDaFeniz(TesouroComum):
    def __init__(self):
        super().__init__("Vaso da Fênix", "Permite ressuscitar com 50% de vida e mana uma vez por batalha.")

# ---------- Tesouros comuns universais ----------

def efeito_moeda_2x(heroi):
    heroi.status['moedas_2x'] = True
    print(f"{heroi.nome} agora ganha o dobro de moedas por inimigos derrotados.")

def efeito_subir_nivel(heroi):
    heroi.subir_de_nivel()

BraceleteOuroboros = TesouroComum("Bracelete de Ouroboros", "Aumenta +6 no menor status do herói.",
                                  efeito_especial=lambda heroi: aumentar_menor_status(heroi, 6))
MoedaDaSorte = TesouroComum("Moeda da Sorte", "Dobra moedas ganhas por inimigo derrotado.", efeito_especial=efeito_moeda_2x)
AmpulhetaJade = TesouroComum("Ampulheta de Jade", "Sobe de nível imediatamente.", efeito_especial=efeito_subir_nivel)

def aumentar_menor_status(heroi, valor):
    attrs = {
        'vida_max': heroi.vida_max,
        'ataque': heroi.ataque,
        'defesa': heroi.defesa,
        'agilidade': heroi.agilidade,
        'mana_max': heroi.mana_max
    }
    menor = min(attrs, key=attrs.get)
    atual = getattr(heroi, menor)
    setattr(heroi, menor, atual + valor)
    print(f"{heroi.nome} teve seu {menor} aumentado em {valor} pontos.")
from .item import Item

class Arma(Item):
    def __init__(self, nome, descricao, bonus_ataque):
        super().__init__(nome, descricao)
        self.bonus_ataque = bonus_ataque
        class Adaga(Arma):
    def __init__(self):
        super().__init__("Adaga", "Arma básica do Ladino (+10 de ataque)", 10, "Ladino")

class Espada(Arma):
    def __init__(self):
        super().__init__("Espada", "Arma básica do Guerreiro (+10 de ataque)", 10, "Guerreiro")

class Grimório(Arma):
    def __init__(self):
        super().__init__("Grimório", "Arma básica do Mago (+10 de ataque)", 10, "Mago")
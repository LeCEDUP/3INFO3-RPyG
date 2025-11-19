from .item import Item

class Armadura(Item):
    def __init__(self, nome, descricao, bonus_defesa):
        super().__init__(nome, descricao)
        self.bonus_defesa = bonus_defesa
        ArmaduraBarbara = Armadura("Armadura Bárbara", "Armadura básica do Guerreiro (+10 de defesa)", 10, "Guerreiro")
CapaDasSombras = Armadura("Capa das Sombras", "Armadura básica do Ladino (+4 de defesa)", 4, "Ladino")
RobeDaAcademiaArcana = Armadura("Robe da Academia Arcana", "Armadura básica do Mago (+8 de defesa)", 8, "Mago")
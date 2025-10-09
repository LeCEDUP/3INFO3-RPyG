from .item import Item

class Armadura(Item):
    def __init__(self, nome, descricao, bonus_defesa):
        super().__init__(nome, descricao)
        self.bonus_defesa = bonus_defesa
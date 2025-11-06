from .item import Item

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


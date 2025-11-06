from .item import Item

class Arma(Item):
    def __init__(self, nome, descricao, preco, bonus_ataque=0, bonus_poder_habilidade=0):
        super().__init__(nome, descricao, preco)
        self.bonus_ataque = bonus_ataque
        self.bonus_poder_habilidade = bonus_poder_habilidade

    def aplicar_bonus(self, personagem):
        personagem.ataque += self.bonus_ataque
        personagem.poder_habilidade += self.bonus_poder_habilidade
        print(f"{personagem.nome} equipou {self.nome}. Bônus aplicados.")

    def remover_bonus(self, personagem):
        personagem.ataque -= self.bonus_ataque
        personagem.poder_habilidade -= self.bonus_poder_habilidade
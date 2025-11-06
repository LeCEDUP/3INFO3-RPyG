from .personagem import Personagem

class Monstro(Personagem):
    def __init__(self, nome, vida_base, ataque_base, defesa_base, tipo="Tropa"):
        super().__init__(nome, vida_base, ataque_base, defesa_base)
        self.tipo = tipo

    def atacar(self, alvo):
        dano_bruto = self.ataque
        print(f"[{self.nome}] ({self.tipo}) ataca [{alvo.nome}].")
        alvo.receber_dano(dano_bruto, tipo_dano="fisico")

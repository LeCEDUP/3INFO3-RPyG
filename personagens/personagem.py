class Personagem:
    def __init__(self, nome, vida_base, ataque_base, defesa_base):
        self.nome = nome
        self.vida_maxima = vida_base
        self.vida = vida_base
        self.ataque = ataque_base
        self.defesa = defesa_base
        self.poder_habilidade = 0
        self.resistencia_magica = 0
        self.inventario = []

    def esta_vivo(self):
        return self.vida > 0

    def calcular_dano_recebido(self, dano_bruto, tipo_dano="fisico"):
        if tipo_dano == "fisico":
            reducao = self.defesa / (100 + self.defesa)
        elif tipo_dano == "magico":
            reducao = self.resistencia_magica / (100 + self.resistencia_magica)
        else:
            reducao = 0
        dano_final = dano_bruto * (1 - reducao)
        return int(dano_final)

    def receber_dano(self, dano_bruto, tipo_dano="fisico"):
        dano_final = self.calcular_dano_recebido(dano_bruto, tipo_dano)
        self.vida -= dano_final
        print(f"[{self.nome}] recebeu {dano_final} de dano ({tipo_dano}). Vida restante: {self.vida}/{self.vida_maxima}")
        if self.vida <= 0:
            self.vida = 0
            print(f"[{self.nome}] foi derrotado!")
            return True
        return False

    def atacar(self, alvo):
        dano_bruto = self.ataque
        print(f"[{self.nome}] ataca [{alvo.nome}] com um Ataque Básico.")
        alvo.receber_dano(dano_bruto, tipo_dano="fisico")

    def exibir_status(self):
        print(f"\n--- Status de {self.nome} ---")
        print(f"Vida: {self.vida}/{self.vida_maxima}")
        print(f"Ataque (AD): {self.ataque}")
        print(f"Armadura (Defesa): {self.defesa}")
        print(f"Poder de Habilidade (AP): {self.poder_habilidade}")
        print(f"Resistência Mágica: {self.resistencia_magica}")
        print(f"Inventário: {[item.nome for item in self.inventario]}")
        print("-" * 25)
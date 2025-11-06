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

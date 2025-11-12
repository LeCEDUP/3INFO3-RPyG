from itens import item


class Equipamento(item):
    def __init__(self, nome, preco, slot, bonus_ataque=0, bonus_defesa=0, bonus_velocidade=0, descricao="Um equipamento."):
        super().__init__(nome, preco, descricao)
        self.slot = slot
        self.bonus_ataque = bonus_ataque
        self.bonus_defesa = bonus_defesa
        self.bonus_velocidade = bonus_velocidade
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "slot": self.slot,
            "bonus_ataque": self.bonus_ataque,
            "bonus_defesa": self.bonus_defesa,
            "bonus_velocidade": self.bonus_velocidade
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["nome"], data["preco"], data["slot"], 
            data["bonus_ataque"], data["bonus_defesa"], data["bonus_velocidade"], 
            data["descricao"]
        )

class Luva(Equipamento):
    def __init__(self, nome, preco, bonus_ataque, descricao="Luvas que aumentam o ataque."):
        super().__init__(nome, preco, "luva", bonus_ataque=bonus_ataque, descricao=descricao)

    @classmethod
    def from_dict(cls, data):
        return cls(data["nome"], data["preco"], data["bonus_ataque"], data["descricao"])

class Quimono(Equipamento):
    def __init__(self, nome, preco, bonus_defesa, descricao="Quimono que aumenta a defesa."):
        super().__init__(nome, preco, "armadura", bonus_defesa=bonus_defesa, descricao=descricao)

    @classmethod
    def from_dict(cls, data):
        return cls(data["nome"], data["preco"], data["bonus_defesa"], data["descricao"])

class Acessorio(Equipamento):
    def __init__(self, nome, preco, bonus_velocidade, descricao="Acessório que aumenta a velocidade."):
        super().__init__(nome, preco, "acessorio", bonus_velocidade=bonus_velocidade, descricao=descricao)

    @classmethod
    def from_dict(cls, data):
        return cls(data["nome"], data["preco"], data["bonus_velocidade"], data["descricao"])


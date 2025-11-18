class Missao:
    def __init__(self, id, nome, descricao, tipo, alvo, quantidade, progresso, gold_recompensa, exp_recompensa):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.tipo = tipo  
        self.alvo = alvo  
        self.quantidade = quantidade
        self.progresso = progresso
        self.gold_recompensa = gold_recompensa
        self.exp_recompensa = exp_recompensa

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "alvo": self.alvo,
            "quantidade": self.quantidade,
            "progresso": self.progresso,
            "gold_recompensa": self.gold_recompensa,
            "exp_recompensa": self.exp_recompensa
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            data["id"], data["nome"], data["descricao"], data["tipo"], 
            data["alvo"], data["quantidade"], data["progresso"], 
            data["gold_recompensa"], data["exp_recompensa"]
        )
    
MISSOES_DISPONIVEIS = [
    Missao("CAÇA_LUTADORES", "Derrote 5 Lutadores no Dojo.", "derrotar_monstro", "Lutador", "Lutador", 5, 0, 50, 100),
    Missao("CAÇA_MESTRES", "Derrote 3 Mestres no Dojo.", "derrotar_monstro", "Mestre", "Mestre", 3, 0, 100, 250),
    Missao("CAÇA_DESAFIANTES", "Derrote 2 Desafiantes no Dojo.", "derrotar_monstro", "Desafiante", "Desafiante", 2, 0, 150, 400)
]
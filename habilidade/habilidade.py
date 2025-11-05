class Habilidade:
    def __init__(self, nome, custo_vigor, dano_base, descricao, nivel_habilidade=1):
        self.nome = nome
        self.custo_vigor = custo_vigor
        self.dano_base = dano_base
        self.descricao = descricao
        self.nivel_habilidade = nivel_habilidade
        self.max_nivel = 5 

    def __str__(self):
        return f"{self.nome} (Nível {self.nivel_habilidade}/{self.max_nivel} | Custo: {self.custo_vigor} Vigor | Dano Base: {self.dano_base}): {self.descricao}"

    def melhorar(self):
        if self.nivel_habilidade < self.max_nivel:
            self.nivel_habilidade += 1
            self.dano_base = int(self.dano_base * 1.1)
            self.custo_vigor = max(5, self.custo_vigor - 1) 
            return True
        return False
    
    def to_dict(self):
        return {
            "__class__": self.__class__.__name__,
            "nome": self.nome,
            "custo_vigor": self.custo_vigor,
            "dano_base": self.dano_base,
            "descricao": self.descricao,
            "nivel_habilidade": self.nivel_habilidade
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["nome"], data["custo_vigor"], data["dano_base"], 
            data["descricao"], data["nivel_habilidade"]
        )
class Item:
    def __init__(self, nome, preco, descricao="Um item comum."):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco 

    def __str__(self):
        return f"{self.nome} (Gold: {self.preco}) - {self.descricao}"
    
    def to_dict(self):
        return {
            "__class__": self.__class__.__name__,
            "nome": self.nome,
            "preco": self.preco,
            "descricao": self.descricao
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None

        return cls(data["nome"], data["preco"], data["descricao"])
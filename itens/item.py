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
    
class Consumivel(Item):
    def __init__(self, nome, preco, descricao, efeito_pv=0, efeito_vigor=0, remove_condicao=None):
        super().__init__(nome, preco, descricao)
        self.efeito_pv = efeito_pv
        self.efeito_vigor = efeito_vigor
        self.remove_condicao = remove_condicao

    def usar(self, alvo):
        usado = False
        if self.efeito_pv > 0:
            alvo.vida = min(alvo.vida_max, alvo.vida + self.efeito_pv)
            print(f"{Fore.GREEN} {alvo.nome} usou {self.nome} e recuperou {self.efeito_pv} PV. Vida atual: {alvo.vida}/{alvo.vida_max}{Style.RESET_ALL}")
            usado = True
        
        if self.efeito_vigor > 0:
            alvo.vigor = min(alvo.vigor_max, alvo.vigor + self.efeito_vigor)
            print(f"{Fore.GREEN} {alvo.nome} usou {self.nome} e recuperou {self.efeito_vigor} Vigor. Vigor atual: {alvo.vigor}/{alvo.vigor_max}{Style.RESET_ALL}")
            usado = True

        if self.remove_condicao and self.remove_condicao in alvo.condicoes:
            del alvo.condicoes[self.remove_condicao]
            print(f"{Fore.GREEN} {alvo.nome} usou {self.nome} e removeu a condição {self.remove_condicao}.{Style.RESET_ALL}")
            usado = True
        
        return usado
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "efeito_pv": self.efeito_pv,
            "efeito_vigor": self.efeito_vigor,
            "remove_condicao": self.remove_condicao
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["nome"], data["preco"], data["descricao"], 
            data["efeito_pv"], data["efeito_vigor"], data["remove_condicao"]
        )
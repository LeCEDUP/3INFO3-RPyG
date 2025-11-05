class Pocao(Item):
 
    
    def __init__(self, nome: str, descricao: str, cura: int):
        super().__init__(nome, descricao)
        self.cura = cura
    
    def usar(self) -> int:
        return self.cura

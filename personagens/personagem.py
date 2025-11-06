class Personagem:
    """Classe base para todos os personagens do jogo"""
    
    def __init__(self, nome: str, vida: int, ataque: int, defesa: int):
        self.nome = nome
        self.vida = vida
        self.vida_maxima = vida
        self.ataque = ataque
        self.defesa = defesa
    
    def atacar(self, alvo: 'Personagem') -> int:
        """Calcula o dano e aplica ao alvo"""
        dano = max(0, self.ataque - alvo.defesa + random.randint(-3, 3))
        alvo.receber_dano(dano)
        return dano
    
    def receber_dano(self, dano: int):
        """Reduz a vida do personagem"""
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0
    
    def esta_vivo(self) -> bool:
        """Retorna True se a vida for maior que 0"""
        return self.vida > 0
    
    def curar(self, quantidade: int):
        """Cura o personagem"""
        self.vida = min(self.vida + quantidade, self.vida_maxima)


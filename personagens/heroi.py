from .personagem import Personagem
from itens.arma import Arma
from itens.armadura import Armadura

class Heroi(Personagem):
    """Representa o personagem jogável"""
    
    def __init__(self, nome: str, classe: str = "Aventureiro"):
        super().__init__(nome, vida=100, ataque=15, defesa=5)
        self.nivel = 1
        self.experiencia = 0
        self.inventario: List['Item'] = []
        self.classe = classe
        self.arma_equipada: Optional['Arma'] = None
        self.armadura_equipada: Optional['Armadura'] = None
        self.ouro = 0
    
    def ganhar_experiencia(self, exp: int):
        """Adiciona experiência e verifica se deve subir de nível"""
        self.experiencia += exp
        exp_necessaria = self.nivel * 100
        
        if self.experiencia >= exp_necessaria:
            self.subir_nivel()
    
    def subir_nivel(self):
        """Aumenta o nível e os atributos do herói"""
        self.nivel += 1
        self.vida_maxima += 20
        self.vida = self.vida_maxima
        self.ataque += 5
        self.defesa += 3
        print(f"\n🎉 Parabéns! {self.nome} subiu para o nível {self.nivel}!")
        print(f"Vida: {self.vida_maxima} | Ataque: {self.ataque} | Defesa: {self.defesa}")
    
    def equipar_item(self, item: 'Item'):
        """Equipa um item do inventário"""
        if isinstance(item, Arma):
            if self.arma_equipada:
                self.ataque -= self.arma_equipada.bonus_ataque
            self.arma_equipada = item
            self.ataque += item.bonus_ataque
            print(f"⚔️ {item.nome} equipada! Ataque +{item.bonus_ataque}")
        
        elif isinstance(item, Armadura):
            if self.armadura_equipada:
                self.defesa -= self.armadura_equipada.bonus_defesa
            self.armadura_equipada = item
            self.defesa += item.bonus_defesa
            print(f"🛡️ {item.nome} equipada! Defesa +{item.bonus_defesa}")
    
    def adicionar_item(self, item: 'Item'):
        """Adiciona um item ao inventário"""
        self.inventario.append(item)
        print(f"📦 {item.nome} adicionado ao inventário!")
    
    def usar_pocao(self):
        """Usa uma poção de cura se disponível"""
        for item in self.inventario:
            if isinstance(item, Pocao):
                cura = item.usar()
                self.curar(cura)
                self.inventario.remove(item)
                print(f"💚 Você usou {item.nome} e recuperou {cura} de vida!")
                return True
        print("❌ Você não tem poções!")
        return False
    
    def mostrar_status(self):
        """Exibe o status atual do herói"""
        print(f"\n{'='*50}")
        print(f"👤 {self.nome} - {self.classe} (Nível {self.nivel})")
        print(f"❤️  Vida: {self.vida}/{self.vida_maxima}")
        print(f"⚔️  Ataque: {self.ataque}")
        print(f"🛡️  Defesa: {self.defesa}")
        print(f"⭐ Experiência: {self.experiencia}/{self.nivel * 100}")
        print(f"💰 Ouro: {self.ouro}")
        if self.arma_equipada:
            print(f"🗡️  Arma: {self.arma_equipada.nome}")
        if self.armadura_equipada:
            print(f"🛡️  Armadura: {self.armadura_equipada.nome}")
        print(f"{'='*50}\n")

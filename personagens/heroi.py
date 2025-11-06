from .personagem import Personagem
from itens.arma import Arma
from itens.armadura import Armadura

class Heroi(Personagem):
    def __init__(self, nome, vida_base, ataque_base, defesa_base, mana_base, classe="Lutador"):
        super().__init__(nome, vida_base, ataque_base, defesa_base)
        self.nivel = 1
        self.experiencia = 0
        self.mana_maxima = mana_base
        self.mana = mana_base
        self.classe = classe
        self.habilidades = {}
        self.item_equipado = None

    def ganhar_experiencia(self, exp):
        self.experiencia += exp
        print(f"{self.nome} ganhou {exp} de experiência. Total: {self.experiencia}")
        xp_para_proximo_nivel = self.nivel * 100
        while self.experiencia >= xp_para_proximo_nivel:
            self.subir_nivel()
            xp_para_proximo_nivel = self.nivel * 100

    def subir_nivel(self):
        self.nivel += 1
        print(f"\n** {self.nome} subiu para o NÍVEL {self.nivel}! **")
        self.vida_maxima += 50
        self.vida = self.vida_maxima
        self.ataque += 5
        self.defesa += 2
        self.mana_maxima += 20
        self.mana = self.mana_maxima
        print(f"Status aumentados: Vida Máxima (+50), Ataque (+5), Defesa (+2), Mana Máxima (+20).")

    def equipar_item(self, item):
        if self.item_equipado:
            print(f"Desequipando {self.item_equipado.nome} antes de equipar o novo item.")
            self.item_equipado.remover_bonus(self)
        if isinstance(item, (Arma, Armadura)):
            item.aplicar_bonus(self)
            self.item_equipado = item
            self.inventario.append(item)
        else:
            print(f"Não é possível equipar {item.nome}.")

    def adicionar_habilidade(self, tecla, magia):
        self.habilidades[tecla] = magia
        print(f"Habilidade '{magia.nome}' adicionada à tecla '{tecla}'.")

    def usar_habilidade(self, tecla, alvo):
        if tecla in self.habilidades:
            magia = self.habilidades[tecla]
            return magia.lancar(self, alvo)
        else:
            print(f"Tecla '{tecla}' não corresponde a nenhuma habilidade.")
            return False

    def exibir_status(self):
        super().exibir_status()
        print(f"Nível: {self.nivel} (XP: {self.experiencia}/{self.nivel * 100})")
        print(f"Mana: {self.mana}/{self.mana_maxima}")
        print(f"Classe: {self.classe}")
        print("Habilidades:")
        for tecla, magia in self.habilidades.items():
            print(f"  [{tecla}] {magia.nome}: {magia.descricao} (Custo: {magia.custo_mana})")
        print("-" * 25)
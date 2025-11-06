from mapa.locais import ITENS_LOJA
from .personagem import Personagem
from itens.arma import Arma
from itens.armadura import Armadura

class Heroi(Personagem):
    def __init__(self, nome, vida, ataque, defesa, nivel=1, experiencia=0, inventario=None):
        super().__init__(nome, vida, ataque, defesa)
        self.nivel = nivel
        self.experiencia = experiencia
        self.inventario = inventario if inventario is not None else []

    def ganhar_experiencia(self, exp):
        self.experiencia += exp
        print(f"{self.nome} ganhou {exp} de experiência. Total: {self.experiencia}")
        while self.experiencia >= self.nivel * 100:
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.vida += 20
        self.ataque += 5
        self.defesa += 2
        self.experiencia -= (self.nivel - 1) * 100
        print(f"{self.nome} subiu para o nível {self.nivel}! Seus atributos aumentaram.")

    def equipar_item(self, item):
        if item in self.inventario:
            if isinstance(item, Arma):
                self.ataque += item.bonus_ataque
                print(f"{self.nome} equipou {item.nome}. Ataque atual: {self.ataque}")
            elif isinstance(item, Armadura):
                self.defesa += item.bonus_defesa
                print(f"{self.nome} equipou {item.nome}. Defesa atual: {self.defesa}")
            else:
                print(f"{item.nome} não pode ser equipado.")
        else:
            print(f"{self.nome} não possui {item.nome} no inventário.")


def criar_novo_heroi():
    print(f"\n{Fore.YELLOW}--- CRIAÇÃO DE PERSONAGEM ---{Style.RESET_ALL}")
    nome = input("Digite o nome do seu Herói: ")
    
    subclasses = {
        1: "Mestre do Punho",
        2: "Tanque de Ferro",
        3: "Vento Veloz"
    }
    
    while True:
        print("\nEscolha sua Subclasse:")
        print("1. Mestre do Punho (Equilibrado, Foco em Dano)")
        print("2. Tanque de Ferro (Alto PV/Defesa, Foco em Sobrevivência)")
        print("3. Vento Veloz (Alto Vigor/Velocidade, Foco em Agilidade)")
        
        escolha = input("Opção: ")
        if escolha.isdigit() and int(escolha) in subclasses:
            subclasse = subclasses[int(escolha)]
            break
        else:
            print("Escolha inválida.")
            
    heroi = GuerreiroDoPunho(nome, subclasse)
    heroi.escolher_talento()
    
    save_game(heroi, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})
    
    return heroi
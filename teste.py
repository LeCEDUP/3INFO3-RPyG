from itens.item import Item
from itens.arma import Arma
from itens.armadura import Armadura
from personagens.heroi import Heroi
from personagens.monstro import Monstro


# Criando personagens
heroi = Heroi("Arthur", 100, 15, 5)
goblin = Monstro("Goblin", 30, 8, 2, "Pequeno")
dragao = Monstro("Dragão", 200, 30, 10, "Grande")

# Criando itens
espada = Arma("Espada Longa", "Uma espada afiada.", 10)
escudo = Armadura("Escudo de Ferro", "Um escudo resistente.", 5)
pocao_vida = Item("Poção de Vida", "Restaura 30 de vida.")

print("--- Início da Aventura ---")

# Herói encontra um item
heroi.inventario.append(espada)
heroi.inventario.append(escudo)
heroi.inventario.append(pocao_vida)
print(f"{heroi.nome} encontrou uma {espada.nome}, um {escudo.nome} e uma {pocao_vida.nome}.")

# Herói equipa itens
heroi.equipar_item(espada)
heroi.equipar_item(escudo)

print("\n--- Batalha contra o Goblin ---")
while heroi.esta_vivo() and goblin.esta_vivo():
    heroi.atacar(goblin)
    if goblin.esta_vivo():
        goblin.atacar(heroi)

if heroi.esta_vivo():
    print(f"{heroi.nome} derrotou o {goblin.nome}!")
    heroi.ganhar_experiencia(50)
    print(f"Vida de {heroi.nome}: {heroi.vida}")
    print(f"Inventário de {heroi.nome}: {[item.nome for item in heroi.inventario]}")

print("\n--- Herói usa poção ---")
if pocao_vida in heroi.inventario:
    heroi.vida += 30
    heroi.inventario.remove(pocao_vida)
    print(f"{heroi.nome} usou {pocao_vida.nome}. Vida atual: {heroi.vida}")

print("\n--- Batalha contra o Dragão (Desafio Final) ---")
while heroi.esta_vivo() and dragao.esta_vivo():
    heroi.atacar(dragao)
    if dragao.esta_vivo():
        dragao.atacar(heroi)

if heroi.esta_vivo():
    print(f"\nParabéns, {heroi.nome}! Você derrotou o {dragao.nome} e salvou o reino!")
    heroi.ganhar_experiencia(200)
else:
    print(f"\n{heroi.nome} foi derrotado pelo {dragao.nome}. Fim de jogo.")

print("\n--- Fim da Aventura ---")
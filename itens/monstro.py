import random

class Monstro:
    def __init__(self, nome, vida, ataque, defesa, tamanho, nivel):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.tamanho = tamanho
        self.nivel = nivel

    def esta_vivo(self):
        return self.vida > 0

# Monstros por nível
monstros_baixa = [
    Monstro("Goblin", 30, 12, 5, "Pequeno", "Baixa"),
    Monstro("Rato Gigante", 25, 10, 4, "Pequeno", "Baixa"),
    Monstro("Lobo Selvagem", 35, 14, 6, "Médio", "Baixa"),
    Monstro("Esqueleto", 28, 11, 5, "Médio", "Baixa"),
    Monstro("Aranha Gigante", 32, 13, 5, "Pequeno", "Baixa"),
]

monstros_media = [
    Monstro("Orc Guerreiro", 60, 20, 15, "Médio", "Média"),
    Monstro("Troll Jovem", 75, 23, 18, "Grande", "Média"),
    Monstro("Mago Sombrio", 55, 25, 12, "Médio", "Média"),
    Monstro("Kobold Arqueiro", 68, 22, 17, "Médio", "Média"),
    Monstro("Ciclope", 70, 27, 20, "Grande", "Média"),
]

monstros_alta = [
    Monstro("Dragão Ancião", 350, 50, 40, "Enorme", "Alta"),
    Monstro("Grim Reaper", 180, 35, 30, "Médio", "Alta"),
    Monstro("Gigante das Montanhas", 220, 48, 35, "Enorme", "Alta"),
    Monstro("Cavaleiro Negro", 300, 52, 33, "Grande", "Alta"),
    Monstro("Behemoth", 410, 55, 38, "Grande", "Alta"),
]

# Função para gerar grupo de monstros
def gerar_grupo_monstros(monstro_base, quantidade):
    return [Monstro(monstro_base.nome, monstro_base.vida, monstro_base.ataque,
                    monstro_base.defesa, monstro_base.tamanho, monstro_base.nivel)
            for _ in range(quantidade)]

# Função de spawn que considera nível do jogador e categoria dos monstros
def spawnar_monstros_por_nivel(nivel_jogador, nivel_monstro):
    if nivel_monstro == "Baixa":
        return [gerar_grupo_monstros(m, 3) for m in monstros_baixa]
    elif nivel_monstro == "Média":
        return monstros_media
    elif nivel_monstro == "Alta":
        if nivel_jogador >= 5:
            return [random.choice(monstros_alta)]
        else:
            return []
    else:
        return []

# Teste da funcionalidade
def main():
    nivel_jogador = 5

    grupos_baixa = spawnar_monstros_por_nivel(nivel_jogador, "Baixa")
    monstros_media = spawnar_monstros_por_nivel(nivel_jogador, "Média")
    monstros_alta = spawnar_monstros_por_nivel(nivel_jogador, "Alta")

    print("Grupos de monstros baixos:")
    for grupo in grupos_baixa:
        print(", ".join(m.nome for m in grupo))

    print("\nMonstros de nível médio:")
    for monstro in monstros_media:
        print(monstro.nome)

    print("\nMonstros de nível alto (se elegível):")
    for monstro in monstros_alta:
        print(monstro.nome)

if __name__ == "__main__":
    main()
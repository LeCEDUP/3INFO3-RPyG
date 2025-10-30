
import json

class Personagem:
    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque
        self.defesa = defesa
        self.status_effects = []

    def adicionar_status(self, efeito):
        """Adiciona um novo efeito ou renova um existente."""
        # Se já tiver o efeito, você pode optar por renovar a duração
        for s in self.status_effects:
            if s.nome == efeito.nome:
                s.duracao_restante = efeito.duracao_restante # Renovando
                return f"{self.nome} já estava sob efeito de {efeito.nome}. Duração renovada."
        
        self.status_effects.append(efeito)
        return f"{self.nome} agora está sob efeito de {efeito.nome}!"

    def processar_efeitos_de_status(self):
        """Chamado no início de cada turno."""
        mensagens = []
        efeitos_a_remover = []

        for efeito in self.status_effects:
            # Aplica o dano/efeito do status
            mensagem_dano = efeito.aplicar_efeito(self)
            
            if mensagem_dano:
                mensagens.append(mensagem_dano)
            
            # Verifica se o efeito terminou
            if efeito.duracao_restante <= 0:
                efeitos_a_remover.append(efeito)
                mensagens.append(f"O efeito de {efeito.nome} em {self.nome} terminou.")

        # Remove os efeitos terminados
        for efeito in efeitos_a_remover:
            self.status_effects.remove(efeito)
            
        return mensagens
        
    def esta_vivo(self):
        return self.vida > 0

    def get_status_info(self):
        if not self.status_effects:
            return "Nenhum status ativo."
        return "Ativo: " + ", ".join([str(s) for s in self.status_effects])

    def atacar(self, alvo):
        dano = max(0, self.ataque - alvo.defesa)
        alvo.receber_dano(dano)
        return dano

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

    def esta_vivo(self):
        return self.vida > 0

class Item:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

class Arma(Item):
    def __init__(self, nome, descricao, bonus_ataque):
        super().__init__(nome, descricao)
        self.bonus_ataque = bonus_ataque

# --- CLASSES DE STATUS (NOVAS) ---
class StatusEffect:
    def __init__(self, nome, duracao, dano_por_turno, tipo):
        self.nome = nome
        self.duracao_restante = duracao
        self.dano_por_turno = dano_por_turno
        self.tipo = tipo # Para fácil identificação

    def aplicar_efeito(self, alvo):
        """Aplica o dano/efeito do status no alvo."""
        if self.duracao_restante > 0:
            dano = self.dano_por_turno
            alvo.vida -= dano
            self.duracao_restante -= 1
            return f"{alvo.nome} sofre {dano} de dano por {self.nome}."
        return None # Efeito não aplicado (durou 0 ou foi removido)

    def __str__(self):
        return f"{self.nome} (Dano: {self.dano_por_turno}, Turnos: {self.duracao_restante})"

class Sangramento(StatusEffect):
    def __init__(self, duracao=4, dano_base=5):
        # Sangramento: Dano físico por turno.
        super().__init__("Sangramento", duracao, dano_base, "Dano por Turno")

class Queimadura(StatusEffect):
    def __init__(self, duracao=3, dano_base=7):
        # Queimadura: Dano maior por turno.
        super().__init__("Queimadura", duracao, dano_base, "Dano por Turno")
        
class Envenenamento(StatusEffect):
    def __init__(self, duracao=5, dano_base=3):
        # Envenenamento: Dano menor, mas mais duradouro.
        super().__init__("Envenenamento", duracao, dano_base, "Dano por Turno")

# --- FIM DAS CLASSES DE STATUS ---

class Armadura(Item):
    def __init__(self, nome, descricao, bonus_defesa):
        super().__init__(nome, descricao)
        self.bonus_defesa = bonus_defesa
        
class Antidoto(Item):
    def __init__(self):
        super().__init__("Poção de Antídoto", "Remove efeitos de Envenenamento e Sangramento/Queimadura leves.")
        
    def usar(self, heroi):
        removidos = []
        
        # Cria uma lista de status para remover
        efeitos_a_remover = [
            s for s in heroi.status_effects 
            if isinstance(s, Envenenamento) or isinstance(s, Sangramento) or isinstance(s, Queimadura)
        ]

        if not efeitos_a_remover:
            return f"{heroi.nome} usou a Poção de Antídoto, mas não havia status negativos para remover."
            
        for efeito in efeitos_a_remover:
            heroi.status_effects.remove(efeito)
            removidos.append(efeito.nome)

        return f"{heroi.nome} usou a Poção de Antídoto! Status removidos: {', '.join(removidos)}. Sentindo-se melhor!"
    
class Heroi(Personagem):
    def __init__(self, nome, vida, ataque, defesa, classe):
        super().__init__(nome, vida, ataque, defesa)
        self.classe = classe
        self.nivel = 1
        self.experiencia = 0
        self.inventario = [] # Itens não equipados
        self.arma_equipada = None
        self.armadura_equipada = None
        self.hp_max = vida # Adicionado para garantir que hp_max seja inicializado

    def ganhar_experiencia(self, exp):
        self.experiencia += exp
        print(f"{self.nome} ganhou {exp} de experiência!")
        while self.experiencia >= self.nivel * 100: # Exemplo simples de XP para subir de nível
            self.experiencia -= self.nivel * 100
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.vida_max += 20
        self.vida = self.vida_max # Cura total ao subir de nível
        self.ataque += 5
        self.defesa += 3
        print(f"PARABÉNS! {self.nome} subiu para o nível {self.nivel}!")

    def equipar_item(self, item):
        if not isinstance(item, (Arma, Armadura)): # Só pode equipar Arma ou Armadura
            print(f"{item.nome} não pode ser equipado.")
            return

        if item not in self.inventario: # Item precisa estar no inventário para ser equipado
            print(f"{item.nome} não está no seu inventário para ser equipado.")
            return

        if isinstance(item, Arma):
            if self.arma_equipada: # Se já tem uma arma equipada, devolve para o inventário
                self.ataque -= self.arma_equipada.bonus_ataque
                self.inventario.append(self.arma_equipada) # Adiciona a arma antiga de volta ao inventário
                print(f"{self.arma_equipada.nome} foi desequipado e voltou para o inventário.")
            
            self.arma_equipada = item
            self.ataque += item.bonus_ataque
            self.inventario.remove(item) # Remove o item recém-equipado do inventário
            print(f"{self.nome} equipou {item.nome} (Ataque: +{item.bonus_ataque}).")

        elif isinstance(item, Armadura):
            if self.armadura_equipada: # Se já tem uma armadura equipada, devolve para o inventário
                self.defesa -= self.armadura_equipada.bonus_defesa
                self.inventario.append(self.armadura_equipada) # Adiciona a armadura antiga de volta ao inventário
                print(f"{self.armadura_equipada.nome} foi desequipado e voltou para o inventário.")

            self.armadura_equipada = item
            self.defesa += item.bonus_defesa
            self.inventario.remove(item) # Remove o item recém-equipado do inventário
            print(f"{self.nome} equipou {item.nome} (Defesa: +{item.bonus_defesa}).")

    def adicionar_ao_inventario(self, item):
        self.inventario.append(item)
        print(f"{item.nome} adicionado ao inventário de {self.nome}.")

    def usar_item(self, item_nome):
        for item in list(self.inventario): # Itera sobre uma cópia para permitir remoção durante a iteração
            if item.nome.lower() == item_nome.lower():
                if isinstance(item, Arma) or isinstance(item, Armadura):
                    self.equipar_item(item) # equipar_item já remove do inventário
                    return True
                elif isinstance(item, Item) and "Poção" in item.nome: # Exemplo: Poções de cura
                    if "Cura Menor" in item.nome:
                        cura = 20
                    elif "Cura Média" in item.nome:
                        cura = 50
                    else:
                        cura = 0 # Outras poções sem efeito de cura

                    if cura > 0:
                        self.vida = min(self.vida_max, self.vida + cura)
                        self.inventario.remove(item)
                        print(f"{self.nome} usou {item.nome} e recuperou {cura} de HP. HP atual: {self.vida}/{self.vida_max}")
                        return True
                    else:
                        print(f"{item.nome} não tem um efeito de uso direto neste momento.")
                        return False
                else:
                    print(f"{item.nome} não é um item utilizável ou equipável.")
                    return False
        print(f"Item \'{item_nome}\' não encontrado no inventário.")
        return False

class Monstro(Personagem):
    def __init__(self, nome, vida, ataque, defesa, tipo):
        super().__init__(nome, vida, ataque, defesa)
        self.tipo = tipo

# --- Funções do Jogo ---

def linha():
    print("-" * 40)

def escolher_classe():
    print("Escolha sua classe:")
    print("1 - Guerreiro (Foco em Ataque e Defesa)")
    print("2 - Mago (Foco em Ataque, menor Defesa)")
    print("3 - Ladino (Foco em Ataque, maior velocidade)")
    escolha = input("Digite o número da classe: ")

    if escolha == "1":
        return "Guerreiro", 100, 15, 10 # Vida, Ataque, Defesa
    elif escolha == "2":
        return "Mago", 80, 20, 5
    elif escolha == "3":
        return "Ladino", 90, 18, 8
    else:
        print("Opção inválida! Você será um Guerreiro.")
        return "Guerreiro", 100, 15, 10

def menu_acao(heroi):
    print("\nO que deseja fazer?")
    print("1 - Atacar")
    print("2 - Usar Habilidade Especial")
    print("3 - Usar Item")
    print("4 - Ver Inventário")
    print("5 - Fugir")
    return input("Escolha: ")

def combate(heroi, inimigo):
    cura_usada = False
    print(f"\n!!! {heroi.nome} o {heroi.classe} entra em batalha contra um {inimigo.nome} ({inimigo.tipo}) !!!")

    while heroi.esta_vivo() and inimigo.esta_vivo():
        linha()
        print(f"HP de {heroi.nome}: {heroi.vida}/{heroi.vida_max} | HP do {inimigo.nome}: {inimigo.vida}/{inimigo.vida_max}")
        print(f"Ataque: {heroi.ataque} | Defesa: {heroi.defesa}")

        acao = menu_acao(heroi)

        if acao == "1":  # ataque normal
            dano_causado = heroi.atacar(inimigo)
            print(f"Você atacou com sua {heroi.arma_equipada.nome if heroi.arma_equipada else 'mãos'} e causou {dano_causado} de dano em {inimigo.nome}!")

        elif acao == "2":  # habilidade especial (simplificada)
            dano_extra = 0
            if heroi.classe == "Guerreiro":
                dano_extra = 8
                print("Você usou Golpe Poderoso!")
            elif heroi.classe == "Mago":
                dano_extra = 10
                print("Você lançou uma Bola de Fogo!")
            elif heroi.classe == "Ladino":
                dano_extra = 6
                print("Você aplicou um Golpe Rápido e preciso!")
            
            dano_habilidade = max(0, (heroi.ataque + dano_extra) - inimigo.defesa)
            inimigo.receber_dano(dano_habilidade)
            print(f"O inimigo recebeu {dano_habilidade} de dano da sua habilidade!")

        elif acao == "3": # Usar Item
            if not heroi.inventario:
                print("Seu inventário está vazio!")
                continue
            print("Itens no seu inventário:")
            for i, item in enumerate(heroi.inventario):
                print(f"{i+1}. {item.nome} - {item.descricao}")
            item_escolhido = input("Digite o nome do item que deseja usar (ou 'cancelar'): ")
            if item_escolhido.lower() == 'cancelar':
                continue
            heroi.usar_item(item_escolhido)

        elif acao == "4": # Ver Inventário
            if not heroi.inventario:
                print("Seu inventário está vazio.")
            else:
                print("--- Inventário ---")
                for item in heroi.inventario:
                    print(f"- {item.nome}: {item.descricao}")
                if heroi.arma_equipada:
                    print(f"Arma Equipada: {heroi.arma_equipada.nome} (Ataque +{heroi.arma_equipada.bonus_ataque})")
                if heroi.armadura_equipada:
                    print(f"Armadura Equipada: {heroi.armadura_equipada.nome} (Defesa +{heroi.armadura_equipada.bonus_defesa})")
                print("------------------")
            continue # Não consome turno

        elif acao == "5":
            print("Você fugiu da batalha!")
            return False

        else:
            print("Ação inválida! Tente novamente.")
            continue # Não consome turno

        # Turno do inimigo
        if inimigo.esta_vivo():
            dano_inimigo_causado = inimigo.atacar(heroi)
            print(f"O {inimigo.nome} atacou e causou {dano_inimigo_causado} de dano em {heroi.nome}!")

    if not heroi.esta_vivo():
        print("Você foi derrotado!")
        return False
    else:
        print(f"Você derrotou o {inimigo.nome}!")
        heroi.ganhar_experiencia(inimigo.vida_max // 2) # Ganha XP baseado na vida do monstro
        return True

def salvar_jogo(heroi, filename="savegame.json"):
    data = {
        "nome": heroi.nome,
        "classe": heroi.classe,
        "vida": heroi.vida,
        "vida_max": heroi.vida_max,
        "ataque": heroi.ataque,
        "defesa": heroi.defesa,
        "nivel": heroi.nivel,
        "experiencia": heroi.experiencia,
        "inventario": [{
            "nome": item.nome,
            "descricao": item.descricao,
            "bonus_ataque": item.bonus_ataque if isinstance(item, Arma) else None,
            "bonus_defesa": item.bonus_defesa if isinstance(item, Armadura) else None,
            "tipo": "Arma" if isinstance(item, Arma) else ("Armadura" if isinstance(item, Armadura) else "Item")
        } for item in heroi.inventario if item is not None], # Garante que não há None no inventário
        "arma_equipada": {
            "nome": heroi.arma_equipada.nome,
            "descricao": heroi.arma_equipada.descricao,
            "bonus_ataque": heroi.arma_equipada.bonus_ataque,
            "tipo": "Arma"
        } if heroi.arma_equipada else None,
        "armadura_equipada": {
            "nome": heroi.armadura_equipada.nome,
            "descricao": heroi.armadura_equipada.descricao,
            "bonus_defesa": heroi.armadura_equipada.bonus_defesa,
            "tipo": "Armadura"
        } if heroi.armadura_equipada else None,
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print("Jogo salvo com sucesso!")

def carregar_jogo(filename="savegame.json"):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        heroi = Heroi(data["nome"], data["vida_max"], data["ataque"], data["defesa"], data["classe"])
        heroi.vida = data["vida"]
        heroi.nivel = data["nivel"]
        heroi.experiencia = data["experiencia"]

        heroi.inventario = []
        for item_data in data["inventario"]:
            if item_data["tipo"] == "Arma":
                heroi.inventario.append(Arma(item_data["nome"], item_data["descricao"], item_data["bonus_ataque"]))
            elif item_data["tipo"] == "Armadura":
                heroi.inventario.append(Armadura(item_data["nome"], item_data["descricao"], item_data["bonus_defesa"]))
            else:
                heroi.inventario.append(Item(item_data["nome"], item_data["descricao"]))
        
        if data["arma_equipada"]:
            heroi.arma_equipada = Arma(data["arma_equipada"]["nome"], data["arma_equipada"]["descricao"], data["arma_equipada"]["bonus_ataque"])
            heroi.ataque += heroi.arma_equipada.bonus_ataque # Restaura o bônus de ataque
        if data["armadura_equipada"]:
            heroi.armadura_equipada = Armadura(data["armadura_equipada"]["nome"], data["armadura_equipada"]["descricao"], data["armadura_equipada"]["bonus_defesa"])
            heroi.defesa += heroi.armadura_equipada.bonus_defesa # Restaura o bônus de defesa

        print("Jogo carregado com sucesso!")
        return heroi
    except FileNotFoundError:
        print("Nenhum jogo salvo encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao carregar jogo: {e}")
        return None

def main():
    print("=== RPG SIMPLES ===")
    heroi = None

    while True:
        print("\n1 - Novo Jogo")
        print("2 - Carregar Jogo")
        print("3 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome do seu herói: ")
            classe_nome, hp, ataque, defesa = escolher_classe()
            heroi = Heroi(nome, hp, ataque, defesa, classe_nome)
            
            # Itens iniciais
            if heroi.classe == "Guerreiro":
                heroi.adicionar_ao_inventario(Arma("Espada Curta", "Uma espada simples, mas eficaz.", 5))
                heroi.adicionar_ao_inventario(Armadura("Armadura de Couro", "Uma armadura leve.", 2))
            elif heroi.classe == "Mago":
                heroi.adicionar_ao_inventario(Arma("Cajado de Aprendiz", "Um cajado para iniciantes.", 7))
                heroi.adicionar_ao_inventario(Item("Poção de Cura Menor", "Restaura 20 de HP."))
            elif heroi.classe == "Ladino":
                heroi.adicionar_ao_inventario(Arma("Adaga Afiada", "Uma adaga rápida e letal.", 6))
                heroi.adicionar_ao_inventario(Item("Cura Média", "Restaura 50 de HP."))
            
            # Define os itens iniciais para cada classe
            initial_items = []
            if heroi.classe == "Guerreiro":
                initial_items.append(Arma("Espada Curta", "Uma espada simples, mas eficaz.", 5))
                initial_items.append(Armadura("Armadura de Couro", "Uma armadura leve.", 3))
                initial_items.append(Item("Poção de Cura Menor", "Restaura 20 de HP."))
            elif heroi.classe == "Mago":
                initial_items.append(Arma("Cajado de Aprendiz", "Um cajado para iniciantes.", 7))
                initial_items.append(Armadura("Chapél de pano", "Um chapel simples", 1))
                initial_items.append(Item("Poção de Cura Média", "Restaura 50 de HP."))
            elif heroi.classe == "Ladino":
                initial_items.append(Arma("Adaga Afiada", "Uma adaga rápida e letal.", 6))
                initial_items.append(Armadura("Manto de seda", "Uma capa leve", 1))
                initial_items.append(Item("Poção de Agilidade", "Aumenta temporariamente a velocidade."))
            
            # Adiciona e equipa os itens iniciais
            for item in initial_items:
                if isinstance(item, Arma) or isinstance(item, Armadura):
                    # Se for um item equipável, tenta equipar diretamente
                    if (isinstance(item, Arma) and not heroi.arma_equipada) or \
                       (isinstance(item, Armadura) and not heroi.armadura_equipada):
                        # Adiciona temporariamente ao inventário para que equipar_item possa encontrá-lo e removê-lo
                        heroi.inventario.append(item)
                        heroi.equipar_item(item)
                    else:
                        heroi.adicionar_ao_inventario(item) # Se já tiver um equipado, adiciona ao inventário
                else:
                    heroi.adicionar_ao_inventario(item) # Itens não equipáveis vão direto para o inventário

            break

        elif opcao == "2":
            heroi = carregar_jogo()
            if heroi:
                break
        elif opcao == "3":
            print("Saindo do jogo. Até a próxima!")
            return
        else:
            print("Opção inválida.")

    if not heroi:
        print("Erro ao iniciar ou carregar herói.")
        return

    # Inimigo fixo para teste
    inimigo1 = Monstro("Lobo", 40, 8, 5, "Pequeno")
    inimigo2 = Monstro("Goblin", 60, 11, 7, "Grande")
    inimigo3 = Monstro("Aranha", 70, 13, 8, "Grande")
    inimigo4 = Monstro("Orc", 80, 15, 8, "Grande")
    inimigo5 = Monstro("Dragão Jovem", 150, 25, 12, "Chefe")

    inimigos = [inimigo1, inimigo2, inimigo3, inimigo4, inimigo5]
    
    for i, inimigo in enumerate(inimigos):
        if heroi.esta_vivo():
            print(f"\n--- Encontro {i+1} ---")
            if combate(heroi, inimigo):
                print(f"{heroi.nome} venceu o {inimigo.nome}!")
                salvar_jogo(heroi) # Salva após cada vitória
            else:
                print(f"{heroi.nome} foi derrotado ou fugiu. Fim de jogo.")
                break
        else:
            break

    if heroi.esta_vivo():
        print("\nParabéns! Você venceu todos os inimigos!")
        print("Fim do jogo!")

if __name__ == "__main__":
    main()
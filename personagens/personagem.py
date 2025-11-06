class Personagem:
    def __init__(self, nome, vida, vigor_max, ataque, defesa, velocidade, nivel=1):
        self.nome = nome
        self.vida_max = vida
        self.vida = vida
        self.vigor_max = vigor_max
        self.vigor = vigor_max
        self.ataque_base = ataque
        self.defesa_base = defesa
        self.velocidade_base = velocidade
        self.nivel = nivel
        self.condicoes = {} 
        self.habilidades = []

    def esta_vivo(self):
        return self.vida > 0

    def get_ataque_total(self):
        return self.ataque_base

    def get_defesa_total(self):
        return self.defesa_base

    def get_velocidade_total(self):
        return self.velocidade_base
    
    def atacar(self, alvo, habilidade=None):
        if 'Atordoado' in self.condicoes:
            print(f"{Fore.YELLOW}{self.nome} está Atordoado e não pode agir!{Style.RESET_ALL}")
            return False

        if habilidade:
            custo_vigor_final = habilidade.custo_vigor
            
            if isinstance(self, GuerreiroDoPunho):
                if self.talento == "Vigor Incansável":
                    custo_vigor_final = int(habilidade.custo_vigor * 0.9)

            if self.vigor < custo_vigor_final:
                print(f"{Fore.RED}{self.nome} não tem Vigor suficiente para usar {habilidade.nome}!{Style.RESET_ALL}")
                return False

            self.vigor -= custo_vigor_final
            dano_bruto = habilidade.dano_base + (self.get_ataque_total() * 0.5)
            
            if isinstance(self, GuerreiroDoPunho):
                if 'Atordoado' in alvo.condicoes:
                    self.karma = max(-100, self.karma - 5)
                    print(f"{Fore.RED} {self.nome} atacou um alvo Atordoado. Karma reduzido para {self.karma}.{Style.RESET_ALL}")

                if self.talento == "Poder Focado":
                    dano_bruto += habilidade.dano_base * 0.1

            print(f"{Fore.CYAN} {self.nome} usa {habilidade.nome}!{Style.RESET_ALL}")
        else:
            vigor_gerado = 5
            self.vigor = min(self.vigor_max, self.vigor + vigor_gerado)
            dano_bruto = self.get_ataque_total() * 0.75
            print(f" {self.nome} desfere um {Fore.GREEN}Ataque Básico{Style.RESET_ALL} e gera {vigor_gerado} Vigor.")

        dano_final = max(1, int(dano_bruto - (alvo.get_defesa_total() * 0.5)))
        alvo.receber_dano(dano_final, self)
        return True

    def receber_dano(self, dano, atacante):
        if 'Bloqueio de Guarda' in self.condicoes:
            dano = int(dano * 0.5)
            print(f"{Fore.BLUE}Dano reduzido pela metade devido ao Bloqueio de Guarda!{Style.RESET_ALL}")

        self.vida -= dano
        print(f"{Fore.RED}{self.nome} recebeu {dano} de dano. Vida restante: {self.vida}/{self.vida_max}{Style.RESET_ALL}")
        
        if isinstance(self, GuerreiroDoPunho) and self.esta_vivo():
            habilidade_contra = next((h for h in self.habilidades if h.nome == "Contra-Ataque"), None)
            if habilidade_contra and self.vigor >= habilidade_contra.custo_vigor and dano > 0 and random.random() < 0.5: 
                self.vigor -= habilidade_contra.custo_vigor
                dano_contra = habilidade_contra.dano_base + (self.get_ataque_total() * 0.75)
                print(f"{Fore.YELLOW} {self.nome} REVIDA com Contra-Ataque!{Style.RESET_ALL}")
                atacante.receber_dano(int(dano_contra), self)
                
        if not self.esta_vivo():
            print(f"{Fore.RED} {self.nome} foi derrotado!{Style.RESET_ALL}")

    def aplicar_condicao(self, condicao, duracao):
        if isinstance(self, GuerreiroDoPunho) and self.talento == "Mente Clara" and condicao in ["Sangramento", "Veneno", "Queimadura"]:
            if random.random() < 0.5: 
                print(f"{Fore.CYAN} {self.nome} resistiu à condição {condicao} devido ao Talento Mente Clara!{Style.RESET_ALL}")
                return

        self.condicoes[condicao] = duracao
        print(f"{Fore.YELLOW} {self.nome} agora está sob a condição: {condicao} por {duracao} turno(s).{Style.RESET_ALL}")

    def processar_condicoes(self):
        condicoes_para_remover = []
        for condicao, duracao in list(self.condicoes.items()):
            if condicao == 'Sangramento':
                dano_sangramento = int(self.vida_max * 0.05)
                self.vida -= dano_sangramento
                print(f"{Fore.RED} {self.nome} sofre dano de Sangramento: {dano_sangramento}. Vida restante: {self.vida}/{self.vida_max}{Style.RESET_ALL}")
                if not self.esta_vivo():
                    break
            
            elif condicao == 'Veneno':
                dano_veneno = int(self.vida_max * 0.03)
                self.vida -= dano_veneno
                print(f"{Fore.MAGENTA} {self.nome} sofre dano de Veneno: {dano_veneno}. Vida restante: {self.vida}/{self.vida_max}{Style.RESET_ALL}")
                if not self.esta_vivo():
                    break
            
            elif condicao == 'Queimadura':
                dano_queimadura = int(self.vida_max * 0.04)
                self.vida -= dano_queimadura
                print(f"{Fore.RED} {self.nome} sofre dano de Queimadura: {dano_queimadura}. Vida restante: {self.vida}/{self.vida_max}{Style.RESET_ALL}")
                if not self.esta_vivo():
                    break
            
            elif condicao == 'Atordoado':
                print(f"{Fore.YELLOW} {self.nome} está Atordoado e perde o turno.{Style.RESET_ALL}")
            
            elif condicao == 'Bloqueio de Guarda':
                pass 

            self.condicoes[condicao] -= 1
            if self.condicoes[condicao] <= 0:
                condicoes_para_remover.append(condicao)

        for condicao in condicoes_para_remover:
            del self.condicoes[condicao]
            print(f"{Fore.GREEN} Condição {condicao} removida de {self.nome}.{Style.RESET_ALL}")

    def recuperar_vigor_turno(self):
        recuperacao = 10
        if isinstance(self, GuerreiroDoPunho) and self.talento == "Vigor Incansável":
            recuperacao += 5
        
        self.vigor = min(self.vigor_max, self.vigor + recuperacao)
        print(f"{Fore.BLUE} {self.nome} recuperou {recuperacao} Vigor. Vigor atual: {self.vigor}/{self.vigor_max}{Style.RESET_ALL}")

    def to_dict(self):
        return {
            "__class__": self.__class__.__name__,
            "nome": self.nome,
            "vida_max": self.vida_max,
            "vida": self.vida,
            "vigor_max": self.vigor_max,
            "vigor": self.vigor,
            "ataque_base": self.ataque_base,
            "defesa_base": self.defesa_base,
            "velocidade_base": self.velocidade_base,
            "nivel": self.nivel,
            "condicoes": self.condicoes,
            "habilidades": [h.to_dict() for h in self.habilidades]
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(
            data["nome"], data["vida_max"], data["vigor_max"], 
            data["ataque_base"], data["defesa_base"], data["velocidade_base"], 
            data["nivel"]
        )
        instance.vida = data["vida"]
        instance.vigor = data["vigor"]
        instance.condicoes = data["condicoes"]
        instance.habilidades = [deserialize_object(h_data) for h_data in data["habilidades"]]
        return instance


class GuerreiroDoPunho(Personagem):
    def __init__(self, nome, subclasse, nivel=1):
        stats = {
            "Mestre do Punho": {"vida": 120, "vigor": 100, "ataque": 20, "defesa": 15, "velocidade": 15},
            "Tanque de Ferro": {"vida": 150, "vigor": 80, "ataque": 15, "defesa": 25, "velocidade": 10},
            "Vento Veloz": {"vida": 100, "vigor": 120, "ataque": 18, "defesa": 10, "velocidade": 25}
        }
        
        base = stats.get(subclasse, stats["Mestre do Punho"])
        
        super().__init__(nome, base["vida"], base["vigor"], base["ataque"], base["defesa"], base["velocidade"], nivel)
        
        self.subclasse = subclasse
        self.experiencia = 0
        self.exp_para_proximo_nivel = 100
        self.talento = None
        self.gold = 0
        self.pontos_treinamento = 0
        self.missoes_completas = []
        self.missao_ativa = None
        self.karma = 0 
        self.usos_foco_vigor = 1 
        
        self.inventario = []
        self.equipamento = {"luva": None, "armadura": None, "acessorio": None}
        
        self.habilidades.append(Habilidade("Jab Rápido", 0, 10, "Ataque rápido que não custa vigor."))
        self.habilidades.append(Habilidade("Contra-Ataque", 20, 40, "Habilidade de Reação: Causa dano massivo após ser atacado (Requer 20 Vigor)."))
        
        if subclasse == "Mestre do Punho":
            self.habilidades.append(Habilidade("Gancho Poderoso", 30, 30, "Alto dano, 30% de chance de Atordoar (1 turno)."))
        elif subclasse == "Tanque de Ferro":
            self.habilidades.append(Habilidade("Bloqueio de Guarda", 15, 0, "Reduz o próximo dano recebido pela metade (Ação de 1 turno)."))
        elif subclasse == "Vento Veloz":
            self.habilidades.append(Habilidade("Soco no Corpo", 20, 20, "Dano moderado, reduz o Vigor Máximo do alvo em 5."))

    def get_ataque_total(self):
        bonus = sum(item.bonus_ataque for item in self.equipamento.values() if item)
        return self.ataque_base + bonus

    def get_defesa_total(self):
        bonus = sum(item.bonus_defesa for item in self.equipamento.values() if item)
        return self.defesa_base + bonus

    def get_velocidade_total(self):
        bonus = sum(item.bonus_velocidade for item in self.equipamento.values() if item)
        return self.velocidade_base + bonus

    def ganhar_experiencia(self, exp):
        self.experiencia += exp
        print(f"{Fore.CYAN}Você ganhou {exp} de Experiência!{Style.RESET_ALL}")
        
        while self.experiencia >= self.exp_para_proximo_nivel:
            self.nivel += 1
            self.experiencia -= self.exp_para_proximo_nivel
            self.exp_para_proximo_nivel = int(self.exp_para_proximo_nivel * 1.5)
            self.vida_max += 10
            self.vida = self.vida_max
            self.vigor_max += 5
            self.vigor = self.vigor_max
            self.ataque_base += 2
            self.defesa_base += 2
            self.velocidade_base += 2
            self.pontos_treinamento += 3
            print(f"\n{Fore.YELLOW}*** PARABÉNS! VOCÊ SUBIU PARA O NÍVEL {self.nivel}! ***{Style.RESET_ALL}")
            print(f"Você ganhou 3 Pontos de Treinamento!")
            
            save_game(self, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})

    def equipar_item(self, item):
        if item.slot in self.equipamento:
            if self.equipamento[item.slot]:
                self.inventario.append(self.equipamento[item.slot])
            self.equipamento[item.slot] = item
            self.inventario.remove(item)
            print(f"{Fore.GREEN} {item.nome} equipado no slot {item.slot.capitalize()}.{Style.RESET_ALL}")
            return True
        return False

    def desequipar_item(self, slot):
        if slot in self.equipamento and self.equipamento[slot]:
            item = self.equipamento[slot]
            self.inventario.append(item)
            self.equipamento[slot] = None
            print(f"{Fore.YELLOW} {item.nome} desequipado do slot {slot.capitalize()}.{Style.RESET_ALL}")
            return True
        return False

    def usar_consumivel(self, indice):
        if 0 <= indice < len(self.inventario):
            item = self.inventario[indice]
            if isinstance(item, Consumivel):
                if item.usar(self):
                    self.inventario.pop(indice)
                    if not hasattr(self, 'venceu'): 
                        save_game(self, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})
                    return True
                else:
                    print(f"{Fore.RED}Não foi possível usar {item.nome} (sem efeito ou condição não presente).{Style.RESET_ALL}")
                    return False
            else:
                print(f"{Fore.RED} {item.nome} não é um item consumível.{Style.RESET_ALL}")
                return False
        return False

    def escolher_talento(self):
        talentos = {
            1: ("Poder Focado", "Aumenta o dano de habilidades em 10%."),
            2: ("Vigor Incansável", "Reduz o custo de vigor das habilidades em 10% e aumenta a recuperação de vigor por turno em 5."),
            3: ("Mente Clara", "50% de chance de resistir a condições negativas (Sangramento, Veneno, Queimadura).")
        }
        
        while True:
            print(f"\n{Fore.YELLOW}--- ESCOLHA DE TALENTO ---{Style.RESET_ALL}")
            for i, (nome, descricao) in talentos.items():
                print(f"{i}. {nome}: {descricao}")
            
            escolha = input("Escolha o número do Talento: ")
            
            if escolha.isdigit() and int(escolha) in talentos:
                self.talento = talentos[int(escolha)][0]
                print(f"{Fore.GREEN}Talento {self.talento} escolhido!{Style.RESET_ALL}")
                save_game(self, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})
                break
            else:
                print("Escolha inválida.")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "__class__": self.__class__.__name__,
            "subclasse": self.subclasse,
            "experiencia": self.experiencia,
            "exp_para_proximo_nivel": self.exp_para_proximo_nivel,
            "talento": self.talento,
            "gold": self.gold,
            "pontos_treinamento": self.pontos_treinamento,
            "missoes_completas": self.missoes_completas,
            "missao_ativa": self.missao_ativa.to_dict() if self.missao_ativa else None,
            "karma": self.karma, 
            "usos_foco_vigor": self.usos_foco_vigor,
            "inventario": [item.to_dict() for item in self.inventario],
            "equipamento": {slot: item.to_dict() if item else None for slot, item in self.equipamento.items()},
        })
        return data

    @classmethod
    def from_dict(cls, data):
        instance = cls(data["nome"], data["subclasse"], data["nivel"])
        
        instance.vida_max = data["vida_max"]
        instance.vida = data["vida"]
        instance.vigor_max = data["vigor_max"]
        instance.vigor = data["vigor"]
        instance.ataque_base = data["ataque_base"]
        instance.defesa_base = data["defesa_base"]
        instance.velocidade_base = data["velocidade_base"]
        instance.condicoes = data["condicoes"]
        
        instance.experiencia = data["experiencia"]
        instance.exp_para_proximo_nivel = data["exp_para_proximo_nivel"]
        instance.talento = data["talento"]
        instance.gold = data["gold"]
        instance.pontos_treinamento = data["pontos_treinamento"]
        instance.missoes_completas = data["missoes_completas"]
        instance.missao_ativa = Missao.from_dict(data["missao_ativa"])
        instance.karma = data["karma"]
        instance.usos_foco_vigor = data["usos_foco_vigor"]

        instance.inventario = [deserialize_object(item_data) for item_data in data["inventario"]]
        instance.equipamento = {
            slot: deserialize_object(item_data) 
            for slot, item_data in data["equipamento"].items()
        }

        instance.habilidades = [deserialize_object(h_data) for h_data in data["habilidades"]]
        
        return instance


class OponenteIA(GuerreiroDoPunho):
    def __init__(self, modelo_key):
        modelo = OPONENTE_MODELOS[modelo_key]

        super().__init__(modelo["nome"], modelo["subclasse"]) 
        
        self.nivel = modelo["nivel"]
        self.vida_max = modelo["vida"]
        self.vida = modelo["vida"]
        self.vigor_max = modelo["vigor"]
        self.vigor = modelo["vigor"]
        self.ataque_base = modelo["ataque"]
        self.defesa_base = modelo["defesa"]
        self.velocidade_base = modelo["velocidade"]
        self.talento = modelo["talento"]

        self.tipo = modelo["tipo"]
        self.gold_recompensa = modelo["gold_recompensa"]
        self.exp_recompensa = modelo["exp_recompensa"]

        self.habilidades = [h for h in self.habilidades if h.nome not in ["Jab Rápido", "Contra-Ataque"]]
        self.habilidades.append(Habilidade("Contra-Ataque", 20, 40, "Habilidade de Reação: Causa dano massivo após ser atacado (Requer 20 Vigor)."))

        if modelo_key == "Desafiante":
            self.habilidades.append(Habilidade("Golpe Venenoso", 20, 10, "Aplica Veneno (3 turnos)."))
        elif modelo_key == "Lenda":
            self.habilidades.append(Habilidade("Punho Flamejante", 25, 20, "Aplica Queimadura (2 turnos)."))

        for _ in range(1, self.nivel):
            self.vida_max += 10
            self.vida = self.vida_max
            self.vigor_max += 5
            self.vigor = self.vigor_max
            self.ataque_base += 2
            self.defesa_base += 2
            self.velocidade_base += 2


    def acao_ia(self, heroi):
        
        habilidades_controle = [h for h in self.habilidades if h.nome in ["Gancho Poderoso", "Terremoto de Punho"] and self.vigor >= h.custo_vigor]
        if habilidades_controle and random.random() < 0.4 and "Atordoado" not in heroi.condicoes:
            h = random.choice(habilidades_controle)
            if self.atacar(heroi, h):
                heroi.aplicar_condicao("Atordoado", 1)
                return

        habilidades_dano = [h for h in self.habilidades if h.dano_base > 20 and self.vigor >= h.custo_vigor]
        if habilidades_dano and random.random() < 0.6:
            self.atacar(heroi, random.choice(habilidades_dano))
            return

        if self.subclasse == "Tanque de Ferro" and self.vida > self.vida_max * 0.7 and "Bloqueio de Guarda" not in self.condicoes:
            bloqueio = next((h for h in self.habilidades if h.nome == "Bloqueio de Guarda"), None)
            if bloqueio and self.vigor >= bloqueio.custo_vigor:
                self.aplicar_condicao("Bloqueio de Guarda", 1)
                self.vigor -= bloqueio.custo_vigor
                print(f"{Fore.BLUE}🛡️ {self.nome} assume Postura de Bloqueio de Guarda.{Style.RESET_ALL}")
                return

        self.atacar(heroi)

def iniciar_combate(heroi, oponente):
    print(f"\n{Fore.RED}--- COMBATE INICIADO! ---{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{heroi.nome} (Nível {heroi.nivel}){Style.RESET_ALL} vs {Fore.RED}{oponente.nome} (Nível {oponente.nivel}){Style.RESET_ALL}")
    time.sleep(1)

    turno = 1
    heroi.usos_foco_vigor = 1 

    heroi_velocidade = heroi.get_velocidade_total()
    if heroi.karma < -50:
        heroi_velocidade = max(1, heroi_velocidade - 5)
        print(f"{Fore.RED}A hostilidade ao seu redor reduz sua velocidade de combate!{Style.RESET_ALL}")

    if heroi_velocidade >= oponente.get_velocidade_total():
        primeiro = heroi
        segundo = oponente
    else:
        primeiro = oponente
        segundo = heroi

    while heroi.esta_vivo() and oponente.esta_vivo():
        print(f"\n{Fore.YELLOW}==== TURNO {turno} ===={Style.RESET_ALL}")

        primeiro.processar_condicoes()
        segundo.processar_condicoes()
        
        if not heroi.esta_vivo() or not oponente.esta_vivo():
            break

        primeiro.recuperar_vigor_turno()
        segundo.recuperar_vigor_turno()

        if primeiro.esta_vivo():
            if primeiro == heroi:
                menu_combate(heroi, oponente)
            else:
                primeiro.acao_ia(heroi)
        
        if not heroi.esta_vivo() or not oponente.esta_vivo():
            break

        if segundo.esta_vivo():
            if segundo == heroi:
                menu_combate(heroi, oponente)
            else:
                segundo.acao_ia(heroi)

        turno += 1
        time.sleep(1)

    heroi.venceu = heroi.esta_vivo()
    
    if heroi.venceu:
        print(f"\n{Fore.GREEN}VITÓRIA!{Style.RESET_ALL}")
        gold_ganho = oponente.gold_recompensa
        exp_ganha = oponente.exp_recompensa

        if heroi.karma > 50:
            bonus = int(gold_ganho * 0.25)
            gold_ganho += bonus
            print(f"{Fore.YELLOW}Sua reputação lhe rendeu um bônus de {bonus} Gold!{Style.RESET_ALL}")

        heroi.gold += gold_ganho
        heroi.ganhar_experiencia(exp_ganha) 

        if heroi.missao_ativa and heroi.missao_ativa.tipo == "derrotar_monstro" and heroi.missao_ativa.alvo == oponente.tipo:
            heroi.missao_ativa.progresso += 1
            print(f"{Fore.CYAN}Progresso da Missão: {heroi.missao_ativa.progresso}/{heroi.missao_ativa.quantidade}{Style.RESET_ALL}")
        
        print(f"Você ganhou {Fore.YELLOW}{gold_ganho} Gold{Style.RESET_ALL} e {Fore.CYAN}{exp_ganha} EXP{Style.RESET_ALL}!")

        if oponente.vida <= 0:
            print(f"\n{Fore.YELLOW}O corpo de {oponente.nome} jaz no chão. O que você faz?{Style.RESET_ALL}")
            print("1. Ignorar e seguir em frente.")
            print("2. Prestar os primeiros socorros (Aumenta Karma).")
            
            escolha = input("Opção: ")
            if escolha == '2':
                heroi.karma = min(100, heroi.karma + 5)
                print(f"{Fore.GREEN}Você demonstrou piedade. Karma aumentado para {heroi.karma}.{Style.RESET_ALL}")

        if not heroi.experiencia >= heroi.exp_para_proximo_nivel:
            save_game(heroi, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})

        return True 
    else:
        print(f"\n{Fore.RED}DERROTA!{Style.RESET_ALL}")
        save_game(heroi, {"OPONENTE_MODELOS": OPONENTE_MODELOS, "MISSOES_DISPONIVEIS": MISSOES_DISPONIVEIS, "ITENS_LOJA": ITENS_LOJA})
        return False

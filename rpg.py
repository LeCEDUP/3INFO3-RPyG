# Desenvolva o seu jogo aqui
class SistemaJogo:
    """Gerencia o fluxo do jogo"""
    
    def __init__(self):
        self.heroi: Optional[Heroi] = None
        self.modo_jogo: Optional[str] = None
        self.nivel_historia = 1
        self.nivel_infinito = 1
        self.arquivo_save = "save_game.json"
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def pausar(self):
        """Pausa e aguarda entrada do usuário"""
        input("\nPressione ENTER para continuar...")
    
    def menu_principal(self):
        """Exibe o menu principal do jogo"""
        while True:
            self.limpar_tela()
            print("╔" + "═" * 58 + "╗")
            print("║" + " " * 15 + "🐉 RPG DE TEXTO 🐉" + " " * 15 + "║")
            print("╚" + "═" * 58 + "╝")
            print("\n" + "─" * 60)
            print("1. 🆕 Novo Jogo")
            print("2. 💾 Continuar")
            print("3. ℹ️  Como Jogar")
            print("4. 🚪 Sair")
            print("─" * 60)
            
            escolha = input("\nEscolha uma opção: ").strip()
            
            if escolha == "1":
                self.novo_jogo()
            elif escolha == "2":
                if self.carregar_jogo():
                    self.menu_modo_jogo()
                else:
                    print("\n❌ Nenhum save encontrado!")
                    self.pausar()
            elif escolha == "3":
                self.mostrar_instrucoes()
            elif escolha == "4":
                print("\n👋 Até logo, aventureiro!")
                break
            else:
                print("\n❌ Opção inválida!")
                self.pausar()
    
    def mostrar_instrucoes(self):
        """Mostra as instruções do jogo"""
        self.limpar_tela()
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 18 + "📖 COMO JOGAR" + " " * 19 + "║")
        print("╚" + "═" * 58 + "╝\n")
        
        print("🎮 OBJETIVO:")
        print("   Derrote monstros, ganhe experiência, suba de nível e")
        print("   torne-se o herói mais poderoso!\n")
        
        print("🎯 MODOS DE JOGO:")
        print("   • MODO HISTÓRIA: Siga uma narrativa épica com 10 níveis")
        print("   • MODO INFINITO: Enfrente ondas infinitas de inimigos\n")
        
        print("⚔️  COMBATE:")
        print("   • Escolha entre atacar, usar poção ou fugir")
        print("   • Derrote monstros para ganhar XP e ouro")
        print("   • Use o ouro para comprar equipamentos\n")
        
        print("📈 PROGRESSÃO:")
        print("   • Ganhe XP para subir de nível")
        print("   • Equipe armas e armaduras para ficar mais forte")
        print("   • Gerencie seu inventário com sabedoria\n")
        
        self.pausar()
    
    def novo_jogo(self):
        """Inicia um novo jogo"""
        self.limpar_tela()
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 17 + "🆕 NOVO JOGO" + " " * 20 + "║")
        print("╚" + "═" * 58 + "╝\n")
        
        nome = input("Digite o nome do seu herói: ").strip()
        if not nome:
            nome = "Aventureiro"
        
        print("\nEscolha sua classe:")
        print("1. ⚔️  Guerreiro (Mais vida e defesa)")
        print("2. 🏹 Arqueiro (Ataque balanceado)")
        print("3. 🔮 Mago (Mais ataque, menos defesa)")
        
        escolha_classe = input("\nEscolha (1-3): ").strip()
        
        if escolha_classe == "1":
            self.heroi = Heroi(nome, "Guerreiro")
            self.heroi.vida_maxima = 120
            self.heroi.vida = 120
            self.heroi.defesa = 8
        elif escolha_classe == "3":
            self.heroi = Heroi(nome, "Mago")
            self.heroi.ataque = 20
            self.heroi.defesa = 3
        else:
            self.heroi = Heroi(nome, "Arqueiro")
        
        # Itens iniciais
        self.heroi.adicionar_item(Pocao("Poção Pequena", "Restaura 30 de vida", 30))
        
        print(f"\n✨ Bem-vindo, {self.heroi.nome} o {self.heroi.classe}!")
        self.pausar()
        
        self.menu_modo_jogo()
    
    def menu_modo_jogo(self):
        """Menu para escolher o modo de jogo"""
        while True:
            self.limpar_tela()
            self.heroi.mostrar_status()
            
            print("╔" + "═" * 58 + "╗")
            print("║" + " " * 16 + "🎮 MODO DE JOGO" + " " * 19 + "║")
            print("╚" + "═" * 58 + "╝\n")
            print("1. 📖 Modo História")
            print("2. ♾️  Modo Infinito")
            print("3. 🎒 Inventário")
            print("4. 💾 Salvar Jogo")
            print("5. 🔙 Voltar ao Menu Principal")
            print("─" * 60)
            
            escolha = input("\nEscolha uma opção: ").strip()
            
            if escolha == "1":
                self.modo_jogo = "historia"
                self.iniciar_modo_historia()
            elif escolha == "2":
                self.modo_jogo = "infinito"
                self.iniciar_modo_infinito()
            elif escolha == "3":
                self.mostrar_inventario()
            elif escolha == "4":
                self.salvar_jogo()
            elif escolha == "5":
                break
            else:
                print("\n❌ Opção inválida!")
                self.pausar()
    
    def mostrar_inventario(self):
        """Mostra o inventário do herói"""
        self.limpar_tela()
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 18 + "🎒 INVENTÁRIO" + " " * 19 + "║")
        print("╚" + "═" * 58 + "╝\n")
        
        if not self.heroi.inventario:
            print("Seu inventário está vazio!")
        else:
            for i, item in enumerate(self.heroi.inventario, 1):
                print(f"{i}. {item.nome} - {item.descricao}")
                if isinstance(item, Arma):
                    print(f"   ⚔️ Ataque +{item.bonus_ataque}")
                elif isinstance(item, Armadura):
                    print(f"   🛡️ Defesa +{item.bonus_defesa}")
                elif isinstance(item, Pocao):
                    print(f"   💚 Cura {item.cura} de vida")
                print()
            
            print("\nDeseja equipar algum item? (Digite o número ou 0 para voltar)")
            escolha = input("Escolha: ").strip()
            
            if escolha.isdigit():
                idx = int(escolha) - 1
                if 0 <= idx < len(self.heroi.inventario):
                    item = self.heroi.inventario[idx]
                    if isinstance(item, (Arma, Armadura)):
                        self.heroi.equipar_item(item)
                        self.pausar()
        
        self.pausar()
    
    def salvar_jogo(self):
        """Salva o progresso do jogo"""
        dados = {
            "nome": self.heroi.nome,
            "classe": self.heroi.classe,
            "nivel": self.heroi.nivel,
            "vida": self.heroi.vida,
            "vida_maxima": self.heroi.vida_maxima,
            "ataque": self.heroi.ataque,
            "defesa": self.heroi.defesa,
            "experiencia": self.heroi.experiencia,
            "ouro": self.heroi.ouro,
            "nivel_historia": self.nivel_historia,
            "nivel_infinito": self.nivel_infinito
        }
        
        with open(self.arquivo_save, 'w') as f:
            json.dump(dados, f, indent=4)
        
        print("\n💾 Jogo salvo com sucesso!")
        self.pausar()
    
    def carregar_jogo(self) -> bool:
        """Carrega o progresso salvo"""
        if not os.path.exists(self.arquivo_save):
            return False
        
        with open(self.arquivo_save, 'r') as f:
            dados = json.load(f)
        
        self.heroi = Heroi(dados["nome"], dados["classe"])
        self.heroi.nivel = dados["nivel"]
        self.heroi.vida = dados["vida"]
        self.heroi.vida_maxima = dados["vida_maxima"]
        self.heroi.ataque = dados["ataque"]
        self.heroi.defesa = dados["defesa"]
        self.heroi.experiencia = dados["experiencia"]
        self.heroi.ouro = dados["ouro"]
        self.nivel_historia = dados.get("nivel_historia", 1)
        self.nivel_infinito = dados.get("nivel_infinito", 1)
        
        print("\n💾 Jogo carregado com sucesso!")
        self.pausar()
        return True
    
    def iniciar_modo_historia(self):
        """Inicia o modo história com narrativa progressiva"""
        if self.nivel_historia == 1:
            self.introducao_historia()
        
        while self.heroi.esta_vivo() and self.nivel_historia <= 10:
            self.limpar_tela()
            self.capitulo_historia(self.nivel_historia)
            
            if not self.heroi.esta_vivo():
                print("\n💀 Você foi derrotado! Game Over.")
                self.pausar()
                break
            
            self.nivel_historia += 1
            
            if self.nivel_historia > 10:
                self.final_historia()
                break
            
            # Oferecer loja entre níveis
            self.loja()
    
    def introducao_historia(self):
        """Introdução narrativa do jogo"""
        self.limpar_tela()
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 15 + "📖 A LENDA DO HERÓI" + " " * 15 + "║")
        print("╚" + "═" * 58 + "╝\n")
        
        print("Era uma vez, em um reino distante chamado Eldoria...\n")
        print("Uma escuridão ancestral despertou nas profundezas das")
        print("Montanhas Sombrias. Criaturas malignas começaram a")
        print("aterrorizar as aldeias, e o rei convocou os mais")
        print("corajosos aventureiros para enfrentar esta ameaça.\n")
        print(f"Você, {self.heroi.nome} o {self.heroi.classe}, atendeu")
        print("ao chamado. Sua jornada começa agora...\n")
        
        self.pausar()
    
    def capitulo_historia(self, nivel: int):
        """Gerencia cada capítulo da história"""
        capitulos = {
            1: {
                "titulo": "Capítulo 1: A Floresta Assombrada",
                "narrativa": "Você entra na Floresta Assombrada. As árvores parecem\nsussurar avisos enquanto você avança. De repente, um\nlobo selvagem aparece!",
                "monstro": Monstro("Lobo Selvagem", "Pequeno", 30, 8, 2, 50, 10)
            },
            2: {
                "titulo": "Capítulo 2: O Pântano Venenoso",
                "narrativa": "Após derrotar o lobo, você chega a um pântano fétido.\nBolhas de gás tóxico emergem da água. Um goblin\nemboscador salta das sombras!",
                "monstro": Monstro("Goblin Emboscador", "Pequeno", 40, 10, 3, 70, 15)
            },
            3: {
                "titulo": "Capítulo 3: As Ruínas Antigas",
                "narrativa": "Você descobre ruínas de uma civilização perdida.\nInscrições antigas alertam sobre um guardião.\nUm esqueleto guerreiro se levanta!",
                "monstro": Monstro("Esqueleto Guerreiro", "Médio", 60, 12, 5, 100, 25)
            },
            4: {
                "titulo": "Capítulo 4: A Caverna dos Trolls",
                "narrativa": "Uma caverna escura se abre à sua frente. Ossos\nespalhados pelo chão contam histórias de aventureiros\nmal-sucedidos. Um troll enfurecido ataca!",
                "monstro": Monstro("Troll Enfurecido", "Grande", 80, 15, 6, 150, 35)
            },
            5: {
                "titulo": "Capítulo 5: O Vale dos Dragões",
                "narrativa": "Você alcança o Vale dos Dragões. O ar está quente\ne cheira a enxofre. Um jovem dragão vermelho\ndesce dos céus!",
                "monstro": Monstro("Dragão Jovem", "Grande", 100, 18, 8, 200, 50)
            },
            6: {
                "titulo": "Capítulo 6: A Torre do Necromante",
                "narrativa": "Uma torre negra se ergue à distância. Energia sombria\npulsa em suas paredes. O necromante invoca um\ngolem de ossos!",
                "monstro": Monstro("Golem de Ossos", "Grande", 120, 20, 10, 250, 60)
            },
            7: {
                "titulo": "Capítulo 7: O Deserto Ardente",
                "narrativa": "O calor é insuportável. Miragens dançam no horizonte.\nUm elemental de fogo emerge das dunas!",
                "monstro": Monstro("Elemental de Fogo", "Grande", 140, 22, 12, 300, 75)
            },
            8: {
                "titulo": "Capítulo 8: A Fortaleza Sombria",
                "narrativa": "Você chega à Fortaleza Sombria, lar dos servos\nda escuridão. Um cavaleiro das trevas bloqueia\nseu caminho!",
                "monstro": Monstro("Cavaleiro das Trevas", "Chefe", 160, 25, 14, 400, 100)
            },
            9: {
                "titulo": "Capítulo 9: O Portal Demoníaco",
                "narrativa": "Um portal vermelho pulsa com energia maligna.\nDemônios menores o cercam, mas um demônio maior\nemerge do portal!",
                "monstro": Monstro("Demônio Maior", "Chefe", 200, 28, 16, 500, 150)
            },
            10: {
                "titulo": "Capítulo 10: O Senhor das Trevas",
                "narrativa": "Finalmente, você enfrenta o Senhor das Trevas,\nresponsável por toda a destruição. Esta é a\nbatalha final!",
                "monstro": Monstro("Senhor das Trevas", "Chefe Final", 300, 35, 20, 1000, 500)
            }
        }
        
        cap = capitulos[nivel]
        
        print("╔" + "═" * 58 + "╗")
        print(f"║  {cap['titulo']:<54}  ║")
        print("╚" + "═" * 58 + "╝\n")
        print(cap['narrativa'])
        print()
        
        self.pausar()
        self.combate(cap['monstro'])
    
    def final_historia(self):
        """Encerramento da história"""
        self.limpar_tela()
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 20 + "🏆 VITÓRIA! 🏆" + " " * 17 + "║")
        print("╚" + "═" * 58 + "╝\n")
        
        print("Com um golpe final devastador, você derrota o Senhor")
        print("das Trevas! A escuridão se dissipa e a luz retorna")
        print("a Eldoria.\n")
        print("O reino está salvo graças à sua coragem e determinação!")
        print(f"\n{self.heroi.nome}, você é agora uma lenda viva!\n")
        print(f"Nível Final: {self.heroi.nivel}")
        print(f"Ouro Acumulado: {self.heroi.ouro}")
        print("\nParabéns por completar o Modo História!\n")
        
        self.nivel_historia = 1  # Reset para rejogar
        self.pausar()
    
    def loja(self):
        """Sistema de loja entre níveis"""
        self.limpar_tela()
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 20 + "🏪 LOJA DO FERREIRO" + " " * 13 + "║")
        print("╚" + "═" * 58 + "╝\n")
        print(f"💰 Seu ouro: {self.heroi.ouro}\n")
        
        itens_loja = [
            ("Poção de Cura", Pocao("Poção Média", "Restaura 50 de vida", 50), 20),
            ("Espada de Ferro", Arma("Espada de Ferro", "Uma espada resistente", 8), 50),
            ("Armadura de Couro", Armadura("Armadura de Couro", "Proteção básica", 5), 40),
            ("Espada de Aço", Arma("Espada de Aço", "Espada afiada e forte", 15), 100),
            ("Armadura de Ferro", Armadura("Armadura de Ferro", "Proteção sólida", 10), 80)
        ]
        
        print("Itens disponíveis:")
        for i, (nome, item, preco) in enumerate(itens_loja, 1):
            print(f"{i}. {nome} - {preco} ouro")
        print("0. Sair da loja\n")
        
        while True:
            escolha = input("O que deseja comprar? ").strip()
            
            if escolha == "0":
                break
            
            if escolha.isdigit():
                idx = int(escolha) - 1
                if 0 <= idx < len(itens_loja):
                    nome, item, preco = itens_loja[idx]
                    if self.heroi.ouro >= preco:
                        self.heroi.ouro -= preco
                        self.heroi.adicionar_item(item)
                        print(f"\n✅ Você comprou {nome}!")
                        print(f"💰 Ouro restante: {self.heroi.ouro}\n")
                    else:
                        print("\n❌ Ouro insuficiente!\n")
                else:
                    print("\n❌ Opção inválida!\n")
            else:
                print("\n❌ Opção inválida!\n")
    
    def combate(self, monstro: Monstro):
        """Sistema de combate"""
        self.limpar_tela()
        print(f"\n⚔️  Um {monstro.nome} apareceu!\n")
        print(f"👹 {monstro.nome}")
        print(f"❤️  Vida: {monstro.vida}")
        print(f"⚔️  Ataque: {monstro.ataque}")
        print(f"🛡️  Defesa: {monstro.defesa}\n")
        
        self.pausar()
        
        while self.heroi.esta_vivo() and monstro.esta_vivo():
            self.limpar_tela()
            print(f"\n{'='*60}")
            print(f"👤 {self.heroi.nome}: {self.heroi.vida}/{self.heroi.vida_maxima} HP")
            print(f"👹 {monstro.nome}: {monstro.vida} HP")
            print(f"{'='*60}\n")
            
            print("O que você deseja fazer?")
            print("1. ⚔️  Atacar")
            print("2. 💚 Usar Poção")
            print("3. 🏃 Fugir\n")
            
            escolha = input("Escolha: ").strip()
            
            if escolha == "1":
                # Herói ataca
                dano = self.heroi.atacar(monstro)
                print(f"\n⚔️ Você causou {dano} de dano!")
                
                if not monstro.esta_vivo():
                    print(f"\n🎉 Você derrotou {monstro.nome}!")
                    self.heroi.ganhar_experiencia(monstro.exp_drop)
                    self.heroi.ouro += monstro.ouro_drop
                    print(f"⭐ +{monstro.exp_drop} XP")
                    print(f"💰 +{monstro.ouro_drop} ouro")
                    
                    # Chance de drop de item
                    if random.random() < 0.3:  # 30% de chance
                        item_drop = self.gerar_item_aleatorio()
                        self.heroi.adicionar_item(item_drop)
                    
                    self.pausar()
                    break
                
                # Monstro contra-ataca
                dano_monstro = monstro.atacar(self.heroi)
                print(f"👹 {monstro.nome} causou {dano_monstro} de dano!")
                
                self.pausar()
            
            elif escolha == "2":
                if self.heroi.usar_pocao():
                    # Monstro ataca após usar poção
                    dano_monstro = monstro.atacar(self.heroi)
                    print(f"👹 {monstro.nome} causou {dano_monstro} de dano!")
                self.pausar()
            
            elif escolha == "3":
                if random.random() < 0.5:  # 50% de chance de fugir
                    print("\n🏃 Você fugiu da batalha!")
                    self.heroi.receber_dano(10)  # Penalidade por fugir
                    self.pausar()
                    break
                else:
                    print("\n❌ Você não conseguiu fugir!")
                    dano_monstro = monstro.atacar(self.heroi)
                    print(f"👹 {monstro.nome} causou {dano_monstro} de dano!")
                    self.pausar()
            else:
                print("\n❌ Opção inválida!")
                self.pausar()
        
        if not self.heroi.esta_vivo():
            print("\n💀 Você foi derrotado!")
            self.pausar()
    
    def gerar_item_aleatorio(self) -> Item:
        """Gera um item aleatório como drop"""
        itens = [
            Pocao("Poção Pequena", "Restaura 30 de vida", 30),
            Pocao("Poção Média", "Restaura 50 de vida", 50),
            Arma("Adaga", "Uma adaga afiada", 5),
            Arma("Machado", "Um machado pesado", 10),
            Armadura("Elmo", "Protege a cabeça", 3),
            Armadura("Botas", "Botas reforçadas", 2)
        ]
        return random.choice(itens)
    
    def iniciar_modo_infinito(self):
        """Placeholder para modo infinito - será implementado na próxima fase"""
        print("\n♾️ Modo Infinito será implementado...")
        self.pausar()
        if __name__ == "__main__":
    jogo = SistemaJogo()
    jogo.menu_principal()


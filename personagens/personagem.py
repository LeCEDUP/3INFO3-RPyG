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
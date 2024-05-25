class Jogador:
    def __init__(self, nome, saldo, ajudas_disponiveis, ajudas_usadas, respostas):
        self.nome = nome
        self.saldo = saldo
        self.ajudas_disponiveis = ["Pular Pergunta", "Cartas", "Ajuda da Plateia", "Eliminar Duas Opções"] 
        self.ajudas_usadas = []
        self.respostas = {}
    
    def get_nome(self):
        return self.nome
    
    def set_nome(self, nome):
        self.nome = nome
    
    def get_saldo(self):
        return self._saldo
    
    def set_saldo(self, saldo):
        self._saldo = saldo
    
    def get_ajudas_disponiveis(self):
        return self._ajudas_disponiveis
    
    def set_ajudas_disponiveis(self, ajudas_disponiveis):
        self._ajudas_disponiveis = ajudas_disponiveis
        
    def get_ajudas_usadas(self):
        return self._ajudas_usadas
    
    def set_ajudas_usadas(self, ajudas_usadas):
        self._ajudas_usadas = ajudas_usadas
        
    def get_respostas(self):
        return self._respostas
    
    def set_respostas(self, respostas):
        self._respostas = respostas
            
    def remover_ajuda(self,ajuda):
        self.ajudas_disponiveis.remove(ajuda)
        
    def adicionar_resposta(self, numero_pergunta, resposta):
        self.respostas[numero_pergunta] = resposta
    
    def atualizar_saldo(self, valor):
        self.saldo += valor
    
    def usar_ajuda(self, ajuda):
        if ajuda in self._ajudas_disponiveis:
            self.ajudas_disponiveis.remove(ajuda)
            self.ajudas_usadas.append(ajuda)
        else:
            print("Esta ajuda já foi usada.")
        
    def __str__(self):
        return f"Nome: {self.nome}, Saldo: {self.saldo}, Ajudas Disponiveis: {','.join(self.ajudas_disponiveis)}, Ajudas Usadas: {','.join(self.ajudas_usadas)}, Resposta: {self.respostas}"
    

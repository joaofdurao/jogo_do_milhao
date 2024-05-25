class Pergunta:
    def __init__(self, pergunta, resposta_correta, respostas_incorretas, dificuldade):
        self.pergunta = pergunta
        self.resposta_correta = resposta_correta
        self.respostas_incorretas = ['resposta_1', 'resposta_2', 'resposta_3']
        self.dificuldade = dificuldade
    
    def get_pergunta(self):
        return self.pergunta
    
    def get_resposta_correta(self):
        return self.resposta_correta
    
    def get_respostas_incorretas(self):
        return self.respostas_incorretas
    
    def get_dificuldade(self):
        return self.dificuldade
    
    def __str__(self):
        return f"Pergunta: {self.pergunta}\nResposta Correta: {self.resposta_correta}\nRespostas Incorretas: {','.join(self.respostas_incorretas)}\nDificuldade: {self.dificuldade}"
    
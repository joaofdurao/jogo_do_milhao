import json

class Pergunta:
    def __init__(self, texto, resposta_correta, opcoes_respostas, dificuldade, id = None):
        self.id = id
        self.texto = texto
        self.opcoes_respostas = json.dumps(opcoes_respostas)
        self.resposta_correta = resposta_correta
        self.dificuldade = dificuldade
    
    def __str__(self):
        return f"ID: {self.id}, Texto: {self.texto}, Resposta Correta: {self.resposta_correta}, Opções de Respostas: {self.opcoes_respostas}, Dificuldade: {self.dificuldade}"
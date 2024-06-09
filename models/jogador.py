import json

class Jogador:
    def __init__(self, nome, id = None, saldo = 0.0):
        self.id = id
        self.nome = nome
        self.saldo = saldo
        self.ajudas_disponiveis = json.dumps(['pular', 'cartas', 'plateia', '5050'])
        self.respostas = json.dumps([])   

    def __str__(self):
        return f"ID: {self.id()}, Nome: {self.nome()}, Saldo: {self.saldo()}, Ajudas Disponiveis: {self.ajudas_disponiveis()}, Respostas: {self.respostas()}"
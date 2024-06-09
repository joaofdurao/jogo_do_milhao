import json
from models.jogador import Jogador
from repositories.jogadordao import JogadorDAO

class JogadorController:

    def __init__(self):
        self.dao = JogadorDAO()

    def criar_jogador(self, nome):
        jogador = Jogador(nome)
        return self.dao._create(jogador)

    def buscar_jogador_recente(self):
        jogador_info = self.dao.find_max_id()
        jogador = Jogador(id= jogador_info[0], nome = jogador_info[1], saldo = jogador_info[2], respostas_corretas = jogador_info[3], ajudas_disponiveis = jogador_info[4])
        return jogador

    def atualizar_pontuacao(self, jogador_id, respostas_corretas):
        jogador_info = self.dao.find_by_id(jogador_id)
        jogador = Jogador(id= jogador_info[0], nome = jogador_info[1], saldo = jogador_info[2], respostas_corretas = jogador_info[3], ajudas_disponiveis = jogador_info[4])

        if respostas_corretas == 1:
            jogador.saldo = 500
        elif respostas_corretas == 2:
            jogador.saldo = 1000
        elif respostas_corretas == 3:
            jogador.saldo = 2000
        elif respostas_corretas == 4:
            jogador.saldo = 3000
        elif respostas_corretas == 5:
            jogador.saldo = 5000
        elif respostas_corretas == 6:
            jogador.saldo = 10000 
        elif respostas_corretas == 7:
            jogador.saldo = 15000
        elif respostas_corretas == 8:
            jogador.saldo = 20000
        elif respostas_corretas == 9:
            jogador.saldo = 30000
        elif respostas_corretas == 10:
            jogador.saldo = 50000
        elif respostas_corretas == 11:
            jogador.saldo = 100000
        elif respostas_corretas == 12:
            jogador.saldo = 150000
        elif respostas_corretas == 13:
            jogador.saldo = 300000
        elif respostas_corretas == 14:
            jogador.saldo = 500000
        elif respostas_corretas == 15:
            jogador.saldo = 1000000
        
        self.dao.update(jogador, jogador_id)
        return jogador.saldo
        
    def verifica_ajuda(self, jogador_id):
        jogador_info = self.dao.find_by_id(jogador_id)
        jogador = Jogador(id= jogador_info[0], nome = jogador_info[1], saldo = jogador_info[2], respostas_corretas = jogador_info[3], ajudas_disponiveis = jogador_info[4])
        format_ajudas_disponiveis = jogador.ajudas_disponiveis.strip('[]').replace('"','').split(", ")
        
        return format_ajudas_disponiveis

    def usar_ajuda(self, jogador_id, ajuda):

        jogador_info = self.dao.find_by_id(jogador_id)
        jogador = Jogador(id= jogador_info[0], nome = jogador_info[1], saldo = jogador_info[2], respostas_corretas = jogador_info[3], ajudas_disponiveis = jogador_info[4])
        format_ajudas_disponiveis = jogador.ajudas_disponiveis.strip('[]').replace('"','').split(", ")

        format_ajudas_disponiveis.remove(ajuda)
        jogador.ajudas_disponiveis = json.dumps(format_ajudas_disponiveis)
        self.dao.update(jogador, jogador_id)


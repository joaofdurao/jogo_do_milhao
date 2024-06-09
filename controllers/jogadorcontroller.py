import json
from matplotlib.font_manager import json_load
from models import jogador
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

    def atualizar_pontuacao(self, jogador_id, contador):
        jogador_info = self.dao.find_by_id(jogador_id)
        jogador = Jogador(id= jogador_info[0], nome = jogador_info[1], saldo = jogador_info[2], respostas_corretas = jogador_info[3], ajudas_disponiveis = jogador_info[4])

        if contador == 0:
            jogador.saldo = 0
        elif contador == 1:
            jogador.saldo += 500
        elif contador == 2 or contador == 3:
            jogador.saldo += 1000
        elif contador == 4:
            jogador.saldo += 2000
        elif contador == 5 or contador == 6 or contador == 7:
            jogador.saldo += 5000
        elif contador == 8:
            jogador.saldo += 10000
        elif contador == 9:
            jogador.saldo += 20000
        elif contador == 10 or contador == 11:
            jogador.saldo += 50000
        elif contador == 12:
            jogador.saldo += 150000
        elif contador == 13:
            jogador.saldo += 200000
        elif contador == 14:
            jogador.saldo += 500000
        
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


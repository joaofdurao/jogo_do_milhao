from models.jogador import Jogador
from repositories.jogadordao import JogadorDAO

class JogadorController:

    def __init__(self):
        self.dao = JogadorDAO()

    def criar_jogador(self, nome):
        jogador = Jogador(nome)
        return self.dao._create(jogador)

    def buscar_jogador_recente(self):
        return self.dao.find_max_id()

    def atualizar_jogador(self, jogador_id, nome, idade):
        jogador = {"nome": nome, "idade": idade}
        return self.dao.atualizar_jogador(jogador_id, jogador)

    def deletar_jogador(self, jogador_id):
        return self.dao.deletar_jogador(jogador_id)
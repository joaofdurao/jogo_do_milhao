from models.pergunta import Pergunta
from repositories.perguntadao import PerguntaDAO
import random

class PerguntaController:

    def __init__(self):
        self.dao = PerguntaDAO()

    def randomizar_pergunta(self, dificuldade, perguntas_list):
        perguntas = self.dao.find_by_dificuldade(dificuldade, perguntas_list)
        pergunta_selecionada = random.choice(perguntas)

        return pergunta_selecionada
    



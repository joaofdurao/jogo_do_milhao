from operator import index
import tkinter as tk

from matplotlib.pyplot import cla

from controllers.jogadorcontroller import JogadorController
from controllers.perguntacontroller import PerguntaController
from models import jogador
from models.pergunta import Pergunta
import os

class Janela(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("Quem Quer Ser um Milionário")
        self.tela_atual = None
        self.contador = 0
        self.jogador = None
        self.perguntas_list = []
        
        self.mudar_tela(TelaInicio(self, self))

    def mudar_tela(self, nova_tela):
        if self.tela_atual:
            self.tela_atual.destroy()
        self.tela_atual = nova_tela
        self.tela_atual.pack()

    def mudar_tela_jogo(self, nova_tela):
        if self.contador < 15:
            if self.tela_atual:
                self.tela_atual.destroy()
            self.tela_atual = nova_tela
            self.tela_atual.pack()
        else:
            if self.tela_atual:
                self.tela_atual.destroy()
            self.tela_atual = TelaFim(self, self)
            self.tela_atual.pack()
        
        
class TelaInicio(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master)
        self.manager = manager

        current_dir = os.getcwd()
        current_dir = current_dir.replace('\\', '/')
        # Create the image widget
        imagem = tk.PhotoImage(file=f'{current_dir}/quem_quer_ser_um_milionario/views/quem_quer_ser_um_milionario_front.png')
        self.imagem_widget = tk.Label(self, image=imagem)
        self.imagem_widget.image = imagem  # Keep a reference to the image
        self.imagem_widget.pack()
        # C:\Users\LeandroNinja\OneDrive\ENG SW\4º Período\Programação III\QSM\quem_quer_ser_um_milionario\views\quem_quer_ser_um_milionario_front.png
        # Create the "Jogar" button
        botao_jogar = tk.Button(self, text="Jogar", command=self.jogar, width=20, height=7, bg="green", fg="white")
        botao_jogar.lift()  # Mantém o botão em cima dos outros elementos
        botao_jogar.place(x=1000, y=550)

    def jogar(self):
        self.destroy()
        self.manager.mudar_tela(TelaRegras(self.master, self.manager)) 
    
class TelaRegras(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master)
        self.manager = manager

        regras_txt = ("                         Neste jogo, você terá a oportunidade de testar seus conhecimentos em uma série de perguntas de múltipla escolha.\n"
                      "                        O objetivo é acumular o máximo de dinheiro possível respondendo corretamente às perguntas.\n\n"
                      "Regras do Jogo:\n\n"
                      "           1. Perguntas: Você será apresentado a uma série de perguntas de múltipla escolha.\n "
                      "           Cada pergunta terá quatro opções de resposta, das quais apenas uma é correta.\n\n"
                      "           2. Prêmios: Cada pergunta terá um valor em dinheiro associado a ela. Se você responder\n"
                      "           corretamente, ganhará esse valor. Quanto mais perguntas você acertar, mais dinheiro acumulará.\n\n"
                      "           3. Ajudas: Durante o jogo, você terá a oportunidade de usar até quatro tipos de ajudas para ajudá-lo a responder às perguntas:\n"
                      "               - Pular Pergunta\n"   
                      "               - Cartas\n"
                      "               - Ajuda da Plateia\n"
                      "               - Eliminar Duas Opções\n\n"
                      "           4. Desistir: A qualquer momento, você pode decidir desistir do jogo e sair com o dinheiro acumulado até o momento.\n\n"
                      "           5. Vitória e Derrota: Se você responder corretamente a todas as perguntas, você ganha o prêmio máximo de um milhão de reais!\n"
                      "           No entanto, se responder uma pergunta incorretamente, você perde todo o dinheiro acumulado até o momento.\n\n"
                      "                                           Agora que você conhece as regras, está pronto para começar?  Boa sorte!")

        # Create a label for the title
        titulo = tk.Label(self, text="Bem-vindo ao 'Quem Quer Ser um Milionário'!\n", font=("Arial", 24))
        titulo.pack(pady=20)
        
        # Create a text widget for the rules
        regras = tk.Label(self, text=regras_txt, font=("Arial", 12), justify="left")
        regras.pack()

        # Create a label for the name input
        label_nome = tk.Label(self, text="Digite seu nome:", font=("Arial", 12))
        label_nome.pack(pady=10)

        # Create an entry widget for the name input
        entry_nome = tk.Entry(self, font=("Arial", 12))
        entry_nome.pack(pady=5)

        # Create a button to submit the name
        botao_submit = tk.Button(self, text="Iniciar jogo", command=lambda: self.iniciar(entry_nome.get()), width=16, height=7, bg="blue", fg="white")
        botao_submit.pack(pady=10)

    def iniciar(self, nome):
        JogadorController().criar_jogador(nome)
        self.manager.jogador = JogadorController().buscar_jogador_recente()
        print(self.manager.jogador)
        self.destroy()
        self.manager.mudar_tela_jogo(TelaEspera(self.master, self.manager))

class TelaEspera(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master)
        self.manager = manager

        jogador_nome = self.manager.jogador[1]

        # Create a label for the instruction
        label_instrucao = tk.Label(self, text="Aperte quando estiver pronto para responder a pergunta", font=("Arial", 24))
        label_instrucao.pack(pady=20)

        # Create a label for the bottom left corner
        label_bottom_left = tk.Label(self, text=f'Jogador:{jogador_nome}', font=("Arial", 20))
        label_bottom_left.pack(side="bottom", anchor="sw")

        # Create a button for when the user is ready
        botao_pronto = tk.Button(self, text="Pronto", command=self.responder_pergunta, width=10, height=3, bg="yellow", fg="black")
        botao_pronto.pack(pady=10)

    def responder_pergunta(self):
        
        self.destroy()
        self.manager.mudar_tela_jogo(TelaPergunta(self.master, self.manager))

class TelaPergunta(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master)
        self.manager = manager

        self.definir_pergunta()
        self.formatar_respostas()
        jogador_nome = self.manager.jogador[1]
        self.saldo = JogadorController().atualizar_pontuacao(self.manager.jogador[0], self.manager.contador)
        print(self.pergunta)
        print(self.respostas)
        print(type(self.resposta_correta))


        # Create a label for the question
        label_pergunta = tk.Label(self, text=self.pergunta[1], font=("Arial", 24))
        label_pergunta.pack(pady=20)

        # Create a frame to hold the buttons
        frame_botoes = tk.Frame(self)
        frame_botoes.pack()

        # Create buttons individually
        botao_resposta0 = tk.Button(frame_botoes, text=self.respostas[0], command=lambda: self.verifica_resposta(0), width=20, height=7, bg="orange", fg="white")
        botao_resposta0.grid(row=0, column=0, padx=10, pady=10)

        botao_resposta1 = tk.Button(frame_botoes, text=self.respostas[1], command=lambda: self.verifica_resposta(1), width=20, height=7, bg="orange", fg="white")
        botao_resposta1.grid(row=0, column=1, padx=10, pady=10)

        botao_resposta2 = tk.Button(frame_botoes, text=self.respostas[2], command=lambda: self.verifica_resposta(2), width=20, height=7, bg="orange", fg="white")
        botao_resposta2.grid(row=1, column=0, padx=10, pady=10)

        botao_resposta3 = tk.Button(frame_botoes, text=self.respostas[3], command=lambda: self.verifica_resposta(3), width=20, height=7, bg="orange", fg="white")
        botao_resposta3.grid(row=1, column=1, padx=10, pady=10)

        # Create a label for the bottom left corner
        label_bottom_left = tk.Label(self, text=f'Jogador:{jogador_nome}', font=("Arial", 20))
        label_bottom_left.pack(side="bottom", anchor="sw")

        # Create a label for the bottom right corner
        label_bottom_right = tk.Label(self, text=f'Saldo: {self.saldo}', font=("Arial", 20))
        label_bottom_right.pack(side="bottom", anchor="se")

    def definir_pergunta(self):
        if self.manager.contador < 10:
            self.pergunta = PerguntaController().randomizar_pergunta('Fácil', self.manager.perguntas_list)
        elif self.manager.contador < 24:
            self.pergunta = PerguntaController().randomizar_pergunta('Média', self.manager.perguntas_list)
        else:
            self.pergunta = PerguntaController().randomizar_pergunta('Difícil', self.manager.perguntas_list)

        self.manager.perguntas_list.append(self.pergunta[0])
        print(self.manager.perguntas_list)

    def formatar_respostas(self):
        self.respostas = []
        resps = self.pergunta[2].strip('[]').replace('"','').split(", ")
        for resp in resps:
            self.respostas.append(resp)

        self.resposta_correta = self.pergunta[3]

    def verifica_resposta(self, btn):
        print('oi')
        if btn == self.resposta_correta:
            self.manager.contador += 1
            self.manager.mudar_tela_jogo(TelaEspera(self.master, self.manager))
        else:
            self.manager.mudar_tela(TelaFim(self.master, self.manager))

class TelaFim(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master)
        self.manager = manager

        # Create a label for the end of the game
        label_fim = tk.Label(self, text="Fim de jogo!", font=("Arial", 24))
        label_fim.pack(pady=20)

        # Create a button to restart the game
        botao_reiniciar = tk.Button(self, text="Reiniciar", command=self.reiniciar, width=20, height=7, bg="red", fg="white")
        botao_reiniciar.pack(pady=10)

    def reiniciar(self):
        self.manager.contador = 0
        self.manager.perguntas_list = []
        self.destroy()
        self.manager.mudar_tela(TelaInicio(self.master, self.manager))










from operator import index
import tkinter as tk

from matplotlib.pyplot import cla

from controllers.jogadorcontroller import JogadorController
from controllers.perguntacontroller import PerguntaController
from models import jogador
from models.pergunta import Pergunta
import os
from PIL import Image, ImageTk


class Janela(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("480x800")
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

        # Configurar o canvas com fundo azul
        self.canvas = tk.Canvas(self, width=480, height=800, bg="purple")
        self.canvas.pack(fill="both", expand=True)

        # Adicionar a imagem no canvas
        current_dir = os.getcwd()
        current_dir = current_dir.replace('\\', '/')
        imagem = tk.PhotoImage(file=f'{current_dir}/quem_quer_ser_um_milionario/views/logo (256).png')
        self.imagem_widget = self.canvas.create_image(240, 200, anchor="center", image=imagem)
        self.image_ref = imagem  # Keep a reference to the image

        # Adicionar o botão JOGAR no canvas
        botao_jogar = tk.Button(self, text="Jogar", command=self.jogar, width=30, height=2, bg="yellow", fg="black", font=("Arial", 14))
        self.canvas.create_window(240, 600, anchor="center", window=botao_jogar)

    def jogar(self):
        self.manager.mudar_tela(TelaRegras(self.master, self.manager))
    
class TelaRegras(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master, bg="purple") #Definindo o fundo roxo
        self.manager = manager

        regras_txt = (
            "Neste jogo, você terá a oportunidade de testar seus conhecimentos em uma série de perguntas de múltipla escolha.\n"
            "O objetivo é acumular o máximo de dinheiro possível respondendo corretamente às perguntas.\n\n"
            "Regras do Jogo:\n\n"
            "1. Perguntas: Você será apresentado a uma série de perguntas de múltipla escolha.\n"
            "   Cada pergunta terá quatro opções de resposta, das quais apenas uma é correta.\n\n"
            "2. Prêmios: Cada pergunta terá um valor em dinheiro associado a ela. Se você responder\n"
            "   corretamente, ganhará esse valor. Quanto mais perguntas você acertar, mais dinheiro acumulará.\n\n"
            "3. Ajudas: Durante o jogo, você terá a oportunidade de usar até quatro tipos de ajudas para ajudá-lo a responder às perguntas:\n"
            "   - Pular Pergunta\n"
            "   - Cartas\n"
            "   - Ajuda da Plateia\n"
            "   - Eliminar Duas Opções\n\n"
            "4. Desistir: A qualquer momento, você pode decidir desistir do jogo e sair com o dinheiro acumulado até o momento.\n\n"
            "5. Vitória e Derrota: Se você responder corretamente a todas as perguntas, você ganha o prêmio máximo de um milhão de reais!\n"
            "   No entanto, se responder uma pergunta incorretamente, você perde todo o dinheiro acumulado até o momento.\n\n"
            "Agora que você conhece as regras, está pronto para começar? Boa sorte!"
        )

        # Create a label for the title
        titulo = tk.Label(self, text="Bem-vindo ao 'Quem Quer Ser um Milionário'!\n", font=("Arial", 14, "bold"), bg="purple", fg="white")
        titulo.pack(pady=10)
        
        # Create a text widget for the rules
        regras = tk.Label(self, text=regras_txt, font=("Arial", 10), justify="left", wraplength=460, bg="purple", fg="white")
        regras.pack(pady=10)

        # Create a label for the name input
        label_nome = tk.Label(self, text="Digite seu nome:", font=("Arial", 12), bg="purple", fg="white")
        label_nome.pack(pady=10)

        # Create an entry widget for the name input
        self.entry_nome = tk.Entry(self, font=("Arial", 12))
        self.entry_nome.pack(pady=5)

        # Create a button to submit the name
        botao_submit = tk.Button(self, text="Iniciar jogo", command=self.iniciar, width=15, height=2, bg="yellow", fg="black", font=("Arial", 12))
        botao_submit.pack(pady=10)

    def iniciar(self):
        nome = self.entry_nome.get()
        if nome.strip():
            JogadorController().criar_jogador(nome)
            self.manager.jogador = JogadorController().buscar_jogador_recente()
            print(self.manager.jogador)
            self.manager.mudar_tela_jogo(TelaEspera(self.master, self.manager))
        else:
            messagebox.showwarning("Nome inválido", "Por favor, digite um nome válido.")


class TelaEspera(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master, width=400, height=800, bg="purple")  # Definindo as dimensões e o fundo roxo
        self.manager = manager

        jogador_nome = self.manager.jogador[1]

        # Create a label for the player's name
        label_jogador_nome = tk.Label(self, text=f'Jogador: {jogador_nome}', font=("Arial", 12), bg="purple", fg="white")
        label_jogador_nome.place(relx=0.5, rely=0.3, anchor="center")

        # Create a label for the instruction
        label_instrucao = tk.Label(self, text="Aperte quando estiver pronto para\nresponder a pergunta!", font=("Arial", 14), bg="purple", fg="white", wraplength=380, justify="center")
        label_instrucao.place(relx=0.5, rely=0.45, anchor="center")

        # Create a button for when the user is ready
        botao_pronto = tk.Button(self, text="Pronto", command=self.responder_pergunta, width=10, height=3, font=("Arial", 12), bg="yellow", fg="black")
        botao_pronto.place(relx=0.5, rely=0.6, anchor="center")

    def responder_pergunta(self):
        self.destroy()
        self.manager.mudar_tela_jogo(TelaPergunta(self.master, self.manager))
        
class TelaPergunta(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master)
        master.configure(bg="purple")  # Define a cor de fundo da janela principal como roxo
        self.configure(bg="purple")  # Define a cor de fundo da própria frame como roxo
        self.manager = manager

        self.definir_pergunta()
        self.formatar_respostas()
        jogador_nome = self.manager.jogador[1]
        self.saldo = JogadorController().atualizar_pontuacao(self.manager.jogador[0], self.manager.contador)

        # Criando um label para o nome do jogador
        label_jogador_nome = tk.Label(self, text=f'Jogador: {jogador_nome}', font=("Arial", 14), bg="purple", fg="white")
        label_jogador_nome.pack(pady=(20, 10))

        # Criando um frame para o conteúdo principal
        frame_conteudo = tk.Frame(self, bg="purple")
        frame_conteudo.pack(expand=True)

        # Criando um label para a pergunta
        label_pergunta = tk.Label(frame_conteudo, text=self.pergunta[1], font=("Arial", 16), bg="purple", fg="white", wraplength=380)
        label_pergunta.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

        # Criando os botões de resposta
        for i, resposta in enumerate(self.respostas):
            botao_resposta = tk.Button(frame_conteudo, text=resposta, command=lambda idx=i: self.verifica_resposta(idx), width=20, height=2, bg="yellow", fg="black", font=("Arial", 12, "bold"))
            botao_resposta.grid(row=i//2 + 1, column=i%2, padx=10, pady=10)

        # Criando um frame para os botões de ajuda
        frame_ajuda = tk.Frame(frame_conteudo, bg="purple")
        frame_ajuda.grid(row=len(self.respostas)//2 + 2, column=0, columnspan=2, pady=10)

        # Criando os botões de ajuda
        botao_ajuda1 = tk.Button(frame_ajuda, text='PULAR\nPERGUNTA', command=self.executa_ajuda1, width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
        botao_ajuda1.pack(side="left", padx=10)

        botao_ajuda2 = tk.Button(frame_ajuda, text='CARTAS', command=self.executa_ajuda2, width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
        botao_ajuda2.pack(side="left", padx=10)

        botao_ajuda3 = tk.Button(frame_ajuda, text='PLATEIA', command=self.executa_ajuda3, width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
        botao_ajuda3.pack(side="left", padx=10)

        botao_ajuda4 = tk.Button(frame_ajuda, text='5050', command=self.executa_ajuda4, width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
        botao_ajuda4.pack(side="left", padx=10)

        # Criando um label para o saldo do jogador
        label_saldo = tk.Label(self, text=f'Saldo: {self.saldo}', font=("Arial", 14), bg="purple", fg="white")
        label_saldo.pack(side="bottom", padx=10, pady=10)

        # Posicionando a frame no centro da tela
        self.place(relx=0.5, rely=0.5, anchor="center")

    def definir_pergunta(self):
        if self.manager.contador < 10:
            self.pergunta = PerguntaController().randomizar_pergunta('Fácil', self.manager.perguntas_list)
        elif self.manager.contador < 24:
            self.pergunta = PerguntaController().randomizar_pergunta('Média', self.manager.perguntas_list)
        else:
            self.pergunta = PerguntaController().randomizar_pergunta('Difícil', self.manager.perguntas_list)

        self.manager.perguntas_list.append(self.pergunta[0])

    def formatar_respostas(self):
        self.respostas = []

        resps = self.pergunta[2].strip('[]').replace('"','').split(", ")
        for resp in resps:
            self.respostas.append(resp)

        self.resposta_correta = self.pergunta[3]

    def verifica_resposta(self, btn):
        if btn == self.resposta_correta:
            self.manager.contador += 1
            self.master.mudar_tela_jogo(TelaPergunta(self.master, self.manager))
        else:
            self.master.mudar_tela(TelaFim(self.master, self.manager, vencedor=False))

    def executa_ajuda1(self):
        print('ajuda1')
    
    def executa_ajuda2(self):
        print('ajuda2')
    
    def executa_ajuda3(self):
        print('ajuda3')

    def executa_ajuda4(self):
        print('ajuda4')

class TelaFim(tk.Frame):
    def __init__(self, master, manager, vencedor=True):
        super().__init__(master, bg="purple", width=400, height=800)  # Define a cor de fundo como roxo e as dimensões da tela
        self.manager = manager

        # Criando um frame para centralizar o conteúdo
        frame_central = tk.Frame(self, bg="purple")
        frame_central.place(relx=0.5, rely=0.5, anchor="center")  # Coloca o frame no centro da tela

        # Criando um label para o fim do jogo
        if vencedor:
            mensagem = "Parabéns!\nVocê ganhou 1 milhão de reais!"
        else:
            mensagem = "Você perdeu tudo!\nTente novamente!"
        label_fim = tk.Label(frame_central, text=mensagem, font=("Arial", 18), fg="white", bg="purple")  # Define a cor do texto como branco e o fundo como roxo
        label_fim.pack(pady=20)

        # Exibir fogos de artifício se o jogador for um vencedor
        if vencedor:
            try:
                self.exibir_fogos_artificio(frame_central)
            except Exception as e:
                print("Erro ao carregar a imagem de fogos de artifício:", e)

        # Criando um botão para reiniciar o jogo
        botao_reiniciar = tk.Button(frame_central, text="Reiniciar", command=self.reiniciar, width=20, height=2, bg="yellow", fg="black", font=("Arial", 12))  # Define a cor de fundo como amarelo, o texto como preto e a fonte como Arial tamanho 12
        botao_reiniciar.pack(pady=10)

    def exibir_fogos_artificio(self, frame):
        # Carregar a imagem do arquivo GIF
        try:
            image = Image.open("C:\\Users\\LeandroNinja\\OneDrive\\ENG SW\\4º Período\\Programação III\\QSM\\quem_quer_ser_um_milionario\\views\\fogo-de-artificio-imagem-animada-0087.gif")
            photo = ImageTk.PhotoImage(image)

            # Criar um label para exibir o GIF
            label_fogos = tk.Label(frame, image=photo, bg="purple")
            label_fogos.image = photo  # Manter uma referência para evitar que a imagem seja coletada pelo garbage collector
            label_fogos.pack()
        except Exception as e:
            raise e

    def reiniciar(self):
        self.manager.contador = 0
        self.manager.perguntas_list = []
        self.destroy()
        self.manager.mudar_tela(TelaInicio(self.master, self.manager))



# Exemplo de uso:
# Criando uma tela final para o vencedor
# tela_vencedor = TelaFim(master, manager, vencedor=True)

# Criando uma tela final para o perdedor
# tela_perdedor = TelaFim(master, manager, vencedor=False)


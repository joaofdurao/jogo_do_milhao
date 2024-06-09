import os
import tkinter as tk
from tkinter import messagebox

from controllers.jogadorcontroller import JogadorController
from controllers.perguntacontroller import PerguntaController
import random
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Janela(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("480x800")
        self.title("Quem Quer Ser um Milionário")
        self.tela_atual = None
        self.jogador = None
        self.perguntas_list = []
        
        self.mudar_tela(TelaInicio(self, self))

    def mudar_tela(self, nova_tela):
        if self.tela_atual:
            self.tela_atual.destroy()
        self.tela_atual = nova_tela
        self.tela_atual.pack()

    def mudar_tela_jogo(self, nova_tela):
        if self.jogador.respostas_corretas < 15:
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
        self.canvas = tk.Canvas(self, width=480, height=800, bg="purple")
        self.canvas.pack(fill="both", expand=True)

        current_dir = os.getcwd()
        current_dir = current_dir.replace('\\', '/')
        imagem = tk.PhotoImage(file=f'{current_dir}/views/imagem1.png')
        self.imagem_widget = self.canvas.create_image(240, 200, anchor="center", image=imagem)
        self.image_ref = imagem

        botao_jogar = tk.Button(self, text="Jogar", command=self.jogar, width=30, height=2, bg="yellow", fg="black", font=("Arial", 14))
        self.canvas.create_window(240, 600, anchor="center", window=botao_jogar)


    def jogar(self):
        self.manager.mudar_tela(TelaRegras(self.master, self.manager)) 
    
class TelaRegras(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master, bg="purple")
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

        titulo = tk.Label(self, text="Bem-vindo ao 'Quem Quer Ser um Milionário'!\n", font=("Arial", 14, "bold"), bg="purple", fg="white")
        titulo.pack(pady=10)

        regras = tk.Label(self, text=regras_txt, font=("Arial", 10), justify="left", wraplength=460, bg="purple", fg="white")
        regras.pack(pady=10)

        label_nome = tk.Label(self, text="Digite seu nome:", font=("Arial", 12), bg="purple", fg="white")
        label_nome.pack(pady=10)

        self.entry_nome = tk.Entry(self, font=("Arial", 12))
        self.entry_nome.pack(pady=5)

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
        super().__init__(master, width=400, height=800, bg="purple")
        self.manager = manager

        jogador_nome = self.manager.jogador.nome

        label_jogador_nome = tk.Label(self, text=f'Jogador: {jogador_nome}', font=("Arial", 12), bg="purple", fg="white")
        label_jogador_nome.place(relx=0.5, rely=0.3, anchor="center")

        label_instrucao = tk.Label(self, text="Aperte quando estiver pronto para\nresponder a pergunta!", font=("Arial", 14), bg="purple", fg="white", wraplength=380, justify="center")
        label_instrucao.place(relx=0.5, rely=0.45, anchor="center")

        botao_pronto = tk.Button(self, text="Pronto", command=self.responder_pergunta, width=10, height=3, font=("Arial", 12), bg="yellow", fg="black")
        botao_pronto.place(relx=0.5, rely=0.6, anchor="center")

    def responder_pergunta(self):
        self.manager.mudar_tela_jogo(TelaPergunta(self.master, self.manager))

class TelaPergunta(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master)
        master.configure(bg="purple") 
        self.configure(bg="purple") 
        self.manager = manager

        self.definir_pergunta()
        self.formatar_respostas()
        self.definir_ajudas()
        jogador_nome = self.manager.jogador.nome
        self.saldo = JogadorController().atualizar_pontuacao(self.manager.jogador.id, self.manager.jogador.respostas_corretas)
        print(self.pergunta)
        print(self.respostas)
        print(type(self.resposta_correta))

        label_jogador_nome = tk.Label(self, text=f'Jogador: {jogador_nome}', font=("Arial", 14), bg="purple", fg="white")
        label_jogador_nome.pack(pady=(20, 10))

        self.frame_conteudo = tk.Frame(self, bg="purple")
        self.frame_conteudo.pack(expand=True)

        label_pergunta = tk.Label(self.frame_conteudo, text=self.pergunta[1], font=("Arial", 16), bg="purple", fg="white", wraplength=380)
        label_pergunta.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

        botao_resposta0 = tk.Button(self.frame_conteudo, text=f'A) {self.respostas[0]}', command=lambda: self.verifica_resposta(0), width=20, height=2, bg="yellow", fg="black", font=("Arial", 12, "bold"))
        botao_resposta0.grid(row=1, column=0, padx=10, pady=10)

        botao_resposta1 = tk.Button(self.frame_conteudo, text=f'B) {self.respostas[1]}', command=lambda: self.verifica_resposta(1), width=20, height=2, bg="yellow", fg="black", font=("Arial", 12, "bold"))
        botao_resposta1.grid(row=1, column=1, padx=10, pady=10)

        botao_resposta2 = tk.Button(self.frame_conteudo, text=f'C) {self.respostas[2]}', command=lambda: self.verifica_resposta(2), width=20, height=2, bg="yellow", fg="black", font=("Arial", 12, "bold"))
        botao_resposta2.grid(row=2, column=0, padx=10, pady=10)

        botao_resposta3 = tk.Button(self.frame_conteudo, text=f'D) {self.respostas[3]}', command=lambda: self.verifica_resposta(3), width=20, height=2, bg="yellow", fg="black", font=("Arial", 12, "bold"))
        botao_resposta3.grid(row=2, column=1, padx=10, pady=10)


        self.frame_ajuda = tk.Frame(self.frame_conteudo, bg="purple")
        self.frame_ajuda.grid(row= 3, column=0, columnspan=2, pady=10)

        if 'pular' in self.ajudas:
            botao_ajuda1 = tk.Button(self.frame_ajuda, text='PULAR\nPERGUNTA', command= lambda: self.aciona_ajuda('pular'), width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
            botao_ajuda1.grid(row=0, column=0, padx=10, pady=10)

        if 'cartas' in self.ajudas:
            botao_ajuda2 = tk.Button(self.frame_ajuda, text='CARTAS', command= lambda: self.aciona_ajuda('cartas'), width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
            botao_ajuda2.grid(row=0, column=1, padx=10, pady=10)

        if 'plateia' in self.ajudas:
            botao_ajuda3 = tk.Button(self.frame_ajuda, text='PLATEIA', command= lambda: self.aciona_ajuda('plateia'), width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
            botao_ajuda3.grid(row=0, column=2, padx=10, pady=10)

        if '5050' in self.ajudas:
            botao_ajuda4 = tk.Button(self.frame_ajuda, text='5050', command= lambda: self.aciona_ajuda('5050'), width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
            botao_ajuda4.grid(row=0, column=3, padx=10, pady=10)

        label_saldo = tk.Label(self, text=f'Saldo: {self.saldo}', font=("Arial", 14), bg="purple", fg="white")
        label_saldo.pack(side="bottom", padx=10, pady=10)

        self.place(relx=0.5, rely=0.5, anchor="center")

    def definir_pergunta(self):
        if self.manager.jogador.respostas_corretas < 10:
            self.pergunta = PerguntaController().randomizar_pergunta('Fácil', self.manager.perguntas_list)
        elif self.manager.jogador.respostas_corretas < 24:
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
        if btn == self.resposta_correta:
            self.manager.jogador.respostas_corretas += 1
            self.manager.mudar_tela_jogo(TelaEspera(self.master, self.manager))
        else:
            self.manager.mudar_tela(TelaFim(self.master, self.manager))

    def definir_ajudas(self):
        self.ajudas = JogadorController().verifica_ajuda(self.manager.jogador.id)
    
    def aciona_ajuda(self, ajuda):
        JogadorController().usar_ajuda(self.manager.jogador.id, ajuda)
        
        if ajuda == 'pular':
            self.executa_pular()
        elif ajuda == 'cartas':
            self.executa_cartas()
        elif ajuda == 'plateia':
            self.executa_plateia()
        elif ajuda == '5050':
            self.executa_5050()
    
    def executa_pular(self):
        self.manager.jogador.respostas_corretas += 1
        self.manager.mudar_tela_jogo(TelaEspera(self.master, self.manager))

    def executa_cartas(self):

        self.frame_cartas = tk.Frame(self.frame_conteudo, bg="purple")
        self.frame_cartas.grid(row=4, column=0, columnspan=2, pady=10)

        label_carta = tk.Label(self.frame_cartas, text='Escolha uma carta:', font=("Arial", 16), bg="purple", fg="white", wraplength=380)
        label_carta.grid(row=0, columnspan=4, pady=10)

        botao_carta1 = tk.Button(self.frame_cartas, text='A', command=lambda: define_cartas(),  width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
        botao_carta1.grid(row=1, column=0, padx=10, pady=10)

        botao_carta2 = tk.Button(self.frame_cartas, text='B', command=lambda: define_cartas(),  width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
        botao_carta2.grid(row=1, column=1, padx=10, pady=10)

        botao_carta3 = tk.Button(self.frame_cartas, text='C', command=lambda: define_cartas(),  width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
        botao_carta3.grid(row=1, column=2, padx=10, pady=10)

        botao_carta4 = tk.Button(self.frame_cartas, text='D', command=lambda: define_cartas(),  width=10, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
        botao_carta4.grid(row=1, column=3, padx=10, pady=10)

        def define_cartas():
            numero_aleatorio = random.randint(0, 3)
                
            for widget in self.frame_cartas.grid_slaves(row=1):
                widget.grid_remove()

            indices_excluidos = []
            while len(indices_excluidos) < numero_aleatorio:
                indice = random.randint(0, len(self.respostas) - 1)
                if indice != self.resposta_correta and indice not in indices_excluidos:
                    indices_excluidos.append(indice)

            for i in indices_excluidos:
                if i == 0:
                    self.frame_conteudo.grid_slaves(row=1, column=0)[0].grid_remove()
                elif i == 1:
                    self.frame_conteudo.grid_slaves(row=1, column=1)[0].grid_remove()
                elif i == 2:
                    self.frame_conteudo.grid_slaves(row=2, column=0)[0].grid_remove()
                elif i == 3:
                    self.frame_conteudo.grid_slaves(row=2, column=1)[0].grid_remove()

            self.frame_ajuda.grid_slaves(row=0, column=1)[0].grid_remove()

            label_carta.config(text=f"Foram excluídas {numero_aleatorio} opções!")
          
    def executa_plateia(self):
        self.frame_plateia = tk.Frame(self.frame_conteudo, bg="purple")
        self.frame_plateia.grid(row=4, column=0, columnspan=2, pady=10)

        label_plateia = tk.Label(self.frame_plateia, text='A plateia acha que a resposta correta é:', font=("Arial", 16), bg="purple", fg="white", wraplength=380)
        label_plateia.grid(row=0, columnspan=4, pady=10)

        botao_plateia = tk.Button(self.frame_plateia, text='Mostrar Gráfico', command=lambda: mostra_grafico(), width=15, height=2, bg="orange", fg="white", font=("Arial", 10, "bold"))
        botao_plateia.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

        def mostra_grafico():
            botao_plateia.grid_remove()
            labels = ['A', 'B', 'C', 'D']
            respostas_index = [0, 1, 2, 3]
            respostas_index.remove(self.resposta_correta)
            votos_unit = [0, 0, 0, 0]
            votos_porc = [0, 0, 0, 0]
            total_votos = 100  

            probabilidades = [0.4, 0.25, 0.25, 0.1]
            votos_unit[self.resposta_correta] = int(total_votos * probabilidades[0])

            outras_probabilidades = probabilidades[1:]
            random.shuffle(respostas_index)

            for i, j in enumerate(respostas_index):
                votos_unit[j] = int(total_votos * outras_probabilidades[i])

            diff = total_votos - sum(votos_unit)
            if diff != 0:
                votos_unit[self.resposta_correta] += diff

            for index in range(len(votos_unit)):
                votos_porc[index] = (votos_unit[index] / total_votos) * 100

            fig, ax = plt.subplots(figsize=(4.5, 3))

            ax.bar(labels, votos_porc)

            ax.set_xlabel('Respostas')
            ax.set_ylabel('Porcentagem de votos')
            ax.set_title('Opinião da plateia')

            canvas = FigureCanvasTkAgg(fig, master=self.frame_plateia)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=0, columnspan=4, pady=10, sticky="nsew")

    def executa_5050(self):
        indices_excluidos = []
        while len(indices_excluidos) < 2:
            indice = random.randint(0, len(self.respostas) - 1)
            if indice != self.resposta_correta and indice not in indices_excluidos:
                indices_excluidos.append(indice)

        print('iii', indices_excluidos)
        print('rrr', self.resposta_correta)

        for i in indices_excluidos:
            if i == 0:
                self.frame_conteudo.grid_slaves(row=1, column=0)[0].grid_remove()
            elif i == 1:
                self.frame_conteudo.grid_slaves(row=1, column=1)[0].grid_remove()
            elif i == 2:
                self.frame_conteudo.grid_slaves(row=2, column=0)[0].grid_remove()
            elif i == 3:
                self.frame_conteudo.grid_slaves(row=2, column=1)[0].grid_remove()

        self.frame_ajuda.grid_slaves(row=0, column=3)[0].grid_remove()
        
class TelaFim(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master, bg="purple", width=400, height=800)
        self.manager = manager

        respostas = self.manager.jogador.respostas_corretas

        frame_central = tk.Frame(self, bg="purple")
        frame_central.place(relx=0.5, rely=0.5, anchor="center") 

        if respostas == 15:
            mensagem = "Parabéns!\nVocê ganhou 1 milhão de reais!"
        else:
            mensagem = "Você perdeu tudo!\nTente novamente!"
        label_fim = tk.Label(frame_central, text=mensagem, font=("Arial", 18), fg="white", bg="purple")
        label_fim.pack(pady=20)

        if respostas == 15:
            try:
                self.exibir_fogos_artificio(frame_central)
            except Exception as e:
                print("Erro ao carregar a imagem de fogos de artifício:", e)

        botao_reiniciar = tk.Button(frame_central, text="Reiniciar", command=self.reiniciar, width=20, height=2, bg="yellow", fg="black", font=("Arial", 12))  # Define a cor de fundo como amarelo, o texto como preto e a fonte como Arial tamanho 12
        botao_reiniciar.pack(pady=10)

    def exibir_fogos_artificio(self, frame):
        try:

            current_dir = os.getcwd()
            current_dir = current_dir.replace('\\', '/')
            image = Image.open(f'{current_dir}/views/gif_fogos.gif')
            photo = ImageTk.PhotoImage(image)

            label_fogos = tk.Label(frame, image=photo, bg="purple")
            label_fogos.image = photo
            label_fogos.pack()
        except Exception as e:
            raise e

    def reiniciar(self):
        self.manager.contador = 0
        self.manager.perguntas_list = []
        self.destroy()
        self.manager.mudar_tela(TelaInicio(self.master, self.manager))










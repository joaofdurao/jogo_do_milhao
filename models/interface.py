import tkinter as tk

class TelaBoasVindas:
    def __init__(self, root):
        self.root = root
        self.root.title("Bem-vindo ao Quem quer ser um milionário!")
        
        
        self.label_boas_vindas = tk.Label(root, text="Bem-vindo ao Quem quer ser um milionário!", font=("Arial", 18))
        self.label_boas_vindas.pack(pady=20)
        
       
        self.botao_iniciar = tk.Button(root, text="Iniciar", command=self.abrir_introducao)
        self.botao_iniciar.pack(pady=10)
        
    def abrir_introducao(self):
       
        self.root.destroy()
        TelaIntroducao()


def main():
    root = tk.Tk()
    app = TelaBoasVindas(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk

class TelaIntroducao:
    def __init__(self, root):
        self.root = root
        self.root.title("Introdução ao Quem Quer Ser um Milionário")
        
        # Texto de introdução
        introducao_texto = ("Bem-vindo ao 'Quem Quer Ser um Milionário'!\n\n"
                            "Neste jogo, você terá a oportunidade de testar seus conhecimentos em uma série de perguntas de múltipla escolha. "
                            "O objetivo é acumular o máximo de dinheiro possível respondendo corretamente às perguntas.\n\n"
                            "Regras do Jogo:\n"
                            "1. Perguntas: Você será apresentado a uma série de perguntas de múltipla escolha. "
                            "Cada pergunta terá quatro opções de resposta, das quais apenas uma é correta.\n"
                            "2. Prêmios: Cada pergunta terá um valor em dinheiro associado a ela. Se você responder corretamente, ganhará esse valor. "
                            "Quanto mais perguntas você acertar, mais dinheiro acumulará.\n"
                            "3. Ajudas: Durante o jogo, você terá a oportunidade de usar até quatro tipos de ajudas para ajudá-lo a responder às perguntas:\n"
                            "   - Pular Pergunta\n   - Cartas\n   - Ajuda da Plateia\n   - Eliminar Duas Opções\n"
                            "4. Desistir: A qualquer momento, você pode decidir desistir do jogo e sair com o dinheiro acumulado até o momento.\n"
                            "5. Vitória e Derrota: Se você responder corretamente a todas as perguntas, você ganha o prêmio máximo de um milhão de reais! "
                            "No entanto, se responder uma pergunta incorretamente, você perde todo o dinheiro acumulado até o momento.\n\n"
                            "Agora que você conhece as regras, está pronto para começar? Boa sorte!")
        
        # Label para exibir o texto de introdução
        self.label_introducao = tk.Label(root, text=introducao_texto, justify="left", wraplength=600, padx=20, pady=20)
        self.label_introducao.pack()
        
        # Botão para iniciar o jogo
        self.botao_iniciar = tk.Button(root, text="Iniciar Jogo", command=self.iniciar_jogo)
        self.botao_iniciar.pack()
    
    def iniciar_jogo(self):
        # Aqui você pode adicionar o código para iniciar o jogo ou abrir a próxima tela
        # Por exemplo:
        # Fechar a janela atual
        self.root.destroy()
        # Iniciar a próxima tela do jogo
        
def main():
    root = tk.Tk()
    app = TelaIntroducao(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk

class TelaNomeJogador:
    def __init__(self, root):
        self.root = root
        self.root.title("Nome do Jogador")
        
        # Label solicitando o nome do jogador
        self.label_nome = tk.Label(root, text="Digite seu nome:")
        self.label_nome.pack()
        
        # Entry para o jogador digitar seu nome
        self.entry_nome = tk.Entry(root)
        self.entry_nome.pack()
        
        # Botão para confirmar o nome e passar para a próxima tela
        self.botao_confirmar = tk.Button(root, text="Confirmar", command=self.exibir_confirmacao)
        self.botao_confirmar.pack()
    
    def exibir_confirmacao(self):
        nome_jogador = self.entry_nome.get()
        # Fechar a janela atual
        self.root.destroy()
        # Iniciar a próxima tela (Tela de Confirmação)
        TelaConfirmacao(nome_jogador)

class TelaConfirmacao:
    def __init__(self, nome_jogador):
        self.root = tk.Tk()
        self.root.title("Confirmação")
        
        # Label mostrando o nome do jogador e perguntando se está pronto para começar
        mensagem = f"Olá, {nome_jogador}! Você está pronto para começar?"
        self.label_confirmacao = tk.Label(self.root, text=mensagem)
        self.label_confirmacao.pack()
        
        # Botões para iniciar o jogo ou sair
        self.botao_jogar = tk.Button(self.root, text="Jogar", command=self.iniciar_jogo)
        self.botao_jogar.pack(side=tk.LEFT, padx=10)
        self.botao_sair = tk.Button(self.root, text="Sair", command=self.root.quit)
        self.botao_sair.pack(side=tk.RIGHT, padx=10)
    
    def iniciar_jogo(self):
        # Fechar a janela atual
        self.root.destroy()
        # Iniciar a próxima tela do jogo (Tela de Pergunta)

def main():
    root = tk.Tk()
    app = TelaNomeJogador(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    
import tkinter as tk

class TelaPergunta:
    def __init__(self, root, pergunta, opcoes_resposta, valor_pergunta, saldo_atual, callback_resposta):
        self.root = root
        self.root.title("Pergunta")
        
        # Exibir a pergunta atual
        self.label_pergunta = tk.Label(root, text=pergunta)
        self.label_pergunta.pack()
        
        # Exibir opções de resposta
        self.opcoes_resposta = opcoes_resposta
        self.var_resposta = tk.StringVar()
        for opcao in opcoes_resposta:
            radio_button = tk.Radiobutton(root, text=opcao, variable=self.var_resposta, value=opcao)
            radio_button.pack()
        
        # Exibir valor da pergunta e saldo atual
        self.label_valor_pergunta = tk.Label(root, text=f"Valor da Pergunta: R${valor_pergunta}")
        self.label_valor_pergunta.pack()
        
        self.label_saldo_atual = tk.Label(root, text=f"Saldo Atual: R${saldo_atual}")
        self.label_saldo_atual.pack()
        
        # Botão para confirmar a resposta
        self.botao_responder = tk.Button(root, text="Responder", command=self.responder)
        self.botao_responder.pack()
        
        self.callback_resposta = callback_resposta
    
    def responder(self):
        resposta = self.var_resposta.get()
        # Chamar a função de callback para passar a resposta selecionada pelo jogador
        self.callback_resposta(resposta)

def main():
    root = tk.Tk()
    pergunta = "Qual é a capital do Brasil?"
    opcoes_resposta = ["Brasília", "Rio de Janeiro", "São Paulo", "Salvador"]
    valor_pergunta = 1000
    saldo_atual = 0
    def callback_resposta(resposta):
        print("Resposta selecionada:", resposta)
    app = TelaPergunta(root, pergunta, opcoes_resposta, valor_pergunta, saldo_atual, callback_resposta)
    root.mainloop()

if __name__ == "__main__":
    main()

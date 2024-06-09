import mariadb
from repositories.entitydao import EntityDAO

"""
Essa classe representa um objeto de acesso a dados para a entidade 'Pergunta'.
Ela herda da classe 'EntityDAO'.
"""


class PerguntaDAO(EntityDAO):

    def __init__(self):
        """
        Inicializa um objeto PerguntaDAO.

        Args:
        - operation (str): A operação a ser realizada.
        - *args: Argumentos adicionais para a operação.

        """
        super().__init__()

    def create(self, pergunta):
        """
        Cria uma nova pergunta.

        Args:
        - pergunta: A pergunta a ser criada.

        Returns:
        - True se o registro foi criado com sucesso, False caso contrário.

        """
        return super()._create(pergunta)

    def find_by_id(self, pergunta_id):
        """
        Busca uma pergunta pelo ID.

        Args:
        - pergunta_id: O ID da pergunta a ser buscada.

        Returns:
        - A pergunta encontrada ou None, caso não exista.

        """
        return super()._find_by_id(pergunta_id)

    def find_by_dificuldade(self, dificuldade, lista_ids):
        """
        Encontra registros no banco de dados com base na dificuldade fornecida, excluindo os registros cujos IDs estão na lista fornecida.

        Args:
            dificuldade: A dificuldade a ser pesquisada.
            lista_ids: Uma lista de IDs a serem excluídos da pesquisa.

        Returns:
            Uma lista de registros correspondentes, ou None se nenhum for encontrado.
        """
        table_name = "perguntadao_tb"
        query = f"SELECT * FROM {table_name} WHERE dificuldade = %s"
        
        # Se houver IDs a serem excluídos, adicione a cláusula NOT IN
        if lista_ids:
            ids = ', '.join(['%s'] * len(lista_ids))
            query += f" AND id NOT IN ({ids})"
            params = (dificuldade, *lista_ids)
        else:
            params = (dificuldade,)
        
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            if result:
                return result
            else:
                print("Nenhum registro encontrado")
                return None
        except mariadb.Error as e:
            print(f"Erro ao encontrar registros: {e}")
            return None
        finally:
            self.conn.close()

    def update(self, pergunta, pergunta_id):
        """
        Atualiza uma pergunta.

        Args:
        - pergunta: A pergunta a ser atualizada.
        - pergunta_id: O ID da pergunta a ser atualizada.

        Returns:
        - True se a atualização foi bem-sucedida, False caso contrário.

        """
        return super()._update(pergunta, pergunta_id)

    def delete(self, pergunta_id):
        """
        Exclui uma pergunta.

        Args:
        - pergunta_id: O ID da pergunta a ser excluída.

        Returns:
        - True se a pergunta foi excluída com sucesso, False caso contrário.

        """
        return super()._delete(pergunta_id)

    def close_connection(self):
        """
        Fecha a conexão com o banco de dados.

        """
        self.conn.close()
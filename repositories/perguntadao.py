from repositories.entitydao import EntityDAO

"""
Essa classe representa um objeto de acesso a dados para a entidade 'Pergunta'.
Ela herda da classe 'EntityDAO'.
"""


class PerguntaDAO(EntityDAO):

    def __init__(self, operation, *args):
        """
        Inicializa um objeto PerguntaDAO.

        Args:
        - operation (str): A operação a ser realizada.
        - *args: Argumentos adicionais para a operação.

        """
        super().__init__(operation, *args)

    def _create(self, pergunta):
        """
        Cria uma nova pergunta.

        Args:
        - pergunta: A pergunta a ser criada.

        Returns:
        - True se o registro foi criado com sucesso, False caso contrário.

        """
        return super()._create(pergunta)

    def _find_by_id(self, pergunta_id):
        """
        Busca uma pergunta pelo ID.

        Args:
        - pergunta_id: O ID da pergunta a ser buscada.

        Returns:
        - A pergunta encontrada ou None, caso não exista.

        """
        return super()._find_by_id(pergunta_id)

    def _update(self, pergunta, pergunta_id):
        """
        Atualiza uma pergunta.

        Args:
        - pergunta: A pergunta a ser atualizada.
        - pergunta_id: O ID da pergunta a ser atualizada.

        Returns:
        - True se a atualização foi bem-sucedida, False caso contrário.

        """
        return super()._update(pergunta, pergunta_id)

    def _delete(self, pergunta_id):
        """
        Exclui uma pergunta.

        Args:
        - pergunta_id: O ID da pergunta a ser excluída.

        Returns:
        - True se a pergunta foi excluída com sucesso, False caso contrário.

        """
        return super()._delete(pergunta_id)

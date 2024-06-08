"""
Essa classe representa um objeto de acesso a dados para a entidade 'Jogador'.
Ela herda da classe 'EntityDAO'.
"""
from repositories.entitydao import EntityDAO

class JogadorDAO(EntityDAO):
    """
    Classe responsável por realizar operações de acesso a dados para a entidade Jogador.
    """

    def __init__(self, operation, *args):
        """
        Inicializa um objeto JogadorDAO.

        Args:
        - operation (str): A operação a ser realizada.
        - *args: Argumentos adicionais para a operação.

        """
        super().__init__(operation, *args)

    def _create(self, jogador):
        """
        Cria um novo jogador.

        Args:
        - jogador: O jogador a ser criado.

        Returns:
        - True se o registro foi criado com sucesso, False caso contrário.

        """
        return super()._create(jogador)

    def _find_by_id(self, jogador_id):
        """
        Busca um jogador pelo ID.

        Args:
        - jogador_id: O ID do jogador a ser buscado.

        Returns:
        - O jogador encontrado ou None, caso não exista.

        """
        return super()._find_by_id(jogador_id)

    def _update(self, jogador, jogador_id):
        """
        Atualiza um jogador.

        Args:
        - jogador: O jogador a ser atualizado.
        - jogador_id: O ID do jogador a ser atualizado.

        Returns:
        - True se a atualização foi bem-sucedida, False caso contrário.

        """
        return super()._update(jogador, jogador_id)

    def _delete(self, jogador_id):
        """
        Exclui um jogador.

        Args:
        - jogador_id: O ID do jogador a ser excluído.

        Returns:
        - True se o jogador foi excluído com sucesso, False caso contrário.

        """
        return super()._delete(jogador_id)
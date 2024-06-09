from ctypes.util import find_library
import mariadb
from config.cursormariadb import CursorMariaDB
from abc import ABC, abstractmethod

"""
Este módulo contém a classe EntityDAO, que é uma classe abstrata
para Data Access Objects (DAOs) com operações básicas de CRUD.
"""


class EntityDAO(ABC):
    """
    Classe abstrata para Data Access Objects (DAOs) com operações básicas de CRUD.
    """

    def __init__(self):
        """
        Inicializa o DAO com os detalhes da conexão com o banco de dados.

        Args:
            operation: A operação a ser realizada (CREATE, FIND, UPDATE, DELETE).
            *args: Argumentos adicionais baseados na operação.
        """
        self.conn, self.cursor = self._connect()

    def _connect(self):
        """
        Conecta ao banco de dados.

        Returns:
            Os objetos de conexão e cursor do banco de dados.
        """
        return CursorMariaDB().create_connection()

    
    def _create(self, obj):
        """
        Cria um novo registro no banco de dados.

        Args:
            obj: Um objeto contendo os atributos e valores do registro.

        Returns:
            True se o registro foi criado com sucesso, False caso contrário.
        """
        table_name = str(self.__class__.__name__).lower() + "_tb"
        columns = ", ".join([f"{attr}" for attr in vars(obj).keys()])
        values_space = ", ".join("?" * len(vars(obj).keys()))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_space})"
        values = tuple(vars(obj).values())

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Registro criado com sucesso")
            return True
        except mariadb.Error as e:
            print(f"Erro ao criar registro: {e}")
            self.conn.rollback()
            return False
        finally:
            self.conn.close()

    
    def _find_by_id(self, entity_id):
        """
        Encontra um registro no banco de dados com base no ID da entidade fornecido.

        Args:
            entity_id: O ID da entidade a ser pesquisada.

        Returns:
            O registro correspondente, ou None se não encontrado.
        """
        table_name = str(self.__class__.__name__).lower() + "_tb"
        query = f"SELECT * FROM {table_name} WHERE id = %s"
        try:
            self.cursor.execute(query, (entity_id,))
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                print("Registro não encontrado")
                return None
        except mariadb.Error as e:
            print(f"Erro ao encontrar registro: {e}")
            return None
        finally:
            self.conn.close()
    
    def _update(self, obj, entity_id):
        """
        Atualiza um registro no banco de dados com base no ID fornecido.

        Args:
            obj: Um objeto contendo os dados atualizados.
            entity_id: O ID do registro a ser atualizado.

        Returns:
            True se a atualização foi bem-sucedida, False caso contrário.
        """
        obj.id = entity_id
        table_name = str(self.__class__.__name__).lower() + "_tb"
        columns = ", ".join([f"{attr} = ?" for attr in vars(obj).keys()])
        query = f"UPDATE {table_name} SET {columns} WHERE id = {entity_id}"
        values = tuple(vars(obj).values())

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Registro atualizado com sucesso")
            return True
        except mariadb.Error as e:
            print(f"Erro ao atualizar registro: {e}")
            self.conn.rollback()
            return False
        finally:
            self.conn.close()

    
    def _delete(self, entity_id):
        """
        Exclui um registro do banco de dados com base no ID da entidade fornecido.

        Args:
            entity_id: O ID do registro a ser excluído.

        Returns:
            True se a exclusão foi bem-sucedida, False caso contrário.
        """
        table_name = str(self.__class__.__name__).lower() + "_tb"
        query = f"DELETE FROM {table_name} WHERE id = {entity_id}"

        try:
            self.cursor.execute(query)
            self.conn.commit()
            print("Registro excluído com sucesso")
            return True
        except mariadb.Error as e:
            print(f"Erro ao excluir registro: {e}")
            self.conn.rollback()
            return False
        finally:
            self.conn.close()
import logging
import mysql.connector
from mysql.connector import Error

DB_HOST = 'localhost'
DB_USER = 'produtos_user'  # atualize com o seu user da database
DB_PASSWORD = 'senha_segura123'  # atualize com a senha da sua database
DB_DATABASE = 'produtos_database'  # Nome do banco de dados a ser utilizado

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_DATABASE
                )
                logging.info('Conexão com o banco de dados estabelecida.')
            except Error as e:
                logging.error(f'Erro ao conectar ao banco de dados: {e}')
                raise

    def close(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            self.connection = None
            logging.info('Conexão com o banco de dados fechada.')

    def criar_tabela(self):
        tabela_sql = """
        CREATE TABLE IF NOT EXISTS produtos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255),
            link TEXT,
            preco VARCHAR(50)
        )
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(tabela_sql)
            self.connection.commit()
            logging.info('Tabela criada ou já existente.')
        except Error as e:
            logging.error(f'Erro ao criar a tabela: {e}')
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def inserir_produto(self, dados: dict):
        cursor = self.connection.cursor()
        insert_sql = """
        INSERT INTO produtos (
            nome,
            link,
            preco
        ) VALUES (%s, %s, %s)
        """
        valores = (dados['nome'], dados['link'], dados['preco'])
        try:
            cursor.execute(insert_sql, valores)
            self.connection.commit()
            logging.info(f"Produto '{dados['nome']}' inserido no banco de dados.")
        except Error as e:
            logging.error(f"Erro ao inserir o produto '{dados['nome']}': {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def load_data(self):
        cursor = self.connection.cursor()
        select_sql = "SELECT nome, link, preco FROM produtos"
        try:
            cursor.execute(select_sql)
            rows = cursor.fetchall()
            logging.info('Dados carregados do banco de dados.')
            return rows
        except Error as e:
            logging.error(f'Erro ao carregar dados do banco: {e}')
            raise
        finally:
            cursor.close()

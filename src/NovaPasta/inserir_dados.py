import mysql.connector
from mysql.connector import Error

# Função para conectar ao banco de dados
def criar_conexao():
    try:
        conexao = mysql.connector.connect(
            host='localhost',           # Endereço do servidor MySQL (localhost se estiver no mesmo computador)
            user='root',   # Nome de usuário MySQL
            password='', # Senha do usuário
            database='agricultura_db'   # Nome do banco de dados
        )
        if conexao.is_connected():
            print("Conexão bem-sucedida!")
            return conexao
    except Error as e:
        print("Erro ao conectar ao MySQL:", e)
        return None

# Função para inserir dados na tabela
def inserir_dados(umidade, temperatura, nivel_pH, nutriente_P, nutriente_K):
    conexao = criar_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            comando_sql = """
            INSERT INTO dados_sensores (umidade, temperatura, nivel_pH, nutriente_P, nutriente_K)
            VALUES (%s, %s, %s, %s, %s)
            """
            valores = (umidade, temperatura, nivel_pH, nutriente_P, nutriente_K)
            cursor.execute(comando_sql, valores)
            conexao.commit()
            print("Dados inseridos com sucesso!")
        except Error as e:
            print("Erro ao inserir dados:", e)
        finally:
            cursor.close()
            conexao.close()

# Exemplo de uso: substitua pelos dados do ESP32
umidade = 40.0
temperatura = 24.0
nivel_pH = 5.0
nutriente_P = True  # True para detectado, False para não detectado
nutriente_K = False

inserir_dados(umidade, temperatura, nivel_pH, nutriente_P, nutriente_K)

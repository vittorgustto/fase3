from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Função para conectar ao banco de dados
def criar_conexao():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',               # Substitua com seu usuário
            password='',               # Coloque a senha do usuário ou deixe vazio
            database='agricultura_db'
        )
        print("Conexão com o banco de dados estabelecida.")
        return conexao
    except Error as e:
        print("Erro ao conectar ao MySQL:", e)
        return None

# Rota para receber os dados do ESP32 em JSON
@app.route('/inserir_dados', methods=['POST'])
def receber_dados():
    print("Requisição recebida na rota /inserir_dados")  # Log de requisição recebida

    # Verifica se o conteúdo é JSON
    if request.is_json:
        dados = request.get_json()
        print("Dados recebidos:", dados)  # Log para ver os dados recebidos

        umidade = dados.get('umidade')
        temperatura = dados.get('temperatura')
        nivel_pH = dados.get('pH')
        nutriente_P = dados.get('P')
        nutriente_K = dados.get('K')
        irrigacaoAtiva = dados.get('irrigacaoAtiva')

        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                comando_sql = """
                INSERT INTO dados_sensores (umidade, temperatura, nivel_pH, nutriente_P, nutriente_K, irrigacaoAtiva)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                valores = (umidade, temperatura, nivel_pH, nutriente_P, nutriente_K, irrigacaoAtiva)
                cursor.execute(comando_sql, valores)
                conexao.commit()
                cursor.close()
                print("Dados inseridos no banco com sucesso.")  # Log de sucesso
                return jsonify({"message": "Dados inseridos com sucesso!"}), 200
            except Error as e:
                print(f"Erro ao inserir dados: {e}")  # Log de erro
                return jsonify({"error": f"Erro ao inserir dados: {e}"}), 500
            finally:
                conexao.close()
                print("Conexão com o banco de dados fechada.")  # Log de encerramento
        else:
            print("Erro ao conectar ao banco de dados")  # Log de erro de conexão
            return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
    else:
        print("Formato de dados não é JSON.")  # Log de erro de formato
        return jsonify({"error": "Formato de dados inválido. Use JSON."}), 400

# Rota de teste de conexão
@app.route('/teste', methods=['GET'])
def teste_conexao():
    print("Rota de teste acessada.")
    return "Conexão bem-sucedida", 200

if __name__ == '__main__':
    print("Servidor Flask iniciado.")
    app.run(host='0.0.0.0', port=5000)

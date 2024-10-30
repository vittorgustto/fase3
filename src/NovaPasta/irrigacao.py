import mysql.connector
from datetime import datetime

# Conexão com o banco de dados
db = mysql.connector.connect(
    host="localhost",     # Ou o IP do seu servidor
    user="root",          # Nome do usuário
    password="",          # Senha do usuário (deixe vazio se não houver)
    database="irrigacao"  # Nome do banco de dados
)

cursor = db.cursor()

# Função para inserir dados (Create)
def inserir_dados(umidade, temperatura, nivel_pH, nutriente_P, nutriente_K):
    sql = """
    INSERT INTO sensores (umidade, temperatura, nivel_ph, nutriente_P, nutriente_K)
    VALUES (%s, %s, %s, %s, %s)
    """
    valores = (umidade, temperatura, nivel_pH, nutriente_P, nutriente_K)
    cursor.execute(sql, valores)
    db.commit()
    print(f"{cursor.rowcount} registro(s) inserido(s).")

# Função para ler dados (Read)
def ler_dados():
    cursor.execute("SELECT * FROM sensores")
    resultados = cursor.fetchall()
    for linha in resultados:
        print(linha)

# Função para atualizar dados (Update)
def atualizar_dados(id, umidade=None, temperatura=None, nivel_pH=None, nutriente_P=None, nutriente_K=None):
    campos = []
    valores = []
    
    if umidade is not None:
        campos.append("umidade = %s")
        valores.append(umidade)
    if temperatura is not None:
        campos.append("temperatura = %s")
        valores.append(temperatura)
    if nivel_pH is not None:
        campos.append("nivel_ph = %s")
        valores.append(nivel_pH)
    if nutriente_P is not None:
        campos.append("nutriente_P = %s")
        valores.append(nutriente_P)
    if nutriente_K is not None:
        campos.append("nutriente_K = %s")
        valores.append(nutriente_K)

    valores.append(id)
    sql = f"UPDATE sensores SET {', '.join(campos)} WHERE id = %s"
    cursor.execute(sql, tuple(valores))
    db.commit()
    print(f"{cursor.rowcount} registro(s) atualizado(s).")

# Função para excluir dados (Delete)
def excluir_dados(id):
    sql = "DELETE FROM sensores WHERE id = %s"
    cursor.execute(sql, (id,))
    db.commit()
    print(f"{cursor.rowcount} registro(s) excluído(s).")

# Exemplos de uso
# Inserir dados
inserir_dados(55.0, 22.5, 7.2, True, False)

# Ler todos os dados
ler_dados()

# Atualizar dados do registro com id = 1
atualizar_dados(id=1, umidade=60.0, temperatura=24.0)

# Excluir o registro com id = 1
excluir_dados(id=1)

# Fechar a conexão
cursor.close()
db.close()
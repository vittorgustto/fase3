import mysql.connector
from mysql.connector import Error

# Configuração de conexão com o banco de dados
try:
    connection = mysql.connector.connect(
        host='localhost',  # ou o IP do servidor
        user='root',
        password='',
        database='agricultura_db'
    )

    if connection.is_connected():
        print("Conectado ao banco de dados")

except Error as e:
    print("Erro ao conectar ao banco de dados", e)

# Função para inserir dados de sensores
def inserir_dados_sensores(umidade, nivel_ph, nutriente_P, nutriente_K, temperatura):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO dados_sensores (umidade, nivel_ph, nutriente_P, nutriente_K, temperatura)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (umidade, nivel_ph, nutriente_P, nutriente_K, temperatura)
        cursor.execute(query, valores)
        connection.commit()
        print("Dados inseridos com sucesso")
    except Error as e:
        print("Erro ao inserir dados", e)

# Função para consultar o histórico de irrigação
def consultar_historico_irrigacao():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM historico_irrigacao")
        registros = cursor.fetchall()
        for registro in registros:
            print(registro)
    except Error as e:
        print("Erro ao consultar histórico de irrigação", e)

# Função para controlar a irrigação
def controlar_irrigacao(umidade, nivel_ph, nutriente_P, nutriente_K):
    # Defina seus limites
    limite_umidade = 30.0  # Exemplo: ativar irrigação se umidade < 30%
    limite_ph = 6.0  # pH ideal
    nutriente_adequado = nutriente_P and nutriente_K  # Os nutrientes devem estar presentes

    # Lógica de decisão
    if umidade < limite_umidade or nivel_ph < limite_ph or not nutriente_adequado:
        print("Irrigação ligada")
        status_relé = True  # Aqui você acionaria o relé
    else:
        print("Irrigação desligada")
        status_relé = False

    # Salvar o estado da irrigação no banco de dados
    salvar_historico_irrigacao(status_relé)

# Função para salvar o estado da irrigação
def salvar_historico_irrigacao(status_relé):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO historico_irrigacao (status_relé)
            VALUES (%s)
        """
        cursor.execute(query, (status_relé,))
        connection.commit()
        print("Estado da irrigação salvo com sucesso")
    except Error as e:
        print("Erro ao salvar estado da irrigação", e)

# Função para atualizar dados de sensores
def atualizar_dados_sensor(id, umidade=None, nivel_ph=None, nutriente_P=None, nutriente_K=None, temperatura=None):
    try:
        cursor = connection.cursor()
        query = "UPDATE dados_sensores SET "
        valores = []

        if umidade is not None:
            query += "umidade = %s, "
            valores.append(umidade)
        if nivel_ph is not None:
            query += "nivel_ph = %s, "
            valores.append(nivel_ph)
        if nutriente_P is not None:
            query += "nutriente_P = %s, "
            valores.append(nutriente_P)
        if nutriente_K is not None:
            query += "nutriente_K = %s, "
            valores.append(nutriente_K)
        if temperatura is not None:
            query += "temperatura = %s, "
            valores.append(temperatura)

        query = query.rstrip(", ")  # Remove a última vírgula e espaço
        query += " WHERE id = %s"
        valores.append(id)

        cursor.execute(query, valores)
        connection.commit()
        print("Dados atualizados com sucesso")
    except Error as e:
        print("Erro ao atualizar dados", e)

# Função para deletar dados de sensores
def deletar_dados_sensor(id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM dados_sensores WHERE id = %s"
        cursor.execute(query, (id,))
        connection.commit()
        print("Dados deletados com sucesso")
    except Error as e:
        print("Erro ao deletar dados", e)

# Função principal
if __name__ == "__main__":
    # Exemplo de uso (substitua pelos dados reais lidos do Monitor Serial)
    umidade = float(input("Digite o valor da umidade: "))  # Insira a umidade manualmente
    nivel_ph = float(input("Digite o valor do pH: "))  # Insira o pH manualmente
    nutriente_P = input("Nutriente P está presente? (True/False): ") == 'True'  # Insira manualmente
    nutriente_K = input("Nutriente K está presente? (True/False): ") == 'True'  # Insira manualmente
    temperatura = float(input("Digite a temperatura: "))  # Insira a temperatura manualmente

    # Inserir dados dos sensores no banco de dados
    inserir_dados_sensores(umidade, nivel_ph, nutriente_P, nutriente_K, temperatura)

    # Controlar a irrigação com base nos dados inseridos
    controlar_irrigacao(umidade, nivel_ph, nutriente_P, nutriente_K)

    # Consultar histórico de irrigação
    consultar_historico_irrigacao()

    # Exemplos de chamadas para atualizar e deletar dados
    # Atualizar um dado de sensor (substitua pelo ID e dados desejados)
    id_para_atualizar = int(input("Digite o ID do sensor que deseja atualizar: "))
    nova_umidade = input("Digite a nova umidade (pressione Enter para não atualizar): ")
    novo_nivel_ph = input("Digite o novo pH (pressione Enter para não atualizar): ")
    novo_nutriente_P = input("Novo nutriente P está presente? (True/False) (pressione Enter para não atualizar): ")
    novo_nutriente_K = input("Novo nutriente K está presente? (True/False) (pressione Enter para não atualizar): ")
    nova_temperatura = input("Digite a nova temperatura (pressione Enter para não atualizar): ")

    atualizar_dados_sensor(
        id_para_atualizar,
        umidade=float(nova_umidade) if nova_umidade else None,
        nivel_ph=float(novo_nivel_ph) if novo_nivel_ph else None,
        nutriente_P=(novo_nutriente_P == "True") if novo_nutriente_P else None,
        nutriente_K=(novo_nutriente_K == "True") if novo_nutriente_K else None,
        temperatura=float(nova_temperatura) if nova_temperatura else None
    )

    # Deletar um dado de sensor (substitua pelo ID que deseja deletar)
    id_para_deletar = int(input("Digite o ID do sensor que deseja deletar: "))
    deletar_dados_sensor(id_para_deletar)

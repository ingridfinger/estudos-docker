import os # Acessa variáveis de ambiente
import pymysql # Realiza a conexão
import time # Permite aguardar alguns segundos

# Configurações de conexão com o banco de dados
# Recupera os dados de conexão sem deixar as credenciais escritas diretamente no código
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")

# Estabelece a conexão com o MySQL
def conectar():
    conexao = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=3306
    )

    return conexao


# Aguarda o banco de dados estar disponível
# Tenta conectar novamente a cada três segundos caso o banco ainda não esteja disponível
while True:
    try:
        conexao = conectar()
        print("Conexão com o MySQL estabelecida!")

        cursor = conexao.cursor()
        # Recupera os registros da tabela
        cursor.execute("SELECT * FROM beneficiarios;")

        # Retorna os registros encontrados
        resultados = cursor.fetchall()

        print("\nBeneficiários cadastrados:")

        for beneficiario in resultados:
            print(beneficiario)

        # Fecha o cursor e a conexão depois da consulta
        cursor.close()
        conexao.close()
        break

    except pymysql.MySQLError as erro:
        print(f"Aguardando MySQL... {erro}")
        time.sleep(3)

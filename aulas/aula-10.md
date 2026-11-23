# 🐳 Aula 10 — Comunicação entre containers

> 🌷 Aprendendo a conectar containers por meio das redes Docker, integrar uma aplicação Python a um banco de dados MySQL e utilizar o Docker Compose para gerenciar múltiplos serviços.

---

## 🩷 1. Introdução à comunicação entre containers

Em projetos que utilizam Docker, é comum que uma aplicação seja dividida em diferentes serviços, cada um executando em seu próprio container.

Por exemplo, uma aplicação pode possuir:

- Um container responsável pelo backend;
- Um container responsável pelo banco de dados;
- Um container responsável pelo servidor web.

Para que esses serviços trabalhem juntos, é necessário permitir a comunicação entre seus containers.

O Docker oferece redes virtuais que possibilitam essa comunicação de maneira isolada e organizada.

Nesta aula, aprofundamos o uso das redes Docker e desenvolvemos uma aplicação Python que se conecta a um banco de dados MySQL.

## 🧩 2. Revisando as redes do Docker

Na Aula 06, aprendemos que os containers podem se comunicar por meio de uma rede Docker.

Quando utilizamos o Docker Compose, uma rede padrão é criada automaticamente para os serviços definidos no arquivo `compose.yaml`.

Essa rede permite que os containers se comuniquem utilizando os nomes dos serviços como endereços.

### 🌐 Comunicação pelo nome do serviço

No projeto da Aula 09, tínhamos um serviço chamado `db`, responsável pelo MySQL.

Por isso, outros containers conectados à mesma rede poderiam acessar o banco utilizando o endereço:

```text
db:3306
```

Nesse endereço:

- `db`: nome do serviço no Docker Compose;
- `3306`: porta utilizada pelo MySQL.

**Observação:** dentro de uma rede Docker, utilizamos o nome do serviço para localizar outro container, em vez de depender diretamente de seu endereço IP.

## 🔎 3. Testando a comunicação com o MySQL

Antes de desenvolver nossa aplicação Python, realizamos alguns testes para verificar a comunicação com o banco de dados da Aula 09.

### Conferindo o container MySQL

Primeiro, verificamos se o banco estava em execução:

```powershell
docker compose ps
```

O container `mysql-estudos` estava em execução, disponibilizando a porta `3306`.

### Consultando o hostname do container

Para verificar a identificação do container MySQL, utilizamos:

```powershell
docker compose exec db mysql -u aluna -p -e "SELECT @@hostname;"
```

O comando retornou um hostname gerado pelo Docker para o container.

### Testando a resolução DNS

Em seguida, utilizamos o BusyBox para consultar o endereço do serviço `db`:

```powershell
docker run --rm --network aula-09_default busybox nslookup db
```

O resultado mostrou que o nome `db` foi resolvido para o endereço IP `172.18.0.2`.

Também identificamos o servidor DNS interno do Docker:

```text
127.0.0.11
```

Isso demonstrou que o Docker possui um serviço DNS interno para resolver os nomes dos serviços na rede.

### Testando a porta do MySQL

Para verificar se a porta `3306` estava acessível, executamos:

```powershell
docker run --rm --network aula-09_default busybox nc -zvw 3 db 3306
```

O resultado confirmou que a porta estava aberta:

```text
db (172.18.0.2:3306) open
```

### Testando uma conexão real com o banco

Por fim, utilizamos outro container com a imagem do MySQL para estabelecer uma conexão:

```powershell
docker run --rm -it --network aula-09_default mysql:8.4 mysql -h db -P 3306 -u aluna -p
```

Após informar a senha, conseguimos acessar o MySQL e executar consultas SQL.

Os testes confirmaram que:

1. O serviço `db` podia ser localizado pelo DNS do Docker;
2. A porta `3306` estava acessível;
3. Era possível estabelecer uma conexão com o servidor MySQL a partir de outro container.

**Observação:** utilizamos `--network aula-09_default` para conectar os containers temporários à rede criada pelo projeto da Aula 09.

## 🖥️ 4. Criando o projeto da Aula 10

Depois de confirmar a comunicação entre containers, começamos a desenvolver uma aplicação Python integrada ao MySQL.

Criamos uma pasta chamada `aula-10` para organizar o projeto.

A estrutura ficou assim:

```text
aula-10/
├── .env
├── .env.example
├── compose.yaml
├── Dockerfile
└── app/
    ├── app.py
    └── requirements.txt
```

### 📂 Entendendo os arquivos

| Arquivo | Função |
| :------ | :---- |
| `.env` | Armazena as variáveis de ambiente utilizadas na configuração. |
| `.env.example` | Apresenta um modelo das variáveis necessárias, sem utilizar as senhas reais. |
| `compose.yaml` | Define os serviços e as configurações dos containers. |
| `Dockerfile` | Contém as instruções para construir a imagem da aplicação Python. |
| `app.py` | Contém o código da aplicação. |
| `requirements.txt` | Lista as dependências Python necessárias. |

## 🔐 5. Configurando as variáveis de ambiente

Criamos o arquivo `.env` para armazenar as configurações de conexão com o banco de dados.

**Conteúdo do arquivo `.env`:**

```env
DB_HOST=db
MYSQL_DATABASE=estudos_docker
MYSQL_USER=aluna
MYSQL_PASSWORD=senha_aluna_estudo
MYSQL_ROOT_PASSWORD=senha_root_estudo
```

### 🔍 Entendendo as variáveis

| Variável | Função |
| :------- | :---- |
| `DB_HOST` | Define o endereço do serviço MySQL. |
| `MYSQL_DATABASE` | Informa o banco de dados utilizado pela aplicação. |
| `MYSQL_USER` | Define o usuário utilizado na conexão. |
| `MYSQL_PASSWORD` | Armazena a senha do usuário. |
| `MYSQL_ROOT_PASSWORD` | Define a senha do usuário administrador do MySQL. |

O valor `db` em `DB_HOST` corresponde ao nome do serviço MySQL definido no Docker Compose.

### 📄 Arquivo .env.example

Também criamos um arquivo `.env.example` para documentar as variáveis necessárias ao funcionamento do projeto.

```env
DB_HOST=db
MYSQL_DATABASE=estudos_docker
MYSQL_USER=aluna
MYSQL_PASSWORD=sua_senha_aqui
MYSQL_ROOT_PASSWORD=sua_senha_root_aqui
```

**Observação:** o arquivo `.env` contém credenciais e não deve ser publicado no GitHub. Como já configuramos o `.gitignore` na raiz do repositório, ele é ignorado pelo Git.

## 🐍 6. Desenvolvendo a aplicação Python

Para permitir que a aplicação se conectasse ao MySQL, utilizamos a biblioteca **PyMySQL**.

### 📄 Arquivo requirements.txt

Criamos o arquivo `app/requirements.txt` com a dependência:

```text
PyMySQL
```

Essa biblioteca permite que programas Python estabeleçam conexões com bancos de dados MySQL e executem consultas SQL.

### 📄 Arquivo app.py

Em seguida, desenvolvemos a aplicação Python:

```python
import os  # Acessa variáveis de ambiente
import pymysql  # Realiza a conexão
import time  # Permite aguardar alguns segundos

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
```

### 🔍 Entendendo o código

| Elemento | Função |
| :------- | :---- |
| `os` | Permite acessar variáveis de ambiente. |
| `pymysql` | Permite estabelecer a conexão com o MySQL. |
| `time` | Permite controlar o intervalo entre as tentativas de conexão. |
| `os.getenv()` | Recupera o valor de uma variável de ambiente. |
| `pymysql.connect()` | Estabelece a conexão com o banco de dados. |
| `cursor()` | Cria um cursor para executar comandos SQL. |
| `execute()` | Executa uma consulta SQL. |
| `fetchall()` | Recupera todos os registros retornados pela consulta. |
| `close()` | Encerra o cursor ou a conexão. |
| `time.sleep(3)` | Aguarda três segundos antes de tentar novamente. |

### 🌸 Entendendo a lógica de conexão

A aplicação utiliza um laço `while` para tentar estabelecer a conexão com o MySQL.

Caso o banco ainda não esteja disponível, ocorre uma exceção que é tratada pelo `except`.

Nesse caso, a aplicação apresenta uma mensagem informando que está aguardando o MySQL e realiza uma nova tentativa após três segundos.

Quando a conexão é estabelecida, a aplicação:

1. Cria um cursor;
2. Executa uma consulta na tabela `beneficiarios`;
3. Recupera os registros encontrados;
4. Exibe os resultados no terminal;
5. Fecha o cursor e a conexão;
6. Encerra o laço com `break`.

## 🐳 7. Criando o Dockerfile da aplicação

Para construir a imagem da aplicação Python, criamos um arquivo chamado `Dockerfile` na pasta `aula-10`.

**Conteúdo do Dockerfile:**

```dockerfile
# Utiliza uma imagem oficial do Python como base
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para dentro do container
COPY app/requirements.txt .

# Instala as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para dentro do container
COPY app/ .

# Define o comando executado quando o container iniciar
CMD ["python", "app.py"]
```

### 🔍 Entendendo as instruções

| Instrução | Função |
| :-------- | :---- |
| `FROM` | Define a imagem base do Python. |
| `WORKDIR` | Define o diretório de trabalho dentro do container. |
| `COPY` | Copia arquivos do computador para dentro da imagem. |
| `RUN` | Executa comandos durante a construção da imagem. |
| `CMD` | Define o comando padrão executado quando o container inicia. |

Utilizamos a imagem `python:3.12-slim` como base, instalamos a biblioteca PyMySQL e copiamos o código da aplicação para dentro da imagem.

## ⚙️ 8. Configurando os serviços no Docker Compose

Com a aplicação preparada, criamos o arquivo `compose.yaml` para gerenciar os dois serviços: MySQL e Python.

**Conteúdo do arquivo `compose.yaml`:**

```yaml
services:
  # Serviço responsável pelo banco de dados
  db:
    # Imagem oficial do MySQL, versão 8.4
    image: mysql:8.4

    # Nome personalizado do container
    container_name: mysql-aula10

    # Reinicia automaticamente, exceto quando parado manualmente
    restart: unless-stopped

    # Carrega as configurações do arquivo .env
    env_file:
      - .env

    # Mapeia a porta 3306 do computador para o container
    ports:
      - "3306:3306"

    # Utiliza o volume da Aula 09 para preservar os dados
    volumes:
      - mysql_data:/var/lib/mysql

    # Verifica se o MySQL está pronto para receber conexões
    healthcheck:
      # Comando utilizado para verificar a saúde do MySQL
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p${MYSQL_ROOT_PASSWORD}"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 30s

  # Serviço responsável pela aplicação Python
  app:
    # Constrói a imagem utilizando o Dockerfile do projeto
    build:
      context: .
      dockerfile: Dockerfile

    # Nome personalizado do container
    container_name: app-aula10

    # Reinicia a aplicação caso ela falhe
    restart: on-failure

    # Disponibiliza somente as variáveis necessárias à aplicação
    environment:
      DB_HOST: db
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}

    # Aguarda o MySQL ficar saudável antes de iniciar
    depends_on:
      db:
        condition: service_healthy

# Declaração dos volumes utilizados pelo projeto
volumes:
  mysql_data:
    # Informa que o volume já existe e não deve ser criado novamente
    external: true

    # Nome exato do volume criado na Aula 09
    name: aula-09_mysql_data
```

### 🔍 Entendendo a configuração

| Configuração | Função |
| :----------- | :---- |
| `services` | Define os serviços do projeto. |
| `db` | Identifica o serviço responsável pelo MySQL. |
| `app` | Identifica o serviço responsável pela aplicação Python. |
| `image` | Define a imagem utilizada pelo serviço. |
| `build` | Informa como a imagem da aplicação será construída. |
| `container_name` | Define um nome personalizado para o container. |
| `restart` | Define a política de reinicialização do container. |
| `env_file` | Carrega as variáveis do arquivo `.env` no serviço MySQL. |
| `environment` | Define as variáveis de ambiente disponibilizadas à aplicação. |
| `ports` | Publica a porta do MySQL no computador. |
| `volumes` | Associa um volume ao diretório de dados do banco. |
| `healthcheck` | Verifica se o serviço MySQL está saudável. |
| `depends_on` | Define a dependência entre os serviços. |

### 🌸 Entendendo o healthcheck

O `healthcheck` permite verificar se o MySQL está pronto para receber conexões.

Utilizamos o comando `mysqladmin ping` para verificar a disponibilidade do servidor.

Também definimos:

- `interval`: intervalo entre as verificações;
- `timeout`: tempo máximo permitido para cada verificação;
- `retries`: quantidade de tentativas antes de considerar a verificação malsucedida;
- `start_period`: período inicial concedido ao serviço para iniciar.

### 🔗 Entendendo o depends_on

A configuração:

```yaml
depends_on:
  db:
    condition: service_healthy
```

indica que a aplicação deve aguardar até que o serviço `db` seja considerado saudável pelo healthcheck.

Isso é importante porque iniciar um container não significa necessariamente que a aplicação dentro dele já esteja pronta para receber conexões.

**Observação:** o `depends_on` com `service_healthy` ajuda a controlar a ordem de inicialização, enquanto o código Python também possui tentativas de reconexão como proteção adicional.

### 💾 Reutilizando o volume da Aula 09

Nesta prática, decidimos utilizar o mesmo volume criado anteriormente:

```yaml
volumes:
  mysql_data:
    external: true
    name: aula-09_mysql_data
```

A opção `external: true` informa ao Docker Compose que o volume já existe e deve ser utilizado, em vez de criar um novo.

Assim, conseguimos acessar os dados cadastrados durante a Aula 09.

## 🚀 9. Construindo e iniciando os serviços

Com os arquivos preparados, validamos a configuração:

```powershell
docker compose config
```

O comando apresentou a configuração final interpretada pelo Docker Compose, permitindo conferir os serviços, as variáveis de ambiente, as dependências e o volume utilizado.

Em seguida, construímos a imagem da aplicação e iniciamos os serviços:

```powershell
docker compose up -d --build
```

### 🔍 Entendendo o comando

| Parte | Função |
| :---- | :---- |
| `docker compose up` | Cria e inicia os serviços definidos no Compose. |
| `-d` | Executa os containers em segundo plano. |
| `--build` | Constrói ou atualiza as imagens antes de iniciar os serviços. |

Durante a inicialização, o Docker Compose:

1. Criou a rede padrão do projeto;
2. Utilizou o volume externo `aula-09_mysql_data`;
3. Iniciou o serviço MySQL;
4. Verificou a saúde do banco de dados;
5. Iniciou a aplicação Python após o MySQL ficar saudável.

### Conferindo os containers

Utilizamos:

```powershell
docker compose ps
```

Como a aplicação Python executa uma consulta e termina, também utilizamos:

```powershell
docker compose ps -a
```

O resultado mostrou:

- `mysql-aula10`: em execução e com status `healthy`;
- `app-aula10`: finalizado com código de saída `0`.

**Observação:** o status `Exited (0)` da aplicação Python não representa um erro. Como o programa foi desenvolvido para executar uma consulta, apresentar os resultados e encerrar, ele termina normalmente após concluir sua tarefa.

## 🔎 10. Verificando os resultados da aplicação

Para conferir o que aconteceu durante a execução do programa, consultamos os logs da aplicação:

```powershell
docker compose logs app
```

O resultado foi:

```text
app-aula10  | Conexão com o MySQL estabelecida!
app-aula10  |
app-aula10  | Beneficiários cadastrados:
app-aula10  | (2, 'Maria Souza', 'Tres Lagoas')
```

Isso confirmou que a aplicação Python conseguiu:

1. Localizar o serviço MySQL pelo nome `db`;
2. Estabelecer uma conexão com o banco;
3. Executar a consulta SQL;
4. Recuperar os registros da tabela `beneficiarios`;
5. Exibir os resultados no terminal.

### Conferindo os logs do MySQL

Também verificamos os logs do banco:

```powershell
docker compose logs db
```

Entre as mensagens apresentadas, encontramos:

```text
ready for connections. Version: '8.4.13'
```

Essa mensagem confirmou que o servidor MySQL estava pronto para receber conexões.

## 🗄️ 11. Confirmando a persistência dos dados

Como reutilizamos o volume da Aula 09, também verificamos se os registros continuavam disponíveis.

Executamos:

```powershell
docker compose exec db mysql -u aluna -p -D estudos_docker -e "SELECT * FROM beneficiarios;"
```

### Entendendo o comando

| Parte | Função |
| :---- | :---- |
| `docker compose exec` | Executa um comando dentro de um container em execução. |
| `db` | Identifica o serviço MySQL. |
| `mysql` | Inicia o cliente de linha de comando do MySQL. |
| `-u aluna` | Informa o usuário utilizado na conexão. |
| `-p` | Solicita a senha do usuário. |
| `-D estudos_docker` | Seleciona o banco de dados utilizado na consulta. |
| `-e` | Permite executar uma instrução SQL diretamente pelo terminal. |

O resultado foi:

```text
+----+-------------+-------------+
| id | nome        | municipio   |
+----+-------------+-------------+
|  2 | Maria Souza | Tres Lagoas |
+----+-------------+-------------+
```

O registro de Maria Souza continuava armazenado, confirmando que o volume da Aula 09 foi reutilizado corretamente.

**Observação:** ao executar uma consulta diretamente pelo terminal, precisamos selecionar o banco de dados com `-D` ou utilizar `USE estudos_docker;` antes da consulta. Caso contrário, o MySQL pode apresentar o erro `No database selected`.

## 🧠 12. Entendendo a arquitetura do projeto

Ao finalizar a prática, conseguimos visualizar como os diferentes componentes trabalham juntos.

```text
                 DOCKER COMPOSE
                       |
             Rede: aula-10_default
                       |
             +---------+---------+
             |                   |
             v                   v
      +-------------+     +-------------+
      |  Container  |     |  Container  |
      |  Python     |---->|   MySQL     |
      |             |     |             |
      |  app.py     |     |  Porta 3306 |
      +-------------+     +-------------+
                                |
                                v
                       +----------------+
                       | Volume externo |
                       | aula-09_mysql  |
                       | _data          |
                       +----------------+
```

A aplicação Python utiliza o endereço `db` para localizar o MySQL dentro da rede Docker.

O banco de dados, por sua vez, utiliza o volume externo para manter os registros armazenados.

Dessa forma, cada serviço possui sua própria responsabilidade, mas ambos conseguem trabalhar juntos por meio da rede Docker.

## 📝 13. Resumo da aula

- 🌐 Redes Docker permitem a comunicação entre containers.
- 🔎 O Docker possui DNS interno para resolver nomes de serviços.
- 🐳 Containers conectados à mesma rede podem se comunicar utilizando o nome do serviço.
- 🔌 O MySQL utiliza a porta `3306`.
- 🐍 É possível desenvolver aplicações Python que se conectam a bancos de dados MySQL.
- 📦 A biblioteca PyMySQL permite estabelecer conexões e executar consultas SQL.
- ⚙️ Docker Compose permite gerenciar múltiplos serviços em um mesmo projeto.
- 💗 `healthcheck` verifica se um serviço está saudável.
- 🔗 `depends_on` com `service_healthy` permite aguardar a disponibilidade do banco antes de iniciar a aplicação.
- 💾 Volumes externos permitem reutilizar dados entre diferentes projetos Compose.
- 📋 `docker compose logs` permite acompanhar a execução dos serviços.
- ✨ O status `Exited (0)` indica que a aplicação terminou normalmente.

---

🐳 **Fim da Aula 10** 🐳
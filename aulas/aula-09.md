# 🐳 Aula 09 — Docker Compose com MySQL

> 🌷 Aprendendo a executar um banco de dados MySQL em um container Docker, configurar variáveis de ambiente, manipular dados com SQL e garantir sua persistência utilizando volumes.

---

## 🩷 1. Introdução ao MySQL

O **MySQL** é um sistema gerenciador de banco de dados relacional (SGBD) que utiliza SQL (*Structured Query Language*) para criar, consultar e manipular dados.

Em bancos relacionais, as informações são organizadas em tabelas, compostas por linhas e colunas.

Nesta aula, utilizamos o MySQL dentro de um container Docker, gerenciado pelo Docker Compose.

## 🧩 2. Preparando o projeto

Criamos uma pasta chamada `aula-09` para organizar os arquivos da prática.

A estrutura inicial ficou assim:

```text
aula-09/
├── .env
└── compose.yaml
```

Também baixamos a imagem do MySQL:

```powershell
docker pull mysql:8.4
```

Utilizamos a versão `8.4` para definir uma versão específica da imagem, evitando depender da tag genérica `latest`.

A imagem foi baixada com sucesso e ficou disponível localmente.

## 🔐 3. Configurando as variáveis de ambiente

Criamos um arquivo chamado `.env` para armazenar as configurações utilizadas pelo MySQL.

**Conteúdo do arquivo `.env`:**

```env
MYSQL_ROOT_PASSWORD=sua_senha_root
MYSQL_DATABASE=estudos_docker
MYSQL_USER=aluna
MYSQL_PASSWORD=sua_senha_usuario
```

### 🔍 Entendendo as variáveis

| Variável              | Função                                                           |
| :-------------------- | :--------------------------------------------------------------- |
| `MYSQL_ROOT_PASSWORD` | Define a senha do usuário administrador `root`.                  |
| `MYSQL_DATABASE`      | Define o banco de dados que será criado durante a inicialização. |
| `MYSQL_USER`          | Define um usuário adicional.                                     |
| `MYSQL_PASSWORD`      | Define a senha do usuário adicional.                             |

**Observação:** os valores de senha acima são exemplos. As senhas utilizadas na prática foram apenas credenciais fictícias para o ambiente local.

O arquivo `.env` não deve ser publicado no GitHub, pois pode conter informações sensíveis.

Como já configuramos o `.gitignore` na raiz do repositório, arquivos chamados `.env` são ignorados pelo Git.

## 🐳 4. Configurando o Docker Compose

Criamos o arquivo `compose.yaml` com a configuração do serviço MySQL:

```yaml
services:
  db:
    image: mysql:8.4
    container_name: mysql-estudos
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### 🔍 Entendendo a configuração

| Configuração              | Função                                                                        |
| :------------------------ | :---------------------------------------------------------------------------- |
| `services`                | Define os serviços da aplicação.                                              |
| `db`                      | Nome do serviço MySQL no Compose.                                             |
| `image`                   | Define a imagem utilizada pelo container.                                     |
| `container_name`          | Define o nome do container.                                                   |
| `restart: unless-stopped` | Reinicia o container automaticamente, exceto quando ele é parado manualmente. |
| `env_file`                | Informa o arquivo que contém as variáveis de ambiente.                        |
| `ports`                   | Publica a porta do container no computador.                                   |
| `volumes`                 | Associa um volume persistente ao diretório de dados do MySQL.                 |

### 🌐 Entendendo o mapeamento de portas

```yaml
ports:
  - "3306:3306"
```

O mapeamento segue a estrutura:

**PORTA DO COMPUTADOR : PORTA DO CONTAINER**

Nesse caso:

- `3306` à esquerda: porta disponibilizada no computador.
- `3306` à direita: porta utilizada pelo MySQL dentro do container.

### 💾 Entendendo o volume

```yaml
volumes:
  - mysql_data:/var/lib/mysql
```

O volume `mysql_data` armazena os dados do MySQL.

O diretório `/var/lib/mysql` é o local utilizado pela imagem para armazenar os arquivos do banco de dados.

Isso permite preservar os dados mesmo quando o container é removido e recriado.

## ⚙️ 5. Validando a configuração

Antes de iniciar o serviço, utilizamos:

```powershell
docker compose config
```

Esse comando valida e exibe a configuração final interpretada pelo Docker Compose.

Na saída, conseguimos verificar:

- O serviço `db`;
- A imagem `mysql:8.4`;
- As variáveis de ambiente carregadas;
- O mapeamento da porta `3306`;
- O volume `mysql_data`;
- A rede padrão criada pelo Compose.

**Observação:** a saída desse comando pode exibir valores de variáveis de ambiente, inclusive senhas. Por isso, devemos ter cuidado ao compartilhar seu resultado.

## 🚀 6. Iniciando o container MySQL

Com a configuração validada, iniciamos o projeto:

```powershell
docker compose up -d
```

O Docker Compose criou:

- A rede padrão `aula-09_default`;
- O volume `aula-09_mysql_data`;
- O container `mysql-estudos`.

Em seguida, verificamos o funcionamento:

```powershell
docker compose ps
```

O container apareceu com o status `Up`, indicando que estava em execução.

### 🔎 Verificando os logs

Para acompanhar a inicialização do MySQL, utilizamos:

```powershell
docker compose logs db
```

Durante a inicialização, os logs mostraram:

- Inicialização dos arquivos do banco de dados;
- Inicialização do InnoDB;
- Criação do banco `estudos_docker`;
- Criação do usuário `aluna`;
- Concessão de acesso do usuário ao banco;
- Inicialização final do servidor.

A mensagem mais importante foi:

```text
MySQL init process done. Ready for start up.
```

E também:

```text
ready for connections.
```

Essas mensagens confirmaram que o servidor MySQL estava pronto para receber conexões.

## 🖥️ 7. Acessando o MySQL pelo terminal

Para acessar o MySQL dentro do container, utilizamos:

```powershell
docker compose exec db mysql -u aluna -p
```

### Entendendo o comando

| Parte                 | Função                                                 |
| :-------------------- | :----------------------------------------------------- |
| `docker compose exec` | Executa um comando dentro de um container em execução. |
| `db`                  | Identifica o serviço no Docker Compose.                |
| `mysql`               | Inicia o cliente de linha de comando do MySQL.         |
| `-u aluna`            | Informa o usuário utilizado na conexão.                |
| `-p`                  | Solicita a senha do usuário.                           |

Ao digitar a senha, percebemos que nenhum caractere aparecia no terminal. Isso é normal: o MySQL não exibe a senha enquanto ela está sendo digitada.

Após a autenticação, recebemos a mensagem:

```text
Welcome to the MySQL monitor.
Server version: 8.4.13
```

Isso confirmou que a conexão foi estabelecida com sucesso.

## 🗄️ 8. Conhecendo o banco de dados

Primeiro, listamos os bancos disponíveis:

```sql
SHOW DATABASES;
```

Entre os resultados, encontramos:

```text
estudos_docker
information_schema
performance_schema
```

O banco `estudos_docker` havia sido criado automaticamente a partir da variável `MYSQL_DATABASE`.

### Selecionando o banco

Para começar a trabalhar nele, executamos:

```sql
USE estudos_docker;
```

Depois, verificamos o banco selecionado:

```sql
SELECT DATABASE();
```

Resultado:

```text
+----------------+
| DATABASE()     |
+----------------+
| estudos_docker |
+----------------+
```

## 📋 9. Criando nossa primeira tabela

Para praticar os comandos SQL, criamos uma tabela chamada `beneficiarios`, com dados fictícios.

```sql
CREATE TABLE beneficiarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    municipio VARCHAR(100) NOT NULL
);
```

### 🔍 Entendendo a estrutura

| Campo       | Tipo           | Função                                 |
| :---------- | :------------- | :------------------------------------- |
| `id`        | `INT`          | Armazena um número inteiro.            |
| `nome`      | `VARCHAR(100)` | Armazena textos de até 100 caracteres. |
| `municipio` | `VARCHAR(100)` | Armazena textos de até 100 caracteres. |

Outras propriedades importantes:

- `AUTO_INCREMENT`: gera automaticamente um identificador numérico para cada registro.
- `PRIMARY KEY`: define a chave primária da tabela, identificando cada registro de forma única.
- `NOT NULL`: determina que o campo não pode receber um valor nulo.

### Conferindo a estrutura

Utilizamos:

```sql
DESCRIBE beneficiarios;
```

O comando apresentou as três colunas criadas, seus tipos e suas propriedades.

## 📝 10. Inserindo registros

Para cadastrar dois beneficiários fictícios, utilizamos:

```sql
INSERT INTO beneficiarios (nome, municipio)
VALUES
    ('Ana Silva', 'Campo Grande'),
    ('Maria Souza', 'Dourados');
```

O resultado foi:

```text
Query OK, 2 rows affected
Records: 2
Duplicates: 0
Warnings: 0
```

Isso confirmou que dois registros foram inseridos com sucesso.

Perceba que não informamos o campo `id`, pois ele é preenchido automaticamente pelo `AUTO_INCREMENT`.

## 🔎 11. Consultando os registros

Para visualizar os dados cadastrados, executamos:

```sql
SELECT * FROM beneficiarios;
```

Resultado:

```text
+----+-------------+--------------+
| id | nome        | municipio    |
+----+-------------+--------------+
|  1 | Ana Silva   | Campo Grande |
|  2 | Maria Souza | Dourados     |
+----+-------------+--------------+
```

### Entendendo o SELECT

- `SELECT`: solicita uma consulta de dados.
- `*`: indica que queremos todas as colunas.
- `FROM`: informa a tabela de onde os dados serão consultados.

## ✏️ 12. Atualizando registros

Depois, aprendemos a modificar informações existentes.

Utilizamos:

```sql
UPDATE beneficiarios
SET municipio = 'Tres Lagoas'
WHERE id = 2;
```

O comando atualizou o município de Maria Souza.

### Entendendo o UPDATE

- `UPDATE`: indica a tabela que será atualizada.
- `SET`: define o novo valor.
- `WHERE`: especifica qual registro será alterado.

Após executar novamente o `SELECT`, verificamos que Maria Souza estava cadastrada em Três Lagoas.

**Atenção:** o `WHERE` é muito importante. Sem ele, o comando poderia atualizar o município de todos os registros da tabela.

## 🗑️ 13. Excluindo registros

Para finalizar as operações básicas, removemos o cadastro de Ana Silva:

```sql
DELETE FROM beneficiarios
WHERE id = 1;
```

Depois, consultamos novamente:

```sql
SELECT * FROM beneficiarios;
```

Resultado:

```text
+----+-------------+-------------+
| id | nome        | municipio   |
+----+-------------+-------------+
|  2 | Maria Souza | Tres Lagoas |
+----+-------------+-------------+
```

Apenas o registro com `id = 1` foi removido.

**Atenção:** assim como no `UPDATE`, utilizar `WHERE` é fundamental para evitar excluir todos os registros da tabela acidentalmente.

## 💗 14. Conhecendo o CRUD

Durante a prática, utilizamos quatro operações fundamentais de manipulação de dados, conhecidas como CRUD:

| Operação | Comando SQL | Função              |
| :------- | :---------- | :------------------ |
| Create   | `INSERT`    | Insere registros.   |
| Read     | `SELECT`    | Consulta registros. |
| Update   | `UPDATE`    | Atualiza registros. |
| Delete   | `DELETE`    | Exclui registros.   |

Essas operações são utilizadas em aplicações que precisam cadastrar, consultar, editar e excluir informações.

## 💾 15. Testando a persistência dos dados

Uma das partes mais importantes da aula foi verificar se os dados continuariam armazenados mesmo após a remoção do container.

Primeiro, saímos do MySQL:

```sql
exit;
```

Depois, no PowerShell, executamos:

```powershell
docker compose down
```

Esse comando removeu o container e a rede padrão do projeto.

Entretanto, o volume nomeado `mysql_data` foi preservado.

### Recriando o container

Em seguida, iniciamos novamente o projeto:

```powershell
docker compose up -d
```

Verificamos o container:

```powershell
docker compose ps
```

O container `mysql-estudos` apareceu novamente com o status `Up`.

### Conferindo os dados

Acessamos novamente o MySQL:

```powershell
docker compose exec db mysql -u aluna -p
```

Depois, executamos:

```sql
USE estudos_docker;

SELECT * FROM beneficiarios;
```

Para nossa surpresa — e confirmação do que estudamos — o registro de Maria Souza continuava armazenado!

Isso demonstrou que os dados permaneceram no volume Docker, independentemente da remoção e recriação do container.

### ⚠️ Cuidado com o comando down -v

Existe uma diferença importante entre:

```powershell
docker compose down
```

e:

```powershell
docker compose down -v
```

- `docker compose down`: remove os containers e as redes do projeto, preservando os volumes nomeados.
- `docker compose down -v`: também remove os volumes nomeados associados ao projeto, podendo apagar os dados armazenados no banco.

Por isso, devemos ter cuidado ao utilizar a opção `-v`.

## 🔎 16. Conferindo o ambiente final

Para finalizar a prática, saímos novamente do MySQL e executamos:

```powershell
docker compose ps
```

O resultado confirmou que o container estava em execução:

```text
NAME            IMAGE       SERVICE   STATUS
mysql-estudos   mysql:8.4   db        Up
```

Depois, verificamos os volumes:

```powershell
docker volume ls
```

Encontramos:

```text
DRIVER    VOLUME NAME
local     aula-09_mysql_data
```

Isso confirmou que o container e o volume continuavam existindo.

## 📝 17. Resumo da aula

- 🐬 MySQL é um sistema gerenciador de banco de dados relacional.
- 🐳 É possível executar um banco de dados dentro de um container Docker.
- ⚙️ Docker Compose facilita a configuração e o gerenciamento dos serviços.
- 🔐 Arquivos `.env` permitem organizar variáveis de ambiente.
- 🗄️ `CREATE DATABASE` e `CREATE TABLE` permitem criar bancos e tabelas.
- 📝 `INSERT` insere registros.
- 🔎 `SELECT` consulta informações.
- ✏️ `UPDATE` modifica registros.
- 🗑️ `DELETE` exclui registros.
- 💾 Volumes permitem preservar dados mesmo quando containers são removidos.
- ⚠️ `docker compose down -v` também remove os volumes nomeados do projeto.

---

🐳 **Fim da Aula 09** 🐳

# 🐳 Aula 12 — Boas práticas e revisão geral do Docker 🎀

> 🌷 Conhecendo boas práticas para organizar projetos, construir imagens, proteger configurações e manter o ambiente Docker organizado.

---

## 🩷 1. Organização de projetos Docker

Ao trabalhar com Docker, é importante manter os arquivos organizados para facilitar a manutenção e a compreensão dos projetos.

Uma estrutura pode separar arquivos de configuração, código da aplicação e documentação.

Exemplo de organização:

```text
projeto/
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env
├── .env.example
├── app/
│   ├── app.py
│   └── requirements.txt
└── README.md
```

Cada arquivo possui uma finalidade:

- **Dockerfile:** contém as instruções para construir uma imagem.
- **compose.yaml:** define os serviços e as configurações da aplicação.
- **.dockerignore:** determina quais arquivos serão excluídos do contexto de construção.
- **.env:** armazena variáveis de ambiente utilizadas na configuração.
- **.env.example:** apresenta um modelo das variáveis necessárias, sem expor credenciais reais.
- **requirements.txt:** lista as dependências Python do projeto.

Manter essa organização facilita o desenvolvimento e evita misturar configurações com o código da aplicação.

## 🐳 2. Boas práticas na construção de imagens

Ao construir imagens Docker, algumas práticas ajudam a melhorar a organização, a segurança e o desempenho.

### 🖼️ Utilizar imagens adequadas

É interessante utilizar imagens oficiais e escolher versões compatíveis com o projeto.

Por exemplo:

```dockerfile
FROM python:3.12-slim
```

A versão `slim` utiliza uma imagem mais enxuta, reduzindo componentes desnecessários.

### 🏷️ Utilizar tags específicas

Ao trabalhar com imagens, podemos especificar sua versão.

Exemplo:

```bash
docker pull mysql:8.4
```

Utilizar uma versão específica, como `mysql:8.4`, torna a configuração mais previsível do que utilizar `mysql:latest`, pois a tag `latest` pode apontar para uma versão diferente futuramente.

Mesmo as tags de versão podem ser atualizadas. Para identificar exatamente um conteúdo de imagem, também existem os *digests*.

### ⚙️ Aproveitar o cache de construção

Durante a construção de uma imagem, o Docker pode reutilizar etapas anteriores que não sofreram alterações.

Isso é chamado de **cache de build**.

No projeto da Aula 10, utilizamos:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
```

Primeiro copiamos o arquivo `requirements.txt` e instalamos as dependências. Depois copiamos o restante da aplicação.

Dessa maneira, alterações apenas nos arquivos da aplicação podem permitir que o Docker reutilize as etapas anteriores, evitando reinstalar as dependências desnecessariamente.

## 📂 3. Arquivo .dockerignore

O arquivo `.dockerignore` permite excluir arquivos e diretórios do contexto de construção de uma imagem.

Isso evita enviar arquivos desnecessários ao Docker durante o processo de build.

Criamos o arquivo `.dockerignore` dentro da pasta `aula-10` com o seguinte conteúdo:

```text
.git
.env
__pycache__
*.pyc
```

### 🔍 Entendendo as regras

| Regra | O que exclui |
| :--- | :--- |
| `.git` | Diretório de controle de versão do Git. |
| `.env` | Arquivo com variáveis de ambiente. |
| `__pycache__` | Diretório de cache do Python. |
| `*.pyc` | Arquivos compilados do Python. |

### 🩷 Diferença entre .gitignore e .dockerignore

Embora tenham finalidades parecidas, os arquivos atuam em processos diferentes:

- **.gitignore:** impede que arquivos sejam adicionados ao controle de versão do Git.
- **.dockerignore:** impede que arquivos sejam enviados ao contexto de construção da imagem Docker.

No nosso projeto, utilizamos os dois para evitar que o arquivo `.env` seja versionado ou enviado durante a construção da imagem.

### 🧪 Testando o .dockerignore

Executamos novamente a construção da imagem:

```powershell
docker build -t aula-10-app:test .
```

Durante o processo, o Docker identificou o arquivo `.dockerignore` e utilizou as regras configuradas.

A construção foi concluída com sucesso e algumas etapas foram reaproveitadas do cache.

## 🔐 4. Segurança e variáveis de ambiente

Durante as aulas, aprendemos a utilizar arquivos `.env` para organizar configurações e credenciais.

Entretanto, é importante lembrar que o `.env` não criptografa os dados.

Por isso, devemos adotar alguns cuidados:

- Não enviar arquivos `.env` para o GitHub.
- Adicionar `.env` ao `.gitignore`.
- Utilizar `.dockerignore` para excluí-lo do contexto de construção.
- Evitar inserir senhas diretamente no Dockerfile.
- Utilizar `.env.example` para documentar as variáveis necessárias sem expor valores reais.

Em ambientes de produção, também existem recursos específicos para gerenciamento de segredos, como o **Docker Secrets**.

## 🧹 5. Limpeza e gerenciamento de recursos

Durante o desenvolvimento, o Docker pode acumular containers parados, imagens não utilizadas e cache de construção.

Para acompanhar o consumo de espaço, utilizamos:

```bash
docker system df
```

Esse comando apresenta informações sobre o espaço utilizado por imagens, containers, volumes e cache de build.

### 📦 Listando containers

```bash
docker ps
```

Lista somente os containers em execução.

```bash
docker ps -a
```

Lista todos os containers, inclusive os que foram encerrados.

Para remover um container que não está mais em uso:

```bash
docker rm nome-do-container
```

### 🖼️ Listando imagens

```bash
docker image ls
```

Lista as imagens armazenadas localmente.

Para remover imagens não utilizadas e sem tags:

```bash
docker image prune
```

Já o comando abaixo remove todas as imagens que não estão associadas a containers existentes:

```bash
docker image prune -a
```

É importante ter cuidado com essa opção, pois imagens que ainda não estão em uso podem ser removidas.

### 🧱 Gerenciando o cache de build

Para visualizar informações sobre o cache de construção:

```bash
docker builder du
```

Para remover o cache de construção que não está em uso:

```bash
docker builder prune
```

Durante a prática, executamos esse comando e observamos a remoção de algumas entradas do cache.

Os resultados apresentados pelos comandos de gerenciamento de espaço podem utilizar critérios de contabilização diferentes.

### ⚠️ Atenção aos volumes

Os volumes podem armazenar dados importantes, como bancos de dados.

Para listar os volumes:

```bash
docker volume ls
```

Para inspecionar um volume:

```bash
docker volume inspect nome-do-volume
```

**Não devemos remover volumes sem verificar sua finalidade e utilização.**

Na nossa prática, identificamos o volume `aula-09_mysql_data`, que armazenava os dados do MySQL e estava sendo utilizado pelo container `mysql-aula10`.

Por isso, preservamos esse volume.

O comando `docker system prune` também merece atenção: ele remove recursos não utilizados, mas não deve ser executado sem compreender o que será afetado. A opção `--volumes` exige cuidado adicional, pois pode remover volumes não utilizados.

## 📚 6. Revisão dos principais comandos

| Comando | Função |
| :--- | :--- |
| `docker pull` | Baixa uma imagem. |
| `docker images` | Lista as imagens locais. |
| `docker build` | Constrói uma imagem. |
| `docker run` | Cria e inicia um container. |
| `docker ps` | Lista containers em execução. |
| `docker ps -a` | Lista todos os containers. |
| `docker stop` | Para um container. |
| `docker start` | Inicia um container parado. |
| `docker rm` | Remove um container. |
| `docker rmi` | Remove uma imagem. |
| `docker logs` | Exibe os logs de um container. |
| `docker inspect` | Apresenta detalhes de um recurso. |
| `docker exec` | Executa um comando dentro de um container em execução. |
| `docker volume ls` | Lista volumes. |
| `docker network ls` | Lista redes. |
| `docker compose up -d` | Inicia os serviços em segundo plano. |
| `docker compose down` | Para e remove containers e redes do projeto Compose. |
| `docker system df` | Apresenta o uso de espaço do Docker. |

---

## 📝 7. Resumo da aula

- 🐳 A organização dos arquivos facilita a manutenção dos projetos.
- 🖼️ Imagens oficiais e tags específicas ajudam a manter as construções mais previsíveis.
- ⚙️ O cache de build permite reaproveitar etapas de construções anteriores.
- 📂 O `.dockerignore` exclui arquivos do contexto de construção.
- 🔐 O `.gitignore` e o `.dockerignore` ajudam a evitar a exposição acidental de arquivos, mas não substituem práticas adequadas de gerenciamento de segredos.
- 🧹 O Docker disponibiliza comandos para identificar e remover recursos não utilizados.
- 💾 Volumes precisam de atenção especial porque podem armazenar dados persistentes.
- 📚 Conhecer os principais comandos facilita a administração e o diagnóstico do ambiente Docker.

---

🐳 **Fim da Aula 12** 🐳
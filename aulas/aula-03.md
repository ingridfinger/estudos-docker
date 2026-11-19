# 🐳 Aula 03 — Imagens Docker

> 🌷 Conhecendo as imagens Docker, como baixá-las, inspecioná-las e utilizá-las para criar containers.

---

## 🩷 1. O que são imagens Docker?

Uma imagem Docker é um modelo utilizado para criar containers.

Ela contém os arquivos, bibliotecas, dependências e configurações necessários para executar uma aplicação.

As imagens são utilizadas como base para a criação dos containers, permitindo que uma mesma imagem seja utilizada para criar várias instâncias.

Por exemplo, podemos utilizar uma imagem do Nginx para criar um ou mais containers responsáveis por executar um servidor web.

## 📦 2. Docker Hub

O Docker Hub é uma plataforma utilizada para armazenar, compartilhar e distribuir imagens Docker.

Ele funciona como um repositório onde podemos encontrar imagens prontas de diferentes aplicações e ferramentas.

Alguns exemplos de imagens disponíveis são:

- **Ubuntu:** distribuição Linux.
- **Nginx:** servidor web.
- **Python:** ambiente para executar aplicações Python.
- **MySQL:** sistema de gerenciamento de banco de dados.
- **MongoDB:** banco de dados NoSQL.

Uma das vantagens do Docker Hub é permitir que os desenvolvedores baixem imagens prontas, sem precisar configurar manualmente todos os componentes de uma aplicação.

## 🔍 3. Consultando imagens armazenadas

Para visualizar as imagens disponíveis localmente, utilizamos o comando:

```bash
docker images
```

Esse comando apresenta informações sobre as imagens armazenadas no computador.

Durante a prática, inicialmente foi identificada a imagem `hello-world`, utilizada na primeira aula para testar a instalação do Docker.

### 📋 Informações apresentadas

| Informação | Função |
|---|---|
| IMAGE | Nome da imagem. |
| TAG | Identificação da versão da imagem. |
| ID | Identificador da imagem. |
| DISK USAGE | Espaço ocupado no armazenamento do Docker. |
| CONTENT SIZE | Tamanho do conteúdo da imagem. |

A tag `latest` é utilizada para identificar a versão padrão disponibilizada pelo repositório, mas não representa necessariamente uma versão fixa ou imutável.

## ⬇️ 4. Baixando imagens com Docker Pull

Para baixar uma imagem do Docker Hub, utilizamos o comando:

```bash
docker pull nginx
```

Esse comando realiza o download da imagem do Nginx para o ambiente Docker.

Como não especificamos uma tag, o Docker utilizou automaticamente a tag `latest`.

Durante o download, foram exibidas várias mensagens, como:

```text
Using default tag: latest
latest: Pulling from library/nginx
6d2e43921e9e: Pull complete
37fb86c2a767: Pull complete
512ac5e7ce8e: Pull complete
...
Status: Downloaded newer image for nginx:latest
docker.io/library/nginx:latest
```

### 🧩 O que são Layers?

As imagens Docker são formadas por camadas (*layers*).

Cada camada representa uma parte da imagem, contendo arquivos ou alterações necessárias para sua composição.

Durante o download, o Docker obtém essas camadas e as organiza para formar a imagem completa.

Esse mecanismo permite o compartilhamento e o reaproveitamento de camadas entre imagens, evitando downloads e armazenamento desnecessários quando existem conteúdos em comum.

## 🧱 5. Inspecionando imagens

O Docker permite consultar informações detalhadas sobre uma imagem utilizando o comando:

```bash
docker image inspect nginx
```

Esse comando retorna informações em formato JSON, permitindo conhecer características internas da imagem.

### 🔎 Principais informações

| Campo | Descrição |
|---|---|
| Id | Identificador completo da imagem. |
| RepoTags | Nome e tag associados à imagem. |
| RepoDigests | Identificação da imagem por meio de digest. |
| Created | Data de criação da imagem. |
| Architecture | Arquitetura para a qual a imagem foi construída. |
| Os | Sistema operacional da imagem. |
| Config | Configurações utilizadas na imagem. |
| RootFS | Informações sobre o sistema de arquivos e suas camadas. |
| Size | Tamanho da imagem em bytes. |

### 📌 Observações da imagem Nginx

Durante a inspeção da imagem `nginx`, foram identificadas as seguintes informações:

- **Imagem:** `nginx:latest`.
- **Sistema operacional:** Linux.
- **Arquitetura:** AMD64.
- **Porta declarada:** 80/tcp.
- **Versão do Nginx:** 1.31.8.
- **Quantidade de camadas:** 7.

A imagem também apresentou a seguinte configuração:

```json
"ExposedPorts": {
    "80/tcp": {}
}
```

Isso indica que a imagem declara a porta 80 como porta de comunicação do serviço.

Entretanto, declarar uma porta como exposta não significa que ela esteja automaticamente publicada para acesso externo.

## 🌐 6. Criando um container com Nginx

Depois de baixar e inspecionar a imagem, utilizamos o Nginx para criar nosso primeiro servidor web em um container.

O comando utilizado foi:

```bash
docker run -d -p 8080:80 --name meu-nginx nginx
```

### 💻 Entendendo os parâmetros

| Parâmetro | Função |
|---|---|
| `docker run` | Cria e executa um novo container. |
| `-d` | Executa o container em segundo plano. |
| `-p 8080:80` | Mapeia a porta 8080 do computador para a porta 80 do container. |
| `--name meu-nginx` | Define um nome personalizado para o container. |
| `nginx` | Indica a imagem utilizada para criar o container. |

Após executar o comando, o Docker retornou um identificador longo, confirmando a criação do container.

### 🌷 Acessando o servidor

Com o container em execução, foi possível acessar o Nginx pelo navegador utilizando o endereço:

```text
http://localhost:8080
```

A página padrão do Nginx foi exibida corretamente, confirmando que o servidor web estava funcionando.

Esse teste demonstrou como podemos executar uma aplicação em um container e acessá-la por meio de uma porta publicada no computador.

## 🔄 7. Gerenciando containers

Durante a prática, também foram utilizados comandos para verificar, parar e remover o container criado.

### 🖥️ Listando containers em execução

```bash
docker ps
```

Lista somente os containers que estão em execução.

### 📋 Listando todos os containers

```bash
docker ps -a
```

Lista todos os containers existentes, incluindo aqueles que já foram encerrados.

### ⏸️ Parando um container

```bash
docker stop meu-nginx
```

Interrompe a execução do container, mas não o remove.

Após executar esse comando, o Docker retornou:

```text
meu-nginx
```

Em seguida, ao executar `docker ps`, o container não apareceu mais, pois já estava parado.

### 🗑️ Removendo um container

```bash
docker rm meu-nginx
```

Remove um container que esteja parado.

Depois da remoção, o comando `docker ps -a` não apresentou mais o container `meu-nginx`.

**Importante:** remover um container não significa remover a imagem utilizada para criá-lo. A imagem Nginx continuou armazenada localmente.

## 🧪 8. Prática: comandos utilizados

Durante a aula, foram utilizados os seguintes comandos:

| Comando | Função |
|---|---|
| `docker images` | Lista as imagens armazenadas localmente. |
| `docker pull nginx` | Baixa a imagem Nginx do Docker Hub. |
| `docker image inspect nginx` | Exibe informações detalhadas da imagem. |
| `docker run -d -p 8080:80 --name meu-nginx nginx` | Cria e executa um container Nginx em segundo plano. |
| `docker ps` | Lista os containers em execução. |
| `docker ps -a` | Lista todos os containers, inclusive os encerrados. |
| `docker stop meu-nginx` | Para a execução do container. |
| `docker rm meu-nginx` | Remove o container parado. |

### 📦 Observações da prática

Durante os testes, foi possível observar que:

- Inicialmente, havia apenas a imagem `hello-world` armazenada localmente.
- Após executar `docker pull nginx`, a imagem Nginx foi baixada do Docker Hub.
- A imagem `nginx` apresentou tamanho maior que a imagem `hello-world`, pois contém os componentes necessários para executar um servidor web.
- O comando `docker image inspect nginx` permitiu consultar informações internas da imagem, incluindo arquitetura, sistema operacional, porta declarada e camadas.
- Uma mesma imagem pode ser utilizada para criar vários containers diferentes.
- O container `meu-nginx` foi criado e executado com sucesso.
- O mapeamento `8080:80` permitiu acessar o servidor pelo endereço `localhost:8080`.
- O comando `docker stop` interrompeu a execução, mas manteve o container armazenado.
- O status `Exited (0)` indicou que o container foi encerrado com sucesso.
- Após utilizar `docker rm`, o container foi removido, mas a imagem Nginx continuou armazenada no computador.

## 📝 9. Resumo da aula

- 🐳 Imagens Docker são modelos utilizados para criar containers.
- 🌐 Docker Hub é uma plataforma para armazenar e compartilhar imagens.
- ⬇️ `docker pull` permite baixar imagens de um repositório.
- 🧩 Imagens Docker são compostas por camadas (*layers*).
- 🔍 `docker image inspect` apresenta informações detalhadas sobre uma imagem.
- 📦 Uma mesma imagem pode ser utilizada para criar vários containers.
- 🌐 O Nginx pode ser executado em um container e acessado pelo navegador.
- 🔌 O parâmetro `-p` permite mapear portas entre o computador e o container.
- ⏸️ `docker stop` interrompe a execução de um container sem removê-lo.
- 🗑️ `docker rm` remove um container parado.
- 💡 Imagens e containers possuem ciclos de vida independentes.

---

🎀 *Fim da Aula 03* 🎀
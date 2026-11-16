# 🐳 Aula 02 — Como o Docker funciona?

> 🌷 Conhecendo os componentes do Docker e como eles trabalham juntos.

---

## 🩷 1. O que é Docker Engine?

Docker Engine é o conjunto de componentes responsável por construir e executar containers, além de gerenciar imagens, redes e volumes.

É a parte central do Docker que permite que as aplicações sejam executadas em containers.

Seus principais componentes são:

- Docker Client;
- Docker Daemon;
- Docker API.

## 💻 2. Componentes principais

### 🖥️ Docker Client

É a interface utilizada para interagir com o Docker.

Quando abrimos o PowerShell e digitamos um comando, como:

```bash
docker run hello-world
```

Estamos utilizando o Docker Client.

Ele recebe os comandos digitados e envia as solicitações ao Docker Daemon.

### ⚙️ Docker Daemon

É o serviço responsável por processar as solicitações recebidas e executar as operações.

Ele trabalha em segundo plano e gerencia:

- Containers;
- Imagens;
- Redes;
- Volumes.

Por exemplo, quando solicitamos a criação de um container, o Daemon realiza essa operação.

### 🔗 Docker API

É a interface de comunicação entre o Docker Client e o Docker Daemon.

Ela permite que os dois componentes troquem solicitações e respostas.

## 🔄 3. Como eles trabalham juntos?

Quando executamos um comando no terminal, acontece o seguinte processo:

1. O usuário digita um comando no Docker Client.
2. O Client envia a solicitação por meio da Docker API.
3. O Daemon recebe a solicitação.
4. O Daemon realiza a operação solicitada.
5. O resultado é retornado ao Client.

Dessa forma, o Client funciona como a interface de interação, enquanto o Daemon é responsável por executar as operações.

## 🛠️ 4. Docker Engine x Docker Desktop

Embora estejam relacionados, Docker Engine e Docker Desktop não são a mesma coisa.

**Docker Engine:** conjunto de componentes responsável por construir e executar containers.

**Docker Desktop:** aplicativo que facilita o uso do Docker no Windows e no macOS, oferecendo interface gráfica, configurações e integração com o ambiente Docker.

Também é possível utilizar o Docker pelo terminal, executando comandos diretamente pelo PowerShell.

## 🐧 5. Docker no Windows e WSL 2

O WSL 2 (*Windows Subsystem for Linux*) permite executar um ambiente Linux dentro do Windows.

O Docker Desktop pode utilizar o WSL 2 como base para executar containers Linux.

No ambiente Windows, a estrutura funciona de maneira integrada:

- **Windows:** sistema operacional principal.
- **Docker Desktop:** gerencia o ambiente Docker.
- **WSL 2:** fornece o ambiente Linux utilizado pelo Docker Desktop.
- **Docker Engine:** executa e gerencia os containers.
- **Containers:** ambientes isolados onde as aplicações são executadas.

Essa integração permite utilizar ferramentas e aplicações desenvolvidas para Linux sem precisar substituir o Windows como sistema operacional principal.

## 🧪 6. Prática: comandos utilizados

Durante a aula, foram utilizados alguns comandos para visualizar e gerenciar containers e imagens.

| Comando | Função |
|---|---|
| `docker ps` | Lista os containers em execução. |
| `docker ps -a` | Lista todos os containers, inclusive os encerrados. |
| `docker run hello-world` | Cria e executa um novo container a partir da imagem. |
| `docker rm` | Remove um container. |
| `docker images` | Lista as imagens armazenadas localmente. |

### 📦 Observações da prática

Durante os testes, foi possível observar que:

- O comando `docker ps` não exibiu containers porque não havia nenhum em execução.
- O comando `docker ps -a` mostrou os containers criados anteriormente, mesmo após o encerramento.
- Executar `docker run hello-world` novamente criou um novo container utilizando a mesma imagem.
- O status `Exited (0)` indicou que o container encerrou sua execução com sucesso.
- Ao remover um container com `docker rm`, a imagem utilizada continuou armazenada no computador.

## 📝 7. Resumo da aula

- 🐳 Docker Engine é responsável por construir e executar containers.
- 🖥️ Docker Client recebe os comandos digitados pelo usuário.
- ⚙️ Docker Daemon processa as solicitações e gerencia os recursos.
- 🔗 Docker API permite a comunicação entre Client e Daemon.
- 💻 Docker Desktop facilita o gerenciamento do Docker.
- 🐧 WSL 2 permite executar um ambiente Linux dentro do Windows.
- 📦 Containers e imagens são recursos diferentes e possuem ciclos de vida independentes.

---

🎀 *Fim da Aula 02* 🎀
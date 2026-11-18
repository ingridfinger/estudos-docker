# 🐳 Aula 07 — Docker Compose

> 🌷 Aprendendo a definir, configurar e executar aplicações compostas por múltiplos containers.

---

## 🩷 1. O que é Docker Compose?

Docker Compose é uma ferramenta que permite definir e executar aplicações compostas por múltiplos containers por meio de um único arquivo de configuração, geralmente chamado `compose.yaml`.

Em vez de configurar e executar cada container individualmente com `docker run`, podemos descrever todos os serviços da aplicação em um arquivo YAML.

Isso facilita o gerenciamento, a organização e a execução de aplicações com diferentes componentes, como sistemas, APIs e bancos de dados.

## 💻 2. Verificando a instalação

Para verificar se o Docker Compose estava disponível no ambiente, utilizamos:

```powershell
docker compose version
```

**Resultado:**

```text
Docker Compose version v5.7.0
```

O Docker Compose moderno já vem integrado ao comando `docker`, por isso utilizamos `docker compose`, com espaço, em vez do antigo `docker-compose`.

## 🧩 3. Arquivo de configuração YAML

O Docker Compose utiliza arquivos YAML para descrever os serviços e suas configurações.

O arquivo utilizado nesta aula foi:

```text
compose.yaml
```

O YAML organiza as informações por meio de indentação, utilizando espaços para representar a hierarquia dos elementos.

### Principais elementos

| Elemento | Função |
|---|---|
| `services` | Define os serviços da aplicação. |
| `image` | Especifica a imagem utilizada pelo serviço. |
| `container_name` | Define o nome do container. |
| `ports` | Configura o mapeamento de portas. |
| `volumes` | Define armazenamento persistente ou compartilhado. |
| `networks` | Configura as redes utilizadas pelos serviços. |
| `environment` | Define variáveis de ambiente. |

## 🌸 4. Criando o primeiro projeto

Criamos uma pasta chamada `projeto-compose` dentro do repositório `estudos-docker`.

Dentro dela, criamos o arquivo `compose.yaml`.

A primeira estrutura utilizada foi:

```yaml
services:
```

O elemento `services` indica que serão declarados os serviços que compõem a aplicação.

## 📦 5. Configurando os serviços

Nosso projeto foi composto por dois serviços, ambos utilizando a imagem `nginx:latest`.

**Conteúdo completo do arquivo `compose.yaml`:**

```yaml
services:
  web:
    image: nginx:latest
    container_name: compose-web
    ports:
      - "8080:80"

  app:
    image: nginx:latest
    container_name: compose-app
```

### Entendendo a configuração

**Serviço web:**

- `web`: nome do serviço.
- `image`: utiliza a imagem Nginx.
- `container_name`: define o nome `compose-web`.
- `ports`: publica a porta 80 do container na porta 8080 do computador.

**Serviço app:**

- `app`: nome do segundo serviço.
- `image`: também utiliza a imagem Nginx.
- `container_name`: define o nome `compose-app`.

O segundo serviço não precisou de uma configuração `ports`, pois seria acessado pela rede interna do Docker.

## 🌐 6. Redes automáticas no Docker Compose

Uma das vantagens do Docker Compose é a criação automática de uma rede padrão para o projeto.

Quando os serviços são iniciados, eles são conectados a essa rede, permitindo a comunicação entre eles.

Além disso, o Docker disponibiliza resolução automática de nomes por meio do DNS interno.

Isso significa que um serviço consegue localizar outro utilizando o nome do serviço, sem precisar descobrir manualmente seu endereço IP.

## 🔎 7. Validando o arquivo de configuração

Antes de executar a aplicação, utilizamos:

```powershell
docker compose config
```

Esse comando valida e apresenta a configuração interpretada pelo Docker Compose.

O resultado confirmou os dois serviços:

- `web`
- `app`

Também foi possível observar a criação da rede padrão:

```text
projeto-compose_default
```

O comando permite identificar problemas de sintaxe e configuração antes de iniciar os serviços.

## 🚀 8. Executando a aplicação

Para criar e iniciar os dois serviços, utilizamos:

```powershell
docker compose up -d
```

### Entendendo o comando

| Parâmetro | Função |
|---|---|
| `docker compose` | Chama a ferramenta Docker Compose. |
| `up` | Cria e inicia os serviços definidos no arquivo. |
| `-d` | Executa os containers em segundo plano. |

Depois, verificamos os serviços com:

```powershell
docker compose ps
```

**Resultado observado:**

| Serviço | Container | Status | Porta |
|---|---|---|---|
| `web` | `compose-web` | Up | `8080 → 80` |
| `app` | `compose-app` | Up | `80` interna |

Os dois serviços foram iniciados corretamente.

## 🖥️ 9. Testando a aplicação

Para verificar o funcionamento do serviço `web`, acessamos no navegador:

```text
http://localhost:8080
```

A página padrão do Nginx foi exibida, confirmando que o serviço estava funcionando.

## 🩷 10. Testando a comunicação entre serviços

Para verificar se o serviço `web` conseguia acessar o serviço `app`, executamos:

```powershell
docker compose exec web curl http://app
```

O comando realizou uma requisição HTTP para o serviço `app`.

**Resultado:**

Foi retornado o HTML da página padrão do Nginx, incluindo a mensagem:

```html
<h1>Welcome to nginx!</h1>
```

Isso comprovou que:

1. Os serviços estavam conectados à mesma rede.
2. O DNS interno conseguiu resolver o nome `app`.
3. O serviço `web` conseguiu alcançar o serviço `app`.
4. O Nginx do serviço `app` recebeu e respondeu à requisição HTTP.

**Observação importante:** não foi necessário publicar a porta 80 do serviço `app` no computador. A comunicação aconteceu internamente pela rede do Docker.

## ⚙️ 11. Principais comandos do Docker Compose

| Comando | Função |
|---|---|
| `docker compose up` | Cria e inicia os serviços. |
| `docker compose up -d` | Inicia os serviços em segundo plano. |
| `docker compose ps` | Lista os serviços do projeto. |
| `docker compose logs` | Exibe os logs dos serviços. |
| `docker compose logs -f` | Acompanha os logs em tempo real. |
| `docker compose stop` | Para os serviços sem removê-los. |
| `docker compose start` | Inicia novamente os serviços parados. |
| `docker compose down` | Para e remove os containers e a rede padrão do projeto. |

### Diferença entre stop e down

- `docker compose stop`: interrompe os containers, mas mantém os recursos criados.
- `docker compose down`: interrompe e remove os containers e a rede padrão do projeto.

Por padrão, o comando `down` não remove as imagens nem os volumes nomeados.

## 🧹 12. Limpando o ambiente

Após concluir os testes, encerramos a aplicação utilizando:

```powershell
docker compose down
```

Depois, verificamos os containers:

```powershell
docker compose ps
```

E também:

```powershell
docker ps -a
```

As duas consultas retornaram vazias, confirmando que os containers do projeto foram removidos.

✨ Limpeza concluída com sucesso!

## 📚 13. Resumo da aula

- 🐳 Docker Compose permite gerenciar aplicações com múltiplos containers.
- 📝 O arquivo `compose.yaml` descreve os serviços e suas configurações.
- 🧩 Conhecemos elementos como `services`, `image`, `container_name` e `ports`.
- 🌐 O Compose cria automaticamente uma rede padrão para o projeto.
- 🔎 Os serviços conseguem se comunicar utilizando seus nomes por meio do DNS interno.
- 🚀 Utilizamos `docker compose up -d` para iniciar os serviços.
- 🖥️ Testamos o Nginx pelo navegador.
- 💻 Testamos a comunicação HTTP entre serviços com `curl`.
- 🧹 Utilizamos `docker compose down` para encerrar e remover os recursos do projeto.

---

🐳 **Fim da Aula 07** 🐳

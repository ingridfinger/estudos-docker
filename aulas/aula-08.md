# 🐳 Aula 08 — Variáveis de ambiente e configuração de containers

> 🌷 Aprendendo a configurar containers de forma flexível, organizada e segura utilizando variáveis de ambiente e Docker Compose.

---

## 🩷 1. O que são variáveis de ambiente?

Variáveis de ambiente (*Environment Variables*) são valores disponibilizados para um processo durante sua execução.

Elas permitem configurar uma aplicação sem precisar deixar todas as configurações diretamente no código.

Em uma aplicação, podemos utilizar variáveis de ambiente para definir:

- Endereço do banco de dados;
- Porta de comunicação;
- Ambiente de execução (desenvolvimento ou produção);
- Nome do sistema;
- Credenciais e outras configurações.

Por exemplo, uma aplicação pode utilizar uma variável chamada `AMBIENTE` para identificar onde está sendo executada.

```python
import os

ambiente = os.getenv("AMBIENTE")

print(f"Executando em: {ambiente}")
```

Se a variável estiver configurada como `desenvolvimento`, o resultado será:

```text
Executando em: desenvolvimento
```

O código permanece igual. O que muda é a configuração recebida pela aplicação.

## 💻 2. Por que utilizar variáveis de ambiente no Docker?

As variáveis de ambiente permitem utilizar uma mesma imagem Docker com configurações diferentes.

Por exemplo, uma aplicação pode funcionar em dois ambientes:

| Desenvolvimento | Produção |
| :--- | :--- |
| `AMBIENTE=desenvolvimento` | `AMBIENTE=producao` |
| Configurações de teste | Configurações reais |
| Banco de dados de desenvolvimento | Banco de dados de produção |

Dessa forma, não precisamos criar uma imagem diferente apenas para alterar configurações.

## ⚙️ 3. Configurando variáveis com `docker run -e`

A opção `-e` (ou `--env`) permite definir variáveis de ambiente no momento em que criamos um container.

**Exemplo utilizado:**

```powershell
docker run -d --name teste-env -e AMBIENTE=desenvolvimento nginx
```

Nesse comando:

- `docker run`: cria e inicia um container;
- `-d`: executa o container em segundo plano;
- `--name teste-env`: define o nome do container;
- `-e AMBIENTE=desenvolvimento`: configura a variável de ambiente;
- `nginx`: imagem utilizada.

Para consultar a variável dentro do container, utilizamos:

```powershell
docker exec teste-env printenv AMBIENTE
```

**Resultado obtido:**

```text
desenvolvimento
```

### 3.1. Configurando várias variáveis

Também podemos passar várias variáveis utilizando múltiplas opções `-e`.

**Comando utilizado:**

```powershell
docker run -d `
  --name teste-env-2 `
  -e AMBIENTE=desenvolvimento `
  -e PORTA=8080 `
  -e SISTEMA=meu-sistema `
  nginx
```

O acento grave (`` ` ``) permite dividir um comando em várias linhas no PowerShell.

Para consultar uma variável específica:

```powershell
docker exec teste-env-2 printenv PORTA
```

**Resultado:**

```text
8080
```

Para visualizar todas as variáveis disponíveis:

```powershell
docker exec teste-env-2 printenv
```

Além das variáveis configuradas manualmente, aparecem outras disponibilizadas pelo ambiente do container e pela imagem, como `PATH`, `HOSTNAME`, `HOME` e `NGINX_VERSION`.

## 🖥️ 4. Passando variáveis do PowerShell para o container

Também podemos utilizar uma variável de ambiente que já existe no computador.

No PowerShell, podemos criar uma variável utilizando:

```powershell
$env:AMBIENTE = "desenvolvimento"
```

Para consultar seu conteúdo:

```powershell
echo $env:AMBIENTE
```

Depois, podemos passá-la para o Docker:

```powershell
docker run -d --name teste-env-3 -e AMBIENTE nginx
```

Observe que não precisamos escrever `=desenvolvimento` novamente. O Docker utiliza o valor da variável existente no PowerShell.

Para verificar dentro do container:

```powershell
docker exec teste-env-3 printenv AMBIENTE
```

**Resultado obtido:**

```text
desenvolvimento
```

### Diferença entre os comandos

| Comando | Função |
| :--- | :--- |
| `$env:AMBIENTE` | Acessa uma variável de ambiente do PowerShell. |
| `-e AMBIENTE=valor` | Define uma variável diretamente no container. |
| `-e AMBIENTE` | Passa para o container o valor da variável existente no ambiente do cliente Docker. |
| `printenv AMBIENTE` | Consulta a variável dentro do container. |

## 📁 5. Arquivos `.env`

O arquivo `.env` é um arquivo de texto utilizado para centralizar e organizar variáveis de ambiente de um projeto.

Em vez de passar várias configurações diretamente no comando Docker, podemos armazená-las em um único arquivo.

**Exemplo de arquivo `.env`:**

```env
AMBIENTE=desenvolvimento
PORTA=8080
SISTEMA=meu-sistema
```

O arquivo pode ficar diretamente na raiz do projeto ou em uma pasta específica.

Exemplo de organização:

```text
docker-env/
├── .env
└── compose.yaml
```

### 5.1. Utilizando `--env-file`

A opção `--env-file` permite informar ao Docker qual arquivo deve ser utilizado para carregar as variáveis dentro do container.

**Comando utilizado:**

```powershell
docker run -d --name teste-env-arquivo --env-file .env nginx
```

Para verificar as variáveis:

```powershell
docker exec teste-env-arquivo printenv
```

**Resultado obtido:**

```text
AMBIENTE=desenvolvimento
PORTA=8080
SISTEMA=meu-sistema
```

O Docker leu o arquivo `.env` e disponibilizou as configurações dentro do container.

**Importante:** o arquivo `.env` não precisa conter todas as variáveis existentes no container. Ele contém apenas as configurações que desejamos definir.

## 🐳 6. Variáveis de ambiente no Docker Compose

O Docker Compose também permite configurar variáveis de ambiente de maneira organizada.

Existem duas opções importantes:

### 6.1. `environment`

Permite definir variáveis diretamente no arquivo `compose.yaml`.

**Exemplo:**

```yaml
services:
  web:
    image: nginx:latest
    container_name: compose-env
    ports:
      - "8080:80"
    environment:
      AMBIENTE: desenvolvimento
      SISTEMA: meu-sistema
      PORTA: "8080"
```

### 6.2. `env_file`

Permite carregar variáveis de um arquivo externo, como o `.env`.

**Exemplo:**

```yaml
services:
  web:
    image: nginx:latest
    container_name: compose-env
    ports:
      - "8080:80"
    env_file:
      - .env
```

### 6.3. Diferença entre `environment` e `env_file`

| `environment` | `env_file` |
| :--- | :--- |
| Define valores diretamente no YAML. | Carrega valores de um arquivo externo. |
| Bom para configurações simples. | Bom para organizar várias configurações. |
| Os valores ficam no `compose.yaml`. | Os valores ficam separados do YAML. |

Quando a mesma variável é definida nas duas opções, `environment` prevalece sobre `env_file`.

### 6.4. Validando a configuração

O comando abaixo permite verificar e visualizar a configuração interpretada pelo Docker Compose:

```powershell
docker compose config
```

Durante a prática, o comando apresentou:

```yaml
name: docker-env
services:
  web:
    container_name: compose-env
    environment:
      AMBIENTE: desenvolvimento
      PORTA: "8080"
      SISTEMA: meu-sistema
    image: nginx:latest
```

Isso confirmou que as variáveis do arquivo `.env` foram carregadas corretamente.

### 6.5. Iniciando o serviço

Para iniciar os serviços definidos no Compose:

```powershell
docker compose up -d
```

Para consultar os containers:

```powershell
docker compose ps
```

Para verificar as variáveis dentro do serviço:

```powershell
docker compose exec web printenv
```

**Resultado obtido:**

```text
SISTEMA=meu-sistema
AMBIENTE=desenvolvimento
PORTA=8080
```

O container foi iniciado com sucesso e recebeu as configurações do arquivo `.env`.

## 🔄 7. Interpolação de variáveis no Docker Compose

A interpolação permite utilizar variáveis dentro do próprio `compose.yaml`, utilizando a sintaxe `${NOME_DA_VARIAVEL}`.

O Docker Compose substitui essas referências pelos valores disponíveis no ambiente de interpolação, que pode incluir o arquivo `.env`.

**Exemplo de arquivo `.env`:**

```env
AMBIENTE=desenvolvimento
PORTA=8080
SISTEMA=meu-sistema
```

**Exemplo de `compose.yaml`:**

```yaml
services:
  web:
    image: nginx:latest
    container_name: ${SISTEMA}
    ports:
      - "${PORTA}:80"
    environment:
      AMBIENTE: ${AMBIENTE}
      PORTA: ${PORTA}
      SISTEMA: ${SISTEMA}
```

O Compose substitui as referências pelos valores encontrados no `.env`.

O resultado da configuração será equivalente a:

```yaml
services:
  web:
    image: nginx:latest
    container_name: meu-sistema
    ports:
      - "8080:80"
    environment:
      AMBIENTE: desenvolvimento
      PORTA: "8080"
      SISTEMA: meu-sistema
```

### 7.1. Diferença entre interpolação e disponibilização de variáveis

Esse foi um dos aprendizados mais importantes da aula!

| Recurso | Função |
| :--- | :--- |
| `${VARIAVEL}` | Substitui valores no arquivo `compose.yaml`. |
| `environment` | Disponibiliza variáveis dentro do container. |
| `env_file` | Carrega variáveis de um arquivo para dentro do container. |

**Atenção:** utilizar `${VARIAVEL}` no `compose.yaml` não significa que ela será automaticamente disponibilizada dentro do container. Para isso, precisamos utilizar `environment` ou `env_file`.

### 7.2. Aplicando alterações

Quando modificamos configurações no `.env` ou no `compose.yaml`, normalmente podemos executar:

```powershell
docker compose up -d
```

O Docker Compose verifica as alterações e recria os containers quando necessário.

Se modificarmos arquivos utilizados na construção da imagem por meio do Dockerfile, podemos utilizar:

```powershell
docker compose up -d --build
```

Não é necessário executar `docker compose down` antes de toda alteração.

## 🧩 8. Serviços e containers no Docker Compose

No Docker Compose, cada aplicação ou componente é definido como um serviço dentro da seção `services`.

Exemplo:

```yaml
services:
  web:
    image: nginx:latest
    container_name: sistema-final
```

Nesse exemplo:

| Conceito | Valor |
| :--- | :--- |
| Nome do serviço | `web` |
| Nome do container | `sistema-final` |
| Imagem utilizada | `nginx:latest` |

O nome do serviço é definido no `compose.yaml`. O container é criado a partir dessa configuração.

Podemos utilizar o nome do serviço em comandos como:

```powershell
docker compose exec web printenv
docker compose logs web
docker compose restart web
```

O `web` não é uma palavra obrigatória. Poderíamos utilizar nomes como `frontend`, `backend`, `servidor` ou outros nomes que representem melhor a função do serviço.

## 🔐 9. Segurança e boas práticas

As variáveis de ambiente facilitam a configuração de aplicações, mas exigem cuidados quando armazenam informações sensíveis.

Exemplo de um arquivo `.env`:

```env
AMBIENTE=producao
DB_HOST=banco
DB_USER=admin
DB_PASSWORD=minha_senha
```

Senhas, tokens e credenciais não devem ser expostos em repositórios públicos ou configurações acessíveis indevidamente.

### 9.1. Utilizando `.gitignore`

Para evitar que arquivos `.env` sejam rastreados pelo Git, podemos adicionar ao `.gitignore`:

```gitignore
.env
```

Isso evita que novos arquivos `.env` sejam adicionados ao repositório quando ainda não estão sendo rastreados.

### 9.2. Utilizando `.env.example`

É comum criar um arquivo `.env.example` contendo os nomes das variáveis necessárias, mas sem credenciais reais.

**Exemplo:**

```env
AMBIENTE=desenvolvimento
DB_HOST=localhost
DB_USER=usuario
DB_PASSWORD=
```

Assim, outras pessoas conseguem identificar quais configurações precisam preencher sem ter acesso às informações sensíveis.

### 9.3. O que são Docker Secrets?

Docker Secrets é um recurso destinado ao gerenciamento de informações sensíveis, como senhas, tokens e credenciais.

No Docker Swarm, os Secrets são gerenciados nativamente e disponibilizados aos serviços autorizados.

Em ambientes Docker Compose locais, existem particularidades e limitações de implementação.

**Importante:** um arquivo `.env` não criptografa os valores armazenados. Portanto, ele não deve ser considerado um cofre de senhas.

## 🛠️ 10. Comandos importantes da aula

| Comando | Função |
| :--- | :--- |
| `docker run -e` | Define variáveis no container. |
| `docker run --env-file` | Carrega variáveis de um arquivo. |
| `printenv` | Exibe as variáveis de ambiente. |
| `docker exec` | Executa comandos dentro de um container em execução. |
| `docker compose config` | Valida e exibe a configuração interpretada. |
| `docker compose up -d` | Inicia os serviços em segundo plano e aplica alterações. |
| `docker compose exec` | Executa comandos dentro de um serviço em execução. |
| `docker compose ps` | Lista os containers do projeto. |
| `docker compose down` | Para e remove os containers e a rede padrão do projeto. |
| `docker compose logs` | Exibe os logs dos serviços. |

## 🧪 11. Exercício prático da aula

Para consolidar os conceitos, foi criado um projeto utilizando Docker Compose e variáveis de ambiente.

**Estrutura utilizada:**

```text
docker-env/
├── .env
└── compose.yaml
```

### 11.1. Arquivo `.env`

```env
AMBIENTE=desenvolvimento
PORTA=8090
SISTEMA=sistema-final
```

### 11.2. Arquivo `compose.yaml`

```yaml
services:
  web:
    image: nginx:latest
    container_name: ${SISTEMA}
    ports:
      - "${PORTA}:80"
    environment:
      AMBIENTE: ${AMBIENTE}
      PORTA: ${PORTA}
      SISTEMA: ${SISTEMA}
```

### 11.3. Validando e executando

Primeiro, foi validada a configuração:

```powershell
docker compose config
```

Em seguida, os serviços foram iniciados:

```powershell
docker compose up -d
```

Para verificar o container:

```powershell
docker compose ps
```

**Resultado obtido:**

| Informação | Resultado |
| :--- | :--- |
| Nome do container | `sistema-final` |
| Imagem | `nginx:latest` |
| Serviço | `web` |
| Status | `Up` |
| Porta publicada | `8090 → 80` |

### 11.4. Verificando as variáveis

Foi executado:

```powershell
docker compose exec web printenv
```

**Resultado obtido:**

```text
SISTEMA=sistema-final
AMBIENTE=desenvolvimento
PORTA=8090
```

Todas as variáveis foram carregadas corretamente!

### 11.5. Limpeza dos recursos

Após a conclusão dos testes, os containers foram removidos.

Primeiro, o projeto Compose foi encerrado:

```powershell
docker compose down
```

Depois, foram removidos os containers criados com `docker run`:

```powershell
docker rm -f teste-env teste-env-2 teste-env-3 teste-env-arquivo
```

Por fim, foi realizada a conferência:

```powershell
docker ps -a
```

O resultado apresentou a lista vazia, confirmando que os containers da aula foram removidos.

## 📝 12. Resumo da aula

- 🌷 Variáveis de ambiente permitem configurar aplicações sem modificar diretamente seu código.
- 🐳 A opção `-e` permite definir variáveis durante a criação de containers.
- 🖥️ Também podemos passar variáveis existentes no PowerShell.
- 📁 Arquivos `.env` ajudam a centralizar configurações.
- ⚙️ `--env-file` permite carregar variáveis de um arquivo para o container.
- 🧩 `environment` define variáveis diretamente no Docker Compose.
- 🔄 A interpolação `${VARIAVEL}` substitui valores no arquivo `compose.yaml`.
- 🔐 `.gitignore` ajuda a evitar o envio de arquivos sensíveis ao GitHub.
- 🔑 Docker Secrets é um recurso para gerenciar informações sensíveis.
- 📦 Serviços são definidos no Compose e utilizados para gerenciar seus respectivos containers.

---

🐳 **Fim da Aula 08** 🐳
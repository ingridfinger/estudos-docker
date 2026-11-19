# 🐳 Aula 05 — Volumes e persistência de dados

> 🌷 Aprendendo a armazenar dados de forma persistente e compartilhar arquivos entre o computador e os containers utilizando Docker Volumes e Bind Mounts.

---

## 🩷 1. O que é persistência de dados?

Por padrão, os arquivos criados ou modificados na camada gravável de um container pertencem ao próprio container.

Isso significa que, quando removemos um container, os dados armazenados nessa camada também são removidos.

Para evitar a perda de informações, o Docker oferece mecanismos de armazenamento que permitem manter os dados separados do ciclo de vida dos containers.

Os principais são:

- **Volumes:** áreas de armazenamento gerenciadas pelo Docker.
- **Bind Mounts:** mecanismos que conectam arquivos ou diretórios do computador aos containers.

## 📦 2. O que são Docker Volumes?

Os **Docker Volumes** são utilizados para armazenar dados fora da camada gravável dos containers.

Eles possuem um ciclo de vida independente dos containers, permitindo que diferentes containers utilizem os mesmos dados.

Isso é especialmente importante em aplicações que trabalham com informações que precisam ser preservadas, como bancos de dados e sistemas de cadastro.

### 🧠 Como funciona?

Imagine que temos um container conectado a um volume:

**Container → Volume**

Quando o container é removido, o volume continua existindo e pode ser conectado a outro container.

Dessa forma, os dados armazenados permanecem disponíveis.

## 🛠️ 3. Criando e gerenciando volumes

Para começar nossa prática, criamos um volume chamado `meu-volume`.

### Criando um volume

```powershell
docker volume create meu-volume
```

O comando criou o volume com sucesso e retornou:

```text
meu-volume
```

### Listando os volumes

```powershell
docker volume ls
```

O resultado apresentou:

```text
DRIVER    VOLUME NAME
local     meu-volume
```

O campo `DRIVER` indica o driver utilizado para armazenar os dados. Nesse caso, utilizamos o driver `local`.

### 🔎 Inspecionando um volume

Para consultar informações detalhadas, executamos:

```powershell
docker volume inspect meu-volume
```

Entre as informações apresentadas, encontramos:

```json
[
    {
        "CreatedAt": "2026-11-18T11:48:41Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/meu-volume/_data",
        "Name": "meu-volume",
        "Options": null,
        "Scope": "local"
    }
]
```

### Entendendo os principais campos

| Campo | Função |
| :--- | :--- |
| `CreatedAt` | Data e horário de criação do volume. |
| `Driver` | Driver utilizado para armazenar os dados. |
| `Mountpoint` | Caminho interno onde o Docker armazena os dados do volume. |
| `Name` | Nome do volume. |
| `Scope` | Escopo de utilização do volume. |

**Observação:** como utilizamos Docker Desktop com WSL 2, o caminho apresentado em `Mountpoint` pertence ao ambiente Linux gerenciado pelo Docker. Não precisamos acessar esse diretório manualmente.

## 🐳 4. Utilizando um volume em um container

Depois de criar o volume, precisamos conectá-lo a um container.

Para isso, podemos utilizar a opção `-v` no comando `docker run`.

A estrutura é:

```powershell
docker run -v nome-do-volume:caminho-no-container imagem
```

### 🌸 Entendendo os caminhos

Durante nossa prática, utilizamos a imagem oficial do Nginx.

Seu diretório padrão para disponibilizar arquivos HTML é:

```text
/usr/share/nginx/html
```

Esse caminho pode ser encontrado na documentação oficial da imagem Nginx no Docker Hub ou investigando o sistema de arquivos do container.

É importante diferenciar:

- **Mountpoint:** local interno onde o Docker armazena os dados do volume.
- **Caminho no container:** diretório em que o volume será conectado e acessado pela aplicação.

## 🧪 5. Testando a persistência de dados

Para comprovar que os dados permanecem armazenados mesmo após a remoção de um container, realizamos um teste utilizando o Nginx.

### Criando o container

Executamos:

```powershell
docker run -d --name nginx-volume -p 8080:80 -v meu-volume:/usr/share/nginx/html nginx:latest
```

### Entendendo o comando

| Parte | Significado |
| :--- | :--- |
| `docker run` | Cria e inicia um container. |
| `-d` | Executa o container em segundo plano. |
| `--name nginx-volume` | Define o nome do container. |
| `-p 8080:80` | Mapeia a porta 8080 do computador para a porta 80 do container. |
| `-v meu-volume:/usr/share/nginx/html` | Conecta o volume ao diretório de arquivos do Nginx. |
| `nginx:latest` | Define a imagem utilizada. |

### 📄 Criando um arquivo dentro do volume

Com o container em execução, criamos um arquivo chamado `teste.txt`:

```powershell
docker exec nginx-volume sh -c "echo 'Meus dados continuam salvos no Docker Volume!' > /usr/share/nginx/html/teste.txt"
```

Para verificar o conteúdo, executamos:

```powershell
docker exec nginx-volume cat /usr/share/nginx/html/teste.txt
```

O terminal retornou:

```text
Meus dados continuam salvos no Docker Volume!
```

Isso confirmou que o arquivo havia sido criado corretamente no diretório conectado ao volume.

### 🧹 Removendo o primeiro container

Depois do teste, paramos e removemos o container:

```powershell
docker stop nginx-volume
docker rm nginx-volume
```

Conferimos os containers existentes:

```powershell
docker ps -a
```

O container `nginx-volume` não apareceu mais na listagem.

**Importante:** removemos o container, mas mantivemos o volume `meu-volume`.

### 🔄 Criando outro container com o mesmo volume

Em seguida, criamos um novo container utilizando o volume anterior:

```powershell
docker run -d --name nginx-volume-teste -p 8080:80 -v meu-volume:/usr/share/nginx/html nginx:latest
```

Para verificar se o arquivo continuava existindo, executamos:

```powershell
docker exec nginx-volume-teste cat /usr/share/nginx/html/teste.txt
```

O resultado foi:

```text
Meus dados continuam salvos no Docker Volume!
```

✨ **Teste concluído com sucesso!**

Mesmo depois de remover o primeiro container, conseguimos recuperar o conteúdo do arquivo utilizando outro container conectado ao mesmo volume.

Isso comprovou que os dados armazenados no volume não dependem do ciclo de vida do container.

## 🌐 6. O que são Bind Mounts?

Os **Bind Mounts** permitem conectar um arquivo ou diretório do computador diretamente a um caminho dentro do container.

Diferentemente dos volumes, que são gerenciados pelo Docker, os Bind Mounts utilizam caminhos existentes no sistema de arquivos do computador.

São muito úteis durante o desenvolvimento, pois permitem modificar arquivos no computador e visualizar as alterações dentro do container.

### 🧩 Entendendo a conexão

**Pasta do computador → Bind Mount → Diretório do container**

Dessa maneira, o container consegue acessar os arquivos presentes na pasta compartilhada.

## 💻 7. Utilizando Bind Mounts na prática

Para testar esse recurso, reutilizamos o projeto criado na Aula 04:

```text
projeto-dockerfile/
├── Dockerfile
└── index.html
```

Nosso diretório no Windows era:

```text
C:\Users\APLAN\Documents\Projetos_Ing\estudos-docker\projeto-dockerfile
```

### 🔎 Conferindo os arquivos

Utilizamos o comando:

```powershell
Get-ChildItem
```

Esse comando lista os arquivos e diretórios existentes no local atual do PowerShell.

O resultado apresentou:

```text
Dockerfile
index.html
```

Também aprendemos que, no PowerShell, `ls` e `dir` são aliases de `Get-ChildItem`.

### 🚀 Criando o container com Bind Mount

Antes de iniciar o novo teste, paramos e removemos o container anterior:

```powershell
docker stop nginx-volume-teste
docker rm nginx-volume-teste
```

Depois, ainda dentro da pasta `projeto-dockerfile`, executamos:

```powershell
docker run -d --name nginx-bind -p 8080:80 --mount "type=bind,source=$($PWD.Path),target=/usr/share/nginx/html" nginx:latest
```

### Entendendo o comando

| Parte | Significado |
| :--- | :--- |
| `docker run` | Cria e inicia um container. |
| `-d` | Executa o container em segundo plano. |
| `--name nginx-bind` | Define o nome do container. |
| `-p 8080:80` | Publica a aplicação na porta 8080 do computador. |
| `type=bind` | Define que será utilizado um Bind Mount. |
| `source=$($PWD.Path)` | Indica o caminho da pasta atual do computador. |
| `target=/usr/share/nginx/html` | Define o diretório de destino dentro do container. |
| `nginx:latest` | Define a imagem utilizada. |

A variável `$PWD.Path` permite obter o caminho completo do diretório atual no PowerShell.

### 🌷 Testando no navegador

Acessamos:

```text
http://localhost:8080
```

A página personalizada foi exibida corretamente.

Em seguida, abrimos o arquivo `index.html` no VS Code e adicionamos uma nova mensagem:

```html
<p>Aprendendo Docker Volumes e Bind Mounts! 🐳</p>
```

Depois de salvar o arquivo, atualizamos o navegador utilizando `Ctrl + F5`.

A alteração apareceu imediatamente, sem precisar reconstruir a imagem ou recriar o container.

✨ **Teste concluído com sucesso!**

Isso confirmou que o Bind Mount estava compartilhando os arquivos entre o Windows e o container.

## 🩷 8. Volumes x Bind Mounts

Durante a aula, aprendemos que os dois mecanismos permitem compartilhar e armazenar dados, mas possuem diferenças importantes.

| Característica | Volumes | Bind Mounts |
| :--- | :--- | :--- |
| Gerenciamento | Gerenciados pelo Docker. | Utilizam caminhos do computador. |
| Local de armazenamento | Área gerenciada pelo Docker. | Diretórios ou arquivos do host. |
| Persistência após remover o container | Sim, enquanto o volume não for removido. | Os arquivos originais permanecem no host. |
| Uso comum | Bancos de dados e dados persistentes. | Desenvolvimento e edição de arquivos. |

### 🧠 Quando utilizar cada um?

- **Volumes:** são recomendados para armazenar dados que precisam continuar existindo independentemente dos containers, como dados de bancos de dados.
- **Bind Mounts:** são úteis durante o desenvolvimento, quando precisamos compartilhar arquivos do computador com o container e visualizar alterações rapidamente.

## 🧹 9. Finalizando a prática

Depois de concluir os testes, realizamos a limpeza dos containers e do volume utilizado.

### Parando e removendo o container

```powershell
docker stop nginx-bind
docker rm nginx-bind
```

Também removemos o container de teste anterior:

```powershell
docker rm nginx-volume-teste
```

### Conferindo os containers

```powershell
docker ps -a
```

Após remover os containers restantes, a listagem ficou vazia.

### Conferindo os volumes

```powershell
docker volume ls
```

Antes da limpeza, encontramos:

```text
DRIVER    VOLUME NAME
local     meu-volume
```

Como já havíamos comprovado a persistência dos dados, removemos o volume de teste:

```powershell
docker volume rm meu-volume
```

Depois, executamos novamente:

```powershell
docker volume ls
```

A listagem ficou vazia, confirmando que o volume havia sido removido.

**Observação:** a remoção de um volume é diferente da remoção de um container. Ao remover o volume, seus dados também são excluídos. Por isso, devemos ter cuidado antes de executar esse comando.

## 📝 10. Resumo da aula

- 📦 Docker Volumes permitem armazenar dados independentemente dos containers.
- 🛠️ `docker volume create` cria um volume.
- 🔎 `docker volume ls` lista os volumes existentes.
- 🔍 `docker volume inspect` apresenta informações detalhadas de um volume.
- 🔗 A opção `-v` permite conectar um volume a um container.
- 🔄 Os dados de um volume continuam disponíveis mesmo após a remoção do container.
- 💻 Bind Mounts conectam arquivos ou diretórios do computador aos containers.
- 🌐 Alterações nos arquivos compartilhados por Bind Mounts podem ser visualizadas sem reconstruir a imagem.
- 🩷 Volumes são gerenciados pelo Docker, enquanto Bind Mounts utilizam caminhos do computador.
- 🧹 `docker volume rm` remove um volume e seus dados.

---

🎀 **Fim da Aula 05** 🐳
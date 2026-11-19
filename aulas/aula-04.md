# 🐳 Aula 04 — Dockerfile e construção de imagens

> 🌷 Aprendendo a criar imagens Docker personalizadas a partir de um Dockerfile e executar aplicações em containers.

---

## 🩷 1. O que é um Dockerfile?

O **Dockerfile** é um arquivo de texto que contém instruções utilizadas pelo Docker para construir uma imagem personalizada.

Por meio dele, podemos definir:

- Qual imagem será utilizada como base;
- Quais arquivos serão adicionados;
- Quais comandos serão executados durante a construção;
- Qual será o diretório de trabalho;
- Qual comando será executado quando o container iniciar.

O processo funciona da seguinte maneira:

**Dockerfile → docker build → Imagem → docker run → Container**

## 🧩 2. Principais instruções do Dockerfile

| Instrução | Função |
| :--- | :--- |
| `FROM` | Define a imagem base utilizada na construção. |
| `WORKDIR` | Define o diretório de trabalho dentro da imagem. |
| `COPY` | Copia arquivos do contexto de construção para dentro da imagem. |
| `RUN` | Executa comandos durante a construção da imagem. |
| `CMD` | Define o comando padrão executado quando o container inicia. |
| `EXPOSE` | Documenta a porta que a aplicação utiliza dentro do container. |

### 🌸 Diferença entre RUN e CMD

- **RUN:** executa comandos durante a construção da imagem.
- **CMD:** define o comando padrão que será executado quando o container for iniciado.

### 🌐 Atenção ao EXPOSE

A instrução `EXPOSE` não publica automaticamente uma porta no computador.

Para permitir o acesso à aplicação pelo navegador, utilizamos `-p` no comando `docker run`.

## 🖥️ 3. Criando nosso primeiro projeto

Para colocar os conceitos em prática, criamos uma pasta chamada `projeto-dockerfile`.

Dentro dela, criamos dois arquivos:

```text
projeto-dockerfile/
├── Dockerfile
└── index.html
```

### 📄 Arquivo index.html

Criamos uma página HTML simples para ser servida pelo Nginx:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu primeiro Dockerfile</title>
</head>
<body>
    <h1>Olá, Docker! 🐳</h1>
    <p>Minha primeira página servida por uma imagem personalizada.</p>
</body>
</html>
```

## 🐳 4. Criando nosso Dockerfile

Em seguida, criamos o arquivo `Dockerfile` com as seguintes instruções:

```dockerfile
# Define a imagem base que será utilizada
FROM nginx:latest

# Copia nossa página HTML para a pasta padrão do Nginx
COPY index.html /usr/share/nginx/html/index.html

# Documenta a porta utilizada pela aplicação
EXPOSE 80
```

### 🔍 Entendendo o arquivo

1. `FROM nginx:latest`: utiliza a imagem do Nginx como base.
2. `COPY`: copia nosso arquivo HTML para o diretório padrão de páginas do Nginx.
3. `EXPOSE 80`: documenta que a aplicação utiliza a porta 80 dentro do container.

## ⚙️ 5. Construindo nossa imagem

Com os arquivos preparados, executamos o comando:

```powershell
docker build -t minha-pagina:v1 .
```

### Entendendo o comando

| Parte | Significado |
| :--- | :--- |
| `docker build` | Constrói uma imagem Docker. |
| `-t` | Define o nome e a tag da imagem. |
| `minha-pagina:v1` | Nome da imagem e sua versão. |
| `.` | Indica que o contexto de construção é a pasta atual. |

### ✨ Resultado

A construção foi concluída com sucesso!

Durante o processo, o Docker:

1. Leu o arquivo Dockerfile;
2. Utilizou `nginx:latest` como imagem base;
3. Copiou o arquivo `index.html`;
4. Gerou a imagem personalizada `minha-pagina:v1`.

**Observação:** como a imagem Nginx já havia sido baixada na aula anterior, o Docker pôde reutilizá-la durante a construção.

## 🚀 6. Executando nosso container

Depois de construir a imagem, criamos um container com o comando:

```powershell
docker run -d -p 8080:80 --name minha-pagina minha-pagina:v1
```

### Entendendo o comando

| Parte | Função |
| :--- | :--- |
| `docker run` | Cria e inicia um container. |
| `-d` | Executa o container em segundo plano. |
| `-p 8080:80` | Mapeia a porta 8080 do computador para a porta 80 do container. |
| `--name minha-pagina` | Define o nome do container. |
| `minha-pagina:v1` | Define a imagem utilizada. |

### 🌷 Testando no navegador

Acessamos o endereço:

```text
http://localhost:8080
```

A página personalizada foi exibida corretamente, mostrando a mensagem:

**Olá, Docker! 🐳**

Inicialmente, o navegador ainda apresentou a página padrão do Nginx. Após atualizar utilizando `Ctrl + F5`, a página criada por nós foi exibida.

## 🔎 7. Verificando o conteúdo dentro do container

Para confirmar se nosso HTML havia sido copiado corretamente, executamos:

```powershell
docker exec minha-pagina cat /usr/share/nginx/html/index.html
```

O comando exibiu o conteúdo do arquivo HTML armazenado dentro do container.

Isso confirmou que a instrução `COPY` havia funcionado corretamente.

## 📚 8. Imagem x Container: reforçando o conceito

Durante a prática, vimos que a imagem e o container são elementos diferentes.

- **Imagem:** contém os arquivos e as instruções necessários para criar containers.
- **Container:** é uma instância criada a partir de uma imagem.

Também aprendemos que, na configuração utilizada, o arquivo HTML é copiado para dentro da imagem durante a construção.

Portanto, alterar o `index.html` original no computador não atualiza automaticamente o arquivo que está dentro da imagem.

Para aplicar uma alteração, precisamos:

1. Modificar o arquivo HTML;
2. Construir novamente a imagem;
3. Recriar o container utilizando a imagem atualizada.

Mais adiante, estudaremos **Volumes e Bind Mounts**, que permitem compartilhar arquivos entre o computador e os containers.

## 🧹 9. Finalizando a prática

Depois de testar nossa aplicação, realizamos a limpeza do ambiente.

### Parando o container

```powershell
docker stop minha-pagina
```

O comando interrompeu a execução do container.

### Removendo o container

```powershell
docker rm minha-pagina
```

O comando removeu o container.

### Conferindo os containers

```powershell
docker ps -a
```

O resultado ficou vazio, confirmando que o container havia sido removido.

### Conferindo as imagens

```powershell
docker images
```

Nossa imagem personalizada continuou armazenada:

```text
minha-pagina:v1
```

Isso confirmou novamente que remover um container não significa remover a imagem utilizada para criá-lo.

## 📝 10. Resumo da aula

- 🐳 Dockerfile é um arquivo que contém instruções para construir imagens.
- 🖼️ `FROM` define a imagem base.
- 📂 `COPY` copia arquivos para dentro da imagem.
- ⚙️ `RUN` executa comandos durante a construção.
- 🚀 `CMD` define o comando padrão executado na inicialização do container.
- 🌐 `EXPOSE` documenta a porta utilizada pela aplicação.
- 🛠️ `docker build` constrói imagens personalizadas.
- 📦 `docker run` cria e inicia containers.
- 🔄 Alterações em arquivos copiados para a imagem exigem uma nova construção para serem aplicadas.

---

🎀 **Fim da Aula 04** 🐳

# 🐳 Aula 01 — Introdução ao Docker

> 🌷 Primeiros conceitos e configurações para começar a trabalhar com containers.

---

## 🩷 1. O que é Docker?

Docker é uma plataforma que permite criar, executar e gerenciar aplicações em **containers**.

Um container reúne a aplicação e os recursos necessários para executá-la, como bibliotecas, dependências e configurações. Isso ajuda a manter o ambiente de execução consistente, mesmo quando a aplicação é executada em computadores diferentes.

Na prática, o Docker facilita o desenvolvimento, os testes e a distribuição de aplicações.

## 💻 2. Máquinas virtuais x Containers

Embora os dois recursos permitam ambientes isolados, eles funcionam de maneiras diferentes.

| Máquinas virtuais 🖥️ | Containers 📦 |
|---|---|
| Possuem um sistema operacional próprio. | Compartilham o kernel do sistema operacional do host. |
| Virtualizam o hardware. | Isolam aplicações e seus processos. |
| Geralmente consomem mais recursos. | Geralmente são mais leves. |
| Podem levar mais tempo para iniciar. | Costumam iniciar mais rapidamente. |

## 🧩 3. Conceitos fundamentais

### 🖼️ Imagem (Image)

É o modelo utilizado para criar containers. Contém os arquivos, dependências e instruções necessários para executar uma aplicação.

### 📦 Container

É uma instância criada a partir de uma imagem. É nele que a aplicação é executada.

### 🌐 Docker Hub

É um serviço que funciona como um repositório de imagens Docker, permitindo que usuários encontrem, baixem e compartilhem imagens.

## ⚙️ 4. Primeiro teste com Docker

Após a instalação, foi executado o comando:

```bash
docker run hello-world
```

Esse comando realiza as seguintes etapas:

1. Verifica se a imagem `hello-world` está disponível localmente.
2. Caso não esteja, baixa a imagem do Docker Hub.
3. Cria um container a partir dessa imagem.
4. Executa o programa dentro do container.

Ao final, o Docker exibe a mensagem `Hello from Docker!`, confirmando que a instalação e a comunicação com o Docker Engine estão funcionando.

## 🛠️ 5. Outros conceitos importantes

- **Dockerfile:** arquivo que contém as instruções utilizadas para construir uma imagem Docker.
- **Docker Compose:** ferramenta que permite definir e executar aplicações que utilizam múltiplos serviços.

---

## 📝 6. Resumo da aula

- 🐳 Docker é uma plataforma para trabalhar com containers.
- 🖼️ Imagens são utilizadas como modelos para criar containers.
- 📦 Containers são ambientes isolados nos quais as aplicações são executadas.
- 🌐 Docker Hub permite armazenar e compartilhar imagens.
- ⚙️ O comando `docker run hello-world` foi utilizado para verificar o funcionamento da instalação.

---

🎀 *Fim da Aula 01* 🎀

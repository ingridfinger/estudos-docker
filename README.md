# 🐳₊˚⊹ Estudos com Docker

\<p align="center">
&#x20; \<img src="[https://img.shields.io/badge/Docker-29.9.3-2496ED?style=for-the-badge&logo=docker&logoColor=white](https://img.shields.io/badge/Docker-29.9.3-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)" />
&#x20; \<img src="[https://img.shields.io/badge/WSL-2-4A90D9?style=for-the-badge&logo=linux&logoColor=white](https://img.shields.io/badge/WSL-2-4A90D9?style=for-the-badge\&logo=linux\&logoColor=white)" />
&#x20; \<img src="[https://img.shields.io/badge/Status-Em%20aprendizado-FFB6C1?style=for-the-badge](https://img.shields.io/badge/Status-Em%20aprendizado-FFB6C1?style=for-the-badge)" />
\</p>

\<p align="center">
&#x20; 🌷 Um cantinho dedicado aos meus estudos, experimentos e descobertas com Docker!
\</p>

---

## 🎀 Sobre o projeto

Este repositório foi criado para documentar minha jornada de aprendizado com **Docker**, desde a instalação e configuração do ambiente até a criação e execução de contêineres em projetos práticos.

A ideia é reunir anotações, comandos, exercícios e pequenos projetos para acompanhar minha evolução. ♡

## 🖥️ Meu ambiente de desenvolvimento

| Ferramenta          | Configuração   |
| :------------------ | :------------- |
| Sistema operacional | Windows        |
| Subsistema Linux    | WSL 2          |
| Distribuição Linux  | Ubuntu         |
| Plataforma          | Docker Desktop |
| Versão do Docker    | 29.9.3         |

## 🐧 01. Preparando o ambiente

Antes de começar os estudos, configurei o ambiente com:

- WSL 2 (Windows Subsystem for Linux);
- Ubuntu instalado no WSL;
- Docker Desktop para Windows;
- Integração com o WSL 2.

## 🧪 02. Primeiro teste: Hello World!

Depois da instalação, chegou a hora de verificar se estava tudo funcionando.

**Comando utilizado:**

```powershell
docker --version
```

**Resultado:**

```text
Docker version 29.9.3, build 5457199
```

Em seguida, executei meu primeiro contêiner:

```powershell
docker run hello-world
```

\<details>
\<summary>🌸 Resultado do primeiro teste\</summary>

```text
Hello from Docker!

This message shows that your installation
appears to be working correctly.
```

\</details>

✨ **Teste concluído com sucesso!**

O Docker conseguiu:

1. Estabelecer comunicação entre o cliente Docker e o Docker Engine;
2. Baixar a imagem `hello-world` do Docker Hub;
3. Criar um contêiner a partir da imagem;
4. Executar o contêiner e apresentar o resultado no terminal.

## 🌷 Objetivo

Construir uma base sólida em Docker, desenvolver habilidades práticas e aprender a utilizar contêineres no desenvolvimento e na implantação de aplicações.

---

\<p align="center">   Feito com dedicação, café e um pouquinho de fofura. ♡   \<br/>   \<strong>Um passo de cada vez! 🎀\</strong> \</p>

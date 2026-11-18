# 🐳 Aula 06 — Redes no Docker

> 🌷 Aprendendo como os containers se comunicam entre si e com o mundo externo.

---

## 🌐 1. O que são redes no Docker?

As redes do Docker permitem que os containers se comuniquem uns com os outros e com outras redes.

Uma aplicação pode ser dividida em diferentes serviços, como:

- **Container da aplicação:** executa o sistema.
- **Container do banco de dados:** armazena as informações.

Esses containers precisam trocar informações. As redes do Docker permitem essa comunicação de maneira organizada e isolada.

## 🧩 2. Principais tipos de rede

O Docker possui diferentes drivers de rede. Conhecemos três dos principais:

| Tipo | Funcionamento |
|---|---|
| `bridge` | Permite a comunicação entre containers em uma rede local do Docker. |
| `host` | Compartilha a rede do host diretamente com o container. |
| `none` | Desativa a conectividade de rede externa do container, mantendo a interface de loopback. |

Nesta aula, nosso foco foi a rede `bridge`, especialmente as redes criadas pelo próprio usuário (*user-defined bridge*).

## 💻 3. Listando as redes existentes

Para visualizar as redes disponíveis no Docker, utilizamos:

```powershell
docker network ls
```

Inicialmente, foram apresentadas três redes padrão:

| Rede | Driver | Scope |
|---|---|---|
| `bridge` | bridge | local |
| `host` | host | local |
| `none` | null | local |

A rede `bridge` padrão é utilizada quando um container é iniciado sem especificar outra rede. Já as redes `bridge` criadas pelo usuário oferecem resolução automática de nomes entre os containers conectados.

## 🎀 4. Criando uma rede personalizada

Criamos uma rede chamada `minha-rede` com o comando:

```powershell
docker network create minha-rede
```

Em seguida, executamos novamente:

```powershell
docker network ls
```

A nova rede apareceu com as seguintes configurações:

| Propriedade | Valor |
|---|---|
| Nome | `minha-rede` |
| Driver | `bridge` |
| Scope | `local` |

## 📦 5. Conectando containers à rede

Criamos dois containers utilizando a imagem `nginx:latest` e conectando ambos à rede `minha-rede`.

**Primeiro container:**

```powershell
docker run -d --name container1 --network minha-rede nginx:latest
```

**Segundo container:**

```powershell
docker run -d --name container2 --network minha-rede nginx:latest
```

Para verificar se estavam em execução, utilizamos:

```powershell
docker ps
```

Os dois containers apareceram com status `Up`.

### Entendendo os parâmetros

| Parâmetro | Função |
|---|---|
| `-d` | Executa o container em segundo plano. |
| `--name` | Define o nome do container. |
| `--network` | Conecta o container à rede especificada. |
| `nginx:latest` | Imagem utilizada para criar o container. |

## 🌐 6. Comunicação entre containers

Uma das vantagens das redes `bridge` criadas pelo usuário é a resolução automática de nomes por meio do DNS interno do Docker.

Isso permite que um container encontre outro utilizando seu nome, sem precisar descobrir manualmente o endereço IP.

**Teste do container1 para o container2:**

```powershell
docker exec container1 getent hosts container2
```

Resultado:

```text
172.18.0.3      container2
```

**Teste do container2 para o container1:**

```powershell
docker exec container2 getent hosts container1
```

Resultado:

```text
172.18.0.2      container1
```

Os resultados demonstraram que os dois containers conseguiram resolver os nomes um do outro.

## 🩷 7. Testando a comunicação HTTP

Além de localizar o outro container, também testamos a comunicação HTTP.

Executamos dentro do `container1`:

```powershell
docker exec container1 curl http://container2
```

O comando retornou o HTML da página padrão do Nginx, incluindo a mensagem `Welcome to nginx!`.

Isso comprovou que o `container1` conseguiu acessar o serviço Nginx executado no `container2`.

**Uma observação importante:** não foi necessário publicar a porta 80 no computador utilizando `-p`. Os containers conseguiram se comunicar diretamente pela rede interna do Docker.

## 🔎 8. Inspecionando a rede

Para visualizar os detalhes da rede, utilizamos:

```powershell
docker network inspect minha-rede
```

Entre as informações apresentadas, estavam:

| Propriedade | Valor observado |
|---|---|
| Nome | `minha-rede` |
| Driver | `bridge` |
| Sub-rede | `172.18.0.0/16` |
| Gateway | `172.18.0.1` |
| IPv4 | Habilitado |
| IPv6 | Desabilitado |
| Scope | `local` |

### Containers conectados

| Container | Endereço IP |
|---|---|
| `container1` | `172.18.0.2` |
| `container2` | `172.18.0.3` |

O comando também apresentou informações como os identificadores dos containers, endereços MAC e configurações de conectividade.

## 🧹 9. Limpando o ambiente

Após os testes, removemos os recursos criados durante a aula.

**Parando os containers:**

```powershell
docker stop container1 container2
```

**Removendo os containers:**

```powershell
docker rm container1 container2
```

**Removendo a rede personalizada:**

```powershell
docker network rm minha-rede
```

Por fim, verificamos as redes restantes:

```powershell
docker network ls
```

O resultado apresentou novamente apenas as três redes padrão:

- `bridge`
- `host`
- `none`

✨ Limpeza concluída com sucesso!

## 📚 10. Resumo da aula

- 🌐 Redes Docker permitem a comunicação entre containers.
- 🧩 Conhecemos os drivers `bridge`, `host` e `none`.
- ⚙️ Utilizamos `docker network ls` para listar redes.
- 🎀 Criamos uma rede personalizada com `docker network create`.
- 📦 Conectamos containers à rede utilizando `--network`.
- 🔎 Utilizamos o DNS interno para localizar containers pelos nomes.
- 🌐 Testamos a comunicação HTTP entre containers com `curl`.
- 🔍 Inspecionamos as configurações da rede com `docker network inspect`.
- 🧹 Removemos os containers e a rede criada durante a prática.

---

🐳 **Fim da Aula 06** 🐳
# 🐳 Aula 11 — Logs, inspeção e diagnóstico de problemas

> 🌷 Aprendendo a monitorar containers, consultar informações detalhadas e identificar possíveis problemas utilizando ferramentas do Docker.

---

## 🩷 1. Consultando logs de containers

Os **logs** permitem acompanhar as mensagens produzidas pelos processos executados dentro de um container.

São muito úteis para entender o comportamento de uma aplicação, verificar se ela iniciou corretamente e identificar possíveis erros.

### 🔎 Visualizando todos os logs

Para consultar os registros de um container, utilizamos:

```powershell
docker logs mysql-aula10
```

O comando exibiu os registros de inicialização do MySQL, incluindo:

- Inicialização do servidor;
- Preparação do banco de dados;
- Inicialização do InnoDB;
- Configuração das conexões;
- Mensagem `ready for connections`.

Essa última mensagem confirmou que o servidor MySQL estava pronto para receber conexões na porta 3306.

### 🌸 Exibindo apenas as últimas linhas

Quando queremos consultar somente as mensagens mais recentes, podemos utilizar `--tail`.

```powershell
docker logs --tail 5 mysql-aula10
```

O comando exibe apenas as cinco últimas linhas dos logs.

### 📡 Acompanhando os logs em tempo real

Também podemos acompanhar novas mensagens à medida que são produzidas:

```powershell
docker logs -f mysql-aula10
```

A opção `-f` significa *follow* e permite acompanhar os registros continuamente.

Para interromper a visualização, utilizamos `Ctrl + C`. Isso não interrompe o container, apenas encerra o acompanhamento dos logs.

---

## 🔍 2. Inspecionando containers com docker inspect

O comando `docker inspect` permite consultar informações detalhadas sobre um container, incluindo seu estado, imagem, configurações, variáveis de ambiente, redes, portas e volumes.

Para visualizar todas as informações, executamos:

```powershell
docker inspect mysql-aula10
```

O resultado é apresentado em formato JSON.

### 🧩 Informações importantes

Durante a inspeção do `mysql-aula10`, identificamos:

| Informação | Resultado |
| :--- | :--- |
| Estado | `running` |
| Em execução | `true` |
| Estado de saúde | `healthy` |
| Reinicializações | `0` |
| Imagem | `mysql:8.4` |
| Porta | `3306` |
| Rede | `aula-10_default` |
| Volume | `aula-09_mysql_data` |
| IP interno | `172.19.0.2` |

### 🌷 Diferença entre running e healthy

- **Running:** indica que o container está em execução.
- **Healthy:** indica que o container passou no teste de saúde (*healthcheck*) configurado.

Um container pode estar em execução sem estar saudável. No nosso caso, o MySQL apresentou os dois estados positivos.

### ⚙️ Consultando informações específicas com --format

O parâmetro `--format` permite selecionar somente a informação desejada, utilizando templates.

Para consultar o estado de saúde:

```powershell
docker inspect --format='{{.State.Health.Status}}' mysql-aula10
```

**Resultado:**

```text
healthy
```

Também utilizamos o comando abaixo para consultar o endereço IP interno:

```powershell
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql-aula10
```

**Resultado observado:**

```text
172.19.0.2
```

Nesse caso, utilizamos `range` para percorrer as redes conectadas ao container e obter o endereço IP de cada uma.

---

## 📊 3. Monitorando recursos com docker stats

O comando `docker stats` permite acompanhar o consumo de recursos dos containers em execução.

Executamos:

```powershell
docker stats
```

Durante a prática, observamos os seguintes dados do `mysql-aula10`:

| Métrica | Resultado observado | Significado |
| :--- | :--- | :--- |
| CPU % | 5,13% | Percentual de utilização da CPU. |
| MEM USAGE | 459,6 MiB | Memória utilizada. |
| MEM LIMIT | 3,709 GiB | Limite de memória apresentado. |
| MEM % | 12,10% | Percentual do limite utilizado. |
| NET I/O | 5,49 kB / 4,5 kB | Dados recebidos e enviados pela rede. |
| BLOCK I/O | 134 MB / 17 MB | Dados lidos e escritos em dispositivos de armazenamento. |
| PIDS | 35 | Quantidade de processos no container. |

O comando atualiza as informações continuamente.

Para sair da visualização, utilizamos `Ctrl + C`.

### 🌸 Consultando processos com docker top

Enquanto `docker stats` apresenta o consumo de recursos, `docker top` permite visualizar os processos em execução dentro de um container.

```powershell
docker top mysql-aula10
```

Durante a prática, identificamos o processo:

```text
UID   PID   PPID   C   STIME   TTY   TIME       CMD
999   566   540    1   12:31   ?     00:00:40   mysqld
```

O processo `mysqld` corresponde ao servidor MySQL.

Alguns campos importantes:

- **UID:** usuário responsável pela execução do processo.
- **PID:** identificador do processo.
- **PPID:** identificador do processo pai.
- **TIME:** tempo de CPU acumulado.
- **CMD:** comando ou processo executado.

---

## 🚨 4. Identificando problemas em containers

Uma etapa importante do trabalho com Docker é identificar por que um container parou de funcionar.

Para visualizar todos os containers, inclusive os que já foram encerrados, utilizamos:

```powershell
docker ps -a
```

Durante a prática, identificamos três containers:

| Container | Estado | Interpretação |
| :--- | :--- | :--- |
| `app-aula10` | `Exited (0)` | Aplicação Python finalizada normalmente. |
| `mysql-aula10` | `Up (healthy)` | MySQL em execução e saudável. |
| `mysql-estudos` | `Exited (0)` | Container antigo da Aula 09, encerrado normalmente. |

### 🌷 Entendendo os códigos de saída

O código de saída indica como o processo terminou.

| Código | Significado |
| :--- | :--- |
| `0` | Execução concluída com sucesso. |
| `1` | Execução encerrada indicando erro. |

**Importante:** o estado `Exited` não significa necessariamente que ocorreu um problema.

Na Aula 10, nossa aplicação Python consultava o banco de dados, apresentava os registros encontrados e encerrava sua execução. Por isso, o resultado `Exited (0)` era esperado.

### 🔎 Consultando os logs da aplicação

Para investigar o `app-aula10`, executamos:

```powershell
docker logs app-aula10
```

**Resultado:**

```text
Conexão com o MySQL estabelecida!

Beneficiários cadastrados:
(2, 'Maria Souza', 'Tres Lagoas')
```

As mensagens confirmaram que a aplicação conseguiu se conectar ao MySQL, executar a consulta e recuperar o registro cadastrado.

Portanto, o encerramento do container não representava uma falha.

---

## 🧪 5. Simulando um erro proposital

Para entender como o Docker registra falhas, realizamos uma simulação controlada utilizando a imagem `aula-10-app`.

Executamos:

```powershell
docker run --name app-teste-erro aula-10-app python -c "import sys; print('Erro simulado'); sys.exit(1)"
```

O comando executou um pequeno código Python que:

1. Importou o módulo `sys`;
2. Exibiu a mensagem `Erro simulado`;
3. Encerrou o processo utilizando `sys.exit(1)`.

**Resultado exibido:**

```text
Erro simulado
```

### 🔍 Identificando o container com erro

Em seguida, consultamos os containers:

```powershell
docker ps -a
```

Identificamos:

```text
Exited (1)
```

Isso indicava que o processo havia terminado com código de erro.

### 📄 Consultando os logs

Para investigar o que aconteceu, executamos:

```powershell
docker logs app-teste-erro
```

**Resultado:**

```text
Erro simulado
```

A mensagem confirmou o que havia sido executado pelo programa.

### ⚙️ Consultando o código de saída

Também utilizamos o `docker inspect` para consultar diretamente o código de saída:

```powershell
docker inspect --format='{{.State.ExitCode}}' app-teste-erro
```

**Resultado:**

```text
1
```

Assim, confirmamos que o processo havia sido encerrado com erro.

### 🌸 Removendo o container de teste

Após concluir a simulação, removemos o container:

```powershell
docker rm app-teste-erro
```

A remoção do container não apagou a imagem `aula-10-app`.

---

## 🧩 6. Diagnóstico utilizando docker inspect

Para finalizar a prática, reunimos diferentes informações em um único comando.

Executamos:

```powershell
docker inspect --format='Status={{.State.Status}} | ExitCode={{.State.ExitCode}} | Error={{.State.Error}}' app-aula10
```

**Resultado:**

```text
Status=exited | ExitCode=0 | Error=
```

### 🔍 Interpretando o resultado

- `Status=exited`: o container não está mais em execução.
- `ExitCode=0`: o processo terminou normalmente.
- `Error=`: nenhuma mensagem de erro foi registrada nesse campo.

Concluímos que o `app-aula10` havia finalizado corretamente, pois sua função era executar uma consulta no MySQL e encerrar o processo.

---

## 📚 7. Principais comandos da aula

| Comando | Função |
| :--- | :--- |
| `docker logs` | Exibe os logs de um container. |
| `docker logs --tail 5` | Exibe as últimas cinco linhas. |
| `docker logs -f` | Acompanha os logs em tempo real. |
| `docker inspect` | Exibe informações detalhadas do container. |
| `docker inspect --format` | Consulta informações específicas. |
| `docker stats` | Monitora o consumo de recursos. |
| `docker top` | Exibe os processos em execução. |
| `docker ps -a` | Lista todos os containers, inclusive os encerrados. |
| `docker rm` | Remove um container. |

---

## 📝 8. Resumo da aula

- 📝 Os logs permitem acompanhar o funcionamento e investigar problemas em containers.
- 🔍 `docker inspect` apresenta informações detalhadas sobre configurações e estados.
- ⚙️ `--format` permite consultar campos específicos sem exibir todo o JSON.
- 💻 `docker stats` monitora o consumo de CPU, memória, rede e armazenamento.
- 📊 `docker top` apresenta os processos em execução.
- 🚨 `docker ps -a` permite identificar containers encerrados.
- 🔢 O código `0` indica encerramento bem-sucedido, enquanto o código `1` indica uma execução com erro.
- 🧪 A simulação com `sys.exit(1)` permitiu observar como o Docker registra uma falha.
- 🩷 A combinação de logs, inspeção e códigos de saída ajuda a diagnosticar problemas.

---

🐳 **Fim da Aula 11** 🐳
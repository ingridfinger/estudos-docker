
# Utiliza uma imagem oficial do Python como base
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para dentro do container
COPY app/requirements.txt .

# Instala as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para dentro do container
COPY app/ .

# Define o comando executado quando o container iniciar
CMD ["python", "app.py"]

FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY . .

# Instalar dependências de sistema necessárias para Prophet
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install numpy cython && \
    pip install prophet && \
    pip install -r requirements.txt

# Configure environment variables to suppress TensorFlow warnings and use CPU only
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV CUDA_VISIBLE_DEVICES=-1

# Criar diretórios necessários
RUN mkdir -p data

EXPOSE 8501
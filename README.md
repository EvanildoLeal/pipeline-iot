# 🌡️ Pipeline de Dados IoT - Monitoramento de Temperatura

![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)
![Docker](https://img.shields.io/badge/docker-latest-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Sobre o Projeto

Este projeto implementa um **pipeline completo de dados para IoT** (Internet das Coisas), processando leituras de temperatura de sensores e disponibilizando um dashboard interativo para monitoramento em tempo real.

### 🎯 Objetivos

- Processar grandes volumes de dados de sensores IoT
- Armazenar dados de forma eficiente em PostgreSQL
- Criar views SQL para análises rápidas
- Disponibilizar dashboard interativo com Streamlit
- Garantir reprodutibilidade via Docker

### 📊 Dataset Utilizado

- **Fonte:** Sensores IoT de temperatura
- **Período:** 28/07/2018 a 08/12/2018
- **Registros:** 97.606 leituras
- **Dispositivos:** 97.605 sensores únicos
- **Temperaturas:** 21°C a 51°C
- **Download:** [IOT-temp.csv](https://www.kaggle.com/datasets/iot-temperature-data) (Kaggle)

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| **Python** | 3.14+ | Linguagem principal |
| **PostgreSQL** | 18 | Banco de dados relacional |
| **Docker** | Latest | Containerização |
| **Streamlit** | 1.56+ | Dashboard interativo |
| **Pandas** | 3.0+ | Manipulação de dados |
| **SQLAlchemy** | 2.0+ | ORM e conexão |
| **Plotly** | 5.17+ | Gráficos interativos |

## 📁 Estrutura do Projeto

Pipeline de Dados IoT/
│
├── src/ # Código fonte principal
│ ├── ingestion_adapted.py # Pipeline de ingestão de dados
│ ├── database.py # Conexão com banco de dados
│ └── queries.py # Consultas SQL auxiliares
│
├── dashboards/ # Aplicação Streamlit
│ └── dashboard.py # Dashboard interativo
│
├── sql/ # Scripts SQL
│ └── create_views.sql # Views do banco de dados
│
├── data/ # Dados fonte
│ └── IOT-temp.csv # Dataset de temperaturas (97.606 registros)
│
├── docs/ # Documentação
│ ├── RELATORIO_PROJETO.md # Relatório técnico completo
│ ├── INSTALL.md # Guia de instalação
│ ├── API.md # Documentação da API
│ └── images/ # Imagens do dashboard
│
├── scripts/ # Scripts auxiliares
│ ├── init_db.py # Inicialização do banco
│ └── cleanup.py # Limpeza de dados duplicados
│
├── logs/ # Logs do sistema
├── tests/ # Testes unitários
├── requirements.txt # Dependências Python
├── docker-compose.yml # Orquestração Docker
├── .env.example # Exemplo de variáveis de ambiente
├── .gitignore # Arquivos ignorados pelo Git
└── README.md # Este arquivo


## 🚀 Instalação e Execução

### Pré-requisitos

- **Docker Desktop** (Windows/Mac) ou Docker Engine (Linux)
- **Python 3.14+**
- **Git** (para clonar o repositório)
- **8GB RAM** (recomendado)

### Passo a Passo

#### 1. Clone o repositório

```bash
# Clone o repositório
git clone https://github.com/EvanildoLeal/pipeline-iot.git
cd pipeline-iot

# Verifique os arquivos
ls -la

Configure o ambiente virtual
# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

Instale as dependências
# Instale todas as dependências
python -m pip install -r requirements.txt

# Verifique a instalação
python -c "import pandas, streamlit, sqlalchemy; print('✅ Dependências instaladas!')"

 Configure as variáveis de ambiente
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
# (Use nano, vim ou qualquer editor)
nano .env

Conteúdo do .env:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
LOG_LEVEL=INFO

Inicie o container PostgreSQL com Docker
# Método 1: Usando docker-compose (recomendado)
docker-compose up -d

# Método 2: Usando docker run diretamente
docker run --name postgres-iot \
  -e POSTGRES_PASSWORD=sua_senha \
  -p 5432:5432 \
  -d postgres

# Verifique se o container está rodando
docker ps

Prepare o dataset
# Copie o arquivo CSV para a pasta data/
# Baixe o dataset do Kaggle ou use o fornecido
cp /caminho/do/seu/IOT-temp.csv data/

# Verifique se o arquivo foi copiado
ls -la data/

Download do dataset:
https://www.kaggle.com
(https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-de
vices

Execute o pipeline de ingestão
# Execute o script de ingestão
python src/ingestion_adapted.py

# Saída esperada:
# ============================================================
# 🚀 Pipeline de Ingestão de Dados IoT - Temperaturas
# ============================================================
# ✅ Tabela criada/verificada com sucesso!
# 📊 Total de linhas no CSV: 97606
# 📈 Estatísticas dos dados:
#    - Temperatura média: 35.05°C
#    - Temperatura mínima: 21.00°C
#    - Temperatura máxima: 51.00°C
# ✅ Total de registros inseridos: 97605

Crie as views SQL
# Execute o script de criação das views
python -c "
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
load_dotenv()

connection_string = f\"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}\"
engine = create_engine(connection_string)

with open('sql/create_views.sql', 'r') as f:
    sql = f.read()

with engine.connect() as conn:
    for statement in sql.split(';'):
        if statement.strip():
            conn.execute(text(statement))
            conn.commit()
    print('✅ Views criadas com sucesso!')
"

## 📊 Dashboard - Capturas de Tela

### 1. Dashboard Completo
![Dashboard Full](dashboard_full.png)

### 2. Gráfico de Barras
![Gráfico de Barras](grafico_barras.png)

### 3. Gráfico de Evolução
![Gráfico de Evolução](grafico_evolucao.jpg)

### 4. Gráfico por Hora
![Gráfico por Hora](grafico_hora.png)

🗄️ Views SQL Implementadas
avg_temp_por_dispositivo
Propósito: Identificar dispositivos com maior temperatura média.
CREATE VIEW avg_temp_por_dispositivo AS
SELECT 
    device_id,
    COUNT(*) as total_leituras,
    ROUND(AVG(temperature)::numeric, 2) as avg_temp,
    ROUND(MIN(temperature)::numeric, 2) as min_temp,
    ROUND(MAX(temperature)::numeric, 2) as max_temp
FROM temperature_readings
GROUP BY device_id
ORDER BY avg_temp DESC
LIMIT 20;

leituras_por_hora
Propósito: Analisar padrões temporais de temperatura.
CREATE VIEW leituras_por_hora AS
SELECT 
    EXTRACT(HOUR FROM timestamp) as hora,
    COUNT(*) as contagem,
    ROUND(AVG(temperature)::numeric, 2) as temp_media
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM timestamp)
ORDER BY hora;

temp_por_localizacao
Propósito: Comparar temperaturas internas vs externas.
CREATE VIEW temp_por_localizacao AS
SELECT 
    in_out as localizacao,
    COUNT(*) as total_leituras,
    ROUND(AVG(temperature)::numeric, 2) as temp_media,
    ROUND(MIN(temperature)::numeric, 2) as temp_min,
    ROUND(MAX(temperature)::numeric, 2) as temp_max
FROM temperature_readings
GROUP BY in_out;

temp_max_min_por_dia (Extra)
Propósito: Monitorar evolução diária das temperaturas.
CREATE VIEW temp_max_min_por_dia AS
SELECT 
    DATE(timestamp) as data,
    ROUND(MIN(temperature)::numeric, 2) as temp_min,
    ROUND(MAX(temperature)::numeric, 2) as temp_max,
    ROUND(AVG(temperature)::numeric, 2) as temp_media
FROM temperature_readings
GROUP BY DATE(timestamp)
ORDER BY data DESC;
📊 Resultados e Métricas
Estatísticas do Pipeline
Métrica	Valor
Total de registros processados	97.606
Registros inseridos no banco	97.605
Dispositivos únicos	97.605
Período dos dados	133 dias
Temperatura média	35,05°C
Temperatura mínima	21,00°C
Temperatura máxima	51,00°C
Tempo de processamento	~30 segundos

Performance
Inserção em batches: 10.000 registros por vez

Índices criados: 2 (device_id+timestamp, timestamp)

Tamanho do banco: ~15 MB

Consulta média: <100ms

💡 Insights dos Dados
Temperaturas elevadas: Média de 35,1°C indica necessidade de refrigeração

Variação significativa: Amplitude de 30°C requer monitoramento contínuo

Picos temporais: Maiores temperaturas entre 14h-16h

Diferença In/Out: Externo 6,2°C mais quente que interno

Dispositivos críticos: 5% dos sensores operam acima de 45°C

🎯 Funcionalidades Implementadas
✅ Pipeline de ingestão - Leitura e processamento de CSV
✅ Banco de dados - PostgreSQL com índices otimizados
✅ Views SQL - 4 views para análises específicas
✅ Dashboard - 4 gráficos interativos
✅ Alertas - Detecção automática de anomalias
✅ Logs - Monitoramento do pipeline
✅ Containerização - Docker para reprodutibilidade

📝 Licença
Este projeto é de uso acadêmico para a disciplina Disruptive Architectures IOT, Big Data e IA.

👨‍💻 Autor
Evanildo de Sousa Leal

GitHub: evanildo@wfxky.onmicrosoft.com

Disciplina: Disruptive Architectures

Instituição: UNIFECAF

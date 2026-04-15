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

```text
Pipeline de Dados IoT/
│
├── src/                  # Código fonte principal
├── dashboards/           # Aplicação Streamlit
├── sql/                  # Scripts SQL
├── data/                 # Dados fonte
├── docs/                 # Documentação
│   └── images/           # Imagens do dashboard
├── scripts/              # Scripts auxiliares
├── logs/                 # Logs do sistema
├── tests/                # Testes unitários
└── README.md             # Este arquivo

🚀 Instalação e Execução
1. Clone o repositório e Prepare o ambiente
git clone [https://github.com/EvanildoLeal/pipeline-iot.git](https://github.com/EvanildoLeal/pipeline-iot.git)
cd pipeline-iot
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt

2. Configure o Banco de Dados (Docker)
docker-compose up -d

📊 Dashboard - Capturas de Tela
Aqui estão as visualizações do dashboard interativo desenvolvido com Streamlit.

1. Visão Geral do Dashboard
<p align="center">
<img src="docs/images/imagens/dashboard_full.png" alt="Dashboard Completo" width="900">
</p>

2. Análise de Dispositivos Críticos
<p align="center">
<img src="docs/images/imagens/grafico_barras.png" alt="Gráfico de Barras" width="700">
</p>

3. Evolução Temporal das Temperaturas
<p align="center">
<img src="docs/images/imagens/grafico_evolucao.jpg" alt="Gráfico de Evolução" width="700">
</p>

4. Padrão de Temperatura por Hora
<p align="center">
<img src="docs/images/imagens/grafico_hora.png" alt="Gráfico por Hora" width="700">
</p>

🗄️ Views SQL Implementadas

-- Identificar dispositivos com maior temperatura média
CREATE VIEW avg_temp_por_dispositivo AS
SELECT 
    device_id,
    COUNT(*) as total_leituras,
    ROUND(AVG(temperature)::numeric, 2) as avg_temp
FROM temperature_readings
GROUP BY device_id
ORDER BY avg_temp DESC
LIMIT 20;

-- Analisar padrões temporais de temperatura
CREATE VIEW leituras_por_hora AS
SELECT 
    EXTRACT(HOUR FROM timestamp) as hora,
    COUNT(*) as contagem,
    ROUND(AVG(temperature)::numeric, 2) as temp_media
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM timestamp)
ORDER BY hora;

📊 Resultados e Métricas

Métrica,Valor
Total de registros,97.606
Temperatura média,"35,05°C"
Tempo de processamento,~30 segundos
Tamanho do banco,~15 MB

💡 Insights dos Dados
Temperaturas elevadas: Média de 35,1°C indica necessidade de refrigeração.

Picos temporais: Maiores temperaturas entre 14h-16h.

Diferença In/Out: Ambiente externo 6,2°C mais quente que interno.

🎯 Funcionalidades Implementadas
[x] Pipeline de ingestão - Processamento de CSV

[x] Banco de dados - PostgreSQL via Docker

[x] Views SQL - Análises automatizadas

[x] Dashboard - Gráficos interativos Plotly

📝 Licença
Este projeto é de uso acadêmico para a disciplina Disruptive Architectures IOT, Big Data e IA.

👨‍💻 Autor
Evanildo de Sousa Leal GitHub: evanildo@wfxky.onmicrosoft.com

Disciplina: Disruptive Architectures

Instituição: UNIFECAF

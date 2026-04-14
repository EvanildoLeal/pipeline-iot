import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Dashboard IoT - Monitoramento de Temperatura",
    page_icon="🌡️",
    layout="wide"
)

# Conexão com o banco
@st.cache_resource
def init_connection():
    connection_string = f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'sua_senha')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'postgres')}"
    return create_engine(connection_string)

engine = init_connection()

# Função para carregar dados
@st.cache_data(ttl=60)
def load_data(query):
    return pd.read_sql(query, engine)

# Título
st.title("🌡️ Dashboard IoT - Monitoramento de Temperatura")
st.markdown("---")

# Sidebar
st.sidebar.header("📊 Filtros")
st.sidebar.markdown(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

# Carregar dados de métricas
df_temp_stats = load_data("SELECT COUNT(*) as total, AVG(temperature) as media, MIN(temperature) as min, MAX(temperature) as max FROM temperature_readings")
df_local_stats = load_data("SELECT in_out, COUNT(*) as total FROM temperature_readings GROUP BY in_out")

with col1:
    st.metric("Total de Leituras", f"{df_temp_stats['total'].iloc[0]:,}")
with col2:
    st.metric("Temperatura Média", f"{df_temp_stats['media'].iloc[0]:.1f}°C")
with col3:
    st.metric("Temperatura Mínima", f"{df_temp_stats['min'].iloc[0]:.1f}°C")
with col4:
    st.metric("Temperatura Máxima", f"{df_temp_stats['max'].iloc[0]:.1f}°C")

st.markdown("---")

# Gráfico 1: Temperatura por Localização
st.header("📍 Temperatura por Localização (In/Out)")
df_local_temp = load_data("SELECT * FROM temp_por_localizacao")
if not df_local_temp.empty:
    fig1 = px.bar(df_local_temp, x='localizacao', y='temp_media', 
                  color='localizacao',
                  text='temp_media',
                  title="Média de Temperatura por Localização",
                  labels={'localizacao': 'Localização', 'temp_media': 'Temperatura Média (°C)'})
    fig1.update_traces(texttemplate='%{text:.1f}°C', textposition='outside')
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Leituras por Hora
st.header("⏰ Distribuição de Leituras por Hora")
df_hora = load_data("SELECT * FROM leituras_por_hora")
if not df_hora.empty:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_hora['hora'], y=df_hora['contagem'],
                              mode='lines+markers', name='Leituras',
                              line=dict(color='blue', width=2)))
    fig2.add_trace(go.Scatter(x=df_hora['hora'], y=df_hora['temp_media'],
                              mode='lines+markers', name='Temperatura Média',
                              line=dict(color='red', width=2),
                              yaxis='y2'))
    fig2.update_layout(title="Leituras e Temperatura por Hora",
                       xaxis_title="Hora do Dia",
                       yaxis_title="Número de Leituras",
                       yaxis2=dict(title="Temperatura Média (°C)", overlaying='y', side='right'))
    st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Temperaturas por Dia
st.header("📈 Evolução das Temperaturas por Dia")
df_dia = load_data("SELECT * FROM temp_max_min_por_dia")
if not df_dia.empty:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_dia['data'], y=df_dia['temp_max'],
                              mode='lines+markers', name='Máxima',
                              line=dict(color='red', width=2)))
    fig3.add_trace(go.Scatter(x=df_dia['data'], y=df_dia['temp_min'],
                              mode='lines+markers', name='Mínima',
                              line=dict(color='blue', width=2)))
    fig3.add_trace(go.Scatter(x=df_dia['data'], y=df_dia['temp_media'],
                              mode='lines', name='Média',
                              line=dict(color='green', width=2, dash='dash')))
    fig3.update_layout(title="Temperaturas Máximas, Mínimas e Médias por Dia",
                       xaxis_title="Data",
                       yaxis_title="Temperatura (°C)")
    st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: Top Dispositivos
st.header("🏆 Top 20 Dispositivos com Maior Temperatura Média")
df_top = load_data("SELECT * FROM avg_temp_por_dispositivo")
if not df_top.empty:
    fig4 = px.bar(df_top.head(20), x='device_id', y='avg_temp',
                  color='avg_temp',
                  title="Top 20 Dispositivos - Média de Temperatura",
                  labels={'device_id': 'Dispositivo', 'avg_temp': 'Temperatura Média (°C)'})
    fig4.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)

# Tabela de alertas
st.header("⚠️ Alertas de Temperatura")
df_alertas = load_data("""
    SELECT device_id, temperature, in_out, timestamp 
    FROM temperature_readings 
    WHERE temperature > 40 OR temperature < 25
    ORDER BY timestamp DESC 
    LIMIT 100
""")
if not df_alertas.empty:
    st.dataframe(df_alertas, use_container_width=True)
    st.warning(f"⚠️ {len(df_alertas)} alertas encontrados (temperatura > 40°C ou < 25°C)")
else:
    st.success("✅ Nenhum alerta no momento")

st.markdown("---")
st.markdown("📊 **Pipeline de Dados IoT** - Desenvolvido para Disruptive Architectures UniFECAF - Evanildo Leal")

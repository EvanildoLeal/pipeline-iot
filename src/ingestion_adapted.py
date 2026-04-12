"""
Pipeline de ingestão de dados IoT - Adaptado para o CSV específico
"""
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import os
import uuid
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'postgres'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'sua_senha')
}

def criar_conexao():
    """Cria conexão com o banco"""
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(connection_string)

def criar_tabela(engine):
    """Cria a tabela adaptada para os dados do CSV"""
    create_table_sql = text("""
    CREATE TABLE IF NOT EXISTS temperature_readings (
        id SERIAL PRIMARY KEY,
        device_id VARCHAR(200),
        room_location VARCHAR(200),
        timestamp TIMESTAMP,
        temperature FLOAT,
        in_out VARCHAR(10),
        ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        batch_id VARCHAR(100)
    );
    
    CREATE INDEX IF NOT EXISTS idx_device_timestamp 
    ON temperature_readings(device_id, timestamp);
    
    CREATE INDEX IF NOT EXISTS idx_timestamp 
    ON temperature_readings(timestamp);
    """)
    
    with engine.connect() as conn:
        conn.execute(create_table_sql)
        conn.commit()
        print("✅ Tabela criada/verificada com sucesso!")

def ler_e_processar_csv(csv_path, engine):
    """Lê o CSV e processa os dados"""
    print(f"\n📖 Lendo arquivo CSV: {csv_path}")
    
    # Ler CSV
    df = pd.read_csv(csv_path)
    print(f"📊 Total de linhas no CSV: {len(df)}")
    print(f"📋 Colunas encontradas: {df.columns.tolist()}")
    
    # Mostrar primeiras linhas
    print("\n📝 Primeiras 5 linhas do CSV:")
    print(df.head())
    
    # Renomear colunas para o padrão do banco
    df = df.rename(columns={
        'id': 'device_id',
        'room_id/id': 'room_location',
        'noted_date': 'timestamp',
        'temp': 'temperature',
        'out/in': 'in_out'
    })
    
    # Converter timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M')
    
    # Adicionar colunas de metadados
    df['ingestion_time'] = datetime.now()
    df['batch_id'] = str(uuid.uuid4())
    
    # Selecionar apenas as colunas necessárias
    df = df[['device_id', 'room_location', 'timestamp', 'temperature', 'in_out', 'ingestion_time', 'batch_id']]
    
    # Remover possíveis duplicatas
    df = df.drop_duplicates(subset=['device_id', 'timestamp'])
    
    print(f"\n📈 Estatísticas dos dados:")
    print(f"   - Dispositivos únicos: {df['device_id'].nunique()}")
    print(f"   - Período: {df['timestamp'].min()} até {df['timestamp'].max()}")
    print(f"   - Temperatura média: {df['temperature'].mean():.2f}°C")
    print(f"   - Temperatura min: {df['temperature'].min():.2f}°C")
    print(f"   - Temperatura max: {df['temperature'].max():.2f}°C")
    
    # Inserir no banco em batches para melhor performance
    print(f"\n💾 Inserindo {len(df)} registros no banco...")
    batch_size = 10000
    total_inserido = 0
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        batch.to_sql('temperature_readings', engine, if_exists='append', index=False)
        total_inserido += len(batch)
        print(f"   Batch {i//batch_size + 1}: {len(batch)} registros inseridos")
    
    print(f"\n✅ Total de registros inseridos: {total_inserido}")
    return total_inserido

def main():
    print("=" * 60)
    print("🚀 Pipeline de Ingestão de Dados IoT - Temperaturas")
    print("=" * 60)
    
    # Caminho do CSV
    csv_path = "data/IOT-temp.csv"
    
    # Verificar se o CSV existe
    if not os.path.exists(csv_path):
        print(f"❌ Arquivo {csv_path} não encontrado!")
        return
    
    # Conectar ao banco
    engine = criar_conexao()
    
    # Criar tabela
    criar_tabela(engine)
    
    # Processar CSV
    total_registros = ler_e_processar_csv(csv_path, engine)
    
    print("\n" + "=" * 60)
    print("🎉 Pipeline concluído com sucesso!")
    print(f"📊 Total de registros inseridos: {total_registros}")
    print("=" * 60)
    
    # Verificar registros inseridos
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM temperature_readings"))
        count = result.fetchone()[0]
        print(f"📈 Total de registros no banco: {count}")

if __name__ == "__main__":
    main()

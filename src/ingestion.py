"""
Pipeline de ingestão de dados IoT
Responsável por ler CSV e inserir no PostgreSQL
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
    """Cria a tabela se não existir"""
    create_table_sql = text("""
    CREATE TABLE IF NOT EXISTS temperature_readings (
        id SERIAL PRIMARY KEY,
        device_id VARCHAR(100) NOT NULL,
        temperature FLOAT NOT NULL,
        humidity FLOAT,
        timestamp TIMESTAMP NOT NULL,
        location VARCHAR(200),
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
        print("Tabela criada/verificada com sucesso!")

def ler_e_processar_csv(csv_path, engine):
    """Lê o CSV e processa os dados"""
    print(f"\nLendo arquivo CSV: {csv_path}")
    
    # Verificar se arquivo existe
    if not os.path.exists(csv_path):
        print(f"Arquivo não encontrado: {csv_path}")
        return 0
    
    # Ler CSV
    df = pd.read_csv(csv_path)
    print(f"Total de linhas no CSV: {len(df)}")
    print(f"Colunas encontradas: {df.columns.tolist()}")
    
    # Mostrar primeiras linhas
    print("\nPrimeiras 5 linhas do CSV:")
    print(df.head())
    
    # Verificar colunas necessárias e ajustar
    # Se o CSV tiver colunas diferentes, faça o mapeamento aqui
    required_cols = ['device_id', 'temperature', 'timestamp']
    
    # Verificar se as colunas existem
    for col in required_cols:
        if col not in df.columns:
            print(f"Coluna '{col}' não encontrada. Colunas disponíveis: {df.columns.tolist()}")
            # Se não encontrar, tentar encontrar colunas similares
            if 'temp' in df.columns and col == 'temperature':
                df = df.rename(columns={'temp': 'temperature'})
            elif 'device' in df.columns and col == 'device_id':
                df = df.rename(columns={'device': 'device_id'})
            elif 'date' in df.columns and col == 'timestamp':
                df = df.rename(columns={'date': 'timestamp'})
            elif 'time' in df.columns and col == 'timestamp':
                df = df.rename(columns={'time': 'timestamp'})
    
    # Adicionar colunas de metadados se não existirem
    if 'humidity' not in df.columns:
        df['humidity'] = None
    
    if 'location' not in df.columns:
        df['location'] = 'Nao especificado'
    
    df['ingestion_time'] = datetime.now()
    df['batch_id'] = str(uuid.uuid4())
    
    # Converter timestamp
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Inserir no banco
    print(f"\nInserindo {len(df)} registros no banco...")
    df.to_sql('temperature_readings', engine, if_exists='append', index=False)
    
    print(f"Dados inseridos com sucesso!")
    return len(df)

def main():
    print("=" * 50)
    print("Pipeline de Ingestão de Dados IoT")
    print("=" * 50)
    
    # Caminho do CSV
    csv_path = "data/IOT-temp.csv"
    
    # Criar pasta data se não existir
    os.makedirs("data", exist_ok=True)
    
    # Verificar se o CSV existe
    if not os.path.exists(csv_path):
        print(f"AVISO: Arquivo {csv_path} não encontrado!")
        print(f"Por favor, coloque seu arquivo CSV na pasta 'data/'")
        print(f"Ou use o caminho correto para seu arquivo.")
        
        # Listar arquivos na pasta data
        print(f"\nArquivos na pasta data:")
        for file in os.listdir("data"):
            print(f"  - {file}")
        return
    
    # Conectar ao banco
    engine = criar_conexao()
    
    # Criar tabela
    criar_tabela(engine)
    
    # Processar CSV
    total_registros = ler_e_processar_csv(csv_path, engine)
    
    print("\n" + "=" * 50)
    print(f"Pipeline concluído!")
    print(f"Total de registros inseridos: {total_registros}")
    print("=" * 50)
    
    # Verificar registros inseridos
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM temperature_readings"))
        count = result.fetchone()[0]
        print(f"Total de registros no banco: {count}")

if __name__ == "__main__":
    main()

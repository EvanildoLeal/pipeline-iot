"""
Teste de conexão com o PostgreSQL
"""
from sqlalchemy import create_engine, text
import os
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

print("=" * 50)
print("Teste de conexão com PostgreSQL")
print("=" * 50)
print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
print(f"Database: {DB_CONFIG['database']}")
print(f"User: {DB_CONFIG['user']}")

try:
    # Criar conexão
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    engine = create_engine(connection_string)
    
    # Testar conexão
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"\nConexao bem sucedida!")
        print(f"PostgreSQL Version: {version[:50]}...")
        
        # Listar tabelas
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = result.fetchall()
        
        if tables:
            print(f"\nTabelas existentes:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print(f"\nNenhuma tabela encontrada ainda.")
            
    print("\nTeste concluido com sucesso!")
    
except Exception as e:
    print(f"\nErro na conexao: {e}")
    print("\nVerifique se o container Docker esta rodando:")
    print("   docker ps")
    print("   docker start postgres-iot")
    
finally:
    if 'engine' in locals():
        engine.dispose()

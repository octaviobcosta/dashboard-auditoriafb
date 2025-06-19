import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

print("=== Teste de Conexão ===\n")

# Verificar variáveis de ambiente
print("1. Verificando variáveis de ambiente:")
env_vars = ['SUPABASE_URL', 'SUPABASE_KEY', 'PGURL', 'FLASK_SECRET_KEY']
for var in env_vars:
    value = os.getenv(var)
    if value:
        print(f"✓ {var}: {value[:20]}...")
    else:
        print(f"✗ {var}: NÃO ENCONTRADA")

print("\n2. Testando conexão com Supabase:")
try:
    from supabase import create_client, Client
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    if url and key:
        supabase: Client = create_client(url, key)
        print("✓ Cliente Supabase criado com sucesso!")
        
        # Tentar uma query simples
        try:
            response = supabase.table('categorias').select('*').limit(1).execute()
            print("✓ Conexão com banco de dados OK!")
            print(f"  Categorias encontradas: {len(response.data)}")
        except Exception as e:
            print(f"✗ Erro ao consultar banco: {str(e)}")
    else:
        print("✗ URL ou KEY do Supabase não encontradas")
        
except Exception as e:
    print(f"✗ Erro ao criar cliente Supabase: {str(e)}")
    print("\n3. Tentando conexão direta com PostgreSQL:")
    
    try:
        import psycopg2
        
        pgurl = os.getenv('PGURL')
        if pgurl:
            conn = psycopg2.connect(pgurl)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM categorias")
            count = cursor.fetchone()[0]
            print(f"✓ Conexão PostgreSQL OK! Categorias: {count}")
            cursor.close()
            conn.close()
        else:
            print("✗ PGURL não encontrada")
    except Exception as pg_error:
        print(f"✗ Erro PostgreSQL: {str(pg_error)}")

print("\n4. Verificando imports da aplicação:")
try:
    import flask
    print("✓ Flask importado com sucesso")
except:
    print("✗ Erro ao importar Flask")

try:
    import pandas
    print("✓ Pandas importado com sucesso")
except:
    print("✗ Erro ao importar Pandas")

print("\n=== Fim do teste ===")
print("\nPara corrigir erros:")
print("1. Verifique se o .env está no diretório correto")
print("2. Reinstale as dependências: pip install -r requirements.txt --upgrade")
print("3. Se o erro persistir com Supabase, usaremos conexão direta PostgreSQL")
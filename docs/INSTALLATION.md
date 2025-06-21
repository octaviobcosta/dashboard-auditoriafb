# Guia de Instalação e Configuração 🚀

## Índice
- [Requisitos](#requisitos)
- [Instalação Local](#instalação-local)
- [Configuração do Supabase](#configuração-do-supabase)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Primeiro Acesso](#primeiro-acesso)
- [Instalação com Docker](#instalação-com-docker)
- [Troubleshooting](#troubleshooting)

## Requisitos

### Sistema Operacional
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian 10+, CentOS 8+)

### Software Necessário
- **Python 3.12** ou superior
- **Git** 2.25+
- **pip** (gerenciador de pacotes Python)
- **Conta no Supabase** (gratuita)

### Requisitos de Hardware
- **Mínimo**: 2GB RAM, 1GB espaço em disco
- **Recomendado**: 4GB RAM, 2GB espaço em disco

## Instalação Local

### 1. Clonar o Repositório

```bash
# Via HTTPS
git clone https://github.com/seu-usuario/dashboard-auditoriafb.git

# Via SSH (recomendado)
git clone git@github.com:seu-usuario/dashboard-auditoriafb.git

# Entrar no diretório
cd dashboard-auditoriafb
```

### 2. Configurar Ambiente Virtual

#### Windows
```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Verificar se está ativo (deve mostrar (venv) no prompt)
```

#### Linux/macOS
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se está ativo (deve mostrar (venv) no prompt)
```

### 3. Instalar Dependências

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências do projeto
pip install -r requirements.txt

# Verificar instalação
pip list
```

### 4. Estrutura de Diretórios

Criar diretórios necessários:

```bash
# Windows
mkdir uploads logs database

# Linux/macOS
mkdir -p uploads logs database
```

## Configuração do Supabase

### 1. Criar Projeto no Supabase

1. Acesse [https://supabase.com](https://supabase.com)
2. Faça login ou crie uma conta
3. Clique em "New Project"
4. Configure:
   - **Project name**: dashboard-auditoriafb
   - **Database Password**: (anote em local seguro)
   - **Region**: Escolha a mais próxima
   - **Pricing Plan**: Free tier

### 2. Configurar Banco de Dados

#### Opção A: Via Interface Web

1. No painel do Supabase, vá em "SQL Editor"
2. Cole e execute cada script em ordem:

```sql
-- 1. Criar schema (se necessário)
CREATE SCHEMA IF NOT EXISTS public;

-- 2. Executar scripts da pasta database/
-- Copie o conteúdo de database/01_tables.sql
-- Copie o conteúdo de database/02_indexes.sql
-- Copie o conteúdo de database/03_functions.sql
```

#### Opção B: Via Script Automatizado

```bash
# Configurar variáveis
export SUPABASE_DB_URL="postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres"

# Executar scripts
psql $SUPABASE_DB_URL -f database/01_tables.sql
psql $SUPABASE_DB_URL -f database/02_indexes.sql
psql $SUPABASE_DB_URL -f database/03_functions.sql
```

### 3. Obter Credenciais

No painel do Supabase:

1. Vá em "Settings" → "API"
2. Copie:
   - **Project URL**: `https://[SEU-PROJETO].supabase.co`
   - **Anon Key**: `eyJ...` (chave pública)
   - **Service Role Key**: `eyJ...` (chave privada - MANTER SEGURA!)

## Variáveis de Ambiente

### 1. Criar Arquivo .env

```bash
# Copiar template
cp .env.example .env

# Editar arquivo (use seu editor preferido)
nano .env  # ou vim, code, notepad, etc.
```

### 2. Configurar Variáveis

```env
# Flask Configuration
FLASK_APP=src/app.py
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=True

# Supabase Configuration
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-anon-key-aqui
SUPABASE_SERVICE_KEY=sua-service-key-aqui  # Opcional, para operações admin

# Application Settings
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB em bytes
ALLOWED_EXTENSIONS=xlsx,xls,csv,json

# Database Settings
DATABASE_POOL_SIZE=10
DATABASE_POOL_TIMEOUT=30

# Security
SESSION_COOKIE_SECURE=False  # True em produção com HTTPS
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=3600  # 1 hora em segundos

# Admin User (primeiro acesso)
ADMIN_EMAIL=octavio@eshows.com.br
ADMIN_PASSWORD_HASH=$2b$12$...  # Gerado pelo script setup_admin.py

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_MAX_SIZE=10485760  # 10MB
LOG_BACKUP_COUNT=5

# Email (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-de-app
```

### 3. Gerar Secret Key

```python
# Python shell
import secrets
print(secrets.token_hex(32))
# Copie o resultado para SECRET_KEY no .env
```

### 4. Gerar Hash de Senha Admin

```bash
# Executar script auxiliar
python scripts/generate_password_hash.py
# Digite a senha desejada
# Copie o hash para ADMIN_PASSWORD_HASH no .env
```

## Primeiro Acesso

### 1. Inicializar Banco de Dados

```bash
# Criar usuário admin padrão
python scripts/init_db.py

# Saída esperada:
# ✅ Banco de dados inicializado
# ✅ Usuário admin criado: octavio@eshows.com.br
```

### 2. Executar Aplicação

```bash
# Modo desenvolvimento
python run.py

# Ou usando Flask CLI
flask run --host=0.0.0.0 --port=5000

# Saída esperada:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

### 3. Acessar Dashboard

1. Abra o navegador em `http://localhost:5000`
2. Faça login com:
   - Email: `octavio@eshows.com.br`
   - Senha: (a que você definiu)

### 4. Configurações Iniciais

Após o login:

1. **Alterar senha** (recomendado)
2. **Criar usuários adicionais**
3. **Configurar categorias de indicadores**
4. **Importar dados iniciais**

## Instalação com Docker

### 1. Dockerfile

```dockerfile
FROM python:3.12-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Copiar arquivos de requisitos
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p uploads logs

# Expor porta
EXPOSE 5000

# Comando de inicialização
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.app:app"]
```

### 2. docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    env_file:
      - .env
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Opcional: Nginx como proxy reverso
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped
```

### 3. Executar com Docker

```bash
# Construir imagem
docker-compose build

# Iniciar serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

## Configuração para Produção

### 1. Nginx Configuration

```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seu-dominio.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location / {
        proxy_pass http://web:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 2. Gunicorn Configuration

```python
# gunicorn_config.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
threads = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
```

### 3. Systemd Service

```ini
# /etc/systemd/system/dashboard-auditoriafb.service
[Unit]
Description=Dashboard Auditoria FB
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/dashboard-auditoriafb
Environment="PATH=/opt/dashboard-auditoriafb/venv/bin"
ExecStart=/opt/dashboard-auditoriafb/venv/bin/gunicorn \
    --config gunicorn_config.py \
    src.app:app

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Problema: ModuleNotFoundError

```bash
# Solução 1: Verificar ambiente virtual
which python  # Deve mostrar caminho do venv

# Solução 2: Reinstalar dependências
pip install --force-reinstall -r requirements.txt

# Solução 3: Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### Problema: Conexão com Supabase falha

```python
# Testar conexão
python scripts/test_connection.py

# Verificar:
# 1. URL está correta (https://...)
# 2. Chave API está completa
# 3. Firewall não está bloqueando
# 4. Projeto Supabase está ativo
```

### Problema: ImportError no Windows

```powershell
# Instalar Visual C++ Build Tools
# Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Ou usar wheels pré-compilados
pip install --only-binary :all: pandas numpy
```

### Problema: Permissão negada em uploads

```bash
# Linux/macOS
chmod 755 uploads
chown -R $USER:$USER uploads

# Verificar permissões
ls -la uploads/
```

### Problema: Memória insuficiente

```bash
# Aumentar swap (Linux)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Configurar limites Python
export PYTHONOPTIMIZE=1
```

## Verificação Final

### Health Check Script

```python
# scripts/health_check.py
import requests
import sys

def check_health():
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Aplicação está rodando")
            return True
    except:
        pass
    
    print("❌ Aplicação não está respondendo")
    return False

if __name__ == "__main__":
    sys.exit(0 if check_health() else 1)
```

### Checklist de Verificação

- [ ] Python 3.12+ instalado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas sem erros
- [ ] Arquivo .env configurado
- [ ] Supabase configurado e acessível
- [ ] Diretórios criados com permissões corretas
- [ ] Aplicação inicia sem erros
- [ ] Login funciona corretamente
- [ ] Upload de arquivos funciona
- [ ] Gráficos são exibidos

## Próximos Passos

1. Leia o [Manual do Usuário](USER_GUIDE.md)
2. Configure [backups automáticos](BACKUP.md)
3. Implemente [monitoramento](MONITORING.md)
4. Configure [CI/CD](CI_CD.md)

---

Em caso de dúvidas, consulte a [FAQ](FAQ.md) ou abra uma [issue](https://github.com/seu-usuario/dashboard-auditoriafb/issues).
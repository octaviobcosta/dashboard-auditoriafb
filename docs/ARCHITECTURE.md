# Arquitetura do Sistema 🏗️

## Índice
- [Visão Geral](#visão-geral)
- [Arquitetura de Software](#arquitetura-de-software)
- [Componentes Principais](#componentes-principais)
- [Fluxo de Dados](#fluxo-de-dados)
- [Padrões de Design](#padrões-de-design)
- [Segurança](#segurança)
- [Performance](#performance)
- [Escalabilidade](#escalabilidade)

## Visão Geral

O Dashboard Auditoria FB segue uma arquitetura MVC (Model-View-Controller) modificada, com camadas bem definidas para separação de responsabilidades. A aplicação é construída sobre Flask e utiliza Supabase como backend-as-a-service.

### Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   HTML5     │  │  JavaScript │  │   Chart.js  │         │
│  │ Templates   │  │    (ES6)    │  │  Bootstrap  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/HTTPS
┌─────────────────────────┴───────────────────────────────────┐
│                    Flask Application                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Routes    │  │   Models    │  │    Utils    │         │
│  │   (app.py)  │  │ (database.py)│  │  (helpers)  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                              │
│  ┌─────────────────────────────────────────────────┐        │
│  │              Data Processing Module              │        │
│  │  ┌─────────┐ ┌───────────┐ ┌─────────────┐     │        │
│  │  │ Mappers │ │Validators │ │ Converters  │     │        │
│  │  └─────────┘ └───────────┘ └─────────────┘     │        │
│  └─────────────────────────────────────────────────┘        │
└─────────────────────────┬───────────────────────────────────┘
                          │ Supabase Client
┌─────────────────────────┴───────────────────────────────────┐
│                      Supabase (BaaS)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ PostgreSQL  │  │   Auth      │  │   Storage   │         │
│  │  Database   │  │   Service   │  │   Service   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Arquitetura de Software

### Stack Tecnológico

#### Backend
- **Flask 3.0**: Framework web principal
- **Python 3.12**: Linguagem de programação
- **Pandas**: Processamento e análise de dados
- **Flask-Login**: Gerenciamento de sessões
- **Flask-CORS**: Suporte para CORS

#### Frontend
- **Jinja2**: Template engine
- **Bootstrap 5**: Framework CSS responsivo
- **Chart.js**: Biblioteca de gráficos
- **Vanilla JavaScript**: Interatividade client-side

#### Banco de Dados
- **Supabase/PostgreSQL**: Banco relacional
- **Row Level Security (RLS)**: Segurança em nível de linha

### Estrutura de Diretórios

```
src/
├── app.py              # Ponto de entrada da aplicação
├── config/             # Configurações e constantes
│   └── settings.py     # Variáveis de ambiente e config
├── models/             # Camada de dados
│   └── database.py     # Conexão e queries Supabase
├── data/               # Módulo de processamento
│   ├── mappers/        # Mapeamento de dados
│   ├── validators/     # Validação de entrada
│   ├── converters/     # Conversão de tipos
│   ├── processors/     # Pipeline de processamento
│   └── utils/          # Importação/Exportação
└── utils/              # Funções auxiliares
```

## Componentes Principais

### 1. Camada de Apresentação (View)

**Templates Jinja2**
- `base.html`: Template base com estrutura comum
- `dashboard.html`: Dashboard principal
- `indicators.html`: Página de indicadores
- `login.html`: Autenticação

**Assets Estáticos**
- `/static/css/`: Estilos customizados
- `/static/js/`: Scripts client-side
- `/static/images/`: Recursos visuais

### 2. Camada de Controle (Controller)

**Rotas Principais**
```python
/                    # Redirect para dashboard ou login
/login               # Autenticação
/dashboard           # Dashboard principal
/indicators          # Indicadores detalhados
/api/*               # Endpoints da API REST
```

**Middleware**
- Autenticação via `@login_required`
- Validação de permissões por perfil
- Tratamento de erros global

### 3. Camada de Modelo (Model)

**Database.py**
- Classe singleton para conexão Supabase
- Métodos para operações CRUD
- Queries otimizadas com índices

**Esquema de Dados**
```sql
-- Principais tabelas
usuarios            # Gestão de usuários
categorias          # Categorias de indicadores
indicadores         # Definições de KPIs
dados_indicadores   # Valores históricos
produtos_vendidos   # Dados de vendas
estornos_cancelamento # Estornos e cancelamentos
logs_auditoria      # Rastreamento de ações
```

### 4. Módulo de Processamento de Dados

**Pipeline de Processamento**
1. **Importação**: Leitura de Excel/CSV/JSON
2. **Limpeza**: Remoção de dados inválidos
3. **Mapeamento**: Conversão de colunas
4. **Validação**: Regras de negócio
5. **Conversão**: Tipos de dados
6. **Exportação**: Gravação no banco

**Componentes**
- `ColumnMapper`: Mapeamento flexível de colunas
- `DataValidator`: Validações customizáveis
- `TypeConverter`: Conversão inteligente de tipos
- `DataProcessor`: Orquestração do pipeline

## Fluxo de Dados

### 1. Fluxo de Autenticação
```
Cliente → Login Form → Flask-Login → Supabase Auth → Session → Dashboard
```

### 2. Fluxo de Importação
```
Upload File → DataImporter → Validation → Mapping → Processing → Supabase → Success/Error
```

### 3. Fluxo de Visualização
```
Dashboard → API Request → Database Query → Data Processing → JSON Response → Chart.js → Display
```

## Padrões de Design

### 1. Singleton Pattern
- Conexão única com Supabase
- Gerenciamento centralizado de configurações

### 2. Factory Pattern
- Criação de validadores e conversores
- Instanciação de processadores

### 3. Pipeline Pattern
- Processamento sequencial de dados
- Etapas configuráveis e reutilizáveis

### 4. Repository Pattern
- Abstração da camada de dados
- Queries centralizadas no database.py

## Segurança

### Autenticação e Autorização
- **Senhas**: Hash bcrypt com salt
- **Sessões**: Flask-Login com timeout
- **Permissões**: RBAC (Role-Based Access Control)
  - Admin: Acesso total
  - Gestor: Importação e visualização
  - Usuário: Apenas visualização

### Proteções Implementadas
- CSRF Protection
- SQL Injection: Queries parametrizadas
- XSS: Escape automático no Jinja2
- Upload seguro: Validação de tipos e tamanho
- Rate limiting: Proteção contra brute force

### Boas Práticas
- Variáveis sensíveis em .env
- HTTPS em produção
- Logs de auditoria completos
- Backup automático do banco

## Performance

### Otimizações Implementadas

1. **Banco de Dados**
   - Índices em colunas frequentes
   - Queries paginadas
   - Cache de queries repetitivas

2. **Frontend**
   - Minificação de assets
   - Lazy loading de gráficos
   - CDN para bibliotecas

3. **Backend**
   - Processamento assíncrono para imports
   - Pool de conexões
   - Compressão gzip

### Métricas de Performance
- Tempo de resposta médio: < 200ms
- Upload de arquivos: até 16MB
- Processamento: ~1000 registros/segundo

## Escalabilidade

### Horizontal
- Aplicação stateless
- Suporte a múltiplas instâncias
- Load balancer ready

### Vertical
- Otimização de queries
- Processamento em batches
- Uso eficiente de memória

### Limites Atuais
- Conexões simultâneas: 100
- Tamanho máximo de upload: 16MB
- Registros por importação: 100.000

## Monitoramento

### Logs
- Aplicação: Flask logger
- Auditoria: Tabela logs_auditoria
- Erros: Sentry (opcional)

### Métricas
- Uso de CPU/Memória
- Tempo de resposta
- Taxa de erro
- Usuários ativos

## Deployment

### Desenvolvimento
```bash
flask run --debug
```

### Produção
```bash
gunicorn -w 4 -b 0.0.0.0:8000 src.app:app
```

### Docker
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "src.app:app"]
```

## Considerações Futuras

### Melhorias Planejadas
1. WebSockets para atualizações em tempo real
2. Cache Redis para performance
3. Fila de processamento (Celery)
4. API GraphQL
5. Testes automatizados completos

### Possíveis Expansões
1. Multi-tenancy
2. Internacionalização (i18n)
3. Módulo de relatórios PDF
4. Integração com outros sistemas
5. Mobile app
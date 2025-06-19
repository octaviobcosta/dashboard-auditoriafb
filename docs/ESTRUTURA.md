# Estrutura do Projeto Dashboard Auditoria FB

## Organização dos Diretórios

```
dashboard-auditoriafb/
│
├── docs/                       # Documentação completa do projeto
│   ├── database/              # Schemas e migrações do banco de dados
│   │   ├── database_schema.sql
│   │   ├── create_produtos_vendidos_table.sql
│   │   └── migrations/        # Futuras migrações
│   ├── setup/                 # Scripts de instalação e configuração
│   │   ├── install.sh        # Instalação Linux/Mac
│   │   └── install.bat       # Instalação Windows
│   └── ESTRUTURA.md          # Este arquivo
│
├── src/                       # Código fonte principal da aplicação
│   ├── app.py                # Aplicação Flask principal
│   ├── config/               # Configurações
│   │   ├── __init__.py
│   │   └── settings.py       # Variáveis de configuração
│   ├── models/               # Modelos e acesso ao banco de dados
│   │   ├── __init__.py
│   │   ├── database.py       # Cliente Supabase
│   │   └── database_pg.py   # Cliente PostgreSQL direto
│   ├── routes/               # Rotas da aplicação (futuro)
│   ├── services/             # Lógica de negócio (futuro)
│   └── utils/                # Funções utilitárias
│
├── static/                    # Arquivos estáticos
│   ├── images/
│   │   ├── logo/            # Logos da aplicação
│   │   │   ├── logofb.png   # Logo colorido
│   │   │   └── logofb_white.png # Logo branco
│   │   └── icons/           # Ícones diversos
│   ├── css/                 # Estilos customizados
│   └── js/                  # Scripts JavaScript
│
├── templates/                 # Templates HTML
│   ├── base.html            # Template base
│   ├── login.html           # Página de login
│   └── dashboard.html       # Dashboard principal
│
├── tests/                     # Testes da aplicação
│   └── test_connection.py   # Teste de conexão com banco
│
├── data/                      # Dados e arquivos enviados
│   ├── uploads/             # Arquivos enviados pelos usuários
│   └── ProdutosVendidos.csv # Exemplo de dados
│
├── venv/                      # Ambiente virtual Python (ignorado no git)
│
├── .env                       # Variáveis de ambiente (ignorado no git)
├── .env.example              # Exemplo de variáveis de ambiente
├── .gitignore                # Arquivos ignorados pelo git
├── requirements.txt          # Dependências Python
├── README.md                 # Documentação principal
└── run.py                    # Script principal para executar a aplicação
```

## Como Executar

1. **Windows (PowerShell):**
   ```powershell
   python run.py
   ```

2. **Linux/Mac:**
   ```bash
   python3 run.py
   ```

## Principais Componentes

### Backend (src/)
- **app.py**: Aplicação Flask com rotas e configuração
- **models/**: Acesso ao banco de dados (Supabase/PostgreSQL)
- **config/**: Configurações centralizadas

### Frontend (templates/ e static/)
- **Templates**: HTML com Jinja2
- **Estilos**: CSS customizado + Bootstrap
- **Scripts**: JavaScript para interatividade

### Banco de Dados (docs/database/)
- Schema completo das tabelas
- Scripts de migração
- Documentação do modelo de dados

## Padrões de Desenvolvimento

1. **Python**: PEP 8
2. **JavaScript**: ES6+
3. **CSS**: BEM methodology
4. **Git**: Conventional Commits

## Segurança

- Senhas com hash bcrypt
- Variáveis sensíveis em .env
- CSRF protection
- SQL injection prevention
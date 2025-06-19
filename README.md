# Dashboard Auditoria FB

Sistema de dashboard para indicadores de controladoria, desenvolvido para análise e acompanhamento de métricas empresariais.

## Funcionalidades

- 📊 Dashboard interativo com indicadores principais
- 📈 Visualização de dados de vendas e produtos
- 📤 Importação de arquivos CSV
- 👥 Sistema de usuários com diferentes perfis
- 🔐 Autenticação segura
- 📱 Interface responsiva

## Tecnologias Utilizadas

- **Backend**: Python 3.12, Flask
- **Banco de Dados**: Supabase (PostgreSQL)
- **Frontend**: Bootstrap 5, Chart.js
- **Autenticação**: Flask-Login, JWT

## Estrutura do Projeto

```
dashboard-auditoriafb/
├── app.py              # Aplicação principal Flask
├── config/             # Configurações
│   └── settings.py
├── models/             # Modelos de dados
│   └── database.py
├── routes/             # Rotas da API (futuro)
├── static/             # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
├── templates/          # Templates HTML
│   ├── base.html
│   ├── login.html
│   └── dashboard.html
├── data/               # Dados e uploads
├── requirements.txt    # Dependências Python
└── .env               # Variáveis de ambiente
```

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/octaviobcosta/dashboard-auditoriafb.git
cd dashboard-auditoriafb
```

2. Crie um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
- Copie o arquivo `.env.example` para `.env`
- Atualize as credenciais do Supabase e outras configurações

5. Execute a aplicação:
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## Uso

### Login
- Acesse a aplicação e faça login com as credenciais padrão:
  - Email: `admin@auditoriafb.com.br`
  - Senha: (definida no .env)

### Importação de Dados
- Acesse o menu "Importar Dados" (disponível para admin/gestor)
- Faça upload de arquivos CSV no formato esperado
- O sistema processará e armazenará os dados automaticamente

### Dashboard
- Visualize métricas principais
- Filtre por período
- Analise gráficos de vendas e categorias
- Veja os produtos mais vendidos

## Estrutura do Banco de Dados

### Tabelas Principais:
- `usuarios`: Gerenciamento de usuários
- `categorias`: Categorias de indicadores
- `indicadores`: Definição de indicadores
- `dados_indicadores`: Valores históricos
- `produtos_vendidos`: Dados de vendas importados
- `configuracoes`: Parâmetros do sistema

## Segurança

- Senhas armazenadas com hash bcrypt
- Autenticação por sessão e JWT
- Validação de permissões por perfil
- Logs de auditoria

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto é propriedade da Auditoria FB.

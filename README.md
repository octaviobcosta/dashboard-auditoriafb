# Dashboard Auditoria FB 📊

Sistema de dashboard para análise e visualização de dados de auditoria, desenvolvido para fornecer insights em tempo real sobre operações, vendas e indicadores de desempenho.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Documentação](#documentação)
- [Contribuindo](#contribuindo)

## 🎯 Visão Geral

O Dashboard Auditoria FB é uma aplicação web moderna que permite:
- Visualização de dados em tempo real
- Análise de indicadores de performance
- Importação e processamento de dados de múltiplas fontes
- Geração de relatórios customizados
- Gestão de usuários e permissões

### Screenshots

![Dashboard Principal](docs/images/dashboard-preview.png)
*Interface principal do dashboard com tema Clean/Grafite*

## ✨ Funcionalidades

### Para Usuários
- 📊 **Visualização de Dados**: Gráficos interativos e KPIs em tempo real
- 📈 **Indicadores**: Acompanhamento de métricas de vendas, estornos e cancelamentos
- 📱 **Responsivo**: Interface adaptável para desktop e mobile
- 🎨 **Tema Moderno**: Design clean com tema grafite e amarelo

### Para Administradores
- 📤 **Importação de Dados**: Suporte para Excel, CSV e JSON
- 👥 **Gestão de Usuários**: Controle de acesso e permissões
- 🔧 **Configurações**: Personalização de parâmetros do sistema
- 📝 **Logs de Auditoria**: Rastreamento de todas as ações

## 🛠 Tecnologias

### Backend
- **Python 3.12**: Linguagem principal
- **Flask 3.0**: Framework web
- **Supabase**: Banco de dados PostgreSQL
- **Pandas**: Processamento de dados

### Frontend
- **HTML5/CSS3**: Estrutura e estilo
- **JavaScript**: Interatividade
- **Chart.js**: Visualização de dados
- **Bootstrap 5**: Framework CSS

### Ferramentas
- **MCP (Model Context Protocol)**: Integração com IA
- **Git**: Controle de versão
- **Docker**: Containerização (opcional)

## 🚀 Instalação

### Pré-requisitos
- Python 3.12 ou superior
- Git
- Conta no Supabase
- Node.js (opcional, para desenvolvimento frontend)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/dashboard-auditoriafb.git
cd dashboard-auditoriafb
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Execute a aplicação**
```bash
python run.py
```

A aplicação estará disponível em `http://localhost:5000`

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```env
# Flask
FLASK_APP=src/app.py
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-aqui

# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-aqui

# Configurações da aplicação
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
DEBUG=True
```

### Configuração do Banco de Dados

1. Crie um projeto no Supabase
2. Execute os scripts SQL em `database/schema.sql`
3. Configure as URLs e chaves no arquivo `.env`

## 📖 Uso

### Login
- Acesse `http://localhost:5000`
- Use as credenciais fornecidas pelo administrador
- Email padrão: `octavio@eshows.com.br`

### Navegação Principal
- **Dashboard**: Visão geral dos indicadores
- **Indicadores**: Análise detalhada de métricas
- **Importar Dados**: Upload de arquivos (admin)
- **Configurações**: Ajustes do sistema (admin)

### Importação de Dados
1. Acesse "Importar Dados" no menu
2. Selecione o tipo de arquivo (Excel/CSV)
3. Faça upload do arquivo
4. Confirme o mapeamento de colunas
5. Aguarde o processamento

## 📁 Estrutura do Projeto

```
dashboard-auditoriafb/
├── src/                    # Código fonte principal
│   ├── app.py             # Aplicação Flask
│   ├── config/            # Configurações
│   ├── models/            # Modelos de dados
│   ├── data/              # Módulo de tratamento de dados
│   │   ├── mappers/       # Mapeamento de colunas
│   │   ├── validators/    # Validação de dados
│   │   ├── converters/    # Conversão de tipos
│   │   ├── processors/    # Processamento
│   │   └── utils/         # Utilitários
│   └── utils/             # Funções auxiliares
├── templates/             # Templates HTML
├── static/                # Arquivos estáticos
│   ├── css/              # Estilos
│   ├── js/               # Scripts
│   └── images/           # Imagens
├── database/              # Scripts SQL
├── docs/                  # Documentação
├── tests/                 # Testes
├── requirements.txt       # Dependências Python
├── run.py                # Script de execução
└── README.md             # Este arquivo
```

## 📚 Documentação

### Para Desenvolvedores
- [Arquitetura do Sistema](docs/ARCHITECTURE.md)
- [Módulo de Dados](docs/DATA_MODULE.md)
- [API Reference](docs/API.md)
- [Guia de Contribuição](docs/CONTRIBUTING.md)

### Para Usuários
- [Manual do Usuário](docs/USER_GUIDE.md)
- [FAQ](docs/FAQ.md)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia nosso [Guia de Contribuição](docs/CONTRIBUTING.md) para detalhes sobre nosso código de conduta e processo de submissão de pull requests.

### Como Contribuir
1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Nova funcionalidade'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença proprietária. Todos os direitos reservados.

## 👥 Equipe

- **Octavio Costa** - Desenvolvedor Principal - [@octavio](https://github.com/octavio)

## 📞 Suporte

- Email: octavio@eshows.com.br
- Issues: [GitHub Issues](https://github.com/seu-usuario/dashboard-auditoriafb/issues)

---

Desenvolvido com ❤️ por Octavio Costa
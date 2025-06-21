from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import pandas as pd
import json
import os

from config.settings import Config
from models.database import db
from services.data_service import data_service

# Definir caminhos para templates e static
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(Config)
CORS(app)

# Configuração do LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User:
    def __init__(self, user_data):
        self.id = user_data['id']
        self.email = user_data['email']
        self.nome = user_data['nome']
        self.perfil = user_data['perfil']
        self.is_authenticated = True
        self.is_active = user_data['ativo']
        self.is_anonymous = False
    
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    user_data = db.supabase.table('usuarios').select('*').eq('id', user_id).execute()
    if user_data.data:
        return User(user_data.data[0])
    return None

# ========== Rotas de Autenticação ==========
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        senha = data.get('senha')
        
        user_data = db.get_usuario_by_email(email)
        print(f"DEBUG - User data: {user_data}")  # Debug temporário
        if user_data:
            try:
                # Verifica se o hash existe e não está vazio
                if user_data.get('senha_hash') and check_password_hash(user_data['senha_hash'], senha):
                    user = User(user_data)
                    login_user(user)
                    db.update_ultimo_acesso(user_data['id'])
                    
                    if request.is_json:
                        return jsonify({"success": True, "redirect": url_for('dashboard')})
                    return redirect(url_for('dashboard'))
            except Exception as e:
                print(f"Erro ao verificar senha: {e}")
                print(f"Hash recebido: {user_data.get('senha_hash', 'VAZIO')}")
        
        if request.is_json:
            return jsonify({"success": False, "message": "Email ou senha inválidos"}), 401
        return render_template('login.html', error="Email ou senha inválidos")
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ========== Rotas Principais ==========
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/indicators')
@login_required
def indicators():
    return render_template('indicators.html')

@app.route('/test')
def test():
    return render_template('test.html')

# Rotas administrativas
@app.route('/import-data')
@login_required
def import_data():
    if current_user.perfil not in ['admin', 'gestor']:
        return redirect(url_for('dashboard'))
    return render_template('import_data.html')

@app.route('/users')
@login_required
def users():
    if current_user.perfil != 'admin':
        return redirect(url_for('dashboard'))
    return render_template('users.html')

@app.route('/settings')
@login_required
def settings():
    if current_user.perfil != 'admin':
        return redirect(url_for('dashboard'))
    return render_template('settings.html')

# ========== API de Indicadores ==========
@app.route('/api/indicadores', methods=['GET'])
@login_required
def get_indicadores():
    categoria_id = request.args.get('categoria_id')
    indicadores = db.get_indicadores(categoria_id=categoria_id)
    return jsonify(indicadores)

@app.route('/api/indicadores/<indicador_id>/dados', methods=['GET'])
@login_required
def get_dados_indicador(indicador_id):
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    if data_inicio:
        data_inicio = datetime.fromisoformat(data_inicio)
    if data_fim:
        data_fim = datetime.fromisoformat(data_fim)
    
    df = db.get_dados_indicador(indicador_id, data_inicio, data_fim)
    return jsonify(df.to_dict('records'))

@app.route('/api/indicadores', methods=['POST'])
@login_required
def create_indicador():
    if current_user.perfil not in ['admin', 'gestor']:
        return jsonify({"error": "Sem permissão"}), 403
    
    data = request.get_json()
    indicador = db.create_indicador(data)
    
    # Log de auditoria
    db.create_log_auditoria({
        'usuario_id': current_user.id,
        'acao': 'criar_indicador',
        'tabela': 'indicadores',
        'registro_id': indicador['id'],
        'dados_novos': data,
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent')
    })
    
    return jsonify(indicador), 201

# ========== API de Dashboard ==========
@app.route('/api/dashboard/summary', methods=['GET'])
@login_required
def get_dashboard_summary():
    """Retorna o resumo do dashboard com os 4 cards principais."""
    # Parâmetros de filtro
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=int)
    unidade = request.args.get('unidade')
    squad = request.args.get('squad')
    categoria = request.args.get('categoria')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    # Converte datas se fornecidas
    if data_inicio:
        data_inicio = datetime.fromisoformat(data_inicio).date()
    if data_fim:
        data_fim = datetime.fromisoformat(data_fim).date()
    
    # Busca resumo usando o serviço
    resumo = data_service.get_dashboard_summary(
        data_inicio=data_inicio,
        data_fim=data_fim,
        unidade=unidade,
        squad=squad,
        categoria=categoria,
        ano=ano,
        mes=mes
    )
    
    # Formata valores para exibição
    def format_value(value):
        """Formata valores monetários."""
        if value >= 1000000:
            return f"R${value/1000000:.2f}M"
        elif value >= 1000:
            return f"R${value/1000:.1f}k"
        else:
            return f"R${value:.2f}"
    
    # Aplica formatação
    resumo_formatado = {
        'produtos_vendidos': {
            'valor': resumo['produtos_vendidos'],
            'formatado': format_value(resumo['produtos_vendidos'])
        },
        'cancelamentos': {
            'valor': resumo['cancelamentos'],
            'formatado': format_value(resumo['cancelamentos'])
        },
        'estornos': {
            'valor': resumo['estornos'],
            'formatado': format_value(resumo['estornos'])
        },
        'estornos_cancelamentos': {
            'valor': resumo['estornos_cancelamentos'],
            'formatado': format_value(resumo['estornos_cancelamentos'])
        },
        'indice_cancelamento': resumo['indice_cancelamento'],
        'indice_estorno': resumo['indice_estorno']
    }
    
    return jsonify(resumo_formatado)

@app.route('/api/dashboard/filters', methods=['GET'])
@login_required
def get_dashboard_filters():
    """Retorna as opções disponíveis para os filtros."""
    filtros = {
        'anos': data_service.get_anos_disponiveis(),
        'unidades': data_service.get_unidades_disponiveis(),
        'squads': data_service.get_squads_disponiveis(),
        'categorias': data_service.get_categorias_disponiveis(),
        'meses': [
            {'valor': 1, 'nome': 'Janeiro'},
            {'valor': 2, 'nome': 'Fevereiro'},
            {'valor': 3, 'nome': 'Março'},
            {'valor': 4, 'nome': 'Abril'},
            {'valor': 5, 'nome': 'Maio'},
            {'valor': 6, 'nome': 'Junho'},
            {'valor': 7, 'nome': 'Julho'},
            {'valor': 8, 'nome': 'Agosto'},
            {'valor': 9, 'nome': 'Setembro'},
            {'valor': 10, 'nome': 'Outubro'},
            {'valor': 11, 'nome': 'Novembro'},
            {'valor': 12, 'nome': 'Dezembro'}
        ]
    }
    
    return jsonify(filtros)

@app.route('/api/dashboard/semanas', methods=['GET'])
@login_required
def get_semanas_mes():
    """Retorna as semanas disponíveis para um mês específico."""
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=int)
    
    if not ano or not mes:
        return jsonify({'error': 'Ano e mês são obrigatórios'}), 400
    
    # Busca semanas do mês
    df = data_service.get_produtos_vendidos_df(ano=ano, mes=mes)
    
    if df.empty:
        return jsonify({'semanas': []})
    
    # Extrai semanas únicas
    semanas = df['semana_domingo'].dt.date.unique()
    semanas_list = []
    
    for i, semana in enumerate(sorted(semanas)):
        semanas_list.append({
            'numero': i + 1,
            'data': semana.isoformat(),
            'label': f"Semana {i + 1} (até {semana.strftime('%d/%m')})"
        })
    
    return jsonify({'semanas': semanas_list})

# ========== Upload de Arquivos ==========
@app.route('/api/upload/produtos-vendidos', methods=['POST'])
@login_required
def upload_produtos_vendidos():
    if current_user.perfil not in ['admin', 'gestor']:
        return jsonify({"error": "Sem permissão"}), 403
    
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Arquivo sem nome"}), 400
    
    if not file.filename.lower().endswith('.csv'):
        return jsonify({"error": "Apenas arquivos CSV são aceitos"}), 400
    
    # Criar registro de importação
    importacao = db.create_importacao({
        'nome_arquivo': file.filename,
        'tipo_arquivo': 'csv',
        'status': 'processando',
        'usuario_id': current_user.id
    })
    
    try:
        # Ler e processar CSV
        df = pd.read_csv(file, sep=';', encoding='latin-1', skiprows=4)
        
        # Limpar e transformar dados
        df.columns = ['sku', 'nome', 'categoria', 'operacao', 'montavel', 
                     'quantidade', 'valor_unitario', 'subtotal', 'descontos', 'valor_total']
        
        # Remover linhas vazias
        df = df.dropna(subset=['nome'])
        
        # Converter tipos
        df['montavel'] = df['montavel'] == 'VERDADEIRO'
        df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
        
        # Limpar valores monetários
        for col in ['valor_unitario', 'subtotal', 'descontos', 'valor_total']:
            df[col] = df[col].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').astype(float)
        
        # Extrair período do arquivo (exemplo: 01/05/2025 e 31/05/2025)
        # Por enquanto vamos usar a data atual
        df['data_venda'] = datetime.now().date()
        df['periodo_inicio'] = datetime(2025, 5, 1).date()
        df['periodo_fim'] = datetime(2025, 5, 31).date()
        
        # Inserir no banco
        result = db.insert_produtos_vendidos(df)
        
        # Atualizar importação
        db.update_importacao(importacao['id'], {
            'status': 'concluido',
            'total_registros': len(df),
            'registros_importados': len(df),
            'registros_erro': 0,
            'periodo_inicio': df['periodo_inicio'].iloc[0],
            'periodo_fim': df['periodo_fim'].iloc[0]
        })
        
        return jsonify({
            "success": True,
            "message": f"{len(df)} produtos importados com sucesso",
            "importacao_id": importacao['id']
        })
        
    except Exception as e:
        # Registrar erro
        db.update_importacao(importacao['id'], {
            'status': 'erro',
            'mensagem_erro': str(e)
        })
        
        return jsonify({
            "success": False,
            "error": f"Erro ao processar arquivo: {str(e)}"
        }), 500

# ========== API de Categorias ==========
@app.route('/api/categorias', methods=['GET'])
@login_required
def get_categorias():
    categorias = db.get_categorias()
    return jsonify(categorias)

# ========== API de Dashboards ==========
@app.route('/api/dashboards', methods=['GET'])
@login_required
def get_dashboards():
    dashboards = db.get_dashboards_usuario(current_user.id)
    return jsonify(dashboards)

@app.route('/api/dashboards/<dashboard_id>/widgets', methods=['GET'])
@login_required
def get_dashboard_widgets(dashboard_id):
    widgets = db.get_dashboard_widgets(dashboard_id)
    return jsonify(widgets)

# ========== Configurações ==========
@app.route('/api/configuracoes/<chave>', methods=['GET'])
@login_required
def get_configuracao(chave):
    valor = db.get_configuracao(chave)
    return jsonify({"chave": chave, "valor": valor})

@app.route('/api/configuracoes/<chave>', methods=['PUT'])
@login_required
def update_configuracao(chave):
    if current_user.perfil != 'admin':
        return jsonify({"error": "Sem permissão"}), 403
    
    data = request.get_json()
    success = db.update_configuracao(chave, data['valor'])
    
    if success:
        # Log de auditoria
        db.create_log_auditoria({
            'usuario_id': current_user.id,
            'acao': 'atualizar_configuracao',
            'tabela': 'configuracoes',
            'dados_novos': {'chave': chave, 'valor': data['valor']},
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        })
        
        return jsonify({"success": True})
    
    return jsonify({"error": "Configuração não encontrada"}), 404

# ========== Inicialização ==========
def init_db():
    """Cria usuário admin padrão se não existir"""
    admin_email = 'octavio@eshows.com.br'
    if not db.get_usuario_by_email(admin_email):
        db.create_usuario({
            'email': admin_email,
            'nome': 'Octavio Costa',
            'senha_hash': Config.ADMIN_PASSWORD_HASH,
            'perfil': 'admin',
            'cargo': 'Administrador do Sistema',
            'departamento': 'TI'
        })
        print(f"Usuário admin criado: {admin_email}")

if __name__ == '__main__':
    # Criar diretório de uploads se não existir
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    # Inicializar banco
    init_db()
    
    # Rodar aplicação
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
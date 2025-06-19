from supabase import create_client, Client
from config.settings import Config
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self):
        self.supabase: Client = create_client(
            Config.SUPABASE_URL,
            Config.SUPABASE_KEY
        )
    
    # ========== Produtos Vendidos ==========
    def get_produtos_vendidos(self, 
                            periodo_inicio: Optional[datetime] = None,
                            periodo_fim: Optional[datetime] = None,
                            categoria: Optional[str] = None) -> pd.DataFrame:
        """Busca produtos vendidos com filtros opcionais"""
        query = self.supabase.table('produtos_vendidos').select('*')
        
        if periodo_inicio:
            query = query.gte('data_venda', periodo_inicio.isoformat())
        if periodo_fim:
            query = query.lte('data_venda', periodo_fim.isoformat())
        if categoria:
            query = query.eq('categoria', categoria)
        
        response = query.execute()
        return pd.DataFrame(response.data)
    
    def insert_produtos_vendidos(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Insere dados de produtos vendidos"""
        records = df.to_dict('records')
        response = self.supabase.table('produtos_vendidos').insert(records).execute()
        return {"success": True, "count": len(response.data)}
    
    # ========== Categorias ==========
    def get_categorias(self, ativo: bool = True) -> List[Dict]:
        """Busca categorias de indicadores"""
        query = self.supabase.table('categorias').select('*')
        if ativo is not None:
            query = query.eq('ativo', ativo)
        query = query.order('ordem')
        response = query.execute()
        return response.data
    
    # ========== Indicadores ==========
    def get_indicadores(self, categoria_id: Optional[str] = None, ativo: bool = True) -> List[Dict]:
        """Busca indicadores com filtros opcionais"""
        query = self.supabase.table('indicadores').select('*, categorias(*)')
        
        if categoria_id:
            query = query.eq('categoria_id', categoria_id)
        if ativo is not None:
            query = query.eq('ativo', ativo)
        
        response = query.execute()
        return response.data
    
    def create_indicador(self, data: Dict) -> Dict:
        """Cria um novo indicador"""
        response = self.supabase.table('indicadores').insert(data).execute()
        return response.data[0] if response.data else None
    
    # ========== Dados dos Indicadores ==========
    def get_dados_indicador(self, 
                          indicador_id: str,
                          data_inicio: Optional[datetime] = None,
                          data_fim: Optional[datetime] = None) -> pd.DataFrame:
        """Busca dados históricos de um indicador"""
        query = self.supabase.table('dados_indicadores').select('*').eq('indicador_id', indicador_id)
        
        if data_inicio:
            query = query.gte('data_referencia', data_inicio.isoformat())
        if data_fim:
            query = query.lte('data_referencia', data_fim.isoformat())
        
        query = query.order('data_referencia', desc=True)
        response = query.execute()
        return pd.DataFrame(response.data)
    
    def insert_dados_indicador(self, indicador_id: str, data: List[Dict]) -> Dict:
        """Insere dados de um indicador"""
        for record in data:
            record['indicador_id'] = indicador_id
        
        response = self.supabase.table('dados_indicadores').upsert(data).execute()
        return {"success": True, "count": len(response.data)}
    
    # ========== Usuários ==========
    def get_usuario_by_email(self, email: str) -> Optional[Dict]:
        """Busca usuário por email"""
        response = self.supabase.table('usuarios').select('*').eq('email', email).execute()
        return response.data[0] if response.data else None
    
    def create_usuario(self, data: Dict) -> Dict:
        """Cria um novo usuário"""
        response = self.supabase.table('usuarios').insert(data).execute()
        return response.data[0] if response.data else None
    
    def update_ultimo_acesso(self, usuario_id: str):
        """Atualiza último acesso do usuário"""
        self.supabase.table('usuarios').update({
            'ultimo_acesso': datetime.utcnow().isoformat()
        }).eq('id', usuario_id).execute()
    
    # ========== Configurações ==========
    def get_configuracao(self, chave: str) -> Optional[str]:
        """Busca uma configuração específica"""
        response = self.supabase.table('configuracoes').select('valor').eq('chave', chave).execute()
        return response.data[0]['valor'] if response.data else None
    
    def update_configuracao(self, chave: str, valor: str) -> bool:
        """Atualiza uma configuração"""
        response = self.supabase.table('configuracoes').update({
            'valor': valor
        }).eq('chave', chave).execute()
        return len(response.data) > 0
    
    # ========== Logs de Auditoria ==========
    def create_log_auditoria(self, data: Dict):
        """Cria um log de auditoria"""
        self.supabase.table('logs_auditoria').insert(data).execute()
    
    # ========== Dashboards ==========
    def get_dashboards_usuario(self, usuario_id: str) -> List[Dict]:
        """Busca dashboards de um usuário"""
        response = self.supabase.table('dashboards').select('*').eq('usuario_id', usuario_id).execute()
        return response.data
    
    def get_dashboard_widgets(self, dashboard_id: str) -> List[Dict]:
        """Busca widgets de um dashboard"""
        response = self.supabase.table('dashboard_widgets').select(
            '*, indicadores(*, categorias(*))'
        ).eq('dashboard_id', dashboard_id).execute()
        return response.data
    
    # ========== Importações ==========
    def create_importacao(self, data: Dict) -> Dict:
        """Registra uma nova importação de arquivo"""
        response = self.supabase.table('importacoes_arquivos').insert(data).execute()
        return response.data[0] if response.data else None
    
    def update_importacao(self, importacao_id: str, data: Dict):
        """Atualiza status de uma importação"""
        self.supabase.table('importacoes_arquivos').update(data).eq('id', importacao_id).execute()
    
    def create_erro_importacao(self, data: Dict):
        """Registra erro de importação"""
        self.supabase.table('importacoes_erros').insert(data).execute()

# Instância global
db = Database()
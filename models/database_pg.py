import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
from config.settings import Config
import json

class Database:
    def __init__(self):
        self.connection_string = Config.DATABASE_URL
        
    def get_connection(self):
        """Cria uma nova conexão com o banco"""
        return psycopg2.connect(self.connection_string)
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Executa uma query e retorna os resultados"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    return cursor.fetchall()
                conn.commit()
                return []
    
    def execute_insert(self, query: str, params: tuple = None) -> Dict:
        """Executa um INSERT e retorna o registro criado"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query + " RETURNING *", params)
                result = cursor.fetchone()
                conn.commit()
                return dict(result) if result else None
    
    # ========== Produtos Vendidos ==========
    def get_produtos_vendidos(self, 
                            periodo_inicio: Optional[datetime] = None,
                            periodo_fim: Optional[datetime] = None,
                            categoria: Optional[str] = None) -> pd.DataFrame:
        """Busca produtos vendidos com filtros opcionais"""
        query = "SELECT * FROM produtos_vendidos WHERE 1=1"
        params = []
        
        if periodo_inicio:
            query += " AND data_venda >= %s"
            params.append(periodo_inicio)
        if periodo_fim:
            query += " AND data_venda <= %s"
            params.append(periodo_fim)
        if categoria:
            query += " AND categoria = %s"
            params.append(categoria)
        
        query += " ORDER BY data_venda DESC"
        results = self.execute_query(query, tuple(params))
        return pd.DataFrame(results)
    
    def insert_produtos_vendidos(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Insere dados de produtos vendidos"""
        records_inserted = 0
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                for _, row in df.iterrows():
                    query = """
                        INSERT INTO produtos_vendidos 
                        (sku, nome, categoria, operacao, montavel, quantidade, 
                         valor_unitario, subtotal, descontos, valor_total, 
                         data_venda, periodo_inicio, periodo_fim)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    params = (
                        row['sku'], row['nome'], row['categoria'], row['operacao'],
                        row['montavel'], row['quantidade'], row['valor_unitario'],
                        row['subtotal'], row['descontos'], row['valor_total'],
                        row['data_venda'], row['periodo_inicio'], row['periodo_fim']
                    )
                    cursor.execute(query, params)
                    records_inserted += 1
                conn.commit()
        
        return {"success": True, "count": records_inserted}
    
    # ========== Categorias ==========
    def get_categorias(self, ativo: bool = True) -> List[Dict]:
        """Busca categorias de indicadores"""
        query = "SELECT * FROM categorias WHERE 1=1"
        params = []
        
        if ativo is not None:
            query += " AND ativo = %s"
            params.append(ativo)
        
        query += " ORDER BY ordem"
        return self.execute_query(query, tuple(params))
    
    # ========== Indicadores ==========
    def get_indicadores(self, categoria_id: Optional[str] = None, ativo: bool = True) -> List[Dict]:
        """Busca indicadores com filtros opcionais"""
        query = """
            SELECT i.*, c.nome as categoria_nome, c.cor as categoria_cor 
            FROM indicadores i
            LEFT JOIN categorias c ON i.categoria_id = c.id
            WHERE 1=1
        """
        params = []
        
        if categoria_id:
            query += " AND i.categoria_id = %s"
            params.append(categoria_id)
        if ativo is not None:
            query += " AND i.ativo = %s"
            params.append(ativo)
        
        return self.execute_query(query, tuple(params))
    
    def create_indicador(self, data: Dict) -> Dict:
        """Cria um novo indicador"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO indicadores ({columns}) VALUES ({placeholders})"
        return self.execute_insert(query, tuple(data.values()))
    
    # ========== Dados dos Indicadores ==========
    def get_dados_indicador(self, 
                          indicador_id: str,
                          data_inicio: Optional[datetime] = None,
                          data_fim: Optional[datetime] = None) -> pd.DataFrame:
        """Busca dados históricos de um indicador"""
        query = "SELECT * FROM dados_indicadores WHERE indicador_id = %s"
        params = [indicador_id]
        
        if data_inicio:
            query += " AND data_referencia >= %s"
            params.append(data_inicio)
        if data_fim:
            query += " AND data_referencia <= %s"
            params.append(data_fim)
        
        query += " ORDER BY data_referencia DESC"
        results = self.execute_query(query, tuple(params))
        return pd.DataFrame(results)
    
    def insert_dados_indicador(self, indicador_id: str, data: List[Dict]) -> Dict:
        """Insere dados de um indicador"""
        records_inserted = 0
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                for record in data:
                    record['indicador_id'] = indicador_id
                    columns = ', '.join(record.keys())
                    placeholders = ', '.join(['%s'] * len(record))
                    query = f"""
                        INSERT INTO dados_indicadores ({columns}) 
                        VALUES ({placeholders})
                        ON CONFLICT (indicador_id, data_referencia) 
                        DO UPDATE SET 
                            valor = EXCLUDED.valor,
                            meta = EXCLUDED.meta,
                            observacoes = EXCLUDED.observacoes,
                            updated_at = NOW()
                    """
                    cursor.execute(query, tuple(record.values()))
                    records_inserted += 1
                conn.commit()
        
        return {"success": True, "count": records_inserted}
    
    # ========== Usuários ==========
    def get_usuario_by_email(self, email: str) -> Optional[Dict]:
        """Busca usuário por email"""
        query = "SELECT * FROM usuarios WHERE email = %s"
        results = self.execute_query(query, (email,))
        return results[0] if results else None
    
    def create_usuario(self, data: Dict) -> Dict:
        """Cria um novo usuário"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO usuarios ({columns}) VALUES ({placeholders})"
        return self.execute_insert(query, tuple(data.values()))
    
    def update_ultimo_acesso(self, usuario_id: str):
        """Atualiza último acesso do usuário"""
        query = "UPDATE usuarios SET ultimo_acesso = NOW() WHERE id = %s"
        self.execute_query(query, (usuario_id,))
    
    # ========== Configurações ==========
    def get_configuracao(self, chave: str) -> Optional[str]:
        """Busca uma configuração específica"""
        query = "SELECT valor FROM configuracoes WHERE chave = %s"
        results = self.execute_query(query, (chave,))
        return results[0]['valor'] if results else None
    
    def update_configuracao(self, chave: str, valor: str) -> bool:
        """Atualiza uma configuração"""
        query = "UPDATE configuracoes SET valor = %s, updated_at = NOW() WHERE chave = %s"
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (valor, chave))
                updated = cursor.rowcount > 0
                conn.commit()
                return updated
    
    # ========== Logs de Auditoria ==========
    def create_log_auditoria(self, data: Dict):
        """Cria um log de auditoria"""
        # Converter dicionários para JSON
        if 'dados_anteriores' in data and isinstance(data['dados_anteriores'], dict):
            data['dados_anteriores'] = json.dumps(data['dados_anteriores'])
        if 'dados_novos' in data and isinstance(data['dados_novos'], dict):
            data['dados_novos'] = json.dumps(data['dados_novos'])
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO logs_auditoria ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))
    
    # ========== Dashboards ==========
    def get_dashboards_usuario(self, usuario_id: str) -> List[Dict]:
        """Busca dashboards de um usuário"""
        query = "SELECT * FROM dashboards WHERE usuario_id = %s ORDER BY created_at DESC"
        return self.execute_query(query, (usuario_id,))
    
    def get_dashboard_widgets(self, dashboard_id: str) -> List[Dict]:
        """Busca widgets de um dashboard"""
        query = """
            SELECT w.*, 
                   i.nome as indicador_nome, i.unidade, i.tipo as indicador_tipo,
                   c.nome as categoria_nome, c.cor as categoria_cor
            FROM dashboard_widgets w
            JOIN indicadores i ON w.indicador_id = i.id
            LEFT JOIN categorias c ON i.categoria_id = c.id
            WHERE w.dashboard_id = %s
            ORDER BY w.posicao_y, w.posicao_x
        """
        return self.execute_query(query, (dashboard_id,))
    
    # ========== Importações ==========
    def create_importacao(self, data: Dict) -> Dict:
        """Registra uma nova importação de arquivo"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO importacoes_arquivos ({columns}) VALUES ({placeholders})"
        return self.execute_insert(query, tuple(data.values()))
    
    def update_importacao(self, importacao_id: str, data: Dict):
        """Atualiza status de uma importação"""
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE importacoes_arquivos SET {set_clause}, updated_at = NOW() WHERE id = %s"
        values = list(data.values()) + [importacao_id]
        self.execute_query(query, tuple(values))
    
    def create_erro_importacao(self, data: Dict):
        """Registra erro de importação"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO importacoes_erros ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))
    
    # Compatibilidade com código existente
    @property
    def supabase(self):
        """Propriedade para manter compatibilidade com código que usa db.supabase"""
        class FakeSupabase:
            def __init__(self, db):
                self.db = db
                
            def table(self, table_name):
                return FakeTable(self.db, table_name)
        
        return FakeSupabase(self)

class FakeTable:
    """Classe para simular a interface do Supabase"""
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name
        self.query_parts = []
        
    def select(self, columns='*'):
        self.columns = columns
        self.query_parts.append(f"SELECT {columns} FROM {self.table_name}")
        return self
    
    def eq(self, column, value):
        self.query_parts.append(f"WHERE {column} = '{value}'")
        return self
        
    def execute(self):
        # Simplified - in real implementation would build proper query
        if self.table_name == 'usuarios':
            results = self.db.execute_query(f"SELECT * FROM {self.table_name}", ())
        else:
            results = self.db.execute_query(' '.join(self.query_parts), ())
        
        class Result:
            def __init__(self, data):
                self.data = data
        
        return Result(results)

# Instância global
db = Database()
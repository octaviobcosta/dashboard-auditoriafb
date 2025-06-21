"""
Serviço principal para acesso e manipulação de dados das tabelas produtos_vendidos e estornos_cancelamentos.
"""

import pandas as pd
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, date, timedelta
import numpy as np
from functools import lru_cache
import logging

from models.database import db


class DataService:
    """Serviço para gerenciar dados de produtos vendidos e estornos/cancelamentos."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._cache = {}
        self._cache_timeout = 300  # 5 minutos em segundos
        self._last_cache_update = {}
        
    # ========== Produtos Vendidos ==========
    
    def get_produtos_vendidos_df(self, 
                                 data_inicio: Optional[date] = None,
                                 data_fim: Optional[date] = None,
                                 unidade: Optional[str] = None,
                                 squad: Optional[str] = None,
                                 ano: Optional[int] = None,
                                 mes: Optional[int] = None,
                                 use_cache: bool = True) -> pd.DataFrame:
        """
        Retorna DataFrame com dados de produtos vendidos.
        
        Args:
            data_inicio: Data inicial do período (usa semana_domingo)
            data_fim: Data final do período (usa semana_domingo)
            unidade: Filtrar por unidade específica
            squad: Filtrar por squad específico
            ano: Filtrar por ano específico
            mes: Filtrar por mês específico
            use_cache: Se deve usar cache (padrão: True)
            
        Returns:
            DataFrame com dados de produtos vendidos
        """
        cache_key = f"produtos_vendidos_{data_inicio}_{data_fim}_{unidade}_{squad}_{ano}_{mes}"
        
        # Verifica cache
        if use_cache and self._is_cache_valid(cache_key):
            self.logger.info("Retornando dados de produtos_vendidos do cache")
            return self._cache[cache_key].copy()
        
        # Busca dados do banco
        self.logger.info("Buscando dados de produtos_vendidos do banco")
        
        query = db.supabase.table('produtos_vendidos').select('*')
        
        # Aplica filtros
        if data_inicio:
            query = query.gte('semana_domingo', data_inicio.isoformat())
        if data_fim:
            query = query.lte('semana_domingo', data_fim.isoformat())
        if unidade:
            query = query.eq('unidade', unidade)
        if squad:
            query = query.eq('squad', squad)
        if ano:
            query = query.eq('ano', ano)
        if mes:
            query = query.eq('mes', mes)
            
        # Ordena por data
        query = query.order('semana_domingo', desc=True)
        
        # Executa query
        result = query.execute()
        
        # Converte para DataFrame
        df = pd.DataFrame(result.data)
        
        if not df.empty:
            # Converte tipos de dados
            df['semana_domingo'] = pd.to_datetime(df['semana_domingo'])
            df['produtos_vendidos'] = pd.to_numeric(df['produtos_vendidos'], errors='coerce')
            df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
            df['mes'] = pd.to_numeric(df['mes'], errors='coerce')
            
        # Atualiza cache
        if use_cache:
            self._cache[cache_key] = df.copy()
            self._last_cache_update[cache_key] = datetime.now()
            
        return df
    
    # ========== Estornos e Cancelamentos ==========
    
    def get_estornos_cancelamentos_df(self,
                                     data_inicio: Optional[date] = None,
                                     data_fim: Optional[date] = None,
                                     unidade: Optional[str] = None,
                                     squad: Optional[str] = None,
                                     tipo: Optional[str] = None,
                                     categoria: Optional[str] = None,
                                     ano: Optional[int] = None,
                                     mes: Optional[int] = None,
                                     use_cache: bool = True) -> pd.DataFrame:
        """
        Retorna DataFrame com dados de estornos e cancelamentos.
        
        Args:
            data_inicio: Data inicial do período
            data_fim: Data final do período
            unidade: Filtrar por unidade específica
            squad: Filtrar por squad específico
            tipo: Filtrar por tipo ('Cancelado' ou 'Estornado')
            categoria: Filtrar por categoria de produto
            ano: Filtrar por ano específico
            mes: Filtrar por mês específico
            use_cache: Se deve usar cache (padrão: True)
            
        Returns:
            DataFrame com dados de estornos e cancelamentos
        """
        cache_key = f"estornos_{data_inicio}_{data_fim}_{unidade}_{squad}_{tipo}_{categoria}_{ano}_{mes}"
        
        # Verifica cache
        if use_cache and self._is_cache_valid(cache_key):
            self.logger.info("Retornando dados de estornos_cancelamentos do cache")
            return self._cache[cache_key].copy()
        
        # Busca dados do banco
        self.logger.info("Buscando dados de estornos_cancelamentos do banco")
        
        query = db.supabase.table('estornos_cancelamento').select('*')
        
        # Aplica filtros
        if data_inicio:
            query = query.gte('data', data_inicio.isoformat())
        if data_fim:
            query = query.lte('data', data_fim.isoformat())
        if unidade:
            query = query.eq('unidade', unidade)
        if squad:
            query = query.eq('squad', squad)
        if tipo:
            query = query.eq('tipo', tipo)
        if categoria:
            query = query.eq('categoria', categoria)
        if ano:
            query = query.eq('ano', ano)
        if mes:
            query = query.eq('mes', mes)
            
        # Ordena por data
        query = query.order('data', desc=True)
        
        # Executa query
        result = query.execute()
        
        # Converte para DataFrame
        df = pd.DataFrame(result.data)
        
        if not df.empty:
            # Converte tipos de dados
            df['data'] = pd.to_datetime(df['data'])
            df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
            df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
            df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
            
            # Converte mes para número se estiver como string
            if df['mes'].dtype == 'object':
                mes_map = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
                          'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
                df['mes_num'] = df['mes'].map(mes_map)
            else:
                df['mes_num'] = df['mes']
                
        # Atualiza cache
        if use_cache:
            self._cache[cache_key] = df.copy()
            self._last_cache_update[cache_key] = datetime.now()
            
        return df
    
    # ========== Métodos de Análise ==========
    
    def get_total_produtos_vendidos(self, 
                                   data_inicio: Optional[date] = None,
                                   data_fim: Optional[date] = None,
                                   unidade: Optional[str] = None,
                                   squad: Optional[str] = None,
                                   ano: Optional[int] = None,
                                   mes: Optional[int] = None) -> float:
        """
        Retorna o total de produtos vendidos (soma).
        """
        df = self.get_produtos_vendidos_df(data_inicio, data_fim, unidade, squad, ano, mes)
        
        if df.empty:
            return 0.0
            
        return float(df['produtos_vendidos'].sum())
    
    def get_total_cancelamentos(self,
                               data_inicio: Optional[date] = None,
                               data_fim: Optional[date] = None,
                               unidade: Optional[str] = None,
                               squad: Optional[str] = None,
                               categoria: Optional[str] = None,
                               ano: Optional[int] = None,
                               mes: Optional[int] = None) -> float:
        """
        Retorna o total de cancelamentos (tipo = 'Cancelado').
        """
        df = self.get_estornos_cancelamentos_df(
            data_inicio, data_fim, unidade, squad, 
            tipo='Cancelado', categoria=categoria, ano=ano, mes=mes
        )
        
        if df.empty:
            return 0.0
            
        return float(df['valor'].sum())
    
    def get_total_estornos(self,
                          data_inicio: Optional[date] = None,
                          data_fim: Optional[date] = None,
                          unidade: Optional[str] = None,
                          squad: Optional[str] = None,
                          categoria: Optional[str] = None,
                          ano: Optional[int] = None,
                          mes: Optional[int] = None) -> float:
        """
        Retorna o total de estornos (tipo = 'Estornado').
        """
        df = self.get_estornos_cancelamentos_df(
            data_inicio, data_fim, unidade, squad, 
            tipo='Estornado', categoria=categoria, ano=ano, mes=mes
        )
        
        if df.empty:
            return 0.0
            
        return float(df['valor'].sum())
    
    def get_total_estornos_cancelamentos(self,
                                        data_inicio: Optional[date] = None,
                                        data_fim: Optional[date] = None,
                                        unidade: Optional[str] = None,
                                        squad: Optional[str] = None,
                                        categoria: Optional[str] = None,
                                        ano: Optional[int] = None,
                                        mes: Optional[int] = None) -> float:
        """
        Retorna o total de estornos + cancelamentos.
        """
        cancelamentos = self.get_total_cancelamentos(
            data_inicio, data_fim, unidade, squad, categoria, ano, mes
        )
        estornos = self.get_total_estornos(
            data_inicio, data_fim, unidade, squad, categoria, ano, mes
        )
        
        return cancelamentos + estornos
    
    def get_indice_cancelamento(self,
                               data_inicio: Optional[date] = None,
                               data_fim: Optional[date] = None,
                               unidade: Optional[str] = None,
                               squad: Optional[str] = None,
                               categoria: Optional[str] = None,
                               ano: Optional[int] = None,
                               mes: Optional[int] = None) -> float:
        """
        Calcula o índice de cancelamento (cancelamentos / faturamento).
        """
        faturamento = self.get_total_produtos_vendidos(
            data_inicio, data_fim, unidade, squad, ano, mes
        )
        cancelamentos = self.get_total_cancelamentos(
            data_inicio, data_fim, unidade, squad, categoria, ano, mes
        )
        
        if faturamento == 0:
            return 0.0
            
        return round((cancelamentos / faturamento) * 100, 2)
    
    def get_indice_estorno(self,
                          data_inicio: Optional[date] = None,
                          data_fim: Optional[date] = None,
                          unidade: Optional[str] = None,
                          squad: Optional[str] = None,
                          categoria: Optional[str] = None,
                          ano: Optional[int] = None,
                          mes: Optional[int] = None) -> float:
        """
        Calcula o índice de estorno (estornos / faturamento).
        """
        faturamento = self.get_total_produtos_vendidos(
            data_inicio, data_fim, unidade, squad, ano, mes
        )
        estornos = self.get_total_estornos(
            data_inicio, data_fim, unidade, squad, categoria, ano, mes
        )
        
        if faturamento == 0:
            return 0.0
            
        return round((estornos / faturamento) * 100, 2)
    
    def get_dashboard_summary(self,
                             data_inicio: Optional[date] = None,
                             data_fim: Optional[date] = None,
                             unidade: Optional[str] = None,
                             squad: Optional[str] = None,
                             categoria: Optional[str] = None,
                             ano: Optional[int] = None,
                             mes: Optional[int] = None) -> Dict[str, Any]:
        """
        Retorna resumo completo para o dashboard.
        """
        produtos_vendidos = self.get_total_produtos_vendidos(
            data_inicio, data_fim, unidade, squad, ano, mes
        )
        cancelamentos = self.get_total_cancelamentos(
            data_inicio, data_fim, unidade, squad, categoria, ano, mes
        )
        estornos = self.get_total_estornos(
            data_inicio, data_fim, unidade, squad, categoria, ano, mes
        )
        
        return {
            'produtos_vendidos': produtos_vendidos,
            'cancelamentos': cancelamentos,
            'estornos': estornos,
            'estornos_cancelamentos': cancelamentos + estornos,
            'indice_cancelamento': self.get_indice_cancelamento(
                data_inicio, data_fim, unidade, squad, categoria, ano, mes
            ),
            'indice_estorno': self.get_indice_estorno(
                data_inicio, data_fim, unidade, squad, categoria, ano, mes
            )
        }
        
    def get_resumo_estornos(self,
                           data_inicio: Optional[date] = None,
                           data_fim: Optional[date] = None) -> Dict[str, Any]:
        """
        Retorna resumo dos estornos e cancelamentos no período.
        
        Returns:
            Dicionário com métricas resumidas
        """
        df = self.get_estornos_cancelamentos_df(data_inicio, data_fim)
        
        if df.empty:
            return {
                'total_estornos': 0,
                'total_atendimentos': 0,
                'taxa_estorno': 0,
                'unidades_afetadas': 0,
                'operacoes': []
            }
            
        return {
            'total_estornos': int(df['quantidade'].sum()),
            'total_atendimentos': int(df['total_atendimentos'].sum()),
            'taxa_estorno': float(df['percentual'].mean()),
            'unidades_afetadas': df['unidade'].nunique(),
            'operacoes': df['operacao'].value_counts().to_dict(),
            'periodo': {
                'inicio': df['data'].min().strftime('%d/%m/%Y'),
                'fim': df['data'].max().strftime('%d/%m/%Y')
            }
        }
        
    def get_vendas_por_categoria(self,
                                data_inicio: Optional[date] = None,
                                data_fim: Optional[date] = None) -> pd.DataFrame:
        """
        Retorna vendas agrupadas por categoria.
        """
        df = self.get_produtos_vendidos_df(data_inicio, data_fim)
        
        if df.empty:
            return pd.DataFrame()
            
        return df.groupby('categoria').agg({
            'valor_total': 'sum',
            'quantidade': 'sum',
            'sku': 'nunique'
        }).rename(columns={
            'valor_total': 'total_vendas',
            'quantidade': 'total_produtos',
            'sku': 'produtos_unicos'
        }).sort_values('total_vendas', ascending=False)
        
    def get_vendas_por_periodo(self,
                              data_inicio: Optional[date] = None,
                              data_fim: Optional[date] = None,
                              periodo: str = 'dia') -> pd.DataFrame:
        """
        Retorna vendas agrupadas por período (dia, semana, mês).
        
        Args:
            periodo: 'dia', 'semana' ou 'mes'
        """
        df = self.get_produtos_vendidos_df(data_inicio, data_fim)
        
        if df.empty:
            return pd.DataFrame()
            
        # Define agrupamento
        if periodo == 'dia':
            df['periodo'] = df['data_venda'].dt.date
        elif periodo == 'semana':
            df['periodo'] = df['data_venda'].dt.to_period('W')
        elif periodo == 'mes':
            df['periodo'] = df['data_venda'].dt.to_period('M')
        else:
            df['periodo'] = df['data_venda'].dt.date
            
        return df.groupby('periodo').agg({
            'valor_total': 'sum',
            'quantidade': 'sum',
            'id': 'count'
        }).rename(columns={
            'valor_total': 'total_vendas',
            'quantidade': 'total_produtos',
            'id': 'num_transacoes'
        })
        
    def get_estornos_por_unidade(self,
                                data_inicio: Optional[date] = None,
                                data_fim: Optional[date] = None) -> pd.DataFrame:
        """
        Retorna estornos agrupados por unidade.
        """
        df = self.get_estornos_cancelamentos_df(data_inicio, data_fim)
        
        if df.empty:
            return pd.DataFrame()
            
        return df.groupby('unidade').agg({
            'quantidade': 'sum',
            'total_atendimentos': 'sum',
            'percentual': 'mean'
        }).round(2).sort_values('quantidade', ascending=False)
        
    def get_top_produtos(self,
                        data_inicio: Optional[date] = None,
                        data_fim: Optional[date] = None,
                        top_n: int = 10) -> pd.DataFrame:
        """
        Retorna os produtos mais vendidos.
        
        Args:
            top_n: Número de produtos a retornar
        """
        df = self.get_produtos_vendidos_df(data_inicio, data_fim)
        
        if df.empty:
            return pd.DataFrame()
            
        return df.groupby(['sku', 'nome']).agg({
            'quantidade': 'sum',
            'valor_total': 'sum'
        }).sort_values('valor_total', ascending=False).head(top_n)
        
    # ========== Métodos Auxiliares ==========
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Verifica se o cache ainda é válido."""
        if cache_key not in self._cache:
            return False
            
        last_update = self._last_cache_update.get(cache_key)
        if not last_update:
            return False
            
        # Verifica timeout
        if (datetime.now() - last_update).seconds > self._cache_timeout:
            return False
            
        return True
        
    def clear_cache(self):
        """Limpa todo o cache."""
        self._cache.clear()
        self._last_cache_update.clear()
        self.logger.info("Cache limpo")
        
    def get_unidades_disponiveis(self) -> List[str]:
        """Retorna lista de unidades disponíveis."""
        # Busca unidades em produtos vendidos
        query = db.supabase.table('produtos_vendidos').select('unidade').execute()
        unidades_vendas = set([item['unidade'] for item in query.data if item.get('unidade')])
        
        # Busca unidades em estornos
        query = db.supabase.table('estornos_cancelamento').select('unidade').execute()
        unidades_estornos = set([item['unidade'] for item in query.data if item.get('unidade')])
        
        # Combina e ordena
        todas_unidades = sorted(list(unidades_vendas.union(unidades_estornos)))
        
        return todas_unidades
    
    def get_squads_disponiveis(self) -> List[str]:
        """Retorna lista de squads disponíveis."""
        # Busca squads em produtos vendidos
        query = db.supabase.table('produtos_vendidos').select('squad').execute()
        squads_vendas = set([item['squad'] for item in query.data if item.get('squad')])
        
        # Busca squads em estornos
        query = db.supabase.table('estornos_cancelamento').select('squad').execute()
        squads_estornos = set([item['squad'] for item in query.data if item.get('squad')])
        
        # Combina e ordena
        todos_squads = sorted(list(squads_vendas.union(squads_estornos)))
        
        return todos_squads
        
    def get_categorias_disponiveis(self) -> List[str]:
        """Retorna lista de categorias disponíveis."""
        # Categorias estão apenas na tabela estornos_cancelamento
        query = db.supabase.table('estornos_cancelamento').select('categoria').execute()
        categorias = set([item['categoria'] for item in query.data if item.get('categoria')])
        
        return sorted(list(categorias))
    
    def get_anos_disponiveis(self) -> List[int]:
        """Retorna lista de anos disponíveis."""
        # Busca anos em produtos vendidos
        query = db.supabase.table('produtos_vendidos').select('ano').execute()
        anos_vendas = set([item['ano'] for item in query.data if item.get('ano')])
        
        # Busca anos em estornos
        query = db.supabase.table('estornos_cancelamento').select('ano').execute()
        anos_estornos = set([item['ano'] for item in query.data if item.get('ano')])
        
        # Combina e ordena
        todos_anos = sorted(list(anos_vendas.union(anos_estornos)), reverse=True)
        
        return todos_anos
        
    def get_periodo_dados(self) -> Tuple[date, date]:
        """Retorna o período de dados disponível (data mínima e máxima)."""
        # Produtos vendidos
        query = db.supabase.table('produtos_vendidos').select('data_venda').order('data_venda').limit(1).execute()
        min_vendas = pd.to_datetime(query.data[0]['data_venda']).date() if query.data else None
        
        query = db.supabase.table('produtos_vendidos').select('data_venda').order('data_venda', desc=True).limit(1).execute()
        max_vendas = pd.to_datetime(query.data[0]['data_venda']).date() if query.data else None
        
        # Estornos
        try:
            query = db.supabase.table('estornos_cancelamento').select('data').order('data').limit(1).execute()
        except:
            query = db.supabase.table('estornos_cancelamentos').select('data').order('data').limit(1).execute()
            
        min_estornos = pd.to_datetime(query.data[0]['data']).date() if query.data else None
        
        try:
            query = db.supabase.table('estornos_cancelamento').select('data').order('data', desc=True).limit(1).execute()
        except:
            query = db.supabase.table('estornos_cancelamentos').select('data').order('data', desc=True).limit(1).execute()
            
        max_estornos = pd.to_datetime(query.data[0]['data']).date() if query.data else None
        
        # Retorna o período mais amplo
        data_inicio = min(filter(None, [min_vendas, min_estornos])) if any([min_vendas, min_estornos]) else date.today()
        data_fim = max(filter(None, [max_vendas, max_estornos])) if any([max_vendas, max_estornos]) else date.today()
        
        return data_inicio, data_fim


# Instância global do serviço
data_service = DataService()
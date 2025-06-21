"""
Módulo de tratamento de dados para integração com Supabase.
Fornece mapeamento de colunas, validação, conversão e processamento de dados.
"""

from .mappers.base import ColumnMapper, TableSchema
from .validators.base import DataValidator
from .converters.base import TypeConverter
from .processors.base import DataProcessor

__all__ = [
    'ColumnMapper',
    'TableSchema', 
    'DataValidator',
    'TypeConverter',
    'DataProcessor'
]
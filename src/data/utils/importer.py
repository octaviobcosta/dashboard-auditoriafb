"""
Utilitários para importação de dados de diferentes fontes.
"""

import pandas as pd
from typing import Dict, List, Optional, Any, Union
import os
from pathlib import Path
import json
import csv
from datetime import datetime

from ..mappers.base import ColumnMapper, TableSchema
from ..validators.base import DataValidator
from ..converters.base import TypeConverter
from ..processors.base import DataProcessor, ProcessingResult


class DataImporter:
    """Importador de dados com suporte a múltiplos formatos."""
    
    def __init__(self, 
                 mapper: Optional[ColumnMapper] = None,
                 validator: Optional[DataValidator] = None,
                 converter: Optional[TypeConverter] = None,
                 processor: Optional[DataProcessor] = None):
        self.mapper = mapper or ColumnMapper()
        self.validator = validator or DataValidator()
        self.converter = converter or TypeConverter()
        self.processor = processor or DataProcessor()
        
    def import_excel(self, 
                    filepath: str, 
                    sheet_name: Optional[Union[str, int]] = 0,
                    table_name: Optional[str] = None,
                    **kwargs) -> ProcessingResult:
        """Importa dados de arquivo Excel."""
        self.processor.logger.info(f"Importando Excel: {filepath}")
        
        try:
            # Lê o arquivo Excel
            df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
            
            # Define nome da tabela se não fornecido
            if not table_name:
                table_name = Path(filepath).stem.lower().replace(" ", "_")
                
            # Processa os dados
            return self._process_dataframe(df, table_name)
            
        except Exception as e:
            self.processor.logger.error(f"Erro ao importar Excel: {str(e)}")
            raise
            
    def import_csv(self,
                  filepath: str,
                  table_name: Optional[str] = None,
                  encoding: str = 'utf-8',
                  **kwargs) -> ProcessingResult:
        """Importa dados de arquivo CSV."""
        self.processor.logger.info(f"Importando CSV: {filepath}")
        
        try:
            # Detecta delimitador se não fornecido
            if 'delimiter' not in kwargs and 'sep' not in kwargs:
                delimiter = self._detect_delimiter(filepath, encoding)
                kwargs['sep'] = delimiter
                
            # Lê o arquivo CSV
            df = pd.read_csv(filepath, encoding=encoding, **kwargs)
            
            # Define nome da tabela se não fornecido
            if not table_name:
                table_name = Path(filepath).stem.lower().replace(" ", "_")
                
            # Processa os dados
            return self._process_dataframe(df, table_name)
            
        except Exception as e:
            self.processor.logger.error(f"Erro ao importar CSV: {str(e)}")
            raise
            
    def import_json(self,
                   filepath: str,
                   table_name: Optional[str] = None,
                   **kwargs) -> ProcessingResult:
        """Importa dados de arquivo JSON."""
        self.processor.logger.info(f"Importando JSON: {filepath}")
        
        try:
            # Lê o arquivo JSON
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Converte para DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Tenta diferentes estruturas JSON
                if any(isinstance(v, list) for v in data.values()):
                    # JSON com arrays como valores
                    df = pd.DataFrame(data)
                else:
                    # JSON simples
                    df = pd.DataFrame([data])
            else:
                raise ValueError("Formato JSON não suportado")
                
            # Define nome da tabela se não fornecido
            if not table_name:
                table_name = Path(filepath).stem.lower().replace(" ", "_")
                
            # Processa os dados
            return self._process_dataframe(df, table_name)
            
        except Exception as e:
            self.processor.logger.error(f"Erro ao importar JSON: {str(e)}")
            raise
            
    def import_from_dataframe(self,
                            df: pd.DataFrame,
                            table_name: str) -> ProcessingResult:
        """Importa dados de um DataFrame pandas."""
        return self._process_dataframe(df, table_name)
        
    def _process_dataframe(self, df: pd.DataFrame, table_name: str) -> ProcessingResult:
        """Processa um DataFrame através do pipeline configurado."""
        # Adiciona etapas de processamento
        self.processor.processing_steps = []
        
        # 1. Limpeza inicial
        self.processor.add_processing_step(
            lambda data: self._clean_dataframe(data),
            "Limpeza inicial"
        )
        
        # 2. Mapeamento de colunas
        if table_name in self.mapper.schemas:
            self.processor.add_processing_step(
                lambda data: self._map_columns(data, table_name),
                "Mapeamento de colunas"
            )
            
        # 3. Validação
        self.processor.add_processing_step(
            lambda data: self._validate_data(data, table_name),
            "Validação de dados"
        )
        
        # 4. Conversão de tipos
        self.processor.add_processing_step(
            lambda data: self._convert_types(data, table_name),
            "Conversão de tipos"
        )
        
        # Processa os dados
        return self.processor.process(df)
        
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpa o DataFrame removendo linhas/colunas vazias."""
        # Remove colunas completamente vazias
        df = df.dropna(axis=1, how='all')
        
        # Remove linhas completamente vazias
        df = df.dropna(axis=0, how='all')
        
        # Remove espaços extras nos nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Remove caracteres especiais dos nomes das colunas
        df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True)
        df.columns = df.columns.str.replace(r'\s+', '_', regex=True)
        df.columns = df.columns.str.lower()
        
        return df
        
    def _map_columns(self, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """Mapeia colunas usando o ColumnMapper."""
        if table_name not in self.mapper.schemas:
            return df
            
        mapped_data = []
        
        for _, row in df.iterrows():
            mapped_row = self.mapper.map_data(table_name, row.to_dict())
            mapped_data.append(mapped_row)
            
        return pd.DataFrame(mapped_data)
        
    def _validate_data(self, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """Valida dados usando o DataValidator."""
        # Cria schema de validação baseado nos tipos
        schema = {}
        
        if table_name in self.mapper.schemas:
            table_schema = self.mapper.schemas[table_name]
            for col_name, col_def in table_schema.columns.items():
                schema[col_name] = col_def.data_type.value
        else:
            # Infere tipos das colunas
            for col in df.columns:
                if df[col].dtype == 'int64':
                    schema[col] = 'integer'
                elif df[col].dtype == 'float64':
                    schema[col] = 'float'
                elif df[col].dtype == 'bool':
                    schema[col] = 'boolean'
                else:
                    schema[col] = 'text'
                    
        # Valida cada linha
        validated_rows = []
        
        for idx, row in df.iterrows():
            validation_results = self.validator.validate_row(row.to_dict(), schema)
            
            # Coleta valores sanitizados
            sanitized_row = {}
            for col, result in validation_results.items():
                if result.is_valid:
                    sanitized_row[col] = result.sanitized_value
                else:
                    # Log erros mas mantém valor original
                    for error in result.errors:
                        self.processor.logger.warning(
                            f"Linha {idx}, coluna {col}: {error}"
                        )
                    sanitized_row[col] = row[col]
                    
            validated_rows.append(sanitized_row)
            
        return pd.DataFrame(validated_rows)
        
    def _convert_types(self, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """Converte tipos de dados usando o TypeConverter."""
        type_mapping = {}
        
        if table_name in self.mapper.schemas:
            table_schema = self.mapper.schemas[table_name]
            for col_name, col_def in table_schema.columns.items():
                if col_name in df.columns:
                    type_mapping[col_name] = col_def.data_type.value
                    
        if type_mapping:
            return self.converter.convert_dataframe(df, type_mapping)
            
        return df
        
    def _detect_delimiter(self, filepath: str, encoding: str = 'utf-8') -> str:
        """Detecta o delimitador de um arquivo CSV."""
        with open(filepath, 'r', encoding=encoding) as f:
            # Lê primeira linha
            first_line = f.readline()
            
            # Conta ocorrências de possíveis delimitadores
            delimiters = [',', ';', '\t', '|']
            delimiter_counts = {}
            
            for delimiter in delimiters:
                delimiter_counts[delimiter] = first_line.count(delimiter)
                
            # Retorna o delimitador mais frequente
            return max(delimiter_counts, key=delimiter_counts.get)
            
    def preview_file(self, 
                    filepath: str, 
                    rows: int = 10,
                    file_type: Optional[str] = None) -> pd.DataFrame:
        """Visualiza as primeiras linhas de um arquivo."""
        if not file_type:
            # Detecta tipo pelo extensão
            ext = Path(filepath).suffix.lower()
            file_type = ext[1:]  # Remove o ponto
            
        if file_type in ['xlsx', 'xls']:
            return pd.read_excel(filepath, nrows=rows)
        elif file_type == 'csv':
            encoding = 'utf-8'
            delimiter = self._detect_delimiter(filepath, encoding)
            return pd.read_csv(filepath, sep=delimiter, encoding=encoding, nrows=rows)
        elif file_type == 'json':
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return pd.DataFrame(data[:rows])
                else:
                    return pd.DataFrame([data])
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {file_type}")
            
    def get_file_info(self, filepath: str) -> Dict[str, Any]:
        """Obtém informações sobre o arquivo."""
        path = Path(filepath)
        
        info = {
            "filename": path.name,
            "size_bytes": path.stat().st_size,
            "size_mb": round(path.stat().st_size / (1024 * 1024), 2),
            "extension": path.suffix.lower(),
            "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
            "exists": path.exists()
        }
        
        # Adiciona informações específicas do tipo
        if info["extension"] in ['.xlsx', '.xls']:
            xl_file = pd.ExcelFile(filepath)
            info["sheets"] = xl_file.sheet_names
            info["total_sheets"] = len(xl_file.sheet_names)
            
        return info
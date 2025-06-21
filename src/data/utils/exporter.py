"""
Utilitários para exportação de dados para diferentes formatos.
"""

import pandas as pd
from typing import Dict, List, Optional, Any, Union
import json
import os
from pathlib import Path
from datetime import datetime
import io
import zipfile


class DataExporter:
    """Exportador de dados com suporte a múltiplos formatos."""
    
    def __init__(self):
        self.export_formats = {
            'csv': self.export_csv,
            'excel': self.export_excel,
            'json': self.export_json,
            'sql': self.export_sql,
            'parquet': self.export_parquet
        }
        
    def export(self,
              data: Union[pd.DataFrame, List[Dict]],
              filepath: str,
              format: Optional[str] = None,
              **kwargs) -> Dict[str, Any]:
        """Exporta dados para o formato especificado."""
        # Converte lista para DataFrame se necessário
        if isinstance(data, list):
            data = pd.DataFrame(data)
            
        # Detecta formato pela extensão se não especificado
        if not format:
            ext = Path(filepath).suffix.lower()[1:]  # Remove o ponto
            format = ext
            
        # Valida formato
        if format not in self.export_formats:
            raise ValueError(f"Formato não suportado: {format}")
            
        # Cria diretório se não existir
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Exporta dados
        result = self.export_formats[format](data, filepath, **kwargs)
        
        # Adiciona metadados
        result.update({
            'filepath': filepath,
            'format': format,
            'timestamp': datetime.now().isoformat(),
            'rows_exported': len(data),
            'columns_exported': len(data.columns),
            'file_size': os.path.getsize(filepath) if os.path.exists(filepath) else 0
        })
        
        return result
        
    def export_csv(self, 
                  df: pd.DataFrame, 
                  filepath: str,
                  encoding: str = 'utf-8',
                  sep: str = ',',
                  index: bool = False,
                  **kwargs) -> Dict[str, Any]:
        """Exporta para CSV."""
        df.to_csv(
            filepath,
            encoding=encoding,
            sep=sep,
            index=index,
            **kwargs
        )
        
        return {
            'success': True,
            'encoding': encoding,
            'separator': sep
        }
        
    def export_excel(self,
                    df: pd.DataFrame,
                    filepath: str,
                    sheet_name: str = 'Sheet1',
                    index: bool = False,
                    **kwargs) -> Dict[str, Any]:
        """Exporta para Excel com formatação."""
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index, **kwargs)
            
            # Ajusta largura das colunas
            worksheet = writer.sheets[sheet_name]
            for column in df:
                column_length = max(
                    df[column].astype(str).map(len).max(),
                    len(str(column))
                )
                col_idx = df.columns.get_loc(column)
                worksheet.column_dimensions[
                    worksheet.cell(row=1, column=col_idx + 1).column_letter
                ].width = min(column_length + 2, 50)
                
        return {
            'success': True,
            'sheet_name': sheet_name,
            'total_sheets': 1
        }
        
    def export_json(self,
                   df: pd.DataFrame,
                   filepath: str,
                   orient: str = 'records',
                   indent: int = 2,
                   ensure_ascii: bool = False,
                   **kwargs) -> Dict[str, Any]:
        """Exporta para JSON."""
        # Converte DataFrame para JSON
        json_data = df.to_json(
            orient=orient,
            date_format='iso',
            default_handler=str,
            force_ascii=ensure_ascii
        )
        
        # Parse e reformata com indentação
        parsed = json.loads(json_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(parsed, f, indent=indent, ensure_ascii=ensure_ascii)
            
        return {
            'success': True,
            'orient': orient,
            'records': len(parsed) if isinstance(parsed, list) else 1
        }
        
    def export_sql(self,
                  df: pd.DataFrame,
                  filepath: str,
                  table_name: str,
                  schema: str = 'public',
                  if_exists: str = 'replace',
                  batch_size: int = 100,
                  **kwargs) -> Dict[str, Any]:
        """Exporta para SQL INSERT statements."""
        total_batches = 0
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"-- Generated SQL for table {schema}.{table_name}\n")
            f.write(f"-- Generated at: {datetime.now().isoformat()}\n")
            f.write(f"-- Total records: {len(df)}\n\n")
            
            # Tratamento da tabela existente
            if if_exists == 'replace':
                f.write(f"DROP TABLE IF EXISTS {schema}.{table_name};\n\n")
            elif if_exists == 'fail':
                f.write(f"-- Table must not exist\n\n")
            elif if_exists == 'append':
                f.write(f"-- Appending to existing table\n\n")
                
            # CREATE TABLE se necessário
            if if_exists in ['replace', 'fail']:
                create_sql = self._generate_create_table(df, table_name, schema)
                f.write(create_sql)
                f.write("\n\n")
                
            # INSERT statements em batches
            columns = list(df.columns)
            columns_str = ', '.join([f'"{col}"' for col in columns])
            
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i + batch_size]
                
                f.write(f"INSERT INTO {schema}.{table_name} ({columns_str}) VALUES\n")
                
                values_list = []
                for _, row in batch.iterrows():
                    values = []
                    for col in columns:
                        val = row[col]
                        if pd.isna(val):
                            values.append('NULL')
                        elif isinstance(val, str):
                            # Escapa aspas simples
                            escaped = val.replace("'", "''")
                            values.append(f"'{escaped}'")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        elif isinstance(val, bool):
                            values.append('TRUE' if val else 'FALSE')
                        elif isinstance(val, datetime):
                            values.append(f"'{val.isoformat()}'")
                        else:
                            values.append(f"'{str(val)}'")
                            
                    values_list.append(f"({', '.join(values)})")
                    
                f.write(',\n'.join(values_list))
                f.write(';\n\n')
                
                total_batches += 1
                
        return {
            'success': True,
            'table_name': table_name,
            'schema': schema,
            'total_batches': total_batches,
            'batch_size': batch_size
        }
        
    def export_parquet(self,
                      df: pd.DataFrame,
                      filepath: str,
                      compression: str = 'snappy',
                      **kwargs) -> Dict[str, Any]:
        """Exporta para formato Parquet."""
        df.to_parquet(
            filepath,
            compression=compression,
            index=False,
            **kwargs
        )
        
        return {
            'success': True,
            'compression': compression
        }
        
    def export_multiple(self,
                       datasets: Dict[str, pd.DataFrame],
                       base_path: str,
                       format: str = 'csv',
                       compress: bool = False,
                       **kwargs) -> Dict[str, Any]:
        """Exporta múltiplos datasets."""
        results = {}
        exported_files = []
        
        for name, df in datasets.items():
            # Gera nome do arquivo
            filename = f"{name}.{format}"
            filepath = os.path.join(base_path, filename)
            
            # Exporta dataset
            result = self.export(df, filepath, format, **kwargs)
            results[name] = result
            exported_files.append(filepath)
            
        # Comprime se solicitado
        if compress:
            zip_path = f"{base_path}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for filepath in exported_files:
                    arcname = os.path.basename(filepath)
                    zipf.write(filepath, arcname)
                    
                    # Remove arquivo original após comprimir
                    os.remove(filepath)
                    
            return {
                'success': True,
                'compressed': True,
                'zip_file': zip_path,
                'datasets': results
            }
            
        return {
            'success': True,
            'compressed': False,
            'files': exported_files,
            'datasets': results
        }
        
    def _generate_create_table(self, 
                             df: pd.DataFrame, 
                             table_name: str,
                             schema: str = 'public') -> str:
        """Gera CREATE TABLE statement baseado no DataFrame."""
        type_mapping = {
            'int64': 'INTEGER',
            'float64': 'REAL',
            'object': 'TEXT',
            'bool': 'BOOLEAN',
            'datetime64[ns]': 'TIMESTAMP',
            'timedelta64[ns]': 'INTERVAL',
            'category': 'TEXT'
        }
        
        columns = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            sql_type = type_mapping.get(dtype, 'TEXT')
            
            # Ajusta tipo para strings longas
            if sql_type == 'TEXT' and not df[col].empty:
                max_len = df[col].astype(str).str.len().max()
                if max_len <= 255:
                    sql_type = f'VARCHAR({max_len})'
                    
            columns.append(f'    "{col}" {sql_type}')
            
        create_sql = f"CREATE TABLE {schema}.{table_name} (\n"
        create_sql += ',\n'.join(columns)
        create_sql += "\n);"
        
        return create_sql
        
    def to_buffer(self,
                 df: pd.DataFrame,
                 format: str,
                 **kwargs) -> io.BytesIO:
        """Exporta para buffer em memória."""
        buffer = io.BytesIO()
        
        if format == 'csv':
            df.to_csv(buffer, index=False, **kwargs)
        elif format == 'excel':
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, **kwargs)
        elif format == 'json':
            json_str = df.to_json(orient='records', **kwargs)
            buffer.write(json_str.encode('utf-8'))
        else:
            raise ValueError(f"Formato não suportado para buffer: {format}")
            
        buffer.seek(0)
        return buffer